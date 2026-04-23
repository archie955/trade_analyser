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
    switch (pos) {
        case "QB":
            return SlotType::QB;
        
        case "RB":
            return SlotType::RB;
        
        case "WR":
            return SlotType::WR;

        case "TE":
            return SlotType::TE;
        
        case "DST":
            return SlotType::DST;
        
        case "K":
            return SlotType::K;
    }
}