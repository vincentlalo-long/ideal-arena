#pragma once
#include <vector>
#include <string>

class IStrategy {
public:
    virtual ~IStrategy() = default;
    virtual void reset() {}
    virtual int step(const std::vector<int>& history_self, const std::vector<int>& history_opp) = 0;
};

class MyStrategy : public IStrategy {
public:
    void reset() override {}

    int step(const std::vector<int>& history_self, const std::vector<int>& history_opp) override {
        if (history_opp.empty()) {
            return 1;
        }
        return history_opp.back();
    }
};
