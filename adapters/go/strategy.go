package main

type Strategy interface {
	Reset(seed int64)
	Act(observation any) any
}

type MyStrategy struct{}

func (s *MyStrategy) Reset(seed int64) {}

func (s *MyStrategy) Act(observation any) any {
	return nil
}
