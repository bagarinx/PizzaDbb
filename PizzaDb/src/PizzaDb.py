from PizzaDbEntry import PizzaDbEntry
import csv
import json
from tkinter import filedialog

class PizzaDb:
    """
    - simple database of Pizzeria Inventory System
    """    

    def __init__(self, init=False, dbName='PizzaDb.csv'):       
        self.dbName = dbName
        self.entries = []

    def fetch_item(self):
        return [(entry.id, entry.item, entry.type, entry.price, entry.status) for entry in self.entries]

    def insert_item(self, id, item, type, price, status):
        newEntry = PizzaDbEntry(id=id, item=item, type=type, price=price, status=status)
        self.entries.append(newEntry)

    def delete_item(self, id):
        self.entries = [entry for entry in self.entries if entry.id != id]

    def update_item(self, new_item, new_type, new_price, new_status, id):
        for entry in self.entries:
            if entry.id == id:
                entry.item = new_item
                entry.type = new_type
                entry.price = new_price
                entry.status = new_status
                break

    def export_csv(self):
        with open(self.dbName, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for entry in self.entries:
                csv_writer.writerow([entry.id, entry.item, entry.type, entry.price, entry.status])

    def export_json(self):
        json_data = [{'ref#': entry.id, 'item': entry.item, 'class': entry.type, 'price': entry.price, 'status': entry.status} for entry in self.entries]
        with open(f'{self.dbName.split(".")[0]}.json', 'w') as jsonfile:
            json.dump(json_data, jsonfile, indent=2)

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')], 
                                                  title='Choose a CSV file to import')
        if file_path:
            with open(file_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    values = line.strip().split(',')
                    if len(values) == 5:
                        id, item, type, price, status = values
                        if not self.id_exists(id):
                            self.insert_item(id, item, type, price, status)
                        else:
                            print(f"Skipping import for existing ID:{id}")
                    else:
                        print(f"Skipping invalid entry: {line}")


    def id_exists(self, id):
        return any(entry.id == id for entry in self.entries)
    
