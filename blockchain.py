# from block import Block
from database.helpers import QSL
import pickle


class Chain():

    def __init__(self, chain=[], diff=6):
        self.difficulty = diff
        self.chain = chain

    def addBlock(self, block):
        try:
            if self.chain[-1].current_hash == block.prevhash and block.current_hash[:self.difficulty] == "0"*self.difficulty:
                self.chain.append(block)
            else:
                print("Invalid block")
        except IndexError:
            pass

    def mine(self, block):
        while True:
            if block.current_hash[:self.difficulty] != "0"*self.difficulty:
                block.makeHash()
            else:
                data = block.getData()
                name = 'transaction/{}.ds'.format(block.hash)
                pickle.dump(block, open(name.format(block.hash), 'wb'))
                QSL().trans(data['Seller'], data['Buyer'], data['Plot'], data['Location'],
                      data['hash'], data['prevhash'], data['price'], name)
                self.addBlock(block)
                break
        print("Block {} Minned".format(block))
