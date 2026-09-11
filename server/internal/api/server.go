package api

import (
	"context"
	"encoding/json"
	"net/http"
	"os"
	"path/filepath"
	"time"

	"ideal-arena/server/internal/engine"
	"ideal-arena/server/internal/judger"
	"ideal-arena/server/internal/tournament"
)

type Server struct {
	httpServer *http.Server
}

type SimulateMatchRequest struct {
	PlayerA tournament.BotSpec `json:"player_a"`
	PlayerB tournament.BotSpec `json:"player_b"`
	Rounds  int                `json:"rounds"`
}

type SimulateTournamentRequest struct {
	Bots        []tournament.BotSpec `json:"bots"`
	Rounds      int                  `json:"rounds"`
	Concurrency int                  `json:"concurrency"`
}

func NewServer(addr string) *Server {
	mux := http.NewServeMux()
	s := &Server{}

	// API Routes
	mux.HandleFunc("/api/v1/health", s.handleHealth)
	mux.HandleFunc("/api/v1/domains", s.handleDomains)
	mux.HandleFunc("/api/v1/problems", s.handleProblems)
	mux.HandleFunc("/api/v1/presets", s.handlePresets)
	mux.HandleFunc("/api/v1/matches/simulate", s.handleSimulateMatch)
	mux.HandleFunc("/api/v1/tournaments/simulate", s.handleSimulateTournament)

	s.httpServer = &http.Server{
		Addr:         addr,
		Handler:      corsMiddleware(mux),
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 30 * time.Second,
	}

	return s
}

func corsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}
		next.ServeHTTP(w, r)
	})
}

func (s *Server) Start() error {
	return s.httpServer.ListenAndServe()
}

func (s *Server) Shutdown(ctx context.Context) error {
	return s.httpServer.Shutdown(ctx)
}

func writeJSON(w http.ResponseWriter, status int, data any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(data)
}

func (s *Server) handleHealth(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{
		"status":  "healthy",
		"version": "0.2.0",
		"time":    time.Now().UTC().Format(time.RFC3339),
	})
}

func (s *Server) handleDomains(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{
		"domains": []string{"game_theory", "optimization", "simulation"},
	})
}

func (s *Server) handleProblems(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	problems := []map[string]any{
		{
			"id":          "axelrod",
			"name":        "Iterated Prisoner's Dilemma",
			"domain":      "game_theory",
			"description": "Axelrod's classic 2-player iterated game theory tournament.",
		},
	}
	writeJSON(w, http.StatusOK, map[string]any{
		"problems": problems,
	})
}

func (s *Server) handlePresets(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	runnerPath := filepath.Join("..", "adapters", "python", "runner.py")
	if _, err := os.Stat(runnerPath); os.IsNotExist(err) {
		runnerPath = filepath.Join("adapters", "python", "runner.py")
	}

	presets := []tournament.BotSpec{
		{Name: "Python-TFT", Command: "python", Args: []string{runnerPath}},
	}
	writeJSON(w, http.StatusOK, map[string]any{
		"presets": presets,
	})
}

func (s *Server) handleSimulateMatch(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req SimulateMatchRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "Invalid request payload: " + err.Error()})
		return
	}

	rounds := req.Rounds
	if rounds <= 0 {
		rounds = 200
	}

	cfg := engine.MatchConfig{
		Rounds:        rounds,
		StepTimeoutMs: 100,
		MatchTimeoutS: 10,
	}

	procA := judger.NewBotProcess(req.PlayerA.Name, req.PlayerA.Command, req.PlayerA.Args, time.Duration(cfg.StepTimeoutMs)*time.Millisecond)
	procB := judger.NewBotProcess(req.PlayerB.Name, req.PlayerB.Command, req.PlayerB.Args, time.Duration(cfg.StepTimeoutMs)*time.Millisecond)

	ctx, cancel := context.WithTimeout(r.Context(), time.Duration(cfg.MatchTimeoutS)*time.Second)
	defer cancel()

	result, err := judger.PlayMatch(ctx, procA, procB, cfg)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "Match execution failed: " + err.Error()})
		return
	}

	writeJSON(w, http.StatusOK, result)
}

func (s *Server) handleSimulateTournament(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req SimulateTournamentRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "Invalid request payload: " + err.Error()})
		return
	}

	if len(req.Bots) == 0 {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "At least one bot is required"})
		return
	}

	rounds := req.Rounds
	if rounds <= 0 {
		rounds = 50
	}

	cfg := engine.MatchConfig{
		Rounds:        rounds,
		StepTimeoutMs: 100,
		MatchTimeoutS: 15,
	}

	ctx, cancel := context.WithTimeout(r.Context(), 60*time.Second)
	defer cancel()

	concurrency := req.Concurrency
	if concurrency <= 0 {
		concurrency = 4
	}

	result, err := tournament.RunTournament(ctx, req.Bots, cfg, concurrency)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "Tournament failed: " + err.Error()})
		return
	}

	writeJSON(w, http.StatusOK, result)
}
