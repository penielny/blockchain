from datetime import date
from block import Block
from blockchain import Chain
from database.helpers import QSL
from flask import Flask, render_template, request, redirect, flash, url_for
from threading import Thread
import pickle
import uuid

def data(Buyer, Seller, location, Price, Plot):
    return {"Buyer": Buyer, "Seller": Seller, "Location": str(location), "price": Price, "Plot": Plot, "date": str(date.today())}


def main():
    # initiating chain
    chain = Chain()

    # creating Genesis Block
    block = Block(data("Genesis", "Genesis", "Genesis",
                       0000000, 0000000), str("0"*64))
    block.current_hash = str("0"*64)

    # adding genesis to chain
    chain.chain.append(block)
    # print(chain.chain)
    # get all transaction from db
    trans = QSL().gettrans()
    for tran in trans:
        block = pickle.load(open(str(tran[-1]), "rb"))
        # print(block.prevhash)
        chain.addBlock(block)
    # print(" * BLOCKCHAIN: sync done")
    # print(chain.chain[-1].current_hash)

    # block = Block({"Buyer": "james", "Seller": "kelvin",
    #                "price": 20000, "date": "4444", "Location": "sakomono/ldof", "Plot": 5}, str("0"*64))

    # chain.mine(block)
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "ox"*23

    @app.route('/')
    def index():
        res = []
        for i in chain.chain:
            if i.current_hash != "0"*64:
                res.append(i.getData())
            pass
        return render_template('index.html', data=res)

    @app.route('/doc/<hash_>')
    def single(hash_):
        res = None
        for c in chain.chain:
            if c.current_hash == hash_:
                res = c.getData()
        return render_template('details.html', data=res)

    @app.route('/add_doc', methods=["POST"])
    def proccessDoc():
        if request.method == "POST":
            d = data(request.form.get('buyer'), request.form.get('seller'), request.form.get(
                'location'), request.form.get('price'), request.form.get('plot'))
            block = Block(d, chain.chain[-1].current_hash)
            t = Thread(target=chain.mine, args=[block])
            t.start()
            flash("Document is begin proccessed")
            return redirect('/')
        return redirect('/')
    app.run(debug=True)


if __name__ == "__main__":
    main()
