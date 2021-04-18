from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import time
from cloudipsp import Api, Checkout
time.ctime()
print(time.ctime())

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_shop.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(100),nullable = False)
    prize = db.Column(db.Integer,nullable = False)
    isActive = db.Column(db.Boolean,default = True)
    text = db.Column(db.Text(1000))
    data = db.Column(db.String(100),default = time.ctime())
    def __repr__(self):
        return self.title

@app.route('/home')
@app.route('/')
def index():
    items = Item.query.order_by(Item.prize).all()
    return render_template('home.html',data = items)
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/price',methods=['POST','GET'])
def price():
    if request.method == 'POST':
        title = request.form['title']
        prize = request.form['prize']
        text = request.form['text']
        item = Item(title = title, prize= prize,text=text)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/home')
        except:
            return "ошибка"
    else:
        return render_template('price.html')
@app.route('/shop/<int:id>')
def shop(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(item.prize)+'00'
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)
if __name__ == '__main__':
    app.run(debug=True)