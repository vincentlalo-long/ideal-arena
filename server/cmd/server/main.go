package main

import (
	"flag"
	"fmt"
	"log"

	"ideal-arena/server/internal/api"
)

func main() {
	port := flag.Int("port", 8080, "HTTP server port")
	flag.Parse()

	addr := fmt.Sprintf(":%d", *port)
	server := api.NewServer(addr)

	fmt.Println("=========================================================")
	fmt.Println("   IDEAL ARENA - Judger & REST API Platform              ")
	fmt.Println("=========================================================")
	fmt.Printf(" [API Health]      http://localhost:%d/api/v1/health\n", *port)
	fmt.Printf(" [Domains]         http://localhost:%d/api/v1/domains\n", *port)
	fmt.Printf(" [Problems]        http://localhost:%d/api/v1/problems\n", *port)
	fmt.Printf(" [Presets]         http://localhost:%d/api/v1/presets\n", *port)
	fmt.Println("=========================================================")
	fmt.Println("Server is listening. Press Ctrl+C to terminate.")

	if err := server.Start(); err != nil {
		log.Fatalf("Server terminated: %v", err)
	}
}
