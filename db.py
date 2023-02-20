import sqlite3
import os



class DB:
    db_url : str

    def __init__(self, db_url : str):
        self.db_url = db_url

        if not os.path.exists(self.db_url):
            self.init_db()

    def call_db(self, query, *args):
        conn = sqlite3.connect(self.db_url)
        cur = conn.cursor()
        res = cur.execute(query, args)
        data = res.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        return data

    def init_db(self):
        print("Initierad")
        init_db_query = """
        CREATE TABLE IF NOT EXISTS SGC (
            id INTEGER PRIMARY KEY,
            first_name text NOT NULL,
            last_name text NULL,
            rank text NOT NULL,
            occupation text NULL
        );
        """
        init_db_query2 = """
        CREATE TABLE IF NOT EXISTS SYSTEM_LORDS (
            id INTEGER PRIMARY KEY,
            name text NOT NULL,
            appearance text NULL,
            mythos text NOT NULL,
            status text NOT NULL
        )
        """

        self.call_db(init_db_query)
        self.call_db(init_db_query2)

db = DB("Stargate.db")