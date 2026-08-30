package main

import (
	"context"
	"fmt"
	"time"

	"ideal-arena/server/internal/engine"
	"ideal-arena/server/internal/judger"
	"ideal-arena/server/internal/tournament"
)

func main() {
	fmt.Println("=== Ideal Arena Go Judger Platform ===")

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	config := engine.DefaultMatchConfig()
	config.Rounds = 50

	// Test single match between two bot processes (e.g. Python adapter runner)
	botA := judger.NewBotProcess("Python-Bot-1", "python", []string{"adapters/python/runner.py"}, 10*time.Millisecond)
	botB := judger.NewBotProcess("Python-Bot-2", "python", []string{"adapters/python/runner.py"}, 10*time.Millisecond)

	fmt.Println("\nRunning single pairwise match (Python vs Python)...")
	res, err := judger.PlayMatch(ctx, botA, botB, config)
	if err != nil {
		fmt.Printf("Match error: %v\n", err)
	} else {
		fmt.Println(res.Summary())
	}

	// Test tournament runner
	bots := []tournament.BotSpec{
		{Name: "Python-TFT-1", Command: "python", Args: []string{"adapters/python/runner.py"}},
		{Name: "Python-TFT-2", Command: "python", Args: []string{"adapters/python/runner.py"}},
	}

	fmt.Println("\nRunning mini tournament...")
	tourRes, err := tournament.RunTournament(ctx, bots, config, 2)
	if err != nil {
		fmt.Printf("Tournament error: %v\n", err)
	} else {
		fmt.Println("\n" + tourRes.DisplayLeaderboard())
	}
}
