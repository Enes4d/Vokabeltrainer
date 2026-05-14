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

def sprachen_laden(dateiname):
    pfad = os.path.join(ORDNER, dateiname)
    try:
        with open(pfad, "r") as datei:
            return json.load(datei)
    except FileNotFoundError:
        return []

def einstellungen_laden():
    pfad = os.path.join(ORDNER, "einstellungen.json")
    try:
        with open(pfad, "r")as datei:
            return json.load(datei)
    except FileNotFoundError:
        return {"merkliste_an": True, "merkliste_beibehalten_an": True, "aktuelle_sprache": "englisch"}
    
def einstellungen_speichern():
    pfad = os.path.join(ORDNER, "einstellungen.json")
    with open(pfad, "w")as datei:
        json.dump({"merkliste_an": merkliste_an, "merkliste_beibehalten_an": merkliste_beibehalten_an, "aktuelle_sprache": aktuelle_sprache}, datei)

config = einstellungen_laden()
merkliste_an = config["merkliste_an"]
merkliste_beibehalten_an = config["merkliste_beibehalten_an"]
aktuelle_sprache = config["aktuelle_sprache"]     

sprachen = sprachen_laden("sprachen.json")
merkliste = laden(f"{aktuelle_sprache}_merkliste.json")
vokabeln = laden(f"{aktuelle_sprache}.json")

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
frame_sprachoptionen = tk.Frame(fenster)
frame_sprachen_löschen = tk.Frame(fenster)

def zeige_hinzufügen():
    frame_menu.pack_forget()
    frame_hinzufügen.pack()
def zeige_menu():
    frame_löschen.pack_forget()
    frame_hinzufügen.pack_forget()
    frame_lernen.pack_forget()
    frame_merkliste.pack_forget()
    frame_einstellungen.pack_forget()
    frame_sprachoptionen.pack_forget()
    frame_menu.pack()
    
def vokabeln_speichern():
    key = eingabe_vokabel.get().strip()
    value = eingabe_übersetzung.get().strip()
    if key and value:
        vokabeln[key] = value
        speichern(vokabeln, f"{aktuelle_sprache}.json")
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
                speichern(merkliste, f"{aktuelle_sprache}_merkliste.json")
        aktuelle_index[0] += 1
        fenster.after(1000, nächste_vokabel)
        btn_prüfen.config(state="disabled")
        fenster.after(1000, lambda: btn_prüfen.config(state="normal"))
        fenster.after(1000, nächste_vokabel)

def zeige_löschen():
    frame_menu.pack_forget()
    listbox_vokabeln.delete(0, tk.END)
    for englisch, deutsch in vokabeln.items():
        listbox_vokabeln.insert(tk.END, f"{englisch} = {deutsch}")
    frame_löschen.pack()
    
def vokabeln_löschen():
    auswahl = listbox_vokabeln.curselection()
    if auswahl:
        index = auswahl[0]
        eintrag = listbox_vokabeln.get(index)
        englisch = eintrag.split(" = ")[0]
        del vokabeln[englisch]
        speichern(vokabeln, f"{aktuelle_sprache}.json")
        listbox_vokabeln.delete(index)

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
    merklisten_btn_prüfen.config(state="normal")
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
            speichern(merkliste, f"{aktuelle_sprache}_merkliste.json")
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
    frame_sprachoptionen.pack_forget()
    frame_menu.pack_forget()
    status_merkliste = "An" if merkliste_an else "Aus"
    status_beibehalten = "An" if merkliste_beibehalten_an else "Aus"
    einstellungen_merkliste.config(text=f"Merkliste: {status_merkliste}")
    einstellungen_merkliste_behalten.config(text=f"Merkliste beibehalten: {status_beibehalten}")
    frame_einstellungen.pack()

def zeige_sprachoptionen():
    frame_sprachen_löschen.pack_forget()
    frame_einstellungen.pack_forget()
    frame_sprachoptionen.pack()

def merkliste_ausschalten():
    global merkliste_an
    merkliste_an = not merkliste_an
    status = "An" if merkliste_an else "Aus"
    einstellungen_merkliste.config(text=f"Merkliste: {status}")
    einstellungen_speichern()

def merkliste_beibehalten():
    global merkliste_beibehalten_an
    merkliste_beibehalten_an = not merkliste_beibehalten_an
    status = "An" if merkliste_beibehalten_an else "Aus"
    einstellungen_merkliste_behalten.config(text=f"Merkliste beibehalten: {status}")
    einstellungen_speichern()

