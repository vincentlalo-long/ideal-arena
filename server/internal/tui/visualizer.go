package tui

import (
	"fmt"
	"os"
	"strings"
	"time"

	"golang.org/x/term"
	"ideal-arena/server/internal/engine"
	"ideal-arena/server/internal/judger"
)

// ANSI color codes
const (
	colorReset  = "\033[0m"
	colorBold   = "\033[1m"
	colorGreen  = "\033[32m"
	colorRed    = "\033[31m"
	colorYellow = "\033[33m"
	colorBlue   = "\033[34m"
	colorPurple = "\033[35m"
	colorCyan   = "\033[36m"
	colorGray   = "\033[90m"
	bgGreen     = "\033[42;30m"
	bgRed       = "\033[41;37m"
)

type Visualizer struct {
	result       *judger.MatchResult
	currentRound int
	isPlaying    bool
	speedDelay   time.Duration
}

func NewVisualizer(res *judger.MatchResult) *Visualizer {
	return &Visualizer{
		result:       res,
		currentRound: 0,
		isPlaying:    false,
		speedDelay:   80 * time.Millisecond,
	}
}

func (v *Visualizer) Run() error {
	// Put terminal in raw mode
	oldState, err := term.MakeRaw(int(os.Stdin.Fd()))
	if err != nil {
		return fmt.Errorf("failed to initialize raw terminal: %w", err)
	}
	defer func() {
		_ = term.Restore(int(os.Stdin.Fd()), oldState)
		fmt.Print("\033[?25h\n") // Restore cursor
	}()

	fmt.Print("\033[?25l") // Hide cursor

	keyChan := make(chan []byte)
	go func() {
		buf := make([]byte, 8)
		for {
			n, err := os.Stdin.Read(buf)
			if err != nil {
				return
			}
			msg := make([]byte, n)
			copy(msg, buf[:n])
			keyChan <- msg
		}
	}()

	ticker := time.NewTicker(v.speedDelay)
	defer ticker.Stop()

	v.render()

	for {
		select {
		case keys := <-keyChan:
			if len(keys) == 1 {
				k := keys[0]
				switch k {
				case 'q', 'Q', 3: // 3 is Ctrl+C
					return nil
				case ' ':
					v.isPlaying = !v.isPlaying
				case 'r', 'R':
					v.currentRound = 0
				case 'l':
					v.nextRound()
				case 'h':
					v.prevRound()
				case '1':
					v.speedDelay = 200 * time.Millisecond
					ticker.Reset(v.speedDelay)
				case '2':
					v.speedDelay = 80 * time.Millisecond
					ticker.Reset(v.speedDelay)
				case '3':
					v.speedDelay = 30 * time.Millisecond
					ticker.Reset(v.speedDelay)
				}
			} else if len(keys) >= 3 && keys[0] == 27 && keys[1] == 91 {
				// Escape sequence: Arrow keys
				switch keys[2] {
				case 67: // Right arrow
					v.nextRound()
				case 68: // Left arrow
					v.prevRound()
				}
			}
			v.render()

		case <-ticker.C:
			if v.isPlaying {
				if v.currentRound < v.result.Rounds {
					v.currentRound++
					v.render()
				} else {
					v.isPlaying = false
					v.render()
				}
			}
		}
	}
}

func (v *Visualizer) nextRound() {
	if v.currentRound < v.result.Rounds {
		v.currentRound++
	}
}

func (v *Visualizer) prevRound() {
	if v.currentRound > 0 {
		v.currentRound--
	}
}

