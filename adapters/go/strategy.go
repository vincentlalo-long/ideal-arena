package main

type Strategy interface {
	Reset()
	Step(historySelf []int, historyOpp []int) int
}

type MyStrategy struct{}

func (s *MyStrategy) Reset() {}

func (s *MyStrategy) Step(historySelf []int, historyOpp []int) int {
	if len(historyOpp) == 0 {
		return 1
	}
	return historyOpp[len(historyOpp)-1]
}
