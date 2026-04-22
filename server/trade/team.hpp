#pragma once

#include <vector>
#include "player.hpp"
#include <algorithm>

// figure out the design pattern - players, lineup vs lineup vs players, starters, bench vs starters, bench vs just players

struct Team {
    std::vector<Player> players;

    Team(std::vector<Player> players) {
        this->players = players;
    }

    void sort() {
        std::sort(this->players.begin(), this->players.end(),
        [](Player& p1, Player& p2){ return p1.points > p2.points});
    }

};

