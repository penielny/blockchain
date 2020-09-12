import sqlite3


class QSL():
    def __init__(self):
        self.conn = sqlite3.connect("database/database.sqlite")

    def trans(self, Seller, Buyer, Amount, Location, hash_, prevhash, Price, blob):
        self.conn.cursor().execute('''INSERT INTO "main"."Transaction"("ID","Buyer","Seller","Plot","Location","hash","prevhash","Price",data) VALUES (NULL,?,?,?,?,?,?,?,?);''', (
            Buyer, Seller, Amount, Location, str(hash_), str(prevhash), Price, blob))
        self.conn.commit()

    def gettrans(self):
        c = self.conn.cursor()
        c.execute('''SELECT * FROM `Transaction`;''')
        rows = c.fetchall()
        return rows

    def migrate(self):
        self.conn.cursor().execute('''
        CREATE TABLE "Transaction" (
            "ID"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            "Buyer"	TEXT,
            "Seller"	TEXT,
            "Plot"	TEXT,
            "Location"	TEXT,
            "hash"	TEXT,
            "prevhash"	TEXT,
            "Price"	TEXT,
            "data"	TEXT
        );
        ''')


# data struct
# Buyer
# Seller
# location
# Price
# Plot
# hash
# prevhash
