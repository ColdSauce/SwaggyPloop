#!/usr/in/env python3

import os
import sqlite3
import time

DATABASE_FILENAME = 'database.db'

class Database:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.setup()

    @staticmethod
    def get_default():
        filename = os.path.join(os.environ['PROJECT_ROOT'], DATABASE_FILENAME)
        return Database(sqlite3.connect(filename))

    def setup(self):
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS exfiltrated_data
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                uuid CHAR(6),
                packet_id INTEGER,
                packet_number INTEGER,
                blob BLOB)
            ''')
        self.connection.commit()

    def add_blob(self, uuid, packet_id, packet_number, blob):
        self.cursor.execute(
            '''INSERT INTO exfiltrated_data
            (uuid, packet_id, packet_number, blob) VALUES (?,?,?,?,?)''',
            (uuid, packet_id, packet_number, blob))
        self.connection.commit()

    def _get_data(self, uuid, packet_id):
        self.cursor.execute(
            '''SELECT * FROM exfiltrated_data WHERE uuid=? AND packet_id=?
            ORDER BY packet_number ASC''',
            (uuid, packet_id))
        return "".join([entry[5] for entry in self.cursor])

    def close(self):
        self.connection.close()

if __name__ == '__main__':
    d = Database.get_default()
    # d.add_blob(100, 'user1', 'hash1', 1, 'there once was a ')
    # d.add_blob(101, 'user1', 'hash1', 2, ' gay fat fox who')
    # d.add_blob(103, 'user1', 'hash2', 1, 'fuck')
    # d.add_blob(102, 'user1', 'hash1', 3, ' ate chese')
    # d.add_blob(104, 'user1', 'hash2', 2, 'fuck')
    # d.add_blob(105, 'user1', 'hash2', 3, 'fuck')
    print(d._get_data('user1', 'hash1'))
