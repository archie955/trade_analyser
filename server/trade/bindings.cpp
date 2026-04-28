#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>

#include "team.hpp"

namespace py = pybind11;

py::list run_trade_engine(py::list team1_data, py::list team2_data) {
    std::vector<Player> team1_players;
    std::vector<Player> team2_players;

    for (auto item : team1_data) {
        auto p = item.cast<py::dict>();

        team1_players.emplace_back(
            p["id"].cast<int>(),
            p["name"].cast<std::string>(),
            p["points"].cast<double>(),
            p["position"].cast<std::string>()
        );
    }

    for (auto item : team2_data) {
        auto p = item.cast<py::dict>();

        team2_players.emplace_back(
            p["id"].cast<int>(),
            p["name"].cast<std::string>(),
            p["points"].cast<double>(),
            p["position"].cast<std::string>()
        );
    }

    Team t1(team1_players);
    Team t2(team2_players);

    auto trades = evaluate_trades(t1, t2);

    py::list result;
    
    for (const auto& trade : trades) {
        py::dict row;

        auto players1 = std::get<0>(trade);
        double gain1 = std::get<1>(trade);

        auto players2 = std::get<2>(trade);
        double gain2 = std::get<3>(trade);

        py::list p1_names;
        py::list p2_names;

        for (const auto& p : players1)
            p1_names.append(std::make_tuple(p.id, p.name));

        for (const auto& p : players2)
            p2_names.append(std::make_tuple(p.id, p.name));

        row["team1_players"] = p1_names;
        row["team2_players"] = p2_names;
        row["team1_gain"] = gain1;
        row["team2_gain"] = gain2;

        result.append(row);
    }

    return result;
}

PYBIND11_MODULE(trade_engine, m) {
    m.doc() = "Fantasy football trade engine";
    m.def("evaluate_trades", &run_trade_engine);
}

