#include <vector>
#include "lineupslot.hpp"
#include "enums.hpp"
#include "team.hpp"

struct Lineup {
    std::vector<LineupSlot> slots;

    double projectedScore() const {
        double total = 0.0;
        for (const auto& slot: slots) {
            if (slot.type != SlotType::BENCH && slot.player) {
                total += slot.player->points;
            }
        }
        return total;
    }

    Lineup(std::vector<LineupSlot>& line) {
        this->slots = line;
    }
}

inline Lineup createStandardLineup() {
    std::vector<LineupSlot> line = {
        LineupSlot(SlotType::QB),
        LineupSlot(SlotType::RB),
        LineupSlot(SlotType::RB),
        LineupSlot(SlotType::WR),
        LineupSlot(SlotType::WR),
        LineupSlot(SlotType::FLEX),
        LineupSlot(SlotType::TE),
        LineupSlot(SlotType::DST),
        LineupSlot(SlotType::K)
    };
    return Lineup(line);
}

inline Lineup optimiseLineup(const Team& team, Lineup lineup) {
    team.sort();
    auto players = team.players;
    for (const auto& player: players) {
        for (auto& slot: lineup.slots) {
            if (!slot.isFilled() && slot.canAccept(player)) {
                slot.player = player;
                break;
            }
        }
    }
    return lineup;
}

