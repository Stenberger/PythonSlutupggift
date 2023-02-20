from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from db import DB
# Kolla Lektion 11 för referens


class SG(BaseModel):
    id : int = None
    first_name : str
    last_name : str
    rank : str
    occupation : str

class SL(BaseModel):
    id : int = None
    name : str
    appearance: str
    mythos : str
    status : str
    
    

app = FastAPI()
db = DB("Stargate.db")


app.curr_id = 1
# app.sg: List[SG] = []
# app.sl: List[SL] = []


@app.get("/")
def root():
    return "Välkommen till min nördiga Stargate-lista med onödig info"

# Tänker att vi hämtar all info från SGC
@app.get("/sgc")
def get_sgc():
    get_sgc_query = """
    SELECT * FROM SGC 
    """
    data = db.call_db(get_sgc_query)
    sgc = []
    for element in data:
        id, first_name, last_name, rank, occupation = element
        sgc.append(SG(id=id, first_name= first_name, last_name= last_name, rank= rank, occupation= occupation))
        #print(sgc)
    return sgc
    
# Hämta information om EN karaktär
@app.get("/sgc/{id}")
def get_sgc_id(id: int):
    get_sgc_query2 = """
    SELECT * FROM SGC 
    WHERE id = ?
    """
    data = db.call_db(get_sgc_query2, id)
    sgc = []
    for element in data:
        id, first_name, last_name, rank, occupation = element
        sgc.append(SG(id=id, first_name= first_name, last_name= last_name, rank= rank, occupation= occupation))
        #print(sgc)
    return sgc

# Hämt all System Lords
@app.get("/sl")
def get_sl():
    get_sl_query = """
    SELECT * FROM SYSTEM_LORDS 
    """
    data = db.call_db(get_sl_query)
    sl = []
    for element in data:
        id, name, appearance, mythos, status = element
        sl.append(SL(id=id, name= name, appearance= appearance, mythos=mythos, status= status))
        print(sl)
    return sl

# Hämta en System Lord
@app.get("/sl/{id}")
def get_sl_id(id : int):
    get_sl_query = """
    SELECT * FROM SYSTEM_LORDS 
    WHERE id = ?
    """
    data = db.call_db(get_sl_query, id)
    sl = []
    for element in data:
        id, name, appearance, mythos, status = element
        sl.append(SL(id=id, name= name, appearance= appearance, mythos=mythos, status= status))
        print(sl)
    return sl
    
# Hämta tillbaka både SGC och SL i samma request. Lägg i .dict för att lösa json
@app.get("/all")
def get_all():
    get_sgc = """
    SELECT * FROM SGC
    """
    get_sl = """
    SELECT * FROM SYSTEM_LORDS
    """
    sgc_list = db.call_db(get_sgc)
    sl_list = db.call_db(get_sl)
    data = {
        "SGC": sgc_list,
        "SYSTEM_LORDS": sl_list
    }
    return data

# Lägg till i SGC med all relevant info.
@app.post("/addsgc")
def create_sgc(sg: SG):
    insert_query = """
    INSERT INTO SGC (first_name, last_name, rank, occupation)
    VALUES (
        ?, ?, ?, ?
        )
    """    
    db.call_db(insert_query, sg.first_name, sg.last_name, sg.rank, sg.occupation)
    return sg.dict()

#Lägg till all relevant information i SL
@app.post("/addsl")
def create_sl(sl: SL):
    insert_query = """
    INSERT INTO SYSTEM_LORDS (name, appearance, mythos, status)
    VALUES (
        ?, ?, ?, ?
        )
    """    
    db.call_db(insert_query, sl.name, sl.appearance, sl.mythos, sl.status)
    return sl.dict()

# Separera borttagningen med två separata backend funktioner
# Ta bort en från SGC.
@app.delete("/delete_sgc/{id}")
def delete_sgc(id: int):
    delete_sgc_query = """
    DELETE FROM SGC
    WHERE id = ?
    """
    db.call_db(delete_sgc_query, id)
    return f"ID: {id} raderat från Stargate Command."

# Ta bort från SL med specifik ID
@app.delete("/delete_sl/{id}")
def delete_sl(id: int):
    delete_sl_query = """
    DELETE FROM SYSTEM_LORDS
    WHERE id = ?
    """
    db.call_db(delete_sl_query, id)
    return f"ID: {id} raderat från System Lords."

# Uppdatera i SGC från specifik ID
@app.put("/update_sgc/{id}")
def update_sgc(id: int, new_info: SG):        
        update_table_sgc = """
        UPDATE SGC
        SET first_name = ?,
        last_name = ?,
        rank = ?,
        occupation = ?
        WHERE id = ?
        """

        db.call_db(update_table_sgc, new_info.first_name, new_info.last_name, new_info.rank, new_info.occupation, id)    
        return {"success" : True}

# Lika samma med SL databasen
@app.put("/update_sl/{id}")
def update_sl(id: int, new_info: SL):       
        update_table_sl = """
        UPDATE SYSTEM_LORDS
        SET name = ?,
        appearance = ?,
        mythos = ?,
        status = ?
        WHERE id = ?
        """
        db.call_db(update_table_sl, new_info.name, new_info.appearance, new_info.mythos, new_info.status, id)    
        return {"success" : True}