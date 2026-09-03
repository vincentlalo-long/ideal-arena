package api

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"ideal-arena/server/internal/tournament"
)

func TestHealthEndpoint(t *testing.T) {
	server := NewServer(":8080", "")

	req := httptest.NewRequest(http.MethodGet, "/api/v1/health", nil)
	w := httptest.NewRecorder()

	server.httpServer.Handler.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("Expected status 200, got %d", w.Code)
	}

	var resp map[string]any
	if err := json.NewDecoder(w.Body).Decode(&resp); err != nil {
		t.Fatalf("Failed to decode JSON: %v", err)
	}

	if resp["status"] != "healthy" {
		t.Errorf("Expected status 'healthy', got %v", resp["status"])
	}
}

func TestPresetsEndpoint(t *testing.T) {
	server := NewServer(":8080", "")

	req := httptest.NewRequest(http.MethodGet, "/api/v1/presets", nil)
	w := httptest.NewRecorder()

	server.httpServer.Handler.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("Expected status 200, got %d", w.Code)
	}

	var resp map[string]any
	if err := json.NewDecoder(w.Body).Decode(&resp); err != nil {
		t.Fatalf("Failed to decode JSON: %v", err)
	}

	if _, ok := resp["presets"]; !ok {
		t.Errorf("Expected 'presets' key in response")
	}
}

func TestSimulateMatchAPI(t *testing.T) {
	server := NewServer(":8080", "")

	reqBody := SimulateMatchRequest{
		PlayerA: tournament.BotSpec{
			Name:    "TestBotA",
			Command: "python",
			Args:    []string{"../../../adapters/python/runner.py"},
		},
		PlayerB: tournament.BotSpec{
			Name:    "TestBotB",
			Command: "python",
			Args:    []string{"../../../adapters/python/runner.py"},
		},
		Rounds: 10,
	}

	bodyBytes, _ := json.Marshal(reqBody)
	req := httptest.NewRequest(http.MethodPost, "/api/v1/matches/simulate", bytes.NewReader(bodyBytes))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	server.httpServer.Handler.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("Expected status 200, got %d. Body: %s", w.Code, w.Body.String())
	}

	var result map[string]any
	if err := json.NewDecoder(w.Body).Decode(&result); err != nil {
		t.Fatalf("Failed to decode JSON response: %v", err)
	}

	if result["player_a_name"] != "TestBotA" {
		t.Errorf("Expected player_a_name 'TestBotA', got %v", result["player_a_name"])
	}
	if int(result["rounds"].(float64)) != 10 {
		t.Errorf("Expected 10 rounds, got %v", result["rounds"])
	}
}
