#include <iostream>
#include <vector>
#include "includes/json.hpp"
#include "team.hpp"

using json = nlohmann::json;

int main() {
    // Read JSON from stdin
    json input;
    std::cin >> input;

    std::vector<Player> team1_players;
    std::vector<Player> team2_players;

    for (const auto& p : input["team1"]) {
        team1_players.emplace_back(
            p["id"],
            p["name"],
            p["points"],
            p["pos"]
        );
    }

    for (const auto& p : input["team2"]) {
        team2_players.emplace_back(
            p["id"],
            p["name"],
            p["points"],
            p["pos"]
        );
    }

    Team t1(team1_players);
    Team t2(team2_players);

    auto trades = evaluate_trades(t1, t2);

    // Convert result to JSON
    json output = json::array();

    for (const auto& trade : trades) {
        json trade_json;

        auto players1 = std::get<0>(trade);
        double delta1 = std::get<1>(trade);
        auto players2 = std::get<2>(trade);
        double delta2 = std::get<3>(trade);

        trade_json["team1_gain"] = delta1;
        trade_json["team2_gain"] = delta2;

        trade_json["team1_players"] = json::array();
        for (const auto& p : players1) {
            trade_json["team1_players"].push_back(p.name);
        }

        trade_json["team2_players"] = json::array();
        for (const auto& p : players2) {
            trade_json["team2_players"].push_back(p.name);
        }

        output.push_back(trade_json);
    }

    std::cout << output.dump() << std::endl;

    return 0;
}