package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

const sdk = "go/0.2.0"

type request struct {
	Type    string `json:"type"`
	Episode string `json:"episode"`
	Seed    int64  `json:"seed"`
	T       int64  `json:"t"`
	Obs     any    `json:"obs"`
}

type readyResponse struct {
	Type string `json:"type"`
	SDK  string `json:"sdk"`
}

type ackResponse struct {
	Type    string `json:"type"`
	Episode string `json:"episode"`
}

type actionResponse struct {
	Type   string `json:"type"`
	T      int64  `json:"t"`
	Action any    `json:"action"`
}

func reply(message any) {
	data, err := json.Marshal(message)
	if err != nil {
		return
	}
	fmt.Println(string(data))
}

func main() {
	var bot Strategy = &MyStrategy{}
	scanner := bufio.NewScanner(os.Stdin)

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			continue
		}

		var req request
		if err := json.Unmarshal([]byte(line), &req); err != nil {
			fmt.Fprintln(os.Stderr, "arena-agent: ignoring malformed line")
			continue
		}

		switch req.Type {
		case "hello":
			reply(readyResponse{Type: "ready", SDK: sdk})
		case "reset":
			bot.Reset(req.Seed)
			reply(ackResponse{Type: "ack", Episode: req.Episode})
		case "act":
			action := bot.Act(req.Obs)
			reply(actionResponse{Type: "action", T: req.T, Action: action})
		}
	}
}
