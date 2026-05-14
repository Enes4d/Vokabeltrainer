import json, random, tkinter as tk
import os
from tkinter import simpledialog
ORDNER = os.path.dirname(os.path.abspath(__file__))

def laden(dateiname):
    pfad = os.path.join(ORDNER, dateiname)
    try:
        with open(pfad, "r") as datei:
            return json.load(datei)
    except FileNotFoundError:
        return {}

def speichern(daten, dateiname):
    pfad = os.path.join(ORDNER, dateiname)
    with open(pfad, "w") as datei:
        json.dump(daten, datei)

merkliste = laden("merkliste.json")
vokabeln = laden("englisch.json")

fenster = tk.Tk()
fenster.title("Vocabluray trainer")
fenster.geometry("400x600")

frame_menu = tk.Frame(fenster)
frame_menu.pack()

frame_menu.pack_forget()
frame_menu.pack()

frame_hinzufügen = tk.Frame(fenster)
frame_lernen = tk.Frame(fenster)
frame_löschen = tk.Frame(fenster)
frame_merkliste = tk.Frame(fenster)
frame_einstellungen = tk.Frame(fenster)

def zeige_hinzufügen():
    frame_menu.pack_forget()
    frame_hinzufügen.pack()
def zeige_menu():
    frame_löschen.pack_forget()
    frame_hinzufügen.pack_forget()
    frame_lernen.pack_forget()
    frame_merkliste.pack_forget()
    frame_einstellungen.pack_forget()
    frame_menu.pack()
    
def vokabeln_speichern():
    key = eingabe_vokabel.get().strip()
    value = eingabe_übersetzung.get().strip()
    if key and value:
        vokabeln[key] = value
        speichern(vokabeln, "englisch.json")
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
        eingabe_antwort.delete(0, tk.END)

def prüfen():
    if aktuelle_index[0] < len(vokabeln_liste):
        englisch, deutsch = vokabeln_liste[aktuelle_index[0]]
        antwort = eingabe_antwort.get().strip()
        if antwort == deutsch:
            label_feedback.config(text="Richtig!", fg="green")
        else:
            label_feedback.config(text=f"Falsch!, Richtig: {deutsch}", fg="red")
            if merkliste_an:
                merkliste[englisch] = deutsch
                speichern(merkliste, "merkliste.json")
        aktuelle_index[0] += 1
        fenster.after(1000, nächste_vokabel)
        btn_prüfen.config(state="disabled")
        fenster.after(1000, lambda: btn_prüfen.config(state="normal"))
        fenster.after(1000, nächste_vokabel)

def zeige_löschen():
    frame_menu.pack_forget()
    listbox.delete(0, tk.END)
    for englisch, deutsch in vokabeln.items():
        listbox.insert(tk.END, f"{englisch} = {deutsch}")
    frame_löschen.pack()
    
def vokabeln_löschen():
    auswahl = listbox.curselection()
    if auswahl:
        index = auswahl[0]
        eintrag = listbox.get(index)
        englisch = eintrag.split(" = ")[0]
        del vokabeln[englisch]
        speichern(vokabeln, "englisch.json")
        listbox.delete(index)

def zeige_merkliste():
    global merkliste_liste
    frame_menu.pack_forget()
    merkliste_liste = list(merkliste.items())
    random.shuffle(merkliste_liste)
    aktuelle_index[0] = 0
    if not merkliste:
        merklisten_lernen.config(text="Keine Vokabeln in der Merkliste.")
    else:
        nächste_merklisten_vokabel()
    frame_merkliste.pack()

def nächste_merklisten_vokabel():
    if aktuelle_index[0] < len(merkliste_liste):
        englisch, deutsch = merkliste_liste[aktuelle_index[0]]
        merklisten_lernen.config(text=englisch)
        merklisten_label_feedback.config(text="")
        merklisten_eingabe_antwort.delete(0, tk.END)
    else:
        merklisten_lernen.config(text="Fertig!")
        merklisten_label_feedback.config(text="")
        merklisten_eingabe_antwort.delete(0, tk.END)
        merklisten_btn_prüfen.config(state="disabled")

def merkliste_prüfen():
    if aktuelle_index[0] < len(merkliste_liste):
        englisch, deutsch = merkliste_liste[aktuelle_index[0]]
        antwort = merklisten_eingabe_antwort.get().strip()
        if antwort == deutsch:
            merklisten_label_feedback.config(text="Richtig!", fg="green")
            if not merkliste_beibehalten_an:
                del merkliste[englisch] 
            else: 
                merklisten_label_feedback.config(text="Richtig!", fg="green")
            speichern(merkliste, "merkliste.json")
        else:
            merklisten_label_feedback.config(text=f"Falsch!, Richtig: {deutsch}", fg="red")
        aktuelle_index[0] += 1
        fenster.after(1000, nächste_merklisten_vokabel)
        merklisten_btn_prüfen.config(state="disabled")
        fenster.after(1000, lambda: merklisten_btn_prüfen.config(state="normal"))
        fenster.after(1000, nächste_merklisten_vokabel)
    else:
        merklisten_lernen.config(text="Fertig")
        merklisten_label_feedback.config(text="")
        merklisten_eingabe_antwort.delete(0, tk.END)
        merklisten_btn_prüfen.config(state="disabled")

