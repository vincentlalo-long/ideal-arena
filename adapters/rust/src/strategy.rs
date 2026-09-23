use serde_json::Value;

pub trait Strategy {
    fn reset(&mut self, _seed: u64) {}
    fn act(&mut self, observation: &Value) -> Value;
}

pub struct MyStrategy;

impl MyStrategy {
    pub fn new() -> Self {
        Self
    }
}

impl Strategy for MyStrategy {
    fn reset(&mut self, _seed: u64) {}

    fn act(&mut self, _observation: &Value) -> Value {
        Value::Null
    }
}
