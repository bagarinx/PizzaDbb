'''
This is the interface to an SQLite Database
'''
import json
import sqlite3
from tkinter import filedialog
import csv

class PizzaDbSqlite:
    def __init__(self, dbName='Pizza.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Pizza (
                id TEXT PRIMARY KEY,
                item TEXT,
                type TEXT,
                price TEXT,
                status TEXT)''')
        self.conn.commit()
        self.conn.close()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()        

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Pizza (
                    id TEXT PRIMARY KEY,
                    item TEXT,
                    type TEXT,
                    price TEXT,
                    status TEXT)''')
        self.commit_close()

    def fetch_item(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM Pizza')
        pizza =self.cursor.fetchall()
        self.conn.close()
        return pizza

    def insert_item(self, id, item, type, price, status):
        with sqlite3.connect(self.dbName) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Pizza (id, item, type, price, status) VALUES (?, ?, ?, ?, ?)',
                       (id, item, type, price, status))
            
    def delete_item(self, id):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM Pizza WHERE id = ?', (id,))
        self.commit_close()

    def update_item(self, new_item, new_type, new_price, new_status, id):
        self.connect_cursor()
        self.cursor.execute('UPDATE Pizza SET item = ?, type = ?, price = ?, status = ? WHERE id = ?',
                    (new_item, new_type, new_price, new_status, id))
        self.commit_close()

    def id_exists(self, id):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM Pizza WHERE id = ?', (id,))
        result =self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def export_csv(self):
        with open(self.csvFile, "w") as filehandle:
            dbEntries = self.fetch_item()
            for entry in dbEntries:
                print(entry)
                filehandle.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]},{entry[4]}\n")

    def import_csv(self, csv_file):
        self.connect_cursor()
        with open(csv_file, 'r') as filehandle:
            csv_reader = csv.reader(filehandle)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                self.insert_item(*row)
        self.conn.close()


    def export_json(self, jsonFile='LaRossaInventory.json'):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM Pizza')
        pizza = self.cursor.fetchall()
        self.conn.close()

        json_data = []

        for entry in pizza:
            entry_dict = {
                'ID': entry[0],
                'Item': entry[1],
                'Type': entry[2],
                'Price': entry[3],
                'Status': entry[4]
            }
            json_data.append(entry_dict)

        with open(jsonFile, 'w') as json_file:
            json.dump(json_data, json_file, indent=2)

        print(f'Data exported to {jsonFile} successfully.')

def test_PizzaDb():
    iPizzaDb = PizzaDbSqlite(dbName='PizzaDbSql.db')

    for entry in range(30):
        iPizzaDb.insert_item(entry, f'Item{entry} Type{entry}', f'Price{entry}', 'In Stock')
        assert iPizzaDb.id_exists(entry)

    all_entries = iPizzaDb.fetch_item()
    assert len(all_entries) == 30

    for entry in range(10, 20):
        iPizzaDb.update_item(f'Item{entry} Type{entry}', f'Price{entry}', 'In Stock', entry)
        assert iPizzaDb.id_exists(entry)

    all_entries = iPizzaDb.fetch_item()
    assert len(all_entries) == 30

    for entry in range(10):
        iPizzaDb.delete_item(entry)
        assert not iPizzaDb.id_exists(entry) 

    all_entries = iPizzaDb.fetch_item()
    assert len(all_entries) == 20