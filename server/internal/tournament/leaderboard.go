package tournament

import (
	"fmt"
	"strings"

	"ideal-arena/server/internal/judger"
)

type BotSpec struct {
	Name    string   `json:"name"`
	Command string   `json:"command"`
	Args    []string `json:"args"`
}

type PlayerStats struct {
	Name          string  `json:"name"`
	Rank          int     `json:"rank"`
	TotalScore    int     `json:"total_score"`
	MatchesPlayed int     `json:"matches_played"`
	RoundsPlayed  int     `json:"rounds_played"`
	Wins          int     `json:"wins"`
	Losses        int     `json:"losses"`
	Ties          int     `json:"ties"`
	AvgPayoff     float64 `json:"avg_payoff"`
	CoopRate      float64 `json:"coop_rate"`
}

type TournamentResult struct {
	Standings []*PlayerStats        `json:"standings"`
	Matches   []*judger.MatchResult `json:"matches"`
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
