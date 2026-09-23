#include <iostream>
#include <string>

#include "strategy.hpp"

const char* const SDK = "cpp/0.2.0";

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);

    MyStrategy bot;
    std::string line;

    while (std::getline(std::cin, line)) {
        if (line.find_first_not_of(" \t\r\n") == std::string::npos) continue;

        Json msg;
        try {
            msg = Json::parse(line);
        } catch (const std::exception&) {
            std::cerr << "arena-agent: ignoring malformed line\n";
            continue;
        }
        if (!msg.is_object()) continue;

        const Json& type_value = msg["type"];
        const std::string type = type_value.is_string() ? type_value.as_string() : "";

        if (type == "hello") {
            std::cout << "{\"type\":\"ready\",\"sdk\":\"" << SDK << "\"}\n" << std::flush;
        } else if (type == "reset") {
            const Json& seed_value = msg["seed"];
            long long seed = seed_value.is_number() ? seed_value.as_int() : 0;
            bot.reset(seed);

            const Json& episode_value = msg["episode"];
            std::string episode = episode_value.is_string() ? episode_value.as_string() : "";
            Json ack = Json::object();
            ack["type"] = "ack";
            ack["episode"] = episode;
            std::cout << ack.dump() << "\n" << std::flush;
        } else if (type == "act") {
            const Json& t_value = msg["t"];
            long long t = t_value.is_number() ? t_value.as_int() : 0;
            Json action = bot.act(msg["obs"]);

            Json response = Json::object();
            response["type"] = "action";
            response["t"] = t;
            response["action"] = action;
            std::cout << response.dump() << "\n" << std::flush;
        }
    }
    return 0;
}
