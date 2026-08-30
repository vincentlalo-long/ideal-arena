package judger

import (
	"bufio"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
	"os/exec"
	"strings"
	"time"

	"ideal-arena/server/internal/engine"
)

type StepRequest struct {
	Command     string `json:"command"`
	Round       int    `json:"round"`
	HistorySelf []int  `json:"history_self"`
	HistoryOpp  []int  `json:"history_opp"`
}

type StepResponse struct {
	Action int `json:"action"`
}

type StatusResponse struct {
	Status string `json:"status"`
}

type BotProcess struct {
	Name        string
	ExecCommand string
	ExecArgs    []string
	StepTimeout time.Duration

	cmd    *exec.Cmd
	stdin  io.WriteCloser
	lineCh chan string
	errCh  chan error
	stopCh chan struct{}
}

func NewBotProcess(name, execCmd string, execArgs []string, stepTimeout time.Duration) *BotProcess {
	if stepTimeout <= 0 {
		stepTimeout = 50 * time.Millisecond
	}
	return &BotProcess{
		Name:        name,
		ExecCommand: execCmd,
		ExecArgs:    execArgs,
		StepTimeout: stepTimeout,
		lineCh:      make(chan string, 100),
		errCh:       make(chan error, 1),
		stopCh:      make(chan struct{}),
	}
}

func (b *BotProcess) Start(ctx context.Context) error {
	b.cmd = exec.CommandContext(ctx, b.ExecCommand, b.ExecArgs...)

	stdinPipe, err := b.cmd.StdinPipe()
	if err != nil {
		return fmt.Errorf("failed to create stdin pipe: %w", err)
	}
	b.stdin = stdinPipe

	stdoutPipe, err := b.cmd.StdoutPipe()
	if err != nil {
		return fmt.Errorf("failed to create stdout pipe: %w", err)
	}

	b.cmd.Stderr = os.Stderr

	if err := b.cmd.Start(); err != nil {
		return fmt.Errorf("failed to start bot process: %w", err)
	}

	// Dedicated background goroutine reading stdout sequentially
	go func() {
		reader := bufio.NewReader(stdoutPipe)
		for {
			line, err := reader.ReadString('\n')
			if err != nil {
				select {
				case b.errCh <- err:
				default:
				}
				return
			}
			line = strings.TrimSpace(line)
			if line != "" {
				select {
				case b.lineCh <- line:
				case <-b.stopCh:
					return
				}
			}
		}
	}()

	return nil
}

func (b *BotProcess) Reset() error {
	if b.stdin == nil {
		return errors.New("bot process is not running")
	}

	reqBytes, _ := json.Marshal(StepRequest{Command: "RESET"})
	reqBytes = append(reqBytes, '\n')
	if _, err := b.stdin.Write(reqBytes); err != nil {
		return err
	}

	select {
	case line := <-b.lineCh:
		var statusResp StatusResponse
		if err := json.Unmarshal([]byte(line), &statusResp); err != nil {
			return err
		}
		return nil
	case err := <-b.errCh:
		return err
	case <-time.After(1 * time.Second):
		return errors.New("reset timeout")
	}
}

func (b *BotProcess) Step(round int, historySelf, historyOpp []int) (int, error) {
	if b.stdin == nil {
		return engine.ActionDefect, errors.New("bot process is not running")
	}

	req := StepRequest{
		Command:     "STEP",
		Round:       round,
		HistorySelf: historySelf,
		HistoryOpp:  historyOpp,
	}
	reqBytes, err := json.Marshal(req)
	if err != nil {
		return engine.ActionDefect, err
	}
	reqBytes = append(reqBytes, '\n')

	if _, err := b.stdin.Write(reqBytes); err != nil {
		return engine.ActionDefect, fmt.Errorf("write to stdin failed: %w", err)
	}

	select {
	case line := <-b.lineCh:
		var resp StepResponse
		if err := json.Unmarshal([]byte(line), &resp); err != nil {
			return engine.ActionDefect, fmt.Errorf("malformed JSON from bot: %w", err)
		}
		return engine.ValidateAction(resp.Action), nil
	case err := <-b.errCh:
		return engine.ActionDefect, err
	case <-time.After(b.StepTimeout):
		// Watchdog step timeout penalty: default to Defect (0)
		return engine.ActionDefect, fmt.Errorf("step timeout after %v", b.StepTimeout)
	}
}

func (b *BotProcess) Close() error {
	select {
	case <-b.stopCh:
	default:
		close(b.stopCh)
	}
	if b.stdin != nil {
		_ = b.stdin.Close()
	}
	if b.cmd != nil && b.cmd.Process != nil {
		return b.cmd.Process.Kill()
	}
	return nil
}
