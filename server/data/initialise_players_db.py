import pandas as pd
from models.datatypes import Teams, Positions
from models import models
from database.database import AsyncSessionLocal
import asyncio


def read_data_and_transform():
    qb = pd.read_csv("data/QB.csv")
    qb["pos"] = Positions.QB
    rb = pd.read_csv("data/RB.csv")
    rb["pos"] = Positions.RB
    wr = pd.read_csv("data/WR.csv")
    wr["pos"] = Positions.WR
    te = pd.read_csv("data/TE.csv")
    te["pos"] = Positions.TE
    dst = pd.read_csv("data/DST.csv")
    dst["pos"] = Positions.DST
    k = pd.read_csv("data/K.csv")
    k["pos"] = Positions.K
    data = [qb, rb, wr, te, dst, k]
    return data

async def add_data():
    data = read_data_and_transform()
    async with AsyncSessionLocal() as db:
        for df in data:
            df.columns = df.columns.str.strip().str.upper()

            d = df.to_dict(orient="records")

            filtered_data = [
                {
                    "name": row.get("PLAYER NAME"),
                    "team": Teams[row.get("TEAM")],
                    "position": row.get("POS"),
                    "points_ppr": row.get("FANTASYPTS"),
                    "points_halfppr": row.get("FANTASYPTS"),
                    "points_noppr": row.get("FANTASYPTS")
                }
                for row in d
            ]

            for item in filtered_data:
                db.add(models.Player(**item))

        await db.commit()

    return {"status": "success"}

    




if __name__ == "__main__":
    asyncio.run(add_data())
    print("completed")