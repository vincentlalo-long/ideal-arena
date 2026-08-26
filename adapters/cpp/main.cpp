#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include "strategy.hpp"

std::vector<int> parse_array(const std::string& json, const std::string& key) {
    std::vector<int> res;
    size_t pos = json.find("\"" + key + "\"");
    if (pos == std::string::npos) return res;
    size_t start = json.find('[', pos);
    size_t end = json.find(']', start);
    if (start == std::string::npos || end == std::string::npos) return res;

    std::string sub = json.substr(start + 1, end - start - 1);
    std::stringstream ss(sub);
    std::string token;
    while (std::getline(ss, token, ',')) {
        size_t first = token.find_first_not_of(" \t\r\n");
        if (first != std::string::npos) {
            res.push_back(std::stoi(token.substr(first)));
        }
    }
    return res;
}

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);

    MyStrategy bot;
    std::string line;

    while (std::getline(std::cin, line)) {
        if (line.empty()) continue;

        if (line.find("\"RESET\"") != std::string::npos) {
            bot.reset();
            std::cout << "{\"status\":\"OK\"}\n" << std::flush;
        } else {
            auto hist_self = parse_array(line, "history_self");
            auto hist_opp = parse_array(line, "history_opp");
            int action = bot.step(hist_self, hist_opp);
            std::cout << "{\"action\":" << action << "}\n" << std::flush;
        }
    }
    return 0;
}
