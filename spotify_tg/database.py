
import sqlite3


class Database:
    def __init__(self, db_file="songs.db"):
        self.db_file = db_file

    def initialize(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY AUTOINCREMENT, full_track TEXT)"
        )
        conn.commit()
        conn.close()

    def is_downloaded(self, full_track):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM songs WHERE full_track = ?",
            (full_track,)
        )
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def downloaded(self, full_track):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO songs (full_track) VALUES (?)",
            (full_track,)
        )
        conn.commit()
        conn.close()
