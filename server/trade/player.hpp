#include <string>
#include "position.hpp"

struct Player {
    int id;
    std::string name;
    double points;
    Position pos;

    Player(int id, std::string name, double points, Position pos;) {
        this->id = id;
        this->name = name;
        this->points = points;
        this->pos = pos;
    }
};

