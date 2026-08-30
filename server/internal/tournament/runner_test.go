package tournament

import (
	"context"
	"testing"
	"time"

	"ideal-arena/server/internal/engine"
)

func TestRunTournamentWithPythonBots(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	config := engine.MatchConfig{
		Rounds:        10,
		StepTimeoutMs: 200,
		MatchTimeoutS: 5,
	}

	bots := []BotSpec{
		{Name: "Python-TFT-A", Command: "python", Args: []string{"../../../adapters/python/runner.py"}},
		{Name: "Python-TFT-B", Command: "python", Args: []string{"../../../adapters/python/runner.py"}},
	}

	res, err := RunTournament(ctx, bots, config, 2)
	if err != nil {
		t.Fatalf("RunTournament failed: %v", err)
	}

	if len(res.Standings) != 2 {
		t.Fatalf("Expected 2 standings, got %d", len(res.Standings))
	}

	t.Logf("\n%s", res.DisplayLeaderboard())
}
