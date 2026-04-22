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
    BENCH
};

Position string_to_enum(const std::string& pos) {
    switch (pos) {
        case "QB":
            return Position::QB;
        
        case "RB":
            return Position::RB;
        
        case "WR":
            return Position::WR;

        case "TE":
            return Position::TE;
        
        case "DST":
            return Position::DST;
        
        case "K":
            return Position::K;
    }
}