func (v *Visualizer) render() {
	var sb strings.Builder

	// Clear screen and home cursor
	sb.WriteString("\033[2J\033[H")

	// Header banner
	sb.WriteString(colorBold + colorCyan + "================================================================================" + colorReset + "\r\n")
	sb.WriteString(colorBold + "                     IDEAL ARENA: TERMINAL REPLAY VISUALIZER                    " + colorReset + "\r\n")
	sb.WriteString(colorBold + colorCyan + "================================================================================" + colorReset + "\r\n\r\n")

	// Calculate metrics up to current round
	scoreA, scoreB := 0, 0
	coopA, coopB := 0, 0
	for i := 0; i < v.currentRound; i++ {
		a := v.result.HistoryA[i]
		b := v.result.HistoryB[i]
		pa, pb := engine.EvaluateRound(a, b)
		scoreA += pa
		scoreB += pb
		if a == 1 {
			coopA++
		}
		if b == 1 {
			coopB++
		}
	}

	avgA := 0.0
	avgB := 0.0
	cRateA := 100.0
	cRateB := 100.0
	if v.currentRound > 0 {
		avgA = float64(scoreA) / float64(v.currentRound)
		avgB = float64(scoreB) / float64(v.currentRound)
		cRateA = (float64(coopA) / float64(v.currentRound)) * 100
		cRateB = (float64(coopB) / float64(v.currentRound)) * 100
	}

	curMoveA := "WAIT"
	curMoveB := "WAIT"
	moveBadgeA := colorGray + "[ PENDING ]" + colorReset
	moveBadgeB := colorGray + "[ PENDING ]" + colorReset
	roundPayoff := "Round Start"

	if v.currentRound > 0 {
		idx := v.currentRound - 1
		a := v.result.HistoryA[idx]
		b := v.result.HistoryB[idx]
		pa, pb := engine.EvaluateRound(a, b)

		if a == 1 {
			curMoveA = "COOPERATE"
			moveBadgeA = bgGreen + " COOPERATE " + colorReset
		} else {
			curMoveA = "DEFECT"
			moveBadgeA = bgRed + "  DEFECT   " + colorReset
		}

		if b == 1 {
			curMoveB = "COOPERATE"
			moveBadgeB = bgGreen + " COOPERATE " + colorReset
		} else {
			curMoveB = "DEFECT"
			moveBadgeB = bgRed + "  DEFECT   " + colorReset
		}
		roundPayoff = fmt.Sprintf("Round %d Payoffs: A (+%d pts) | B (+%d pts)", v.currentRound, pa, pb)
	}

	// Player Cards Side by Side
	sb.WriteString(fmt.Sprintf(" %s%-37s%s   %s%-37s%s\r\n", colorBold+colorBlue, "PLAYER A: "+v.result.PlayerAName, colorReset, colorBold+colorPurple, "PLAYER B: "+v.result.PlayerBName, colorReset))
	sb.WriteString(" +-------------------------------------+   +-------------------------------------+\r\n")
	sb.WriteString(fmt.Sprintf(" | Move       : %-23s|   | Move       : %-23s|\r\n", moveBadgeA, moveBadgeB))
	sb.WriteString(fmt.Sprintf(" | Total Score: %-22d |   | Total Score: %-22d |\r\n", scoreA, scoreB))
	sb.WriteString(fmt.Sprintf(" | Avg Payoff : %-22.3f |   | Avg Payoff : %-22.3f |\r\n", avgA, avgB))
	sb.WriteString(fmt.Sprintf(" | Coop Rate  : %-21.1f%% |   | Coop Rate  : %-21.1f%% |\r\n", cRateA, cRateB))
	sb.WriteString(" +-------------------------------------+   +-------------------------------------+\r\n\r\n")

	// Status and Controls Bar
	statusStr := colorYellow + "PAUSED" + colorReset
	if v.isPlaying {
		statusStr = colorGreen + "PLAYING" + colorReset
	}
	sb.WriteString(fmt.Sprintf(" Round: [%s%3d / %3d%s]  Status: [%s]  %s\r\n",
		colorBold, v.currentRound, v.result.Rounds, colorReset, statusStr, colorCyan+roundPayoff+colorReset))

	// Progress Scrubber Bar
	progressLen := 60
	filled := 0
	if v.result.Rounds > 0 {
		filled = (v.currentRound * progressLen) / v.result.Rounds
	}
	bar := strings.Repeat("=", filled) + strings.Repeat("-", progressLen-filled)
	pct := 0.0
	if v.result.Rounds > 0 {
		pct = (float64(v.currentRound) / float64(v.result.Rounds)) * 100
	}
	sb.WriteString(fmt.Sprintf(" Progress: [%s%s%s] %5.1f%%\r\n\r\n", colorCyan, bar, colorReset, pct))

	// Tape View (Window of last 30 rounds)
	windowSize := 35
	startIdx := 0
	if v.currentRound > windowSize {
		startIdx = v.currentRound - windowSize
	}
	endIdx := startIdx + windowSize
	if endIdx > v.result.Rounds {
		endIdx = v.result.Rounds
	}

	var tapeA, tapeB strings.Builder
	for i := startIdx; i < endIdx; i++ {
		cursorPrefix := ""
		if i == v.currentRound-1 {
			cursorPrefix = "\033[4m" // underline current round
		}

		if i < len(v.result.HistoryA) {
			if v.result.HistoryA[i] == 1 {
				tapeA.WriteString(colorGreen + cursorPrefix + "C" + colorReset + " ")
			} else {
				tapeA.WriteString(colorRed + cursorPrefix + "D" + colorReset + " ")
			}
		}

		if i < len(v.result.HistoryB) {
			if v.result.HistoryB[i] == 1 {
				tapeB.WriteString(colorGreen + cursorPrefix + "C" + colorReset + " ")
			} else {
				tapeB.WriteString(colorRed + cursorPrefix + "D" + colorReset + " ")
			}
		}
	}

	sb.WriteString(colorBold + " TIMELINE TAPE (Recent Rounds):" + colorReset + "\r\n")
	sb.WriteString(" A: " + tapeA.String() + "\r\n")
	sb.WriteString(" B: " + tapeB.String() + "\r\n\r\n")

	// Keyboard Controls Help
	sb.WriteString(colorGray + " CONTROLS:" + colorReset + "\r\n")
	sb.WriteString(" [Right / l] Next Round   [Left / h] Prev Round   [Space] Play/Pause\r\n")
	sb.WriteString(" [r] Reset to Start       [1, 2, 3] Speed Control  [q] Quit\r\n")
	sb.WriteString(colorBold + colorCyan + "================================================================================" + colorReset + "\r\n")

	_ = curMoveA
	_ = curMoveB

	fmt.Print(sb.String())
}
