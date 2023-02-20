import requests
from API import SG
from API import SL
from db import DB

db = DB("Stargate.db")


def url(route:str):
    return f"http://127.0.0.1:8000{route}"

def print_menu():
    print(
        """
    1. Lägg till
    2. Hämta 
    3. Ta bort 
    4. Uppdatera
    5. Avsluta
    """
    )

def add_post():
    print("Lägg till ")
    print(
        """
        Vill du lägga till i SGC eller System Lords?
        1. SGC
        2. System Lords
        """
        )
    # Måste kunna välja om man vill lägga till info i SGC eller System Lords
    # Om val är 1, lägg till i SGC

    choice_input = input("> ")
    if choice_input == "1":
        first_name = input("Förnamn: ")
        last_name = input("Efternamn: ")
        rank = input("Rank: ")
        occupation = input("Sysselsättning: ")
        new_sg = SG(first_name = first_name, last_name = last_name, rank = rank, occupation = occupation) # Gör ett objekt att stoppa in i DB
        res = requests.post(url("/addsgc"), json =(new_sg.dict())) # Posta det som JSON
        
    # Om val är 2 lägg till i System Lords
    elif choice_input == "2":
        name = input("Namn: ")
        appearance = input("Beskrivning av utseende: ")
        mythos = input("Mythos: ")
        status = input("Status: ")
        new_sl = SL(name = name, appearance = appearance, mythos = mythos, status = status)
        res = requests.post(url("/addsl"), json =(new_sl.dict()))
        
    # Om det inte är 1 eller 2 så kommer man tillbaka till denna menyn

    else:
        print("Du måste välja 1 eller 2. ")
        add_post() #Anropar rekursivt

    print(res.json()) #Skriv ut vad man lagt till.

    # Gjorde en specifik funktion för att kunna populera en variabel från databasen till uppdateringsfunktionen    

def get_updatesgc():
    sgc = []
    res = requests.get(url("/sgc"))
    if not res.status_code == 200:
        return
    data = res.json()
    for sg in data:
        sg = SG(**sg)
        sgc.append(sg)
    return sgc

    # Exakt samma sak fast från System Lords

def get_updatesl():
    sl = []
    res = requests.get(url("/sl"))
    if not res.status_code == 200:
        return
    data = res.json()
    for sld in data:
        sld = SL(**sld)
        sl.append(sld)
    return sl

    # Hämta info från databasen, var tvungen att lägga lite logik i menyprogrammet för att slippa hämta all info direkt man körde det.

def get_info(get_input: str):
    sgc = []
    sl = []

    if get_input == "1":

        res = requests.get(url("/sgc"))
        if not res.status_code == 200:
            return
        data = res.json()
        for sg in data:
            sg = SG(**sg)
            sgc.append(sg)
            print("")
            print(f"ID: {sg.id}")
            print(f"Förnamn: {sg.first_name}")
            print(f"Efternamn: {sg.last_name}")
            print(f"Rank: {sg.rank}")
            print(f"Sysselsättning: {sg.occupation}\n")
                    
        return sgc
    
    elif get_input == "2":
        res = requests.get(url("/sl"))
        if not res.status_code == 200:
            return
        data = res.json()
        for sld in data:
            sld = SL(**sld)
            sl.append(sld)
            print("")
            print(f"ID: {sld.id}")
            print(f"Namn: {sld.name}")
            print(f"Utseende: {sld.appearance}")
            print(f"Mythos: {sld.mythos}")
            print(f"Status: {sld.status}\n")
        
        return sl
        # Eftersom vi returnerar en json med lista var jag tvungen att loopa och skriva ut specifika element för att få en vettig utskrift
    elif get_input == "3":
        res = requests.get(url("/all"))
        if not res.status_code == 200:
            return
        data = res.json()
        for key in data:
            for sg_class in data[key]:
                if key == "SGC":
                    print("")
                    print(f"ID: {sg_class[0]}")
                    print(f"Förnamn: {sg_class[1]}")
                    print(f"Efternamn: {sg_class[2]}")
                    print(f"Rank: {sg_class[3]}")
                    print(f"Sysselsättning: {sg_class[4]}\n")

                elif key == "SYSTEM_LORDS":
                    print("")
                    print(f"ID: {sg_class[0]}")
                    print(f"Namn: {sg_class[1]}")
                    print(f"Utseende: {sg_class[2]}")
                    print(f"Mythos: {sg_class[3]}")
                    print(f"Status: {sg_class[4]}\n")

