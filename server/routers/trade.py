import json
import subprocess

data = {
    "team1": [
        {"id": 1, "name": "Josh Allen", "points": 25.3, "pos": "QB"},
        {"id": 2, "name": "Theo Johnson", "points": 9.0, "pos": "TE"},
        {"id": 3, "name": "Jaxson Dart", "points": 24.8, "pos": "QB"},
        {"id": 4, "name": "Tyler Higbee", "points": 8.0, "pos": "TE"}
    ],
    "team2": [
        {"id": 5, "name": "Fernando Mendoza", "points": 19.0, "pos": "QB"},
        {"id": 6, "name": "Tyler Warren", "points": 15.0, "pos": "TE"},
        {"id": 7, "name": "Tyler Shough", "points": 17.0, "pos": "QB"},
        {"id": 8, "name": "George Kittle", "points": 14.0, "pos": "TE"}
    ]
}

proc = subprocess.Popen(
    ["./trade_sim"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

output, _ = proc.communicate(json.dumps(data))
result = json.loads(output)

print(result)