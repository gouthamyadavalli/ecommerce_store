from flask import Flask, render_template, redirect, url_for, flash, request, session
from ecommerce_store.models import db, User, Product, Order
from ecommerce_store.forms import RegistrationForm, LoginForm, AddProductForm
from ecommerce_store.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    flash('Product added to cart')
    
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty')
        return redirect(url_for('index'))
    products = Product.query.filter(Product.id.in_(session['cart'])).all()
    return render_template('cart.html', products=products)

@app.route('/checkout')
def checkout():
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty')
        return redirect(url_for('index'))
    products = Product.query.filter(Product.id.in_(session['cart'])).all()
    total = sum([p.price for p in products])
    return render_template('checkout.html', products=products, total=total)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Logged in successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!')
    return redirect(url_for('index'))

@app.route('/admin/add_product', methods=['GET', 'POST'])
def add_product():
    form = AddProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, description=form.description.data, price=form.price.data, image_url=form.image_url.data)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!')
        return redirect(url_for('index'))
    return render_template('add_product.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
