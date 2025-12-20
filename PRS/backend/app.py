from flask import Flask, jsonify, request
from flask_cors import CORS
from recommender import RecommenderSystem
import os
import pandas as pd
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from datetime import timedelta

app = Flask(__name__)
CORS(app)

# Configuration
app.config['JWT_SECRET_KEY'] = 'super-secret-key-change-this' # Change in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# MongoDB Connection
MONGO_URI = "mongodb+srv://shreyas:ShreyasAmruth@cluster0.rnzptia.mongodb.net/?appName=Cluster0"
try:
    client = MongoClient(MONGO_URI)
    db = client['ecommerce_db']
    users_collection = db['users']
    # Ping to check connection
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Initialize Recommender
data_dir = os.path.join(os.path.dirname(__file__), 'data')
ratings_path = os.path.join(data_dir, 'ratings_Beauty.csv')
descriptions_path = os.path.join(data_dir, 'product_descriptions.csv')

recommender = RecommenderSystem(ratings_path, descriptions_path)

# --- Auth Routes ---

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user') # 'user' or 'admin'

    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400

    if users_collection.find_one({'username': username}):
        return jsonify({'message': 'Username already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    new_user = {
        'username': username,
        'password': hashed_password,
        'role': role
    }
    
    users_collection.insert_one(new_user)
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users_collection.find_one({'username': username})

    if user and bcrypt.check_password_hash(user['password'], password):
        access_token = create_access_token(identity={'username': username, 'role': user['role']})
        return jsonify({
            'access_token': access_token,
            'username': username,
            'role': user['role']
        }), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

# --- Product Routes ---

@app.route('/api/popular', methods=['GET'])
def get_popular():
    product_ids = recommender.get_popular_products()
    details = get_product_details(product_ids)
    return jsonify({'products': details})

@app.route('/api/recommend/collab/<product_id>', methods=['GET'])
def get_collab_recommendations(product_id):
    product_ids = recommender.get_collaborative_recommendations(product_id)
    details = get_product_details(product_ids)
    return jsonify({'products': details})

@app.route('/api/search', methods=['GET'])
def search_products():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'products': []})
    product_ids = recommender.get_content_based_recommendations(query)
    details = get_product_details(product_ids)
    return jsonify({'products': details})

@app.route('/api/products', methods=['GET'])
def get_all_products():
    # In a real app with Mongo, we would fetch from Mongo products collection
    # For now, we stick to the CSV/Recommender source for consistency
    columns = ['product_uid', 'product_title', 'product_description', 'image_url']
    # Ensure columns exist before selecting (in case of old data loaded in memory, though we'll restart)
    existing_cols = [c for c in columns if c in recommender.descriptions.columns]
    desc_products = recommender.descriptions[existing_cols].to_dict('records')
    return jsonify({'products': desc_products})

# Helper
def get_product_details(product_ids):
    if not product_ids:
        return []
    df_ids = pd.DataFrame(product_ids, columns=['product_uid'])
    merged = df_ids.merge(recommender.descriptions, on='product_uid', how='left')
    
    # Fill NaN for missing details
    if 'product_description' in merged.columns:
        merged['product_description'] = merged['product_description'].fillna('No description available')
    if 'product_title' in merged.columns:
        merged['product_title'] = merged['product_title'].fillna(merged['product_uid'])
    if 'image_url' in merged.columns:
        merged['image_url'] = merged['image_url'].fillna('')
        
    return merged.to_dict('records')

# --- Cart Routes ---

@app.route('/api/cart', methods=['GET'])
@jwt_required()
def get_cart():
    current_user = get_jwt_identity()
    username = current_user['username']
    
    user_cart = db['carts'].find_one({'username': username})
    if not user_cart:
        return jsonify({'cart': []})
    
    # Enrich with product details
    cart_items = user_cart.get('items', [])
    if not cart_items:
        return jsonify({'cart': []})
        
    product_ids = [item['product_id'] for item in cart_items]
    details = get_product_details(product_ids)
    
    # Merge quantity
    for i, detail in enumerate(details):
        # Find corresponding item to get quantity
        # This simple logic assumes order is preserved or we match by ID
        # Better to create a map
        item = next((x for x in cart_items if x['product_id'] == detail['product_uid']), None)
        if item:
            detail['quantity'] = item.get('quantity', 1)
            
    return jsonify({'cart': details})

@app.route('/api/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    current_user = get_jwt_identity()
    username = current_user['username']
    data = request.get_json()
    product_id = data.get('product_id')
    
    if not product_id:
        return jsonify({'message': 'Product ID required'}), 400
        
    db['carts'].update_one(
        {'username': username},
        {
            '$setOnInsert': {'username': username},
            '$addToSet': {'items': {'product_id': product_id, 'quantity': 1}} 
            # Note: Real app would handle quantity increment if exists
        },
        upsert=True
    )
    
    return jsonify({'message': 'Added to cart'}), 200

@app.route('/api/cart/<product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(product_id):
    current_user = get_jwt_identity()
    username = current_user['username']
    
    db['carts'].update_one(
        {'username': username},
        {'$pull': {'items': {'product_id': product_id}}}
    )
    
    return jsonify({'message': 'Removed from cart'}), 200

# --- Profile Routes ---

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user = get_jwt_identity()
    username = current_user['username']
    user = users_collection.find_one({'username': username}, {'password': 0, '_id': 0})
    return jsonify({'user': user})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
