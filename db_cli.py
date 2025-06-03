import json
import os

class JSONDatabase:
    def __init__(self, filename='database.json'):
        self.filename = filename
        self.data = []
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    self.data = []
        else:
            self.data = []

    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)

    def add(self, record: dict):
        self.data.append(record)
        self.save()
        print("✅ Record aggiunto.")

    def list(self):
        if not self.data:
            print("⚠️  Nessun record presente.")
            return
        for idx, record in enumerate(self.data, start=1):
            print(f"{idx}: {record}")

    def search(self, key, value):
        results = [record for record in self.data if record.get(key) == value]
        if not results:
            print("🔍 Nessun record trovato.")
            return
        for idx, record in enumerate(results, start=1):
            print(f"{idx}: {record}")

    def update(self, index, key, value):
        try:
            self.data[index][key] = value
            self.save()
            print("🔁 Record aggiornato.")
        except IndexError:
            print("❌ Indice non valido.")

    def delete(self, index):
        try:
            del self.data[index]
            self.save()
            print("🗑️ Record eliminato.")
        except IndexError:
            print("❌ Indice non valido.")

def start_cli():
    db = JSONDatabase()
    print("📁 MiniDatabase JSON CLI avviato. Digita 'help' per i comandi.")

    while True:
        command = input("\n> ").strip()

        if command == "help":
            print("""
Comandi disponibili:
  add           → Aggiungi un record (es: add {"nome": "Flavio", "età": 25})
  list          → Mostra tutti i record
  search k v    → Cerca per chiave e valore (es: search nome Flavio)
  update i k v  → Aggiorna record i alla chiave k con valore v (es: update 1 età 26)
  delete i      → Elimina il record numero i (es: delete 1)
  exit          → Esci dal programma
""")
        elif command.startswith("add"):
            try:
                raw_json = command[4:].strip()
                record = json.loads(raw_json)
                if isinstance(record, dict):
                    db.add(record)
                else:
                    print("❗ Il record deve essere un oggetto JSON valido.")
            except json.JSONDecodeError:
                print("❗ Formato JSON non valido.")
        elif command == "list":
            db.list()
        elif command.startswith("search"):
            parts = command.split(maxsplit=2)
            if len(parts) < 3:
                print("❗ Sintassi: search <chiave> <valore>")
            else:
                _, key, value = parts
                db.search(key, value)
        elif command.startswith("update"):
            parts = command.split(maxsplit=3)
            if len(parts) < 4:
                print("❗ Sintassi: update <indice> <chiave> <valore>")
            else:
                try:
                    index = int(parts[1]) - 1
                    db.update(index, parts[2], parts[3])
                except ValueError:
                    print("❗ L'indice deve essere un numero.")
        elif command.startswith("delete"):
            parts = command.split()
            if len(parts) < 2:
                print("❗ Sintassi: delete <indice>")
            else:
                try:
                    index = int(parts[1]) - 1
                    db.delete(index)
                except ValueError:
                    print("❗ L'indice deve essere un numero.")
        elif command == "exit":
            print("👋 Uscita...")
            break
        else:
            print("❓ Comando sconosciuto. Digita 'help' per vedere i comandi.")

if __name__ == "__main__":
    start_cli()
