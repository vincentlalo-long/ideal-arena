#pragma once

#include "json.hpp"

class IStrategy {
public:
    virtual ~IStrategy() = default;
    virtual void reset(long long seed) { (void)seed; }
    virtual Json act(const Json& observation) = 0;
};

class MyStrategy : public IStrategy {
public:
    Json act(const Json& observation) override {
        (void)observation;
        return Json();
    }
};
