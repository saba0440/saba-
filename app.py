from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(11)

users = {} 

def load_products():
    with open("data/products.json", "r") as f:
        return json.load(f)

products = load_products()

@app.route("/")
def index():
    return render_template("index.html", products=products)

@app.route("/product/<int:product_id>")
def product(product_id):
    product = next((item for item in products if item['id'] == product_id), None)
    if product:
        return render_template("product.html", product=product)
    else:
        return "პროდუქტი ვერ მოიძებნა", 404

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = next((item for item in products if item['id'] == product_id), None)
    if product:
        try:
            if 'cart' not in session:
                session['cart'] = []
            cart = session['cart']
            item_in_cart = next((item for item in cart if item["id"] == product_id), None)
            if item_in_cart:
                item_in_cart["quantity"] += 1
            else:
                cart.append({
                    "id": product["id"],
                    "name": product["name"],
                    "price": product["price"],
                    "quantity": 1,
                    "image": product["image"]
                })
            session['cart'] = cart
            print(f"კალათა დამატების შემდეგ: {session['cart']}")
            print(session)
            return jsonify({'message': f'{product["name"]} დამატებულია კალათაში!'})
        except Exception as e:
            print(f"შეცდომა კალათაში დამატებისას: {e}")
            return "შეცდომა მოხდა", 500
    else:
        return "პროდუქტი ვერ მოიძებნა", 404

@app.route("/cart")
def cart_page():
  cart = session.get('cart', [])
  print(f"კალათა კალათის გვერდზე: {cart}")
  total_price = sum(item["price"] * item["quantity"] for item in cart)
  return render_template("cart.html", cart=cart, total_price=total_price)

@app.route("/about")
def about_page():
  return render_template("about.html")

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    session['cart'] = [item for item in cart if item['id'] != product_id]
    return jsonify({'message': 'პროდუქტი წაიშალა კალათიდან'})

@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = request.form.get('quantity', type=int)
    if quantity is None or quantity <= 0:
        return jsonify({'error': 'არასწორი რაოდენობა'}), 400

    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] = quantity
            session['cart'] = cart
            return jsonify({'message': 'რაოდენობა განახლდა'})
    return jsonify({'error': 'პროდუქტი ვერ მოიძებნა კალათაში'}), 404

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users:
             return render_template('register.html', error='ეს ელფოსტა უკვე რეგისტრირებულია')
        users[email] = password
        print(f'მომხმარებელი დარეგისტრირდა: {email}')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            session['email'] = email
            print(f'მომხმარებელი ავტორიზირებულია: {email}')
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='ელფოსტა ან პაროლი არასწორია')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

def is_logged_in():
   return 'email' in session

@app.context_processor
def inject_is_logged_in():
   return dict(is_logged_in=is_logged_in)
   
@app.route('/buy/<int:product_id>')
def buy_product(product_id):
    product = next((item for item in products if item['id'] == product_id), None)
    if product:
        return render_template('buy.html', product=product)
    else:
        return "პროდუქტი ვერ მოიძებნა", 404


if __name__ == "__main__":
    app.run(debug=True)