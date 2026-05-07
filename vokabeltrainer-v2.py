import json, random

def sprachenladen():
    try:
        with open("sprachen.json", "r") as datei:
            return json.load(datei)
    except FileNotFoundError:
        return []

def sprachenspeichern(sprachen):
    with open("sprachen.json", 'w') as datei:
        json.dump(sprachen, datei)

def laden(dateiname):
    try:
        with open(dateiname, "r") as datei:
            return json.load(datei)
    except FileNotFoundError:
        return {}
    
def speichern(vokabeln, dateiname):
    with open(dateiname, "w") as datei:
        json.dump(vokabeln, datei)

def merkliste_laden():
    try:
        with open("merkliste.json", "r") as datei:
            return json.load(datei)
    except FileNotFoundError:
        return {}
    
def merkliste_speichern(merkliste):
        with open("merkliste.json", "w") as datei:
            json.dump(merkliste, datei)

merkliste = merkliste_laden()

def weiter():
    Weiter = input("Willst du weiter machen? (Ja = 1), (Nein = 2) ").strip()
    return Weiter == "2"

def menu():
    print("\n=== Vokabeltrainer ===")
    print("0. Sprache hinzufügen")
    print("1. Vokabeln lernen")
    print("2. Vokabeln hinzufügen")
    print("3. Vokabeln löschen")
    print("4. Merkliste abfragen")
    print("5. Beenden")
    print("6. Einstellungen")

def vokabelhinzufügen(vokabeln):
    while True:
        key_1 = input(f"Schreibe die Englische Vokabel auf: ").strip()
        value_1 = input("Schreibe die Deutsche Vokabel auf: ").strip()
        vokabeln[key_1.lower()] = value_1
        if weiter():
            break

def vokabelnanzeigen(vokabeln):
    vokabeln_liste = list(vokabeln.items())
    for index, (englisch, deutsch) in enumerate(vokabeln_liste, 1):
        print(f"{index} {englisch} = {deutsch}")
        print("")

def vokabellöschen(vokabeln):
    while True:
        vokabeln_liste = list(vokabeln.items())
        vokabelnanzeigen(vokabeln)
        del_1 = input("Schreibe die Nummer der Vokabel, die du löschen möchtest. ").strip()
        try:
            nummer = int(del_1) - 1
            englisch, deutsch = vokabeln_liste[nummer]
            del(vokabeln[englisch])
            print(f"{englisch} wurde gelöscht. ")
            if weiter():
                break
        except ValueError:
            print("Bitte eine Nummer eingeben!")
        except IndexError:
            print("Diese Nummer gibt es nicht! ")

def vokabelnlernen(vokabeln, merkliste):
    Punkte = 0
    vokabeln_liste = list(vokabeln.items())
    random.shuffle(vokabeln_liste)
    while True:
        for englisch, deutsch in vokabeln_liste:
            voc_1 = input(f"Was heißt {englisch} auf Deutsch? ")
            if voc_1 == deutsch:
                print("Richtig! Nächste Vokabel.")
                print("")
                Punkte += 1
            else:
                print(f"Falsch. Die richtige Antwort war {deutsch}. ")
                if einstellungen_dict["merkliste_aktiv"]:
                    merkliste[englisch] = deutsch
                    print("Diese Vokabel wurde der Merkliste hinzugefügt. Nächste Vokabel. ")
                print("")
                
        print(f"Du hast {Punkte} von {len(vokabeln_liste)} Vokabeln richtig beantwortet.")
        print("")
        Punkte = 0
        if weiter():
            break

def merkliste_abfragen(merkliste):
    Punkte = 0 
    while True:
        if not merkliste:
            print("Die Merkliste ist leer! ")
            break
        merkliste_liste = list(merkliste.items())
        random.shuffle(merkliste_liste)
        for englisch, deutsch in merkliste_liste:
            voc_1 = input(f"Was heißt {englisch} auf Deutsch? ")
            if voc_1 == deutsch:
                del(merkliste[englisch])
                print("Richtig! Diese Vokabel wird aus der Merkliste entfernt. ")
                print("Nächste Vokabel. ")
                print("")
                Punkte += 1
            else:
                print(f"Falsch. Die richtige Antwort war {deutsch}. ")
                print("Nächste Vokabel. ")
                print("")
        print(f"Du hast {Punkte} von {len(merkliste_liste)} Vokabeln richtig beantwortet.")
        print("")
        Punkte = 0
        if weiter():
            break

def einstellungen(einstellungen_dict):
    while True:
        print("\n=== Einstellungen ===")
        print("1. Merkliste an/aus schalten. ")
        print("2. Zurück ")
        print("")
        auswahl = input("Bitte eine Nummer eingeben! ")
        if auswahl == "2":
            break
        elif auswahl == "1":
            einstellungen_dict["merkliste_aktiv"] = not einstellungen_dict["merkliste_aktiv"]
            Status = "AN" if einstellungen_dict["merkliste_aktiv"] else "Aus"
            print(f"Merkliste ist jetzt {Status}. ")
            einstellung_speichern(einstellungen_dict)

def einstellung_laden():
    try:
        with open("einstellungen.json", "r") as datei:
            return json.load(datei)
    except FileNotFoundError:
        return {"merkliste_aktiv": True}
    
def einstellung_speichern(einstellungen):
    with open("einstellungen.json", "w") as datei:
        json.dump(einstellungen, datei)

einstellungen_dict = einstellung_laden()

sprachen = sprachenladen()

if sprachen:
    neue_sprache = sprachen[0]
    dateiname = f"{neue_sprache}.json"
    vokabeln = laden(dateiname)
else:
    dateiname = None
    vokabeln = {}

while True:
    menu()
    auswahl = input("\n Deine Wahl: ").strip()
    if auswahl == "0":
        print("")
        if not sprachen:
            print("Keine Sprachen vorhanden. Neue Sprache hinzufügen. ")
            neue_sprache = input("Sprache: ").strip().lower()
            sprachen.append(neue_sprache)
            sprachenspeichern(sprachen)
        auswahl_2 = input("Sprache wählen(1), Sprache hinzufügen(2): ")
        if auswahl_2 == "1":
            print("\nVerfügbare Sprachen: ")
            for index, sprache in enumerate(sprachen, 1):
                print(f"{index} {sprache}")
                print("")
            auswahl = input("Wähle eine der Sprachen: ").strip()
            neue_sprache = sprachen[int(auswahl)-1]
        elif auswahl_2 == "2":
            neue_sprache = input("Sprache: ").strip().lower()
            sprachen.append(neue_sprache)
            sprachenspeichern(sprachen)
        dateiname = f"{neue_sprache}.json"
        vokabeln = laden(dateiname)
    elif auswahl == "1":
        print("")
        vokabelnlernen(vokabeln, merkliste)
    elif auswahl == "2":
        print("")
        vokabelhinzufügen(vokabeln)
    elif auswahl == "3":
        print("")
        vokabellöschen(vokabeln)
    elif auswahl == "4":
        print("")
        merkliste_abfragen(merkliste)
    elif auswahl == "5":
        print("")
        speichern(vokabeln, dateiname)
        merkliste_speichern(merkliste)
        print("Tschüss")
        break
    elif auswahl == "6":
        einstellungen(einstellungen_dict)
    else:
        print("")
        print("Dein Input ist ungültig bitte Tippe 1, 2, 3, 4 oder 5. ")