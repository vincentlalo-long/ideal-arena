package tournament

import (
	"fmt"
	"strings"

	"ideal-arena/server/internal/judger"
)

type BotSpec struct {
	Name    string
	Command string
	Args    []string
}

type PlayerStats struct {
	Name          string
	Rank          int
	TotalScore    int
	MatchesPlayed int
	RoundsPlayed  int
	Wins          int
	Losses        int
	Ties          int
	AvgPayoff     float64
	CoopRate      float64
}

type TournamentResult struct {
	Standings []*PlayerStats
	Matches   []*judger.MatchResult
}

func (tr *TournamentResult) DisplayLeaderboard() string {
	var sb strings.Builder
	sb.WriteString("=== Algorithm Arena Go Judger Leaderboard ===\n")
	sb.WriteString(fmt.Sprintf("%-5s | %-20s | %-10s | %-11s | %-10s | %-7s\n",
		"Rank", "Bot Name", "Avg Payoff", "Total Score", "W - L - T", "Coop %"))
	sb.WriteString("------+----------------------+------------+-------------+------------+--------\n")

	for _, s := range tr.Standings {
		wlt := fmt.Sprintf("%2d-%2d-%2d", s.Wins, s.Losses, s.Ties)
		sb.WriteString(fmt.Sprintf("#%-4d | %-20s | %-10.4f | %-11d | %-10s | %-6.1f%%\n",
			s.Rank, s.Name, s.AvgPayoff, s.TotalScore, wlt, s.CoopRate*100))
	}
	sb.WriteString("------+----------------------+------------+-------------+------------+--------\n")
	return sb.String()
}
