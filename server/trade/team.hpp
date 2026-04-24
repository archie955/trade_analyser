#pragma once

#include <tuple>
#include <vector>
#include <unordered_map>
#include "player.hpp"
#include <algorithm>
#include <stdexcept>
#include <optional>
#include <functional>

// figure out the design pattern - players, lineup vs lineup vs players, starters, bench vs starters, bench vs just players

struct Team {
    std::vector<Player> players;
    double points;

    Team(std::vector<Player> players) {
        this->players = players;
        this->sort();
        this->projected_points();
    }

    void sort() {
        std::sort(this->players.begin(), this->players.end(),
        [](const Player& p1, const Player& p2){ return p1.points > p2.points; });
        this->projected_points();
    }

    void remove_player(const Player& player) {
        int n = this->players.size();
        for (int i = 0; i < n; ++i) {
            if (this->players[i].id == player.id) {
                this->players.erase(this->players.begin() + i);
                break;
            }
        }
        this->sort();
    }

    void add_player(const Player& player) {
        this->players.emplace_back(player);
        this->sort();
    }

    void projected_points() {
        double total = 0.0;
        std::unordered_map<SlotType, int> check;
        for (const auto& p: this->players) {
            SlotType type = p.pos;
            if (type == SlotType::WR || type == SlotType::RB) {
                if (check[type] < 2) {
                    check[type] += 1;
                    total += p.points;
                } else if (check[SlotType::FLEX] < 1) {
                    check[SlotType::FLEX] = 1;
                    total += p.points;
                }
            } else {
                if (check[type] == 0) {
                    check[type] = 1;
                    total += p.points;
                }
            }
        }
        this->points = total;
    }

    const std::optional<std::reference_wrapper<const Player>> qb() const {
        for (const auto& p: this->players) {
            if (p.pos == SlotType::QB) {
                return p;
            }
        }
        return std::nullopt;
    }

    const std::optional<std::reference_wrapper<const Player>> te() const {
        for (const auto& p: this->players) {
            if (p.pos == SlotType::TE) {
                return p;
            }
        }
        return std::nullopt;
    }

    const std::optional<std::reference_wrapper<const Player>> dst() const {
        for (const auto& p: this->players) {
            if (p.pos == SlotType::DST) {
                return p;
            }
        }
        return std::nullopt;
    }

    const std::optional<std::reference_wrapper<const Player>> k() const {
        for (const auto& p: this->players) {
            if (p.pos == SlotType::K) {
                return p;
            }
        }
        return std::nullopt;
    }

    const std::optional<std::reference_wrapper<const Player>> rb1() const {
        for (const auto& p: this->players) {
            if (p.pos == SlotType::RB) {
                return p;
            }
        }
        return std::nullopt;
    }

    const std::optional<std::reference_wrapper<const Player>> rb2() const {
        bool accept = false;
        for (const auto& p: this->players) {
            if (p.pos == SlotType::RB) {
                if (accept) {
                    return p;
                } 
                accept = true;
            }
        }
        return std::nullopt;
    }

    const std::optional<std::reference_wrapper<const Player>> wr1() const {
        for (const auto& p: this->players) {
            if (p.pos == SlotType::WR) {
                return p;
            }
        }
        return std::nullopt;
    }

    const std::optional<std::reference_wrapper<const Player>> wr2() const {
        bool accept = false;
        for (const auto& p: this->players) {
            if (p.pos == SlotType::WR) {
                if (accept) {
                    return p;
                } 
                accept = true;
            }
        }
        return std::nullopt;
    }

    const std::optional<std::reference_wrapper<const Player>> flex() const {
        int wr_count = 0;
        int rb_count = 0;
        for (const auto& p: this->players) {
            if (p.pos == SlotType::RB) {
                if (rb_count == 2) {
                    return p;
                }
                rb_count += 1;
            } else if (p.pos == SlotType::WR) {
                if (wr_count == 2) {
                    return p;
                }
                wr_count += 1;
            }
        }
        return std::nullopt;
    }
};

inline std::vector<double> trade(Team team1, Team team2, const Player& p1, const Player& p2) {
    double points1 = -1 * team1.points;
    double points2 = -1 * team2.points;
    team1.remove_player(p1);
    team2.remove_player(p2);
    team1.add_player(p2);
    team2.add_player(p1);
    points1 += team1.points;
    points2 += team2.points;
    return {points1, points2};
}

inline std::vector<double> two_trade(Team team1, Team team2, const Player& p1, const Player& p2, const Player& p3, const Player& p4) {
    double points1 = -1 * team1.points;
    double points2 = -1 * team2.points;
    team1.remove_player(p1);
    team1.remove_player(p2);
    team2.remove_player(p3);
    team2.remove_player(p4);
    team1.add_player(p3);
    team1.add_player(p4);
    team2.add_player(p1);
    team2.add_player(p2);
    points1 += team1.points;
    points2 += team2.points;
    return {points1, points2};
}

inline double points_over_replacement(Team team, const Player& p) {
    double old_points = team.points;
    team.remove_player(p);
    double new_points = team.points;
    return old_points - new_points;
}

