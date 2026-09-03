package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"

	"ideal-arena/server/internal/api"
)

func main() {
	port := flag.Int("port", 8080, "HTTP server port")
	webDir := flag.String("web", "web", "Directory containing static web dashboard files")
	flag.Parse()

	// Locate web directory relative to working directory or binary
	actualWebDir := *webDir
	if _, err := os.Stat(actualWebDir); os.IsNotExist(err) {
		// Fallback for execution from repo root
		candidate := filepath.Join("server", "web")
		if _, err := os.Stat(candidate); err == nil {
			actualWebDir = candidate
		}
	}

	addr := fmt.Sprintf(":%d", *port)
	server := api.NewServer(addr, actualWebDir)

	fmt.Println("=========================================================")
	fmt.Println("   IDEAL ARENA - Axelrod Judger & REST API Platform      ")
	fmt.Println("=========================================================")
	fmt.Printf(" [Web Visualizer]  http://localhost:%d/\n", *port)
	fmt.Printf(" [API Health]      http://localhost:%d/api/v1/health\n", *port)
	fmt.Printf(" [Static Assets]   %s\n", actualWebDir)
	fmt.Println("=========================================================")
	fmt.Println("Server is listening. Press Ctrl+C to terminate.")

	if err := server.Start(); err != nil {
		log.Fatalf("Server terminated: %v", err)
	}
}
