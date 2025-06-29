from flask import Flask, render_template, request, session, redirect, url_for, json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Load products from JSON
def load_products():
    with open('products.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    products = load_products()
    return render_template('index.html', products=products[:4])

@app.route('/products')
def products():
    products = load_products()
    return render_template('products.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    return render_template('product_detail.html', product=product)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form.get('product_id'))
    quantity = int(request.form.get('quantity', 1))
    
    if 'cart' not in session:
        session['cart'] = []
    
    cart = session['cart']
    found = False
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += quantity
            found = True
            break
    
    if not found:
        products = load_products()
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            cart.append({
                'id': product_id,
                'name': product['name'],
                'price': product['price'],
                'image': product['image'],
                'quantity': quantity
            })
    
    session['cart'] = cart
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    session['cart'] = [item for item in cart if item['id'] != product_id]
    return redirect(url_for('view_cart'))

@app.route('/checkout')
def checkout():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('checkout.html', cart=cart, total=total)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

