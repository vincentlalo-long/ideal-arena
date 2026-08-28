mod strategy;

use std::io::{self, BufRead};
use serde::{Deserialize, Serialize};
use strategy::{MyStrategy, Strategy};

#[derive(Deserialize)]
struct Request {
    #[serde(default)]
    command: String,
    #[serde(default)]
    history_self: Vec<i32>,
    #[serde(default)]
    history_opp: Vec<i32>,
}

#[derive(Serialize)]
struct StepResponse {
    action: i32,
}

#[derive(Serialize)]
struct StatusResponse {
    status: String,
}

fn main() {
    let mut bot = MyStrategy::new();
    let stdin = io::stdin();

    for line in stdin.lock().lines() {
        let line = match line {
            Ok(l) => l.trim().to_string(),
            Err(_) => break,
        };

        if line.is_empty() {
            continue;
        }

        if let Ok(req) = serde_json::from_str::<Request>(&line) {
            if req.command == "RESET" {
                bot.reset();
                let resp = StatusResponse {
                    status: "OK".to_string(),
                };
                println!("{}", serde_json::to_string(&resp).unwrap());
            } else {
                let action = bot.step(&req.history_self, &req.history_opp);
                let resp = StepResponse { action };
                println!("{}", serde_json::to_string(&resp).unwrap());
            }
        }
    }
}
