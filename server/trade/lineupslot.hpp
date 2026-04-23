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
                return p.position == SlotType::QB;

            case SlotType::RB:
                return p.position == SlotType::RB;
                
            case SlotType::WR:
                return p.position == SlotType::WR;
                
            case SlotType::TE:
                return p.position == SlotType::TE;
                
            case SlotType::DST:
                return p.position == SlotType::DST;
                
            case SlotType::K:
                return p.position == SlotType::K;
                
            case SlotType::FLEX:
                return (p.position == SlotType::WR || p.position == SlotType::RB);

            case SlotType::BENCH:
                return true;            
        }
        return false;
    }

    LineupSlot(SlotType type) {
        this->type = type;
    }
};