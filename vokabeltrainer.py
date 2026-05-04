import json, random

try:
    with open("vokabeln.json", "r") as datei:
        vokabeln = json.load(datei)
except FileNotFoundError:
    vokabeln = {}

newvocab = input("Willst du neue Vokabeln hinzufügen? (Ja = 1), (Nein = 2) ").strip()

if newvocab == "1":
    while True:
        key_1 = input("Nenne das Englische Wort. ").strip()
        value_1 = input("Nenne nun das Deutsche Wort. ").strip()
        vokabeln[key_1.lower()] = value_1
        Weiter = input("Weiter? (Ja = 1), (Nein = 2) ").strip()
        if Weiter == "2":
            break
else:
    print("")

del_vocab = input("Willst du eine Vokabel löschen? (Ja = 1), (Nein = 2) ").strip()

if del_vocab == "1":
    while True:
        del_1 = input("Nenne die Englische Vokabel die du löschen möchtest. ").strip().lower()
        del(vokabeln[del_1])
        Weiter = input("Weiter? (Ja = 1), (Nein = 2) ").strip()
        if Weiter == "2":
            break
else:
    print("Ok, hier kommen die Vokabeln.")

vokabeln_liste = list(vokabeln.items())
random.shuffle(vokabeln_liste)

Punkte = 0

while True:
    for englisch, deutsch in vokabeln_liste:
        Vokabel = input(f"Was bedeutet {englisch} auf Deutsch? ").strip()
        if Vokabel == deutsch:
            print("Richtig! Nächste Vokabel. ")
            Punkte += 1
        else:
            print(f"Falsch. Die richtige Antwort war: {deutsch}. Nächste Vokabel. ")

    print("")
    print(f"Du hast {Punkte} von {len(vokabeln_liste)} Vokabeln richtig beantwortet.")
    Punkte = 0
    Weiter = input("Weiter? (Ja = 1), (Nein = 2) ").strip()
    if Weiter == "2":
        break


with open("vokabeln.json", "w") as datei:
    json.dump(vokabeln, datei)
    