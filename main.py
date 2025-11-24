from database_helper import DBHelper
import os
import json

# Die Verbindungs-URL hat das Format:
# dialect+driver://username:password@host:port/database

pw = os.getenv("PASSWD")
usr = os.getenv("USR")
db_url = f"postgresql+psycopg2://{usr}:{pw}@localhost:5433/blitzData"


# Ihr Beispieldatensatz (unverändert)
example_data = {
    "time": 1763940098040551000, "lat": 17.972565, "lon": -86.564342, "alt": 0, "pol": 0,
    "mds": 6870, "mcg": 154, "status": 0, "region": 5, "delay": 7.1, "lonc": 0, "latc": 0,
    "sig": [
        {"sta": 1955, "time": 4016475, "lat": 26.967615, "lon": -80.097351, "alt": -1, "status": 4},
        # ... weitere Signale
    ]
}


def main():
    db = DBHelper(db_url)
    db.initialize()
    db.clear()

    # Fügen wir zwei Einträge hinzu, um die Abfragen zu testen
    print("--- Füge Daten hinzu ---")
    id1 = db.add_row(example_data)
    # Kleiner Unterschied für den zweiten Datensatz
    example_data_2 = example_data.copy()
    example_data_2['lat'] = 18.0
    id2 = db.add_row(example_data_2)

    # --- Test der neuen Funktionen ---
    print("\n--- Hole einzelnen Eintrag ---")
    single_entry = db.get_row_by_id(id1)
    if single_entry:
        print(json.dumps(single_entry, indent=2))

    print("\n--- Hole alle Einträge ---")
    all_entries = db.get_all_rows()
    print(f"Insgesamt {len(all_entries)} Einträge gefunden.")
    # Nur den ersten Eintrag ausgeben, um die Ausgabe kurz zu halten
    if all_entries:
        print(json.dumps(all_entries[0], indent=2))


if __name__ == "__main__":
    main()