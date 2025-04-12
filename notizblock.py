import os

NOTES_FILE = "notes.txt"

def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

def save_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        for note in notes:
            f.write(note + "\n")

def show_notes(notes):
    print("\n--- Notizen ---")
    if not notes:
        print("Keine Notizen vorhanden.")
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note}")
    print("----------------\n")

def add_note(notes):
    new_note = input("Neue Notiz eingeben: ")
    notes.append(new_note)
    save_notes(notes)
    print("✅ Notiz gespeichert.")

def delete_note(notes):
    show_notes(notes)
    try:
        idx = int(input("Nummer der zu löschenden Notiz: "))
        if 1 <= idx <= len(notes):
            deleted = notes.pop(idx - 1)
            save_notes(notes)
            print(f"❌ Notiz gelöscht: {deleted}")
        else:
            print("Ungültige Nummer.")
    except ValueError:
        print("Bitte eine gültige Zahl eingeben.")

def main():
    notes = load_notes()
    while True:
        print("1. Notizen anzeigen")
        print("2. Neue Notiz hinzufügen")
        print("3. Notiz löschen")
        print("4. Beenden")
        choice = input("Auswahl: ")
        if choice == "1":
            show_notes(notes)
        elif choice == "2":
            add_note(notes)
        elif choice == "3":
            delete_note(notes)
        elif choice == "4":
            break
        else:
            print("Ungültige Eingabe.")

if __name__ == "__main__":
    main()
