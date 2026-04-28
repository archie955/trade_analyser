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

SlotType string_to_enum(const std::string& position) {
    if (position == "QB") return SlotType::QB;
    if (position == "RB") return SlotType::RB;
    if (position == "WR") return SlotType::WR;
    if (position == "TE") return SlotType::TE;
    if (position == "DST") return SlotType::DST;
    if (position == "K") return SlotType::K;
    return SlotType::BENCH;
}