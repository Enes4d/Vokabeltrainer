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

def vokabeln_lernen():
    print("Vokabeln lernen gedrückt.")

frame_hinzufügen = tk.Frame(fenster)

def zeige_hinzufügen():
    frame_menu.pack_forget()
    frame_hinzufügen.pack()
def zeige_menu():
    frame_hinzufügen.pack_forget()
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

tk.Label(frame_menu, text="Vokabeltrainer", font=("Arial")).pack(pady=5)
tk.Button(frame_menu, text="Vokabeln lernen", width=20, command=vokabeln_lernen).pack(pady=5)
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
fenster.mainloop()
