#pragma once

#include <string>
#include "enums.hpp"

struct Player {
    int id;
    std::string name;
    double points;
    SlotType position;

    Player(int id, std::string name, double points, std::string position) {
        this->id = id;
        this->name = name;
        this->points = points;
        this->position = string_to_enum(position);
    }
};


