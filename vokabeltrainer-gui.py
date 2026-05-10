import json, random, tkinter as tk
import os
ORDNER = os.path.dirname(os.path.abspath(__file__))

def laden(dateiname):
    pfad = os.path.join(ORDNER, dateiname)
    try:
        with open(pfad, "r") as datei:
            return json.load(datei)
    except FileNotFoundError:
        return {}

def speichern():
    pfad = os.path.join(ORDNER, "englisch.json")
    with open(pfad, "w") as datei:
        json.dump(vokabeln, datei)


fenster = tk.Tk()
fenster.title("Vocabluray trainer")
fenster.geometry("400x600")

frame_menu = tk.Frame(fenster)
frame_menu.pack()

frame_menu.pack_forget()
frame_menu.pack()

frame_hinzufügen = tk.Frame(fenster)
frame_lernen = tk.Frame(fenster)

def zeige_hinzufügen():
    frame_menu.pack_forget()
    frame_hinzufügen.pack()
def zeige_menu():
    frame_hinzufügen.pack_forget()
    frame_lernen.pack_forget()
    frame_menu.pack()
    
vokabeln = laden("englisch.json")

def vokabeln_speichern():
    key = eingabe_vokabel.get().strip().lower()
    value = eingabe_übersetzung.get().strip().lower()
    if key and value:
        vokabeln[key] = value
        speichern()
        eingabe_vokabel.delete(0, tk.END)
        eingabe_übersetzung.delete(0, tk.END)
        print(f"{key} wurde hinzugefügt.")

def zeige_lernen():
    global vokabeln_liste
    frame_menu.pack_forget()
    vokabeln_liste = list(vokabeln.items())
    random.shuffle(vokabeln_liste)
    aktuelle_index[0] = 0
    nächste_vokabel()
    frame_lernen.pack()

def nächste_vokabel():
    if aktuelle_index[0] < len(vokabeln_liste):
        englisch, deutsch = vokabeln_liste[aktuelle_index[0]]
        vokabel_lernen.config(text=englisch)
        label_feedback.config(text="")
        eingabe_antwort.delete(0, tk.END)
    else:
        vokabel_lernen.config(text="Fertig!")
        label_feedback.config(text="")

def prüfen():
    if aktuelle_index[0] < len(vokabeln_liste):
        englisch, deutsch = vokabeln_liste[aktuelle_index[0]]
        antwort = eingabe_antwort.get().strip().lower()
        if antwort == deutsch.lower():
            label_feedback.config(text="Richtig!", fg="green")
        else:
            label_feedback.config(text=f"Falsch!, Richtig: {deutsch}", fg="red")
        aktuelle_index[0] += 1

tk.Label(frame_menu, text="Vokabeltrainer", font=("Arial")).pack(pady=5)
tk.Button(frame_menu, text="Vokabeln lernen", width=20, command=zeige_lernen).pack(pady=5)
tk.Button(frame_menu, text="Vokabeln hinzufügen", width=20, command=zeige_hinzufügen).pack(pady=5)
tk.Button(frame_menu, text="Vokabeln löschen", width=20).pack(pady=5)
tk.Button(frame_menu, text="Merkliste abfragen", width=20).pack(pady=5)
tk.Button(frame_menu, text="Einstellungen", width=20).pack(pady=5)
tk.Button(frame_menu, text="Beenden", width=20).pack(pady=5)

tk.Label(frame_hinzufügen, text="Vokabel hinzufügen", font=("Arial", 14)).pack(pady=10)
tk.Label(frame_hinzufügen, text="Vokabel:").pack()
eingabe_vokabel = tk.Entry(frame_hinzufügen, width=30)
eingabe_vokabel.pack(pady=5)
tk.Label(frame_hinzufügen, text="Übersetzung:").pack()
eingabe_übersetzung = tk.Entry(frame_hinzufügen, width=30)
eingabe_übersetzung.pack(pady=5)
tk.Button(frame_hinzufügen, text="Hinzufügen", width=20, command=vokabeln_speichern).pack(pady=5)
tk.Button(frame_hinzufügen, text="Zurück", width=20, command=zeige_menu).pack(pady=5)

vokabel_lernen = tk.Label(frame_lernen,text="", font=("Arial", 18))
vokabel_lernen.pack(pady=20)

eingabe_antwort = tk.Entry(frame_lernen, width=30)
eingabe_antwort.pack(pady=5)

label_feedback = tk.Label(frame_lernen, text="", font=("Arial", 12))
label_feedback.pack(pady=10)

vokabeln_liste = []
aktuelle_index = [0]

tk.Button(frame_lernen, text="Prüfen", width=20, command=prüfen).pack(pady=5)
tk.Button(frame_lernen, text="Nächste", width=20, command=nächste_vokabel).pack(pady=5)
tk.Button(frame_lernen, text="Zurück", width=20, command=zeige_menu).pack(pady=5)

fenster.mainloop()
