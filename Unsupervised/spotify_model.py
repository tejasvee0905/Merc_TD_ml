"""
Spotify Song Recommendation Model
Uses K-means clustering to recommend similar songs
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy.spatial.distance import euclidean
import pickle
import os


class SpotifyRecommender:
    def __init__(self, data_path='spotify_tracks.csv'):
        """Initialize the recommender with data path"""
        self.data_path = data_path
        self.df = None
        self.scaler = None
        self.kmeans = None
        self.features = ['danceability', 'energy', 'valence', 'tempo', 'duration_ms', 'popularity']
        self.optimal_k = 5
        
    def load_and_prepare_data(self):
        """Load and prepare the data"""
        self.df = pd.read_csv(self.data_path)
        print(f"Loaded {len(self.df)} songs from dataset")
        
        # Select features for clustering
        X = self.df[self.features]
        
        # Standardize the features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Build K-means model
        self.kmeans = KMeans(n_clusters=self.optimal_k, random_state=42, n_init=10)
        self.df['cluster'] = self.kmeans.fit_predict(X_scaled)
        
        print(f"K-means clustering completed with {self.optimal_k} clusters")
        print(f"Cluster distribution:\n{self.df['cluster'].value_counts().sort_index()}")
        
    def recommend_songs(self, song_name, n_recommendations=10):
        """
        Recommend songs similar to the given song
        
        Parameters:
        - song_name: Name of the song to find recommendations for
        - n_recommendations: Number of recommendations to return
        
        Returns:
        - DataFrame with recommended songs
        """
        # Find the song in the dataset (case-insensitive)
        song_data = self.df[self.df['track_name'].str.lower() == song_name.lower()]
        
        if song_data.empty:
            return None, f"Song '{song_name}' not found in the dataset."
        
        # Get the cluster of the input song
        song_cluster = song_data['cluster'].values[0]
        
        # Get all songs from the same cluster
        cluster_songs = self.df[self.df['cluster'] == song_cluster].copy()
        
        # Calculate similarity (Euclidean distance) to the input song
        song_features = song_data[self.features].values[0]
        
        # Calculate distances
        cluster_songs['distance'] = cluster_songs[self.features].apply(
            lambda row: euclidean(row, song_features), axis=1
        )
        
        # Sort by distance and exclude the input song
        recommendations = cluster_songs[cluster_songs['track_name'] != song_data['track_name'].values[0]]
        recommendations = recommendations.sort_values('distance').head(n_recommendations)
        
        # Get song info
        song_info = {
            'track_name': song_data['track_name'].values[0],
            'artist': song_data['artist'].values[0],
            'genre': song_data['genre'].values[0],
            'cluster': int(song_cluster),
            'popularity': int(song_data['popularity'].values[0])
        }
        
        return recommendations[['track_name', 'artist', 'genre', 'playlist_category', 'popularity', 'distance']], song_info
    
    def get_all_songs(self):
        """Get all songs in the dataset"""
        return self.df[['track_name', 'artist', 'genre']].sort_values('track_name')
    
    def get_random_song(self):
        """Get a random song from the dataset"""
        return self.df.sample(1)['track_name'].values[0]
    
    def save_model(self, model_path='spotify_recommender_model.pkl'):
        """Save the trained model"""
        model_data = {
            'scaler': self.scaler,
            'kmeans': self.kmeans,
            'df': self.df,
            'features': self.features,
            'optimal_k': self.optimal_k
        }
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path='spotify_recommender_model.pkl'):
        """Load a saved model"""
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.scaler = model_data['scaler']
        self.kmeans = model_data['kmeans']
        self.df = model_data['df']
        self.features = model_data['features']
        self.optimal_k = model_data['optimal_k']
        print(f"Model loaded from {model_path}")


# Initialize and train the model if run directly
if __name__ == "__main__":
    recommender = SpotifyRecommender()
    recommender.load_and_prepare_data()
    recommender.save_model()
    
    # Test the recommender
    print("\n" + "="*80)
    print("Testing recommendation system...")
    print("="*80)
    
    # Get a random song
    test_song = recommender.get_random_song()
    print(f"\nGetting recommendations for: {test_song}")
    
    recommendations, song_info = recommender.recommend_songs(test_song, n_recommendations=5)
    
    if recommendations is not None:
        print(f"\nSong Info: {song_info}")
        print("\nTop 5 Recommendations:")
        print(recommendations.to_string())
