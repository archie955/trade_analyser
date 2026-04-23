#include <vector>
#include <unordered_map>
#include "lineupslot.hpp"
#include "enums.hpp"
#include "team.hpp"

struct LineUp {
    LineupSlot(SlotType::QB) qb;
    std::vector<LineupSlot(SlotType::RB)> rb;
    std::vector<LineupSlot(SlotType::WR)> wr;
    LineupSlot(SlotType::FLEX) flex;
    LineupSlot(SlotType::TE) te;
    LineupSlot(SlotType::DST) dst;
    LineupSlot(SlotType::K) k;
    std::vector<LineupSlot(SlotType::BENCH) bench;
    double points;

    double projectedScore() const {
        double total = 0.0;
        total += this->qb->player->points;
        total += this->rb[0]->player->points;
        total += this->rb[1]->player->points;
        total += this->wr[0]->player->points;
        total += this->wr[1]->player->points;
        total += this->flex->player->points;
        total += this->te->player->points;
        total += this->dst->player->points;
        total += this->k->player->points;
        this->points = total;
    }

    LineUp(const Team& team) {
        team.sort();
        for (const auto& player: team->players) {
            switch (player->pos) {
                case SlotType::QB:
                    if (!this->qb.isFilled()) {
                        this->qb->player = player;
                    } else {
                        this->bench.emplace_back(player);
                    }
                    break;
                
                case SlotType::WR:
                    if (!this->wr[0].isFilled()) {
                        this->wr[0]->player = player;
                    } else if (!this->wr[1].isFilled()) {
                        this->wr[1]->player = player;
                    } else if (!this->flex.isFilled()) {
                        this->flex->player = player;
                    }
                    break;

                case SlotType::RB:
                    if (!this->rb[0].isFilled()) {
                        this->rb[0]->player = player;
                    } else if (!this->rb[1].isFilled()) {
                        this->rb[1]->player = player;
                    } else if (!this->flex.isFilled()) {
                        this->flex->player = player;
                    }
                    break;

                case SlotType::TE:
                    if (!this->te.isFilled()) {
                        this->te->player = player;
                    } else {
                        this->bench.emplace_back(player);
                    }
                    break;

                case SlotType::DST:
                    if (!this->dst.isFilled()) {
                        this->dst->player = player;
                    } else {
                        this->bench.emplace_back(player);
                    }
                    break;
                
                case SlotType::K:
                    if (!this->k.isFilled()) {
                        this->k->player = player;
                    } else {
                        this->bench.emplace_back(player);
                    }
                    break;
            }
        }

        this->projectedScore();
    }

}

