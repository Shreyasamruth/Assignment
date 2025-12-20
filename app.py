import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' # Needed for session

# ... (Previous model loading code) ...

# --- E-Commerce / Cart Logic (Session Based) ---

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item.get('price', 0) * item.get('quantity', 1) for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=round(total, 2))

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    try:
        data = request.json
        product_uid = data.get('product_uid')
        # product_title = data.get('product_title')
        # ... fetch details from model to be safe ...
        
        # Get details from memory model to ensure price/info is correct
        df = prs_model.descriptions
        product = df[df['product_uid'] == product_uid].iloc[0].to_dict()
        
        # Mock Price generation (since dataset might not have it, or we just generate random)
        # Using a hash of uid to keep price consistent for same item
        price = round(abs(hash(product_uid)) % 100 + 10.99, 2)
        
        item = {
            'product_uid': product_uid,
            'product_title': product.get('product_title', 'Unknown Product'),
            'image_url': product.get('image_url', ''),
            'price': price,
            'quantity': 1
        }

        cart = session.get('cart', [])
        # Check if exists
        found = False
        for cart_item in cart:
            if cart_item['product_uid'] == product_uid:
                cart_item['quantity'] += 1
                found = True
                break
        if not found:
            cart.append(item)
            
        session['cart'] = cart
        return jsonify({'message': 'Added to cart', 'cart_count': len(cart)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/cart/remove', methods=['POST'])
def remove_from_cart():
    try:
        data = request.json
        product_uid = data.get('product_uid')
        cart = session.get('cart', [])
        cart = [item for item in cart if item['product_uid'] != product_uid]
        session['cart'] = cart
        return jsonify({'message': 'Removed', 'cart_count': len(cart)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/checkout', methods=['POST'])
def checkout():
    try:
        cart = session.get('cart', [])
        if not cart:
            return jsonify({'error': 'Cart is empty'}), 400
            
        data = request.json
        shipping_info = data.get('shipping_info', {})
        
        order_id = str(uuid.uuid4())[:8].upper()
        total = sum(item['price'] * item['quantity'] for item in cart)
        
        order = {
            'order_id': order_id,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'items': cart,
            'total': round(total, 2),
            'shipping_info': shipping_info,
            'status': 'Processing'
        }
        
        # Store order in session for demo (in real app, DB)
        orders = session.get('orders', {})
        orders[order_id] = order
        session['orders'] = orders
        
        # Clear Cart
        session['cart'] = []
        
        return jsonify({'order_id': order_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/order_confirmation/<order_id>')
def order_confirmation(order_id):
    orders = session.get('orders', {})
    order = orders.get(order_id)
    if not order:
        return "Order not found", 404
    return render_template('order_success.html', order=order)

@app.route('/track_order')
def track_order_page():
     return render_template('track_order.html')

@app.route('/api/track', methods=['GET'])
def track_order_api():
    order_id = request.args.get('order_id')
    orders = session.get('orders', {})
    order = orders.get(order_id)
    if order:
        return jsonify(order)
    return jsonify({'error': 'Order not found'}), 404
import joblib
import pandas as pd
import numpy as np
import os


# Load Models
try:
    linear_model = joblib.load('models/linear_regression.pkl')
    naive_bayes_model = joblib.load('models/naive_bayes.pkl')
    covid_encoders = joblib.load('models/covid_encoders.pkl')
    kmeans_model = joblib.load('models/kmeans.pkl')
    # Use 'recommender' module name since the class is defined there and pickled object needs it
    from recommender import RecommenderSystem 
    prs_model = joblib.load('models/recommender.pkl')
except Exception as e:
    print(f"Error loading models: {e}. Please run train_models.py first.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/regression')
def regression():
    return render_template('regression.html')

@app.route('/naive_bayes')
def naive_bayes():
    return render_template('naive_bayes.html')

@app.route('/kmeans')
def kmeans():
    return render_template('kmeans.html')

@app.route('/prs')
def prs():
    return render_template('prs.html')

@app.route('/api/predict/regression', methods=['POST'])
def predict_regression():
    try:
        data = request.json
        # Expecting: cylinders, displacement, horsepower, weight, acceleration, model_year, origin
        features = [
            float(data['cylinders']),
            float(data['displacement']),
            float(data['horsepower']),
            float(data['weight']),
            float(data['acceleration']),
            float(data['model_year']),
            float(data['origin'])
        ]
        prediction = linear_model.predict([features])[0]
        return jsonify({'mpg': round(prediction, 2)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/predict/naive_bayes', methods=['POST'])
def predict_naive_bayes():
    try:
        data = request.json
        # Expecting: fever, cough, breathing_difficulty, fatigue, sore_throat, body_ache
        input_data = []
        feature_names = ['fever', 'cough', 'breathing_difficulty', 'fatigue', 'sore_throat', 'body_ache']
        
        for feature in feature_names:
            val = data[feature]
            input_data.append(covid_encoders[feature].transform([val])[0])
            
        prediction = naive_bayes_model.predict([input_data])[0]
        result = covid_encoders['infected'].inverse_transform([prediction])[0]
        return jsonify({'infected': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/predict/kmeans', methods=['POST'])
def predict_kmeans():
    try:
        data = request.json
        # Expecting: weight, horsepower
        features = [
            float(data['weight']),
            float(data['horsepower'])
        ]
        cluster = kmeans_model.predict([features])[0]
        return jsonify({'cluster': int(cluster)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# --- PRS Routes ---

def get_product_details(product_ids):
    if not product_ids:
        return []
    # prs_model.descriptions is a dataframe
    df = prs_model.descriptions
    # Filter by product_uid
    matches = df[df['product_uid'].isin(product_ids)]
    
    # We want to preserve order if possible, but simplest is just return matches
    result = matches.to_dict('records')
    # Handle NaNs for JSON serialization
    for item in result:
        for k, v in item.items():
            if pd.isna(v):
                item[k] = ""
    return result

@app.route('/api/predict/prs_popular', methods=['GET'])
def prs_popular():
    try:
        product_ids = prs_model.get_popular_products(n=10)
        details = get_product_details(product_ids)
        return jsonify({'products': details})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/predict/prs_search', methods=['GET'])
def prs_search():
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'products': []})
        product_ids = prs_model.get_content_based_recommendations(query)
        details = get_product_details(product_ids)
        return jsonify({'products': details})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/predict/prs_collab', methods=['GET'])
def prs_collab():
    try:
        product_id = request.args.get('product_id', '')
        if not product_id:
            return jsonify({'products': []})
        product_ids = prs_model.get_collaborative_recommendations(product_id, n=10)
        details = get_product_details(product_ids)
        return jsonify({'products': details})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/product/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        details = get_product_details([product_id])
        if not details:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify({'product': details[0]})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/predict/prs_all', methods=['GET'])
def prs_all():
    try:
        if prs_model.descriptions.empty:
             return jsonify({'products': []})
             
        # Filter for products that have images
        # Check if column exists
        if 'image_url' in prs_model.descriptions.columns:
            # Filter where image_url is not null, not empty, and looks valid (e.g. length > 5)
            # Ensure it is string first
            desc_df = prs_model.descriptions.copy()
            desc_df['image_url'] = desc_df['image_url'].astype(str)
            
            valid_imgs = desc_df[
                desc_df['image_url'].notna() & 
                (desc_df['image_url'].str.strip() != '') &
                (desc_df['image_url'].str.len() > 5) &
                (desc_df['image_url'] != 'nan')
            ]
            
            # If we have enough with images, show them
            if not valid_imgs.empty:
                product_ids = valid_imgs['product_uid'].head(50).tolist()
            else:
                product_ids = prs_model.descriptions['product_uid'].head(50).tolist()
        else:
            product_ids = prs_model.descriptions['product_uid'].head(50).tolist()

        details = get_product_details(product_ids)
        return jsonify({'products': details})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
