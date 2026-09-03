package judger

import (
	"context"
	"fmt"
	"time"

	"ideal-arena/server/internal/engine"
)

type MatchResult struct {
	PlayerAName string        `json:"player_a_name"`
	PlayerBName string        `json:"player_b_name"`
	Rounds      int           `json:"rounds"`
	ScoreA      int           `json:"score_a"`
	ScoreB      int           `json:"score_b"`
	HistoryA    []int         `json:"history_a"`
	HistoryB    []int         `json:"history_b"`
	Duration    time.Duration `json:"duration_ns"`
}

func (m *MatchResult) Summary() string {
	winner := "Tie"
	if m.ScoreA > m.ScoreB {
		winner = m.PlayerAName
	} else if m.ScoreB > m.ScoreA {
		winner = m.PlayerBName
	}
	avgA := float64(m.ScoreA) / float64(m.Rounds)
	avgB := float64(m.ScoreB) / float64(m.Rounds)
	return fmt.Sprintf("Match: %s vs %s (%d rounds) in %v\n  Score: %d - %d (Winner: %s)\n  Avg Payoff: %.3f - %.3f",
		m.PlayerAName, m.PlayerBName, m.Rounds, m.Duration, m.ScoreA, m.ScoreB, winner, avgA, avgB)
}

func PlayMatch(ctx context.Context, botA, botB *BotProcess, config engine.MatchConfig) (*MatchResult, error) {
	start := time.Now()

	matchCtx, cancel := context.WithTimeout(ctx, time.Duration(config.MatchTimeoutS)*time.Second)
	defer cancel()

	if err := botA.Start(matchCtx); err != nil {
		return nil, fmt.Errorf("failed to start player A (%s): %w", botA.Name, err)
	}
	defer botA.Close()

	if err := botB.Start(matchCtx); err != nil {
		return nil, fmt.Errorf("failed to start player B (%s): %w", botB.Name, err)
	}
	defer botB.Close()

	_ = botA.Reset()
	_ = botB.Reset()

	histA := make([]int, 0, config.Rounds)
	histB := make([]int, 0, config.Rounds)
	scoreA := 0
	scoreB := 0

	for r := 0; r < config.Rounds; r++ {
		actA, _ := botA.Step(r, histA, histB)
		actB, _ := botB.Step(r, histB, histA)

		payA, payB := engine.EvaluateRound(actA, actB)
		scoreA += payA
		scoreB += payB

		histA = append(histA, actA)
		histB = append(histB, actB)
	}

	return &MatchResult{
		PlayerAName: botA.Name,
		PlayerBName: botB.Name,
		Rounds:      config.Rounds,
		ScoreA:      scoreA,
		ScoreB:      scoreB,
		HistoryA:    histA,
		HistoryB:    histB,
		Duration:    time.Since(start),
	}, nil
}
