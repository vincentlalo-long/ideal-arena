package main

import (
	"context"
	"flag"
	"fmt"
	"os"
	"time"

	"ideal-arena/server/internal/engine"
	"ideal-arena/server/internal/judger"
	"ideal-arena/server/internal/tui"
)

func main() {
	botAPath := flag.String("bot-a", "", "Path to Player A runner (e.g. ../adapters/python/runner.py)")
	botBPath := flag.String("bot-b", "", "Path to Player B runner")
	rounds := flag.Int("rounds", 200, "Number of rounds for the match")
	flag.Parse()

	var result *judger.MatchResult

	if *botAPath != "" && *botBPath != "" {
		fmt.Printf("Simulating match: %s vs %s (%d rounds)...\n", *botAPath, *botBPath, *rounds)
		cfg := engine.DefaultMatchConfig()
		cfg.Rounds = *rounds

		botA := judger.NewBotProcess("PlayerA", "python", []string{*botAPath}, 100*time.Millisecond)
		botB := judger.NewBotProcess("PlayerB", "python", []string{*botBPath}, 100*time.Millisecond)

		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()

		var err error
		result, err = judger.PlayMatch(ctx, botA, botB, cfg)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error running match: %v\n", err)
			os.Exit(1)
		}
	} else {
		// Generate realistic Tit-for-Tat vs Prober demonstration match
		result = generateDemoMatch(*rounds)
	}

	viz := tui.NewVisualizer(result)
	if err := viz.Run(); err != nil {
		fmt.Fprintf(os.Stderr, "TUI error: %v\n", err)
		os.Exit(1)
	}
}

func generateDemoMatch(rounds int) *judger.MatchResult {
	histA := make([]int, 0, rounds)
	histB := make([]int, 0, rounds)
	scoreA, scoreB := 0, 0

	for t := 0; t < rounds; t++ {
		// Player A: Tit-for-Tat
		actA := 1
		if t > 0 {
			actA = histB[t-1]
		}

		// Player B: Prober (Detective)
		actB := 1
		if t == 0 {
			actB = 1
		} else if t == 1 {
			actB = 0 // deliberate probe
		} else if t == 2 || t == 3 {
			actB = 1
		} else {
			retaliated := (histA[2] == 0 || histA[3] == 0)
			if retaliated {
				actB = histA[t-1] // plays TFT
			} else {
				actB = 0 // exploit
			}
		}

		payA, payB := engine.EvaluateRound(actA, actB)
		scoreA += payA
		scoreB += payB
		histA = append(histA, actA)
		histB = append(histB, actB)
	}

	return &judger.MatchResult{
		PlayerAName: "Tit-for-Tat",
		PlayerBName: "Prober (Detective)",
		Rounds:      rounds,
		ScoreA:      scoreA,
		ScoreB:      scoreB,
		HistoryA:    histA,
		HistoryB:    histB,
		Duration:    15 * time.Millisecond,
	}
}
