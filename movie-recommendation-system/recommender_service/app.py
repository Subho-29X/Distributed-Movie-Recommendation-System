"""
Recommender Service - Flask Microservice
Port: 5001

This service provides the ML-powered movie recommendation engine.
It uses TF-IDF vectorization and cosine similarity to find similar movies.
"""

from flask import Flask, jsonify, request
from recommender import MovieRecommender
from urllib.parse import unquote

app = Flask(__name__)

# Initialize the recommender (this will precompute the similarity matrix)
print("=" * 60)
print("Initializing Recommender Service...")
print("=" * 60)
recommender = MovieRecommender('movies.csv')
print("=" * 60)
print("Recommender Service Ready!")
print("=" * 60)


@app.route('/')
def home():
    """Home endpoint with API documentation."""
    return jsonify({
        "service": "Recommender Service - ML-Powered Movie Recommendations",
        "version": "1.0",
        "ml_method": "TF-IDF + Cosine Similarity",
        "total_movies": len(recommender.get_all_movies()),
        "endpoints": {
            "/": "API documentation",
            "/recommend/<movie_name>": "Get movie recommendations",
            "/movies": "List all available movies",
            "/movie/<movie_name>": "Get movie details"
        },
        "example": "GET /recommend/Toy%20Story"
    })


@app.route('/recommend/<movie_name>', methods=['GET'])
def recommend(movie_name):
    """
    Generate movie recommendations based on similarity.
    
    Args:
        movie_name (str): Name of the movie to get recommendations for
        
    Returns:
        JSON response with top 5 recommendations
    """
    try:
        # URL decode the movie name
        movie_name = unquote(movie_name)
        
        print(f"[Recommender Service] Processing recommendation request for: {movie_name}")
        
        # Get recommendations from the ML engine
        result = recommender.get_recommendations(movie_name, top_n=5)
        
        print(f"[Recommender Service] Successfully generated recommendations")
        
        return jsonify(result), 200
        
    except ValueError as e:
        # Movie not found
        print(f"[Recommender Service] ERROR: {str(e)}")
        return jsonify({
            "error": str(e),
            "available_movies": recommender.get_all_movies()
        }), 404
        
    except Exception as e:
        print(f"[Recommender Service] ERROR: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500


@app.route('/movies', methods=['GET'])
def list_movies():
    """Get a list of all available movies."""
    try:
        movies = recommender.get_all_movies()
        return jsonify({
            "total_movies": len(movies),
            "movies": movies
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Failed to retrieve movies",
            "message": str(e)
        }), 500


@app.route('/movie/<movie_name>', methods=['GET'])
def get_movie(movie_name):
    """Get detailed information about a specific movie."""
    try:
        movie_name = unquote(movie_name)
        movie_info = recommender.get_movie_info(movie_name)
        return jsonify(movie_info), 200
    except ValueError as e:
        return jsonify({
            "error": str(e),
            "available_movies": recommender.get_all_movies()
        }), 404
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Recommender Service",
        "port": 5001,
        "ml_engine": "active",
        "total_movies": len(recommender.get_all_movies())
    }), 200


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🧠 Recommender Service Starting...")
    print("=" * 60)
    print("Port: 5001")
    print("ML Method: TF-IDF + Cosine Similarity")
    print(f"Total Movies: {len(recommender.get_all_movies())}")
    print("\nEndpoints:")
    print("  - GET /recommend/<movie_name>")
    print("  - GET /movies")
    print("  - GET /movie/<movie_name>")
    print("  - GET /health")
    print("\nExample usage:")
    print("  curl http://localhost:5001/recommend/Toy%20Story")
    print("=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
