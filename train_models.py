import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def train_regression():
    print("Training Linear Regression...")
    try:
        df = pd.read_csv('multiple regression/auto-mpg.csv')
        df['horsepower'] = df['horsepower'].replace('?', np.nan)
        df = df.dropna()
        df['horsepower'] = df['horsepower'].astype(float)
        if 'car name' in df.columns:
            df = df.drop('car name', axis=1)
        
        # Features: cylinders, displacement, horsepower, weight, acceleration, model year, origin
        X = df.drop('mpg', axis=1)
        y = df['mpg']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        if not os.path.exists('models'):
            os.makedirs('models')
            
        joblib.dump(model, 'models/linear_regression.pkl')
        print("Linear Regression Model Saved.")
    except Exception as e:
        print(f"Error training regression: {e}")

def train_naive_bayes():
    print("Training Naive Bayes...")
    try:
        # Check if covid.csv is in root or subfolder. It was created in root.
        df = pd.read_csv('covid.csv')
        
        encoders = {}
        for col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
            
        X = df.drop('infected', axis=1)
        y = df['infected']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = GaussianNB()
        model.fit(X_train, y_train)
        
        if not os.path.exists('models'):
            os.makedirs('models')
            
        joblib.dump(model, 'models/naive_bayes.pkl')
        joblib.dump(encoders, 'models/covid_encoders.pkl')
        print("Naive Bayes Model Saved.")
    except Exception as e:
        print(f"Error training naive bayes: {e}")


def train_kmeans():
    print("Training K-Means...")
    try:
        df = pd.read_csv('multiple regression/auto-mpg.csv')
        df['horsepower'] = df['horsepower'].replace('?', np.nan)
        df = df.dropna()
        df['horsepower'] = df['horsepower'].astype(float)
        
        # Clustering on specific features for visualization potential: Weight & Horsepower
        X = df[['weight', 'horsepower']]
        
        kmeans = KMeans(n_clusters=3, random_state=42)
        kmeans.fit(X)
        
        if not os.path.exists('models'):
            os.makedirs('models')
            
        joblib.dump(kmeans, 'models/kmeans.pkl')
        print("K-Means Model Saved.")
    except Exception as e:
        print(f"Error training kmeans: {e}")

def train_prs():
    print("Training PRS...")
    try:
        # Import here to avoid circular dependency issues if any,
        # though RecommenderSystem is independent usually.
        # Ensure recommender.py is in the same directory.
        from recommender import RecommenderSystem
        
        # Paths to data in the PRS subdirectory
        ratings_path = os.path.join(os.getcwd(), 'PRS/backend/data/ratings_Beauty.csv')
        descriptions_path = os.path.join(os.getcwd(), 'PRS/backend/data/product_descriptions.csv')
        
        recommender = RecommenderSystem(ratings_path, descriptions_path)
        
        if not os.path.exists('models'):
            os.makedirs('models')
            
        # We pickle the entire object which contains the matrices/models
        joblib.dump(recommender, 'models/recommender.pkl')
        print("PRS Model Saved.")
    except Exception as e:
        print(f"Error training PRS: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    train_regression()
    train_naive_bayes()
    train_kmeans()
    train_prs()
