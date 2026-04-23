#pragma once

#include <string>
#include "enums.hpp"

struct Player {
    int id;
    std::string name;
    double points;
    SlotType pos;

    Player(int id, std::string name, double points, std::string pos) {
        this->id = id;
        this->name = name;
        this->points = points;
        this->pos = string_to_enum(pos);
    }
};