# Ta bort info från DB

def delete_info():
    print("Ta bort info: ")
    print("Vill du ta bort från SGC eller System Lords?")
    print("1. SGC\n2. System Lords")
    user_input = input("> ")
    user_input = user_input.strip()
    
    if user_input == "1":
        print("Skriv in det ID du vill ta bort: ")
        delete_id = input("> ")
        res = requests.delete(url(f"/delete_sgc/{delete_id}"))
        print(res.json())

    elif user_input == "2":
        print("Skriv in det ID du vill ta bort: ")
        delete_id = input("> ")
        res = requests.delete(url(f"/delete_sl/{delete_id}"))
        print(res.json())

    else:
        print("Du måste välja mellan 1 & 2 ")
        delete_info()

# Uppdatera redan befintlig information

def update_info():
    print("Vilken tabell vill du uppdatera")
    print("1. Stargate Command")
    print("2. System Lords\n")
    val = input("> ")
    if val == "1":
        print("Uppdatera Stargate Command\n")
        choice = input("Id för uppdatering: ")
        if not str.isdigit(choice):
            print("Du måste välja 1 eller 2.")
            return
        
        print("Uppdatera följande: (Lämnas tom om ingen ändring vill göras.)")
        first_name = input("Förnamn: ")
        last_name = input("Efternamn: ")
        rank = input("Rank: ")
        occupation = input("Sysselsättning: ")
        sgc_list = get_updatesgc() # Jag lyckades inte lösa detta utan denna nya funktionen jag skapade
        sgc = None
        for sgdb in sgc_list:
            if sgdb.id == int(choice): 
                sgc=sgdb
                break
        if sgc == None:
            print("")
            print("ID finns inte, försök igen\n")
            update_info()                
        if not first_name:
            first_name = sgc.first_name
        if not last_name:
            last_name = sgc.last_name
        if not rank:
            rank = sgc.rank
        if not occupation:
            occupation = sgc.occupation
        
        new_sgc = SG(first_name = first_name, last_name = last_name, rank = rank, occupation = occupation)
        res = requests.put(url(f"/update_sgc/{choice}"), json=new_sgc.dict())
        print(res.json)
        return

    if val == "2":
        print("Uppdatera System Lords\n ")
        choice = input("Id för uppdatering: ")
        if not str.isdigit(choice):
            print("Du måste välja 1 eller 2.")
            return
            
        print("Uppdatera följande: (Lämnas tom om ingen ändring vill göras.)")
        name = input("Namn: ")
        appearance = input("Utseende: ")
        mythos = input("Mythos: ")
        status = input("Status: ")
        sl_list = get_updatesl()
        sl = None
        for sldb in sl_list:
            if sldb.id == int(choice):
                sl=sldb
                break
        if sl == None:
            print("")
            print("ID finns inte, försök igen\n")
            update_info()
        if not name:
            name = sl.name
        if not appearance:
            appearance = sl.appearance
        if not mythos:
            mythos = sl.mythos
        if not status:
            status = sl.status
        
        new_sl = SL(name = name, appearance = appearance, mythos = mythos, status = status)
        res = requests.put(url(f"/update_sl/{choice}"), json=new_sl.dict())
        print(res.json)
        return
    
    else: 
        print("Du måste välja mellan 1 och 2.")
        update_info()

def main():
    print_menu()
    menyval = input("Menyval: ")
    menyval = menyval.strip()
    if not str.isdigit(menyval):
        print("Du måste skriva en siffra mellan 1 och 5 \nexit för att avsluta.")
        return
    
    match int(menyval):
        case 1:
            add_post()
        case 2:
            print("Hämta info från: \n")
            print("1. Stargate Command ")
            print("2. System Lords ")
            print("3. Båda \n")
            print("")
            get_input = input("> ")
            get_info(get_input)
        case 3:
            delete_info()
        case 4:
            update_info()
        case 5:
            exit()
        case _:
            print("Välj en siffra")
    pass

while __name__ == "__main__":
    print()
    print(__name__)
    main()