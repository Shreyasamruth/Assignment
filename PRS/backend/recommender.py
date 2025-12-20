import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

class RecommenderSystem:
    def __init__(self, ratings_path, descriptions_path):
        self.ratings_path = ratings_path
        self.descriptions_path = descriptions_path
        self.load_data()
        self.train_models()

    def load_data(self):
        # Load Ratings
        try:
            self.ratings = pd.read_csv(self.ratings_path)
            self.ratings = self.ratings.dropna()
        except Exception as e:
            print(f"Error loading ratings: {e}")
            self.ratings = pd.DataFrame()

        # Load Descriptions
        try:
            self.descriptions = pd.read_csv(self.descriptions_path)
            self.descriptions = self.descriptions.dropna()
        except Exception as e:
            print(f"Error loading descriptions: {e}")
            self.descriptions = pd.DataFrame()

    def train_models(self):
        # 1. Popularity Model
        if not self.ratings.empty:
            popular_products = pd.DataFrame(self.ratings.groupby('ProductId')['Rating'].count())
            self.most_popular = popular_products.sort_values('Rating', ascending=False)
        else:
            self.most_popular = pd.DataFrame()

        # 2. Collaborative Filtering (Item-Item)
        if not self.ratings.empty:
            # Use a subset if data is too large, similar to notebook
            ratings_subset = self.ratings.head(10000) 
            self.utility_matrix = ratings_subset.pivot_table(values='Rating', index='UserId', columns='ProductId', fill_value=0)
            self.X = self.utility_matrix.T
            
            # SVD
            n_components = min(10, self.X.shape[1] - 1) if self.X.shape[1] > 1 else 1
            self.svd = TruncatedSVD(n_components=n_components)
            decomposed_matrix = self.svd.fit_transform(self.X)
            self.correlation_matrix = np.corrcoef(decomposed_matrix)
            self.product_ids_collab = list(self.X.index)
        else:
            self.correlation_matrix = None
            self.product_ids_collab = []

        # 3. Content Based
        if not self.descriptions.empty:
            self.vectorizer = TfidfVectorizer(stop_words='english')
            self.tfidf_matrix = self.vectorizer.fit_transform(self.descriptions["product_description"])
            
            # KMeans
            true_k = 10
            self.kmeans = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
            self.kmeans.fit(self.tfidf_matrix)
            self.order_centroids = self.kmeans.cluster_centers_.argsort()[:, ::-1]
            self.terms = self.vectorizer.get_feature_names_out()
        else:
            self.kmeans = None

    def get_popular_products(self, n=10):
        if self.most_popular.empty:
            return []
        return self.most_popular.head(n).index.tolist()

    def get_collaborative_recommendations(self, product_id, n=10):
        if self.correlation_matrix is None:
            return []
        
        try:
            idx = self.product_ids_collab.index(product_id)
            correlation_product_ID = self.correlation_matrix[idx]
            
            # Get indices where correlation > 0.90 (or just top n)
            # The notebook uses > 0.90. Let's sort and take top N for robustness
            # recommend = list(self.X.index[correlation_product_ID > 0.90])
            
            # Let's use sorting to guarantee N results if possible
            sorted_indices = correlation_product_ID.argsort()[::-1]
            recommend = []
            for i in sorted_indices:
                if len(recommend) >= n:
                    break
                pid = self.product_ids_collab[i]
                if pid != product_id:
                    recommend.append(pid)
            
            return recommend
        except ValueError:
            return [] # Product not found in utility matrix

    def get_content_based_recommendations(self, query):
        if self.kmeans is None:
            return []
        
        Y = self.vectorizer.transform([query])
        prediction = self.kmeans.predict(Y)
        cluster_id = prediction[0]
        
        # Get products in this cluster
        # The notebook prints top terms. To return products, we need to find which products belong to this cluster.
        # We can predict cluster for all products or just filter.
        # For efficiency in this demo, let's just return top terms or find products that map to this cluster.
        
        # Better approach for "products": Find products whose description is in this cluster.
        # We can predict for all descriptions (done implicitly during fit if we stored labels, but we re-predict to be safe or use labels_)
        labels = self.kmeans.labels_
        
        # Get indices of products in this cluster
        cluster_indices = [i for i, x in enumerate(labels) if x == cluster_id]
        
        # Return product UIDs
        recommended_products = self.descriptions.iloc[cluster_indices]['product_uid'].tolist()
        return recommended_products[:10] # Return top 10

