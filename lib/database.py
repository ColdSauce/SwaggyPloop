#!/usr/bin/env python3

import os
import sqlite3
import sys
import time

# Constants
DATABASE_FILENAME = 'database.db'
FILEPATH = os.path.abspath(__file__)

# Path modification for project dependencies
def parent_chain(path, n):
    for i in range(n):
        path = os.path.dirname(path)
    return path

class Database:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.setup()

    @staticmethod
    def get_default():
        filename = os.path.join(parent_chain(FILEPATH, 2), DATABASE_FILENAME)
        return Database(sqlite3.connect(filename))

    def setup(self):
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS exfiltrated_data
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                mac_address INTEGER,
                payload_id INTEGER,
                sequence_number INTEGER,
                payload BLOB)
            ''')
        self.connection.commit()

    def add(self, mac_address, payload_id, sequence_number, payload):
        self.cursor.execute(
            '''INSERT INTO exfiltrated_data
            (mac_address, payload_id, sequence_number, payload)
            VALUES (?,?,?,?)''',
            (mac_address, payload_id, sequence_number, payload))
        self.connection.commit()

    def get_all_mac_addresses(self):
        self.cursor.execute(
            '''SELECT DISTINCT mac_address FROM exfiltrated_data''')
        return [entry for entry in self.cursor]

    def get_all_payload_names(self, mac_address):
        self.cursor.execute(
            '''SELECT payload_id,payload FROM exfiltrated_data
            WHERE mac_address=? AND sequence_number=1
            ORDER BY payload_id ASC''',
            (mac_address,))
        return [entry for entry in self.cursor]

    def get_payload(self, mac_address, payload_id):
        self.cursor.execute(
            '''SELECT * FROM exfiltrated_data
            WHERE mac_address=? AND payload_id=?
            ORDER BY sequence_number ASC''',
            (mac_address, payload_id))
        return [entry[1:] for entry in self.cursor]

    def close(self):
        self.connection.close()

if __name__ == '__main__':
    d = Database.get_default()
