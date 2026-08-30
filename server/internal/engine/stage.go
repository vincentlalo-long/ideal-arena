package engine

const (
	ActionDefect    = 0
	ActionCooperate = 1

	PayoffTemptation = 5
	PayoffReward     = 3
	PayoffPunishment = 1
	PayoffSucker     = 0
)

type MatchConfig struct {
	Rounds        int
	StepTimeoutMs int
	MatchTimeoutS int
}

func DefaultMatchConfig() MatchConfig {
	return MatchConfig{
		Rounds:        200,
		StepTimeoutMs: 10,
		MatchTimeoutS: 2,
	}
}

func ValidateAction(action int) int {
	if action == ActionCooperate {
		return ActionCooperate
	}
	return ActionDefect
}

func EvaluateRound(actionA, actionB int) (int, int) {
	a := ValidateAction(actionA)
	b := ValidateAction(actionB)

	switch {
	case a == ActionCooperate && b == ActionCooperate:
		return PayoffReward, PayoffReward
	case a == ActionCooperate && b == ActionDefect:
		return PayoffSucker, PayoffTemptation
	case a == ActionDefect && b == ActionCooperate:
		return PayoffTemptation, PayoffSucker
	default:
		return PayoffPunishment, PayoffPunishment
	}
}
