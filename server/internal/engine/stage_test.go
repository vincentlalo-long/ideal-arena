package engine

import "testing"

func TestEvaluateRound(t *testing.T) {
	tests := []struct {
		name       string
		actionA    int
		actionB    int
		expectedA  int
		expectedB  int
	}{
		{"Mutual Cooperation", 1, 1, 3, 3},
		{"A Defect B Cooperate", 0, 1, 5, 0},
		{"A Cooperate B Defect", 1, 0, 0, 5},
		{"Mutual Defection", 0, 0, 1, 1},
		{"Invalid Action A Fallback", 99, 1, 5, 0},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			payA, payB := EvaluateRound(tt.actionA, tt.actionB)
			if payA != tt.expectedA || payB != tt.expectedB {
				t.Errorf("EvaluateRound(%d, %d) = (%d, %d); expected (%d, %d)",
					tt.actionA, tt.actionB, payA, payB, tt.expectedA, tt.expectedB)
			}
		})
	}
}
