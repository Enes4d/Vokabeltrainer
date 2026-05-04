import json, random

def laden():
    try:
        with open("vokabeln.json", "r") as datei:
            return json.load(datei)
    except FileNotFoundError:
        return {}
    
def speichern(vokabeln):
    with open("vokabeln.json", "w") as datei:
        json.dump(vokabeln, datei)

def weiter():
    Weiter = input("Willst du weiter machen? (Ja = 1), (Nein = 2) ").strip()
    return Weiter == "2"

def menu():
    print("\n=== Vokabeltrainer ===")
    print("1. Vokabeln lernen")
    print("2. Vokabeln hinzufügen")
    print("3. Vokabeln löschen")
    print("4. Beenden")

vokabeln = laden()

def vokabelhinzufügen(vokabeln):
    while True:
        key_1 = input("Schreibe die Englische Vokabel auf: ").strip()
        value_1 = input("Schreibe die Deutsche Vokabel auf: ").strip()
        vokabeln[key_1.lower()] = value_1
        if weiter():
            break

def vokabellöschen(vokabeln):
    while True:
        del_1 = input("Schreibe die Englische Vokabel die du löschen möchtest. ").strip()
        del(vokabeln[del_1])
        if weiter():
            break

def vokabelnlernen(vokabeln):
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
                print("Nächste Vokabel. ")
                print("")
        print(f"Du hast {Punkte} von {len(vokabeln_liste)} Vokabeln richtig beantwortet.")
        print("")
        Punkte = 0
        if weiter():
            break

while True:
    menu()
    auswahl = input("\n Deine Wahl: ").strip()
    if auswahl == "1":
        vokabelnlernen(vokabeln)
    elif auswahl == "2":
        vokabelhinzufügen(vokabeln)
    elif auswahl == "3":
        vokabellöschen(vokabeln)
    elif auswahl == "4":
        speichern(vokabeln)
        print("Tschüss")
        break
    else:
        print("")
        print("Dein Input ist ungültig bitte Tippe 1, 2, 3 oder 4. ")