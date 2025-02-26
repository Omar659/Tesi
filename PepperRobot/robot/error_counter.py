import tkinter as tk
from tkinter import messagebox
import json
import os

# Funzione per aggiornare la visualizzazione del counter
def update_counter_display(i):
    counter_vars[i].set(str(counter_values[i]))

# Callback per il bottone "Fine"
def finish():
    username = username_entry.get().strip()
    if not username:
        messagebox.showerror("Errore", "Inserire un username")
        return

    # Creazione della cartella data se non esiste
    data_folder = "./"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    file_path = os.path.join(data_folder, "data.json")
    # Carica il file JSON se esiste, altrimenti usa un dizionario vuoto
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    else:
        data = {}

    # Se l'utente non e presente nel file JSON, mostra un alert
    if username not in data:
        messagebox.showerror("Errore", "Utente non presente nel file JSON")
        return

    # Aggiungi/aggiorna le coppie chiave (label) - valore (counter) per quell'utente
    for i, label_text in enumerate(counter_labels):
        data[username.lower()][label_text] = counter_values[i]

    # Salva il JSON aggiornato
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    messagebox.showinfo("Successo", "Dati salvati correttamente")

# Creazione della finestra principale
root = tk.Tk()
root.title("Interfaccia Counter")

# Campo per l'inserimento dell'username
username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky="we")

# Inizializzazione dei counter e relative label
counter_labels = ["Missing 2xPinch zoom", "Missing Pinch move", "Missing Rotation", "Missing Ask Map functionality", "Number of try for asking a position", "Number of try to enter VR"]
counter_values = [0]*len(counter_labels)
counter_vars = [tk.StringVar() for _ in range(len(counter_labels))]
for i in range(len(counter_labels)):
    counter_vars[i].set(str(counter_values[i]))

# Creazione dei quattro blocchi per ogni counter
for i in range(len(counter_labels)):
    # Utilizziamo un frame per organizzare ogni blocco
    frame = tk.Frame(root, relief=tk.RAISED, borderwidth=1)
    frame.grid(row=1, column=i, padx=5, pady=5)

    # Label in alto con il nome del counter
    label_top = tk.Label(frame, text=counter_labels[i])
    label_top.pack(pady=(5, 0))

    # Label per il valore del counter
    value_label = tk.Label(frame, textvariable=counter_vars[i], font=("Helvetica", 16))
    value_label.pack(pady=(0, 5))

    # Frame per contenere i bottoni di incremento e decremento
    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=(0, 5))

    # Funzione per creare il comando di decremento per il counter i-esimo
    def make_decrease(i=i):
        def decrease():
            counter_values[i] -= 1
            update_counter_display(i)
        return decrease

    # Bottone per decrementare
    btn_decrease = tk.Button(btn_frame, text="-", width=4, command=make_decrease(i))
    btn_decrease.pack(side=tk.LEFT, padx=2)

    # Funzione per creare il comando di incremento per il counter i-esimo
    def make_increase(i=i):
        def increase():
            counter_values[i] += 1
            update_counter_display(i)
        return increase

    # Bottone per incrementare
    btn_increase = tk.Button(btn_frame, text="+", width=4, command=make_increase(i))
    btn_increase.pack(side=tk.LEFT, padx=2)

# Bottone "Fine" posizionato in basso a destra
btn_finish = tk.Button(root, text="Fine", command=finish)
btn_finish.grid(row=2, column=3, padx=5, pady=10, sticky="e")

root.mainloop()
