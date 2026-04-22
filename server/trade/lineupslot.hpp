#pragma once

#include "enums.hpp"
#include "player.hpp"
#include <optional>

struct LineupSlot {
    SlotType type;
    std::optional<Player> player;

    bool isFilled() const {
        return player.has_value();
    }

    bool canAccept(const Player& p) const {
        switch (type) {
            case SlotType::QB:
                return p.position == Position::QB;

            case SlotType::RB:
                return p.position == Position::RB;
                
            case SlotType::WR:
                return p.position == Position::WR;
                
            case SlotType::TE:
                return p.position == Position::TE;
                
            case SlotType::DST:
                return p.position == Position::DST;
                
            case SlotType::K:
                return p.position == Position::K;
                
            case SlotType::FLEX:
                return (p.position == Position::WR || p.position == Position::RB);

            case SlotType::BENCH:
                return true;            
        }
        return false;
    }

    LineupSlot(SlotType type) {
        this->type = type;
    }
};