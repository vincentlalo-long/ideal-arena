CXX ?= g++
CXXFLAGS ?= -O3 -std=c++17 -Wall

all: bot

bot: main.cpp strategy.hpp
	$(CXX) $(CXXFLAGS) main.cpp -o bot

clean:
	rm -f bot bot.exe
