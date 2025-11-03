"""
Movie Recommender Engine

This module implements a content-based movie recommendation system using:
- TF-IDF (Term Frequency-Inverse Document Frequency) vectorization
- Cosine Similarity for finding similar movies based on genres

The similarity matrix is precomputed for efficiency.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    """
    A content-based movie recommendation engine using TF-IDF and cosine similarity.
    """
    
    def __init__(self, csv_path='movies.csv'):
        """
        Initialize the recommender system.
        
        Args:
            csv_path (str): Path to the movies CSV file
        """
        self.csv_path = csv_path
        self.movies_df = None
        self.tfidf_matrix = None
        self.cosine_sim = None
        self.movie_indices = None
        
        # Load data and compute similarity matrix
        self._load_data()
        self._compute_similarity()
    
    def _load_data(self):
        """Load the movie dataset from CSV."""
        print(f"Loading dataset from: {self.csv_path}")
        self.movies_df = pd.read_csv(self.csv_path)
        
        # Create a clean version of genres (replace | with spaces for better TF-IDF)
        self.movies_df['genres_clean'] = self.movies_df['genres'].str.replace('|', ' ')
        
        # Create a mapping of movie titles to indices
        self.movie_indices = pd.Series(
            self.movies_df.index,
            index=self.movies_df['title']
        ).to_dict()
        
        print(f"Loaded {len(self.movies_df)} movies")
        print(f"Columns: {list(self.movies_df.columns)}")
    
    def _compute_similarity(self):
        """
        Compute TF-IDF matrix and cosine similarity matrix.
        This is done once at initialization for efficiency (simulates "pretraining").
        """
        print("Computing TF-IDF vectors...")
        
        # Initialize TF-IDF Vectorizer
        tfidf = TfidfVectorizer(
            stop_words='english',
            lowercase=True,
            analyzer='word'
        )
        
        # Compute TF-IDF matrix on movie genres
        self.tfidf_matrix = tfidf.fit_transform(self.movies_df['genres_clean'])
        
        print(f"TF-IDF matrix shape: {self.tfidf_matrix.shape}")
        print("Computing cosine similarity matrix...")
        
        # Compute pairwise cosine similarity
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        
        print(f"Cosine similarity matrix shape: {self.cosine_sim.shape}")
        print("Similarity matrix computed successfully!")
    
    def get_recommendations(self, movie_title, top_n=5):
        """
        Get top N movie recommendations based on similarity.
        
        Args:
            movie_title (str): Title of the movie to get recommendations for
            top_n (int): Number of recommendations to return (default: 5)
            
        Returns:
            dict: Dictionary containing the movie and its recommendations
            
        Raises:
            ValueError: If the movie is not found in the database
        """
        # Check if movie exists
        if movie_title not in self.movie_indices:
            raise ValueError(f"Movie '{movie_title}' not found in database")
        
        # Get the index of the movie
        idx = self.movie_indices[movie_title]
        
        # Get similarity scores for this movie with all other movies
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        
        # Sort movies by similarity score (descending)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top N similar movies (excluding the movie itself at index 0)
        sim_scores = sim_scores[1:top_n+1]
        
        # Get movie indices
        movie_indices_list = [i[0] for i in sim_scores]
        
        # Get movie titles
        recommendations = self.movies_df['title'].iloc[movie_indices_list].tolist()
        
        # Get similarity scores
        scores = [round(i[1], 4) for i in sim_scores]
        
        print(f"Generated {len(recommendations)} recommendations for '{movie_title}'")
        
        return {
            'movie': movie_title,
            'recommendations': recommendations,
            'similarity_scores': scores
        }
    
    def get_all_movies(self):
        """
        Get a list of all available movies.
        
        Returns:
            list: List of all movie titles
        """
        return self.movies_df['title'].tolist()
    
    def get_movie_info(self, movie_title):
        """
        Get detailed information about a movie.
        
        Args:
            movie_title (str): Title of the movie
            
        Returns:
            dict: Movie information including title, genres, etc.
            
        Raises:
            ValueError: If the movie is not found
        """
        if movie_title not in self.movie_indices:
            raise ValueError(f"Movie '{movie_title}' not found in database")
        
        idx = self.movie_indices[movie_title]
        movie = self.movies_df.iloc[idx]
        
        return {
            'movieId': int(movie['movieId']),
            'title': movie['title'],
            'genres': movie['genres']
        }


# For testing the recommender directly
if __name__ == '__main__':
    print("=" * 60)
    print("Testing Movie Recommender Engine")
    print("=" * 60)
    
    # Initialize recommender
    recommender = MovieRecommender()
    
    # Test with a few movies
    test_movies = ['Toy Story', 'The Matrix', 'Inception']
    
    for movie in test_movies:
        print(f"\n📽️  Recommendations for '{movie}':")
        print("-" * 60)
        try:
            result = recommender.get_recommendations(movie)
            for i, rec in enumerate(result['recommendations'], 1):
                score = result['similarity_scores'][i-1]
                print(f"{i}. {rec} (similarity: {score})")
        except ValueError as e:
            print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print(f"Total movies in database: {len(recommender.get_all_movies())}")
    print("=" * 60)
