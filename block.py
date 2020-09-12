from hashlib import sha256
import uuid

def data(buyer, seller, location, price, plot):
    return {"Buyer": buyer, "Seller": seller,
            "location": str(location), "price": price, "plot": plot}


class Block():

    def __init__(self, transaction, prevhash):
        self.transaction = transaction
        self.prevhash = prevhash
        self.id_ = uuid.uuid4()
        self.nonce = 0
        algo = sha256()
        algo.update(
            str({"data": self.transaction, "prevhash": self.prevhash}).encode('utf-8'))
        self.hash = algo.hexdigest()
        self.current_hash = self.hash

    def makeHash(self):
        algo = sha256()
        self.nonce += 1
        algo.update(str({"data": self.hash, "nonce": self.nonce,
                         "current_hash": self.current_hash, "prevhash": self.prevhash}).encode('utf-8'))
        self.current_hash = algo.hexdigest()
        return algo.hexdigest()

    def getData(self):
        return {"id":self.id_,"chash":self.hash ,"hash":self.current_hash,"prevhash":self.prevhash,**self.transaction}

    def __str__(self):
        return str({"prevhash": self.prevhash, "data": self.hash, "hash": self.current_hash})

# trasction data
# data = {"buyer": "james", "seller": "kelvin",
#         "price": 20000, "date": "4444"}

# Defining a block
# block = Block({"buyer": "james", "seller": "kelvin",
#                "price": 20000, "date": "4444"}, str("0"*64))

# block.makeHash()
# print(block)
# print(block.hash)
