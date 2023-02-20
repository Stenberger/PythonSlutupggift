import json
from db import DB

db = DB("Stargate.db")

populate_sgc = """
INSERT INTO SGC (
    first_name, 
    last_name, 
    rank, 
    occupation
) VALUES(
    ?, ?, ?, ?
    )
"""
populate_sl = """
INSERT INTO SYSTEM_LORDS (
    name,
    appearance,
    mythos,
    status
) VALUES (
    ?, ?, ?, ?
    )
"""

with open("seed.json", "r") as seed:
    data = json.load(seed)

    for sgc in data["SGC"]:
        db.call_db(populate_sgc, sgc["first_name"], sgc["last_name"], sgc["rank"], sgc["occupation"])

    for sl in data["SYSTEM_LORDS"]:
        db.call_db(populate_sl, sl["name"], sl["appearance"], sl["mythos"], sl["status"])