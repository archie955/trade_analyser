#include <vector>
#include "player.hpp"

// figure out the design pattern - players, lineup vs lineup vs players, starters, bench vs starters, bench vs just players

struct Team {
    std::vector<Player> players;

    Team(std::vector<Player> players) {
        this->players = players;
    }
};

