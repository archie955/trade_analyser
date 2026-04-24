#pragma once

#include <string>

enum class Position {
    QB,
    RB,
    WR,
    TE,
    DST,
    K
};

enum class SlotType {
    QB,
    RB,
    WR,
    TE,
    DST,
    K,
    FLEX,
    BENCH,
    RB1,
    RB2,
    WR1,
    WR2
};

SlotType string_to_enum(const std::string& pos) {
    if (pos == "QB") return SlotType::QB;
    if (pos == "RB") return SlotType::RB;
    if (pos == "WR") return SlotType::WR;
    if (pos == "TE") return SlotType::TE;
    if (pos == "DST") return SlotType::DST;
    if (pos == "K") return SlotType::K;
    return SlotType::BENCH;
}