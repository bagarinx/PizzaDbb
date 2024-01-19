import unittest
import os
import json
import csv
from PizzaDbSqlite import PizzaDbSqlite

class TestPizzaDbSqlite(unittest.TestCase):

    def setUp(self):
        self.iPizzaDb = PizzaDbSqlite(dbName='PizzaDbSql.db')
        self.iPizzaDb.create_table()
        self.db_name = 'PizzaDbSql_test.db'  # Initialize db_name
        self.db = PizzaDbSqlite(dbName=self.db_name)

    def tearDown(self):
        self.db.conn.close()  # Close the database connection
        os.remove(self.db_name)

    def create_table(self):
        self.db.create_table()
        self.assertTrue(os.path.exists(self.db_name))

    def test_insert_fetch_all_items(self):
        items = [
        ('LR1001', 'Chorizo Flatbread', 'Appetizer', 'P151.00', 'In Stock'),
        ('LR1929', 'Pepperoni', 'Pizza', 'P599.00', 'Running Low')]

        for item in items:
            self.iPizzaDb.insert_item(*item)
        fetched_items = self.iPizzaDb.fetched_items()
        self.assertEqual(fetched_items, items)

    def test_update_item(self):
        self.iPizzaDb.insert_item('LR1001', 'Chorizo Flatbread', 'Appetizer', 'P151.00', 'In Stock')
        self.iPizzaDb.update_item('LR1001', 'Chorizo Flatbread', 'Appetizer', 'P151.00', 'In Stock')

        updated_item = self.db.fetch_items()[0]
        expected_item = ('LR1001', 'Chorizo Flatbread', 'Appetizer', 'P151.00', 'Running Low')
        self.assertEqual(updated_item, ('LR1001', 'Chorizo Flatbread', 'Appetizer', 'P151.00', 'Running Low'))

    def test_delete_item(self):
        self.iPizzaDb.insert_item('LR1001', 'Chorizo Flatbread', 'Appetizer', 'P151.00', 'In Stock')
        self.iPizzaDb.delete_item('LR1001')

        self.assertFalse(self.db.item_exists('LR1001'))
        self.assertEqual(self.db.fetch_items(), [])

    def test_export_csv(self):
        self.db.insert_item('LR1001', 'Chorizo Flatbread', 'Appetizer', 'P151.00', 'In Stock')
        self.db.export_csv()

        with open(self.db.csvFile, 'r') as filehandle:
            content = filehandle.read()
            self.assertEqual(content, 'LR1001,Chorizo Flatbread,Appetizer,P151.00,In Stock\n')

    def test_export_json(self):
        self.db.insert_item('LR1001', 'Chorizo Flatbread', 'Appetizer', 'P151.00', 'In Stock')
        self.db.export_json()

        with open(self.db.jsonFile, 'r') as filehandle:
            data = json.load(filehandle)
            self.assertEqual(data, [{'id':'LR1001', 'item':'Chorizo Flatbread', 'type':'Appetizer', 'price':'P151.00', 'status': 'In Stock'}])

    def test_import_csv(self):
        test_csv_file = 'test_data.csv'
        with open(test_csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'item', 'type', 'price', 'status'])
            writer.writerow(['LR1001', 'Chorizo Flatbread', 'Appetizer', 'P151.00', 'In Stock'])
            writer.writerow(['LR1929', 'Pepperoni', 'Pizza', 'P599.00', 'Running Low'])

        self.db.import_csv(test_csv_file)

        fetched_items = self.db.fetch_items()
        expected_items = [
            ('LR1001', 'Chorizo Flatbread', 'Appetizer', 'P151.00', 'In Stock'),
            ('LR1929', 'Pepperoni', 'Pizza', 'P599.00', 'Running Low')
        ]
        
        self.assertEqual(fetched_items, expected_items)

        os.remove(test_csv_file)

if __name__ == '__main__':
    unittest.main()
