package tournament

import (
	"context"
	"sort"
	"sync"
	"time"

	"ideal-arena/server/internal/engine"
	"ideal-arena/server/internal/judger"
)

type matchJob struct {
	botA BotSpec
	botB BotSpec
}

func RunTournament(ctx context.Context, bots []BotSpec, config engine.MatchConfig, concurrency int) (*TournamentResult, error) {
	if concurrency <= 0 {
		concurrency = 4
	}

	m := len(bots)
	if m == 0 {
		return &TournamentResult{}, nil
	}

	jobs := make(chan matchJob, (m*(m+1))/2)
	results := make(chan *judger.MatchResult, (m*(m+1))/2)

	var wg sync.WaitGroup

	// Worker pool
	for w := 0; w < concurrency; w++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for job := range jobs {
				procA := judger.NewBotProcess(job.botA.Name, job.botA.Command, job.botA.Args, time.Duration(config.StepTimeoutMs)*time.Millisecond)
				procB := judger.NewBotProcess(job.botB.Name, job.botB.Command, job.botB.Args, time.Duration(config.StepTimeoutMs)*time.Millisecond)

				res, err := judger.PlayMatch(ctx, procA, procB, config)
				if err == nil && res != nil {
					results <- res
				}
			}
		}()
	}

	// Enqueue pairwise matches
	for i := 0; i < m; i++ {
		for j := i; j < m; j++ {
			jobs <- matchJob{botA: bots[i], botB: bots[j]}
		}
	}
	close(jobs)

	wg.Wait()
	close(results)

	// Collect match results
	statsMap := make(map[string]*PlayerStats)
	for _, b := range bots {
		statsMap[b.Name] = &PlayerStats{Name: b.Name}
	}

	var allMatches []*judger.MatchResult
	for res := range results {
		allMatches = append(allMatches, res)

		stA := statsMap[res.PlayerAName]
		stB := statsMap[res.PlayerBName]

		if res.PlayerAName == res.PlayerBName {
			// Self-play
			if stA != nil {
				stA.TotalScore += res.ScoreA
				stA.MatchesPlayed++
				stA.RoundsPlayed += res.Rounds
				for _, a := range res.HistoryA {
					if a == engine.ActionCooperate {
						stA.CoopRate++
					}
				}
				if res.ScoreA > res.ScoreB {
					stA.Wins++
				} else if res.ScoreB > res.ScoreA {
					stA.Losses++
				} else {
					stA.Ties++
				}
			}
		} else {
			// Pairwise
			if stA != nil {
				stA.TotalScore += res.ScoreA
				stA.MatchesPlayed++
				stA.RoundsPlayed += res.Rounds
				for _, a := range res.HistoryA {
					if a == engine.ActionCooperate {
						stA.CoopRate++
					}
				}
				if res.ScoreA > res.ScoreB {
					stA.Wins++
				} else if res.ScoreB > res.ScoreA {
					stA.Losses++
				} else {
					stA.Ties++
				}
			}
			if stB != nil {
				stB.TotalScore += res.ScoreB
				stB.MatchesPlayed++
				stB.RoundsPlayed += res.Rounds
				for _, b := range res.HistoryB {
					if b == engine.ActionCooperate {
						stB.CoopRate++
					}
				}
				if res.ScoreB > res.ScoreA {
					stB.Wins++
				} else if res.ScoreA > res.ScoreB {
					stB.Losses++
				} else {
					stB.Ties++
				}
			}
		}
	}

	var standings []*PlayerStats
	for _, st := range statsMap {
		if st.RoundsPlayed > 0 {
			st.AvgPayoff = float64(st.TotalScore) / float64(st.RoundsPlayed)
			st.CoopRate = st.CoopRate / float64(st.RoundsPlayed)
		}
		standings = append(standings, st)
	}

	sort.Slice(standings, func(i, j int) bool {
		if standings[i].AvgPayoff != standings[j].AvgPayoff {
			return standings[i].AvgPayoff > standings[j].AvgPayoff
		}
		if standings[i].Wins != standings[j].Wins {
			return standings[i].Wins > standings[j].Wins
		}
		return standings[i].CoopRate > standings[j].CoopRate
	})

	for r, st := range standings {
		st.Rank = r + 1
	}

	return &TournamentResult{
		Standings: standings,
		Matches:   allMatches,
	}, nil
}
