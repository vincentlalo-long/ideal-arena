mod strategy;

use serde_json::{json, Value};
use std::io::{self, BufRead};
use strategy::{MyStrategy, Strategy};

const SDK: &str = "rust/0.2.0";

#[derive(serde::Deserialize)]
#[serde(tag = "type", rename_all = "lowercase")]
enum Request {
    Hello,
    Reset {
        #[serde(default)]
        episode: String,
        #[serde(default)]
        seed: u64,
    },
    Act {
        #[serde(default)]
        t: i64,
        #[serde(default)]
        obs: Value,
    },
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

        let request = match serde_json::from_str::<Request>(&line) {
            Ok(request) => request,
            Err(_) => {
                if serde_json::from_str::<Value>(&line).is_err() {
                    eprintln!("arena-agent: ignoring malformed line");
                }
                continue;
            }
        };

        match request {
            Request::Hello => {
                println!("{}", json!({"type": "ready", "sdk": SDK}));
            }
            Request::Reset { episode, seed } => {
                bot.reset(seed);
                println!("{}", json!({"type": "ack", "episode": episode}));
            }
            Request::Act { t, obs } => {
                let action = bot.act(&obs);
                println!("{}", json!({"type": "action", "t": t, "action": action}));
            }
        }
    }
}
