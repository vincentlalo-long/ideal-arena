pub trait Strategy {
    fn reset(&mut self) {}
    fn step(&mut self, history_self: &[i32], history_opp: &[i32]) -> i32;
}

pub struct MyStrategy;

impl MyStrategy {
    pub fn new() -> Self {
        Self
    }
}

impl Strategy for MyStrategy {
    fn reset(&mut self) {}

    fn step(&mut self, _history_self: &[i32], history_opp: &[i32]) -> i32 {
        if history_opp.is_empty() {
            return 1;
        }
        *history_opp.last().unwrap_or(&1)
    }
}