def sprache_wechseln():
    global vokabeln, merkliste, aktuelle_sprache
    sprache = simpledialog.askstring("Sprache wechseln", "Welche Sprache möchtest du lernen?")
    if sprache:
        aktuelle_sprache = sprache.strip().lower()
        if aktuelle_sprache not in sprachen:
            print(f"{aktuelle_sprache} ist nicht als Sprache gespeichert.")
        else:
            vokabeln = laden(f"{aktuelle_sprache}.json")
            print(f"Sprache gewechselt zu {sprache}")
            merkliste = laden(f"{aktuelle_sprache}_merkliste.json")
            einstellungen_speichern()

def sprachen_hinzufügen():
    neue_sprache = simpledialog.askstring("Sprache hinzufügen", "Name der neuen Sprache?")
    if neue_sprache:
        neue_sprache = neue_sprache.strip().lower()
        print(f"Versuche {neue_sprache} hinzuzufügen")
        print(f"Sprachen liste: {sprachen}")
        if neue_sprache not in sprachen:
            sprachen.append(neue_sprache)
            speichern(sprachen, "sprachen.json")
            speichern({}, f"{neue_sprache}.json")
            print(f"{neue_sprache} wurde hinzugefügt.")
        else:
            print(f"{neue_sprache} existiert bereits")

def sprachen_zeige_löschen():
    frame_sprachoptionen.pack_forget()
    listbox_sprachen.delete(0, tk.END)
    for sprache in sprachen:
        listbox_sprachen.insert(tk.END, f"{sprache}")
    frame_sprachen_löschen.pack()

def sprachen_löchen():
    auswahl = listbox_sprachen.curselection()
    if auswahl:
        index = auswahl[0]
        eintrag = listbox_sprachen.get(index)
        sprachen.pop(index)
        speichern(sprachen, "sprachen.json")
        listbox_sprachen.delete(index)

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

einstellungen_sprachoptionen = tk.Button(frame_einstellungen, text="Sprach Einstellungen", width=20, command=zeige_sprachoptionen)
einstellungen_sprachoptionen.pack(pady=5)

einstellungen_beenden = tk.Button(frame_einstellungen, text="Zurück", width=20, command=zeige_menu)
einstellungen_beenden.pack(pady=5)

sprachoptionen_label = tk.Label(frame_sprachoptionen, text="Sprach Einstellungen", font=("Arial", 12))
sprachoptionen_label.pack(pady=20)

Sprache_wechseln_option = tk.Button(frame_sprachoptionen, text="Sprache wechseln", width=20, command=sprache_wechseln)
Sprache_wechseln_option.pack(pady=5)

Sprache_hinzufügen_option = tk.Button(frame_sprachoptionen, text="Sprache hinzufügen", width=20, command=sprachen_hinzufügen)
Sprache_hinzufügen_option.pack(pady=5)

sprache_löschen_option = tk.Button(frame_sprachoptionen, text="Sprache löschen", width=20, command=sprachen_zeige_löschen)
sprache_löschen_option.pack(pady=5)

sprachoptionen_beenden = tk.Button(frame_sprachoptionen, text="Zurück", width=20, command=zeige_einstellugen)
sprachoptionen_beenden.pack(pady=5)

vokabeln_liste = []
merkliste_liste = []
aktuelle_index = [0]

btn_prüfen = tk.Button(frame_lernen, text="Prüfen", width=20, command=prüfen)
btn_prüfen.pack(pady=5)

tk.Button(frame_lernen, text="Zurück", width=20, command=zeige_menu).pack(pady=5)

tk.Label(frame_löschen, text="Vokabel löschen", font=("Arial", 14)).pack(pady=10)

listbox_vokabeln = tk.Listbox(frame_löschen, width=40, height=15)
listbox_vokabeln.pack(pady=5)

tk.Button(frame_löschen, text="löschen", width=20, command=vokabeln_löschen).pack(pady=5)
tk.Button(frame_löschen, text="Zurück", width=20, command=zeige_menu).pack(pady=5)

merklisten_btn_prüfen = tk.Button(frame_merkliste, text="Prüfen", width=20, command=merkliste_prüfen)
merklisten_btn_prüfen.pack(pady=5)
tk.Button(frame_merkliste, text="Zurück", width=20, command=zeige_menu).pack(pady=5)

tk.Label(frame_sprachen_löschen, text="Sprachen löschen", font=("Arial", 14)).pack(pady=10)

listbox_sprachen = tk.Listbox(frame_sprachen_löschen, width=40, height=15)
listbox_sprachen.pack(pady=5)

tk.Button(frame_sprachen_löschen, text="löschen", width=20, command=sprachen_löchen).pack(pady=5)
tk.Button(frame_sprachen_löschen, text="Zurück", width=20, command=zeige_sprachoptionen).pack(pady=5)

fenster.mainloop()