package judger

import (
	"context"
	"testing"
	"time"

	"ideal-arena/server/internal/engine"
)

func TestPlayMatchWithPythonAdapters(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	config := engine.MatchConfig{
		Rounds:        10,
		StepTimeoutMs: 100,
		MatchTimeoutS: 5,
	}

	botA := NewBotProcess("PyTFT1", "python", []string{"../../../adapters/python/runner.py"}, 500*time.Millisecond)
	botB := NewBotProcess("PyTFT2", "python", []string{"../../../adapters/python/runner.py"}, 500*time.Millisecond)

	res, err := PlayMatch(ctx, botA, botB, config)
	if err != nil {
		t.Fatalf("PlayMatch failed: %v", err)
	}
	t.Logf("Match summary: %s", res.Summary())

	if res.Rounds != 10 {
		t.Errorf("Expected 10 rounds, got %d", res.Rounds)
	}

	// Two TFTs cooperating for 10 rounds -> 30 points each
	if res.ScoreA != 30 || res.ScoreB != 30 {
		t.Errorf("Expected scores (30, 30), got (%d, %d)", res.ScoreA, res.ScoreB)
	}
}
