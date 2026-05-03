import json

try:
    with open("vokabeln.json", "r") as datei:
        vokabeln = json.load(datei)
except FileNotFoundError:
    vokabeln = {}

newvocab = input("Willst du neue Vokabeln hinzufügen? (Ja = 1), (Nein = 2) ").strip()

if newvocab == "1":
    while True:
        key_1 = input("Nenne das Englische Wort. ")
        value_1 = input("Nenne nun das Deutsche Wort. ")
        vokabeln[key_1] = value_1
        Weiter = input("Weiter? (Ja = 1), (Nein = 2) ").strip()
        if Weiter == "2":
            break
else:
    print("Ok, hier kommen die Vokabeln.")
    print("")

for englisch, deutsch in vokabeln.items():
    Vokabel = input(f"Was bedeutet {englisch} auf Deutsch? ").strip()
    if Vokabel == deutsch:
        print("Richtig! Nächste Vokabel. ")
    else:
        print(f"Falsch. Die richtige Antwort war: {deutsch}. Nächste Vokabel. ")

with open("vokabeln.json", "w") as datei:
    json.dump(vokabeln, datei)
