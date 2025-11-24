from database_helper import DBHelper
import os

pw = os.getenv("PASSWD")
usr = os.getenv("USR")
server = os.getenv("SERVER")  # domain or ip
port = os.getenv("PORT")
db_name = os.getenv("DB_NAME")
db_url = f"postgresql+psycopg2://{usr}:{pw}@{server}:{port}/{db_name}"


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


    print("\n--- Hole alle Einträge ---")
    len_entries = db.get_row_count()
    print(f"Insgesamt {len_entries} Einträge gefunden.")

    size_pretty = db.get_database_size(pretty=True)
    print(f"Die Datenbankgröße beträgt: {size_pretty}")

    """
    if all_entries:
        print(json.dumps(all_entries, indent=2))
    """



if __name__ == "__main__":
    main()