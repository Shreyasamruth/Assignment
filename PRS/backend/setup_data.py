import pandas as pd
import numpy as np
import os
import random
import string

def generate_mock_data():
    if not os.path.exists('data'):
        os.makedirs('data')

    # 1. Generate Mock Ratings Data (ratings_Beauty.csv)
    print("Generating mock ratings_Beauty.csv...")
    user_ids = [''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) for _ in range(50)]
    product_ids = [''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) for _ in range(20)]
    
    ratings_data = []
    for _ in range(500):
        user = random.choice(user_ids)
        product = random.choice(product_ids)
        rating = random.randint(1, 5)
        timestamp = 1369699200 + random.randint(0, 1000000)
        ratings_data.append([user, product, rating, timestamp])
    
    df_ratings = pd.DataFrame(ratings_data, columns=['UserId', 'ProductId', 'Rating', 'Timestamp'])
    df_ratings.to_csv('data/ratings_Beauty.csv', index=False)
    print("ratings_Beauty.csv created.")

    # 2. Generate Mock Product Descriptions (product_descriptions.csv)
    print("Generating mock product_descriptions.csv...")
    # Use the same product IDs from ratings + some extras
    all_product_ids = product_ids + [''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) for _ in range(10)]
    
    products_info = [
        {"title": "Luxury Red Lipstick", "desc": "Beautiful red lipstick with long lasting color.", "image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=300&q=80"},
        {"title": "Anti-Aging Cream", "desc": "Anti-aging face cream with vitamin E.", "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=300&q=80"},
        {"title": "Pro Hair Dryer", "desc": "Hair dryer with multiple heat settings.", "image": "https://images.unsplash.com/photo-1522338140262-f46f5913618a?w=300&q=80"},
        {"title": "Organic Shampoo", "desc": "Organic shampoo for dry hair.", "image": "https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=300&q=80"},
        {"title": "Waterproof Eyeliner", "desc": "Waterproof eyeliner black.", "image": "https://images.unsplash.com/photo-1629198688000-71f23e745b6e?w=300&q=80"},
        {"title": "Matte Foundation", "desc": "Matte finish foundation for oily skin.", "image": "https://images.unsplash.com/photo-1631729371254-42c2892f0e6e?w=300&q=80"},
        {"title": "Electric Shaver", "desc": "Electric shaver for men.", "image": "https://images.unsplash.com/photo-1621607512214-68297480165e?w=300&q=80"},
        {"title": "Floral Perfume", "desc": "Perfume with floral scent.", "image": "https://images.unsplash.com/photo-1541643600914-78b084683601?w=300&q=80"},
        {"title": "Nail Polish Remover", "desc": "Nail polish remover acetone free.", "image": "https://images.unsplash.com/photo-1632515902636-22a49889ab8a?w=300&q=80"},
        {"title": "Sunscreen SPF 50", "desc": "Sunscreen SPF 50 for sensitive skin.", "image": "https://images.unsplash.com/photo-1556228720-19779b2a1970?w=300&q=80"},
        {"title": "Aloe Vera Lotion", "desc": "Moisturizing body lotion with aloe vera.", "image": "https://images.unsplash.com/photo-1608248597279-f99d160bfbc8?w=300&q=80"},
        {"title": "Exfoliating Scrub", "desc": "Exfoliating face scrub.", "image": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=300&q=80"},
        {"title": "Volumizing Mascara", "desc": "Volumizing mascara.", "image": "https://images.unsplash.com/photo-1631214503851-a596848faf18?w=300&q=80"},
        {"title": "Shea Butter Lip Balm", "desc": "Lip balm with shea butter.", "image": "https://images.unsplash.com/photo-1629198727546-f9a460896404?w=300&q=80"},
        {"title": "Ceramic Straightener", "desc": "Hair straightener ceramic plates.", "image": "https://images.unsplash.com/photo-1561389886-f4040a45c227?w=300&q=80"},
        {"title": "Grooming Beard Oil", "desc": "Beard oil for grooming.", "image": "https://images.unsplash.com/photo-1621607512022-6aecc4fed814?w=300&q=80"},
        {"title": "Pro Brush Set", "desc": "Makeup brush set professional.", "image": "https://images.unsplash.com/photo-1596462502278-27bfdd403348?w=300&q=80"},
        {"title": "Vitamin C Serum", "desc": "Vitamin C serum for face.", "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=300&q=80"},
        {"title": "Charcoal Mask", "desc": "Charcoal face mask.", "image": "https://images.unsplash.com/photo-1596462502278-27bfdd403348?w=300&q=80"},
        {"title": "Hand Cream", "desc": "Hand cream for dry hands.", "image": "https://images.unsplash.com/photo-1608248597279-f99d160bfbc8?w=300&q=80"},
        {"title": "Foot Cream", "desc": "Foot cream for cracked heels.", "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=300&q=80"},
        {"title": "Lavender Bath Salts", "desc": "Bath salts with lavender.", "image": "https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?w=300&q=80"},
        {"title": "Scented Candles", "desc": "Scented candles for relaxation.", "image": "https://images.unsplash.com/photo-1602826347632-fc48a78f853e?w=300&q=80"},
        {"title": "Aroma Diffuser", "desc": "Essential oil diffuser.", "image": "https://images.unsplash.com/photo-1602143407151-011141950038?w=300&q=80"},
        {"title": "Yoga Mat", "desc": "Yoga mat non-slip.", "image": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=300&q=80"},
        {"title": "Dumbbells Set", "desc": "Dumbbells set for home workout.", "image": "https://images.unsplash.com/photo-1638536532686-d610adfc8e5c?w=300&q=80"},
        {"title": "Running Shoes", "desc": "Running shoes for men.", "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&q=80"},
        {"title": "Sports Bra", "desc": "Sports bra high impact.", "image": "https://images.unsplash.com/photo-1571945153237-4929e783af4a?w=300&q=80"},
        {"title": "Steel Water Bottle", "desc": "Water bottle stainless steel.", "image": "https://images.unsplash.com/photo-1602143407151-011141950038?w=300&q=80"},
        {"title": "Whey Protein", "desc": "Protein powder chocolate flavor.", "image": "https://images.unsplash.com/photo-1579722821273-0f6c7d44362f?w=300&q=80"}
    ]
    
    desc_data = []
    for i, pid in enumerate(all_product_ids):
        info = products_info[i % len(products_info)]
        desc = info['desc']
        title = info['title']
        image = info['image']
        
        # Add some random words to make them slightly different if we have more products than descriptions
        if i >= len(products_info):
            desc += " " + ''.join(random.choices(string.ascii_lowercase, k=5))
            
        desc_data.append([pid, title, desc, image])
        
    df_desc = pd.DataFrame(desc_data, columns=['product_uid', 'product_title', 'product_description', 'image_url'])
    df_desc.to_csv('data/product_descriptions.csv', index=False)
    print("product_descriptions.csv created.")

if __name__ == "__main__":
    generate_mock_data()