inline std::vector<std::vector<SlotType>> identify_leverages(const Team& t1, const Team& t2) {
    std::vector<SlotType> a;
    std::vector<SlotType> b;

    auto t1_qb = t1.qb();
    auto t2_qb = t2.qb();
    if (t1_qb && t2_qb) {
        if (t1_qb->get().points >= t2_qb->get().points) {
            a.emplace_back(SlotType::QB);
        } else {
            b.emplace_back(SlotType::QB);
        }
    }

    auto t1_wr1 = t1.wr1();
    auto t2_wr1 = t2.wr1();
    if (t1_wr1 && t2_wr1) {
        if (t1_wr1->get().points >= t2_wr1->get().points) {
            a.emplace_back(SlotType::WR1);
        } else {
            b.emplace_back(SlotType::WR1);
        }
    }

    auto t1_wr2 = t1.wr2();
    auto t2_wr2 = t2.wr2();
    if (t1_wr2 && t2_wr2) {
        if (t1_wr2->get().points >= t2_wr2->get().points) {
            a.emplace_back(SlotType::WR2);
        } else {
            b.emplace_back(SlotType::WR2);
        }
    }
    
    auto t1_rb1 = t1.rb1();
    auto t2_rb1 = t2.rb1();
    if (t1_rb1 && t2_rb1) {
        if (t1_rb1->get().points >= t2_rb1->get().points) {
            a.emplace_back(SlotType::RB1);
        } else {
            b.emplace_back(SlotType::RB1);
        }
    }
    
    auto t1_rb2 = t1.rb2();
    auto t2_rb2 = t2.rb2();
    if (t1_rb2 && t2_rb2) {
        if (t1_rb2->get().points >= t2_rb2->get().points) {
            a.emplace_back(SlotType::RB2);
        } else {
            b.emplace_back(SlotType::RB2);
        }
    }
    
    auto t1_te = t1.te();
    auto t2_te = t2.te();
    if (t1_te && t2_te) {
        if (t1_te->get().points >= t2_te->get().points) {
            a.emplace_back(SlotType::TE);
        } else {
            b.emplace_back(SlotType::TE);
        }
    }
    
    auto t1_dst = t1.dst();
    auto t2_dst = t2.dst();
    if (t1_dst && t2_dst) {
        if (t1_dst->get().points >= t2_dst->get().points) {
            a.emplace_back(SlotType::DST);
        } else {
            b.emplace_back(SlotType::DST);
        }
    }
    
    auto t1_k = t1.k();
    auto t2_k = t2.k();
    if (t1_k && t2_k) {
        if (t1_k->get().points >= t2_k->get().points) {
            a.emplace_back(SlotType::K);
        } else {
            b.emplace_back(SlotType::K);
        }
    }
    
    return {a, b};
}

inline const std::optional<std::reference_wrapper<const Player>> player_from_slottype(const Team& team, const SlotType& type) {
    switch (type) {
        case SlotType::QB:
            return team.qb();

        case SlotType::RB1:
            return team.rb1();
        
        case SlotType::RB2:
            return team.rb2();

        case SlotType::WR1:
            return team.wr1();

        case SlotType::WR2:
            return team.wr2();

        case SlotType::TE:
            return team.te();

        case SlotType::DST:
            return team.dst();

        case SlotType::K:
            return team.k();

        case SlotType::FLEX:
            return team.flex();
    }
    throw std::runtime_error("Player not found");
}

inline std::vector<std::tuple<std::vector<Player>, double, std::vector<Player>, double>> evaluate_trades (const Team& t1, const Team& t2) {
    std::vector<std::vector<SlotType>> leverages = identify_leverages(t1, t2);
    std::vector<SlotType> a_lev = leverages[0];
    std::vector<SlotType> b_lev = leverages[1];
    std::vector<Player> a_players;
    std::vector<Player> b_players;
    for (const SlotType& type: a_lev) {
        auto p = player_from_slottype(t1, type);
        if (p) {
            a_players.emplace_back(p->get());
        }
    }
    for (const SlotType& type: b_lev) {
        auto p = player_from_slottype(t2, type);
        if (p) {
            b_players.emplace_back(p->get());
        }
    }

    std::vector<std::tuple<Player, Player>> single_trade_combos;
    for (const Player& p1: a_players) {
        for (const Player& p2: b_players) {
            single_trade_combos.emplace_back(std::make_tuple(p1, p2));
        }
    }
    std::vector<std::tuple<Player, Player, Player, Player>> double_trade_combos;
    int n1 = a_players.size();
    int n2 = b_players.size();

    for (int i = 0; i < n1 - 1; ++i) {
        for (int j = i+1; j < n1; ++j) {
            for (int k = 0; k < n2 - 1; ++k) {
                for (int l = k+1; l < n2; ++l) {
                    double_trade_combos.emplace_back(std::make_tuple(a_players[i], a_players[j], b_players[k], b_players[l]));
                }
            }
        }
    }

    std::vector<std::tuple<std::vector<Player>, double, std::vector<Player>, double>> res;
    

    for (const auto& single: single_trade_combos) {
        std::vector<double> trade_points = trade(t1, t2, std::get<0>(single), std::get<1>(single));
        if (trade_points[0] >= 0 && trade_points[1] >= 0) {
            res.emplace_back(std::make_tuple(std::vector<Player>{std::get<0>(single)}, trade_points[0], std::vector<Player>{std::get<1>(single)}, trade_points[1]));
        }
    }

    for (const auto& double_trade: double_trade_combos) {
        std::vector<double> trade_points = two_trade(t1, t2, std::get<0>(double_trade), std::get<1>(double_trade), std::get<2>(double_trade), std::get<3>(double_trade));
        if (trade_points[0] >= 0 && trade_points[1] >= 0) {
            res.emplace_back(std::make_tuple(std::vector<Player>{std::get<0>(double_trade), std::get<1>(double_trade)}, trade_points[0], std::vector<Player>{std::get<2>(double_trade), std::get<3>(double_trade)}, trade_points[1]));
        }
    }

    return res;
}