import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os


def load_dataset():
    """
    Load the movies dataset from CSV file
    
    Returns:
        DataFrame: Movies dataframe with movieId, title, and genres
    """
    csv_path = os.path.join(os.path.dirname(__file__), 'movies.csv')
    df = pd.read_csv(csv_path)
    return df


def build_similarity_matrix(movies_df):
    """
    Build cosine similarity matrix based on movie genres using TF-IDF
    
    Args:
        movies_df (DataFrame): Movies dataframe
        
    Returns:
        numpy.ndarray: Cosine similarity matrix
    """
    # Create TF-IDF vectorizer
    tfidf = TfidfVectorizer(token_pattern=r'[^|]+')
    
    # Fit and transform genres
    tfidf_matrix = tfidf.fit_transform(movies_df['genres'])
    
    # Compute cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    return similarity_matrix


def get_recommendations(movie_name, movies_df, similarity_matrix, top_n=5):
    """
    Get top N movie recommendations based on similarity
    
    Args:
        movie_name (str): Name of the movie
        movies_df (DataFrame): Movies dataframe
        similarity_matrix (numpy.ndarray): Precomputed similarity matrix
        top_n (int): Number of recommendations to return
        
    Returns:
        list: List of recommended movie titles, or None if movie not found
    """
    # Find movie index (case-insensitive search)
    movie_indices = movies_df[movies_df['title'].str.lower() == movie_name.lower()].index
    
    if len(movie_indices) == 0:
        return None
    
    movie_idx = movie_indices[0]
    
    # Get similarity scores for this movie
    similarity_scores = list(enumerate(similarity_matrix[movie_idx]))
    
    # Sort by similarity score (descending)
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    # Get top N+1 (excluding the movie itself)
    top_indices = [i[0] for i in similarity_scores[1:top_n+1]]
    
    # Get movie titles
    recommendations = movies_df.iloc[top_indices]['title'].tolist()
    
    return recommendations
