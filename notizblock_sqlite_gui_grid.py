import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import datetime

# Setup database
conn = sqlite3.connect("notes.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT,
    created_at TEXT
)
""")
conn.commit()

def load_notes():
    c.execute("SELECT id, title FROM notes ORDER BY created_at DESC")
    return c.fetchall()

def get_note_content(note_id):
    c.execute("SELECT content FROM notes WHERE id=?", (note_id,))
    result = c.fetchone()
    return result[0] if result else ""

def add_note():
    title = simpledialog.askstring("Neue Notiz", "Titel der Notiz:")
    if title:
        now = datetime.datetime.now().isoformat()
        c.execute("INSERT INTO notes (title, content, created_at) VALUES (?, ?, ?)",
                  (title, "", now))
        conn.commit()
        refresh_list()
    else:
        messagebox.showwarning("Fehler", "Titel darf nicht leer sein!")

def delete_note():
    selection = note_list.curselection()
    if not selection:
        messagebox.showwarning("Hinweis", "Bitte eine Notiz auswählen.")
        return
    note_id = note_ids[selection[0]]
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    refresh_list()
    text_area.delete("1.0", tk.END)

def save_note():
    selection = note_list.curselection()
    if not selection:
        messagebox.showwarning("Hinweis", "Bitte eine Notiz auswählen.")
        return
    note_id = note_ids[selection[0]]
    content = text_area.get("1.0", tk.END).strip()
    c.execute("UPDATE notes SET content=? WHERE id=?", (content, note_id))
    conn.commit()
    messagebox.showinfo("Gespeichert", "✅ Notiz wurde gespeichert!")

def on_note_select(event):
    selection = note_list.curselection()
    if not selection:
        return
    note_id = note_ids[selection[0]]
    content = get_note_content(note_id)
    text_area.delete("1.0", tk.END)
    text_area.insert("1.0", content)

def refresh_list():
    global note_ids
    note_list.delete(0, tk.END)
    notes = load_notes()
    note_ids = []
    for note in notes:
        note_ids.append(note[0])
        note_list.insert(tk.END, note[1])

# GUI setup with grid layout
root = tk.Tk()
root.title("Notizblock mit SQLite")
root.geometry("800x500")

# Configure grid weights
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Left panel
left_frame = tk.Frame(root)
left_frame.grid(row=0, column=0, sticky="ns")

note_list = tk.Listbox(left_frame, width=30, font=("Arial", 11))
note_list.pack(side="top", fill="y", expand=True, padx=5, pady=5)
note_list.bind("<<ListboxSelect>>", on_note_select)

btn_add = tk.Button(left_frame, text="➕ Neue Notiz", command=add_note)
btn_add.pack(fill="x", padx=5, pady=2)
btn_delete = tk.Button(left_frame, text="🗑️ Löschen", command=delete_note)
btn_delete.pack(fill="x", padx=5, pady=2)

# Right panel
right_frame = tk.Frame(root)
right_frame.grid(row=0, column=1, sticky="nsew")
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

text_area = tk.Text(right_frame, wrap="word", font=("Arial", 12))
text_area.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

btn_save = tk.Button(right_frame, text="💾 Speichern", command=save_note)
btn_save.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

refresh_list()
root.mainloop()
