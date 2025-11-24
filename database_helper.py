from sqlalchemy import create_engine, Column, Integer, Float, BigInteger, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, joinedload

# Basisklasse für unsere ORM-Modelle
Base = declarative_base()


# Definition der 'measurements'-Tabelle als Python-Klasse
class Measurement(Base):
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    time = Column(BigInteger)
    lat = Column(Float)
    lon = Column(Float)
    alt = Column(Integer)
    pol = Column(Integer)
    mds = Column(Integer)
    mcg = Column(Integer)
    status = Column(Integer)
    region = Column(Integer)
    delay = Column(Float)
    lonc = Column(Float)
    latc = Column(Float)

    # Beziehung: Ein Measurement hat viele Signals.
    # 'cascade' sorgt dafür, dass Signals mit dem Measurement gelöscht werden.
    signals = relationship("Signal", back_populates="measurement", cascade="all, delete-orphan")


# Definition der 'signals'-Tabelle als Python-Klasse
class Signal(Base):
    __tablename__ = 'signals'

    id = Column(Integer, primary_key=True)
    sta = Column(Integer)
    time = Column(BigInteger)
    lat = Column(Float)
    lon = Column(Float)
    alt = Column(Integer)
    status = Column(Integer)

    # Fremdschlüssel zur Verknüpfung mit der 'measurements'-Tabelle
    measurement_id = Column(Integer, ForeignKey('measurements.id', ondelete="CASCADE"))
    # Rückbeziehung zum Measurement-Objekt
    measurement = relationship("Measurement", back_populates="signals")


class DBHelper:
    def __init__(self, db_url):
        """
        Initialisiert den DBHelper mit einer Datenbank-URL.
        z.B.: "postgresql+psycopg2://user:password@host:port/dbname"
        """
        self.engine = create_engine(db_url)
        # Session-Factory, um mit der Datenbank zu kommunizieren
        self.Session = sessionmaker(bind=self.engine)

    def initialize(self):
        """Erstellt die Tabellen basierend auf den Klassen, falls sie nicht existieren."""
        Base.metadata.create_all(self.engine)
        print("Datenbank initialisiert. Tabellen sind bereit.")

    def clear(self):
        """Leert alle Daten aus den Tabellen."""
        with self.Session() as session:
            # Effizienteres Löschen ohne Laden der Objekte
            session.query(Signal).delete()
            session.query(Measurement).delete()
            session.commit()
        print("Alle Tabellen wurden geleert.")

    def add_row(self, data):
        """Fügt einen neuen Datensatz als Objekt hinzu."""
        # Erstelle das Haupt-Measurement-Objekt
        new_measurement = Measurement(
            time=data["time"], lat=data["lat"], lon=data["lon"], alt=data["alt"],
            pol=data["pol"], mds=data["mds"], mcg=data["mcg"], status=data["status"],
            region=data["region"], delay=data["delay"], lonc=data["lonc"], latc=data["latc"]
        )

        # Erstelle die zugehörigen Signal-Objekte und füge sie hinzu
        if data.get("sig"):
            for s_data in data["sig"]:
                signal_obj = Signal(
                    sta=s_data["sta"], time=s_data["time"], lat=s_data["lat"],
                    lon=s_data["lon"], alt=s_data["alt"], status=s_data["status"]
                )
                new_measurement.signals.append(signal_obj)

        with self.Session() as session:
            session.add(new_measurement)
            session.commit()
            # Die ID wird nach dem commit automatisch zugewiesen
            print(f"Datensatz mit ID {new_measurement.id} wurde hinzugefügt.")
            return new_measurement.id

    def remove_row(self, measurement_id):
        """Entfernt einen Datensatz anhand seiner ID."""
        with self.Session() as session:
            # Finde das Objekt anhand des Primärschlüssels
            measurement_to_delete = session.get(Measurement, measurement_id)
            if measurement_to_delete:
                session.delete(measurement_to_delete)
                session.commit()
                print(f"Datensatz mit ID {measurement_id} wurde entfernt.")
            else:
                print(f"Datensatz mit ID {measurement_id} nicht gefunden.")

    def get_row_by_id(self, measurement_id):
        """
        Holt einen einzelnen Datensatz anhand seiner ID, inklusive der zugehörigen Signale.
        Gibt ein Dictionary oder None zurück.
        """
        with self.Session() as session:
            # .options(joinedload(...)) sorgt für eine effiziente Abfrage mit JOIN.
            # .get() ist optimiert für die Suche nach Primärschlüsseln.
            measurement = session.query(Measurement).options(joinedload(Measurement.signals)).get(measurement_id)
            return self._to_dict(measurement)

    def get_all_rows(self):
        """
        Holt alle Datensätze, inklusive der zugehörigen Signale.
        Gibt eine Liste von Dictionaries zurück.
        """
        with self.Session() as session:
            measurements = session.query(Measurement).options(joinedload(Measurement.signals)).all()
            return [self._to_dict(m) for m in measurements]
