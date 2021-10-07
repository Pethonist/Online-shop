from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Flask

users = SQLAlchemy(app)
items = SQLAlchemy(app)

basket_list = []
basket_price = []
counter = []


"""Create class Users and create QSL data base for users"""
class Users(users.Model):

    id = users.Column(users.Integer, primary_key=True)
    first_name = users.Column(users.String(100), nullable=False)
    last_name = users.Column(users.String(100), nullable=False)
    username = users.Column(users.String(100), nullable=False)
    email = users.Column(users.String(100), nullable=False)
    password = users.Column(users.String(100), nullable=False)
    date = users.Column(users.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Users %r>' % self.id


"""Create class Item (product data base)"""
class Items(items.Model):

    id = items.Column(items.Integer, primary_key=True)
    name = items.Column(items.String(100), nullable=False)
    info = items.Column(items.Text, nullable=False)
    price = items.Column(items.Integer, nullable=False)

    def __repr__(self):
        return '<Items %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template('main.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/log_in', methods=['POST', 'GET'])
def log_in():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == 'Admin@gmail.com' and password == 'Admin':
            return redirect('/admin_page')
    return render_template('log_in.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = Users(first_name=first_name, last_name=last_name, username=username, email=email, password=password)

        try:
            users.session.add(user)
            users.session.commit()
            return redirect('/about')
        except:
            return "Error when try to register"

    else:
        return render_template('register.html')


@app.route('/admin_page', methods=['POST', 'GET'])
def administrator():
    if request.method == 'POST':
        name = request.form['productName']
        info = request.form['productInfo']
        price = request.form['productPrice']

        item = Items(name=name, info=info, price=price)

        try:
            items.session.add(item)
            items.session.commit()
            return redirect('/admin_page')
        except:
            return 'Error when try to add new product'

    else:
        products = Items.query.order_by(Items.name.desc()).all()
        return render_template('admin.html', products=products)


@app.route('/shop')
def shop():
    products = Items.query.order_by(Items.name.desc()).all()
    return render_template('shop.html', products=products)


@app.route('/shop/<int:id>/delete')
def delete_product(id):
    product = Items.query.get_or_404(id)

    try:
        items.session.delete(product)
        items.session.commit()
        return redirect('/admin_page')
    except:
        return 'Error when try to delete product'


@app.route('/shop/<int:id>/edit', methods=['POST', 'GET'])
def edit_product(id):
    product = Items.query.get(id)

    if request.method == 'POST':
        product.name = request.form['productName']
        product.info = request.form['productInfo']
        product.price = request.form['productPrice']

        try:
            items.session.commit()
            return redirect('/admin_page')
        except:
            return 'Error when try to edit product'

    else:
        return render_template('edit_product.html', product=product)



@app.route('/shop/<int:id>', methods=['POST', 'GET'])
def info_about_product(id):
    product = Items.query.get(id)
    if request.method == 'POST':
        basket_list.append(product)
        basket_price.append(product.price)
        counter.append(1)

        try:
            return redirect('/shop')
        except: "Error then add new product to basket"

    else:
        return render_template('product_detail.html', product=product)


@app.route('/basket', methods=['POST', 'GET'])
def basket():
    basket_items = basket_list
    full_price = sum(basket_price)
    quantity = sum(counter)
    promo_code = 'EXAMPLECODE'
    size_of_promo = '-$5'

    if request.method == 'POST':
        promo_code = request.form['promo']
        if len(promo_code) > 0:
            full_price -= full_price * 0.05
            size_of_promo = full_price * 0.05
    
    return render_template('basket.html', basket_items=basket_items, basket_price=full_price, quantity=quantity, promo=promo_code, sale=size_of_promo)


'''@app.route('/shop/<int:id>')
def info_about_product(id):
    product = Items.query.get(id)
    return render_template('product_detail.html', product=product)'''


"""In code below we write possible errors in our site
   Main file "support.html" have re-links in different pages"""
@app.route('/support')
def support():
    return render_template('support.html')


@app.route('/basket_error')
def basket_error():
    return render_template('basket_error.html')


@app.route('/login_error')
def log_in_error():
    return render_template('login_error.html')


@app.route('/register_error')
def register_error():
    return render_template('register_error.html')


if __name__ == '__main__':
    app.run(debug=True)
