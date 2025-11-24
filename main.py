from database_helper import DBHelper
import os

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

    # Tabellen erstellen
    db.initialize()

    # Alte Daten löschen
    db.clear()

    # Neuen Datensatz hinzufügen
    new_id = db.add_row(example_data)

    # Datensatz wieder entfernen
    if new_id:
        db.remove_row(new_id)


if __name__ == "__main__":
    main()