def zeige_einstellugen():
    frame_menu.pack_forget()
    frame_einstellungen.pack()

merkliste_an = True

def merkliste_ausschalten():
    global merkliste_an
    merkliste_an = not merkliste_an
    status = "An" if merkliste_an else "Aus"
    einstellungen_merkliste.config(text=f"Merkliste: {status}")

merkliste_beibehalten_an = True

def merkliste_beibehalten():
    global merkliste_beibehalten_an
    merkliste_beibehalten_an = not merkliste_beibehalten_an
    status = "An" if merkliste_beibehalten_an else "Aus"
    einstellungen_merkliste_behalten.config(text=f"Merkliste beibehalten: {status}")

def sprache_wechseln():
    global vokabeln
    sprache = simpledialog.askstring("Sprache wechseln", "Welche Sprache möchtest du lernen?")
    if sprache:
        sprache = sprache.strip().lower()
        vokabeln = laden(f"{sprache}.json")
        print(f"Sprache gewechselt zu {sprache}")

tk.Label(frame_menu, text="Vokabeltrainer", font=("Arial")).pack(pady=5)
tk.Button(frame_menu, text="Vokabeln lernen", width=20, command=zeige_lernen).pack(pady=5)
tk.Button(frame_menu, text="Vokabeln hinzufügen", width=20, command=zeige_hinzufügen).pack(pady=5)
tk.Button(frame_menu, text="Vokabeln löschen", width=20, command=zeige_löschen).pack(pady=5)
tk.Button(frame_menu, text="Merkliste abfragen", width=20, command=zeige_merkliste).pack(pady=5)
tk.Button(frame_menu, text="Einstellungen", width=20, command=zeige_einstellugen).pack(pady=5)
tk.Button(frame_menu, text="Beenden", width=20, command=fenster.destroy).pack(pady=5)

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

merklisten_lernen = tk.Label(frame_merkliste, text="", font=("Arial", 18))
merklisten_lernen.pack(pady=20)

merklisten_eingabe_antwort = tk.Entry(frame_merkliste, width=30)
merklisten_eingabe_antwort.pack(pady=5)

merklisten_label_feedback = tk.Label(frame_merkliste, text="", font=("Arial", 12))
merklisten_label_feedback.pack(pady=10)

einstellungen_label = tk.Label(frame_einstellungen, text="Einstellungen", font=("Arial", 12))
einstellungen_label.pack(pady=20)

einstellungen_merkliste = tk.Button(frame_einstellungen, text="Merkliste: An", width=20, command=merkliste_ausschalten)
einstellungen_merkliste.pack(pady=5)

einstellungen_merkliste_behalten = tk.Button(frame_einstellungen, text="Merkliste behalten", width=20, command=merkliste_beibehalten)
einstellungen_merkliste_behalten.pack(pady=5)

einstellungen_sprache_wechseln = tk.Button(frame_einstellungen, text="Sprache wechseln", width=20, command=sprache_wechseln)
einstellungen_sprache_wechseln.pack(pady=5)

einstellungen_beenden = tk.Button(frame_einstellungen, text="Zurück", width=20, command=zeige_menu)
einstellungen_beenden.pack(pady=5)

vokabeln_liste = []
merkliste_liste = []
aktuelle_index = [0]

btn_prüfen = tk.Button(frame_lernen, text="Prüfen", width=20, command=prüfen)
btn_prüfen.pack(pady=5)

tk.Button(frame_lernen, text="Zurück", width=20, command=zeige_menu).pack(pady=5)

tk.Label(frame_löschen, text="Vokabel löschen", font=("Arial", 14)).pack(pady=10)

listbox = tk.Listbox(frame_löschen, width=40, height=15)
listbox.pack(pady=5)

tk.Button(frame_löschen, text="löschen", width=20, command=vokabeln_löschen).pack(pady=5)
tk.Button(frame_löschen, text="Zurück", width=20, command=zeige_menu).pack(pady=5)

merklisten_btn_prüfen = tk.Button(frame_merkliste, text="Prüfen", width=20, command=merkliste_prüfen)
merklisten_btn_prüfen.pack(pady=5)
tk.Button(frame_merkliste, text="Zurück", width=20, command=zeige_menu).pack(pady=5)

fenster.mainloop()
