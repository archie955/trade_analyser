from models.datatypes import Teams, Positions

data = {
    "team1": [
        {"id": 1, "name": "Josh Allen", "points": 25.3, "position": Positions.QB, "team": Teams.BUF},
        {"id": 2, "name": "Theo Johnson", "points": 9.0, "position": Positions.TE, "team": Teams.NYG},
        {"id": 3, "name": "Jaxson Dart", "points": 24.8, "position": Positions.QB, "team": Teams.NYG},
        {"id": 4, "name": "Tyler Higbee", "points": 8.0, "position": Positions.TE, "team": Teams.LAR},
        {"id": 9, "name": "Brandon Aubrey", "points": 10.0, "position": Positions.K, "team": Teams.DAL},
        {"id": 10, "name": "Chris Boswell", "points": 9.0, "position": Positions.K, "team": Teams.PIT},
        {"id": 13, "name": "CAR", "points": 5.0, "position": Positions.DST, "team": Teams.CAR},
        {"id": 14, "name": "ARI", "points": 4.0, "position": Positions.DST, "team": Teams.ARI}
    ],
    "team2": [
        {"id": 5, "name": "Fernando Mendoza", "points": 19.0, "position": Positions.QB, "team": Teams.LV},
        {"id": 6, "name": "Tyler Warren", "points": 15.0, "position": Positions.TE, "team": Teams.IND},
        {"id": 7, "name": "Tyler Shough", "points": 17.0, "position": Positions.QB, "team": Teams.NO},
        {"id": 8, "name": "George Kittle", "points": 14.0, "position": Positions.TE, "team": Teams.SF},
        {"id": 11, "name": "Younghoe Koo", "points": 6.0, "position": Positions.K, "team": Teams.NYG},
        {"id": 12, "name": "Graham Gano", "points": 4.0, "position": Positions.K, "team": Teams.NYG},
        {"id": 15, "name": "NYG", "points": 9.0, "position": Positions.DST, "team": Teams.NYG},
        {"id": 16, "name": "HOU", "points": 8.0, "position": Positions.DST, "team": Teams.HOU}
    ]
}