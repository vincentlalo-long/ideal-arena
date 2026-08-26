package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

type Request struct {
	Command     string `json:"command"`
	HistorySelf []int  `json:"history_self"`
	HistoryOpp  []int  `json:"history_opp"`
}

type StepResponse struct {
	Action int `json:"action"`
}

type StatusResponse struct {
	Status string `json:"status"`
}

func main() {
	var bot Strategy = &MyStrategy{}
	scanner := bufio.NewScanner(os.Stdin)

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			continue
		}

		var req Request
		if err := json.Unmarshal([]byte(line), &req); err != nil {
			continue
		}

		if req.Command == "RESET" {
			bot.Reset()
			resp, _ := json.Marshal(StatusResponse{Status: "OK"})
			fmt.Println(string(resp))
		} else {
			action := bot.Step(req.HistorySelf, req.HistoryOpp)
			resp, _ := json.Marshal(StepResponse{Action: action})
			fmt.Println(string(resp))
		}
	}
}
