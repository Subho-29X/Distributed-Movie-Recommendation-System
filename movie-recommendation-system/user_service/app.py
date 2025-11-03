"""
User Service - Flask Microservice
Port: 5000

This service acts as the user-facing API that accepts movie recommendation requests
and forwards them to the Recommender Service.
"""

from flask import Flask, jsonify
import requests
from urllib.parse import quote

app = Flask(__name__)

# URL of the Recommender Service
RECOMMENDER_URL = "http://127.0.0.1:5001"


@app.route('/')
def home():
    """Home endpoint with API documentation."""
    return jsonify({
        "service": "User Service - Movie Recommendation System",
        "version": "1.0",
        "endpoints": {
            "/": "API documentation",
            "/recommend/<movie_name>": "Get movie recommendations"
        },
        "example": "GET /recommend/Toy%20Story"
    })


@app.route('/recommend/<movie_name>', methods=['GET'])
def recommend(movie_name):
    """
    Accept a movie name and request recommendations from the Recommender Service.
    
    Args:
        movie_name (str): Name of the movie to get recommendations for
        
    Returns:
        JSON response with recommendations or error message
    """
    try:
        # URL encode the movie name for the HTTP request
        encoded_movie = quote(movie_name)
        
        # Make HTTP request to Recommender Service
        print(f"[User Service] Requesting recommendations for: {movie_name}")
        print(f"[User Service] Calling Recommender Service at: {RECOMMENDER_URL}/recommend/{encoded_movie}")
        
        response = requests.get(
            f"{RECOMMENDER_URL}/recommend/{encoded_movie}",
            timeout=5  # 5 second timeout
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            recommendations = response.json()
            print(f"[User Service] Successfully received recommendations")
            return jsonify(recommendations), 200
        elif response.status_code == 404:
            # Movie not found
            error_data = response.json()
            print(f"[User Service] Movie not found: {movie_name}")
            return jsonify(error_data), 404
        else:
            # Other errors from recommender service
            print(f"[User Service] Recommender service error: {response.status_code}")
            return jsonify({
                "error": "Error from recommender service",
                "status_code": response.status_code
            }), 500
            
    except requests.exceptions.ConnectionError:
        print("[User Service] ERROR: Cannot connect to Recommender Service")
        return jsonify({
            "error": "Recommender service is currently unavailable",
            "message": "Please ensure the Recommender Service is running on port 5001"
        }), 503
        
    except requests.exceptions.Timeout:
        print("[User Service] ERROR: Request to Recommender Service timed out")
        return jsonify({
            "error": "Request timeout",
            "message": "The recommender service took too long to respond"
        }), 504
        
    except Exception as e:
        print(f"[User Service] ERROR: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "User Service",
        "port": 5000
    }), 200


if __name__ == '__main__':
    print("=" * 60)
    print("🎬 User Service Starting...")
    print("=" * 60)
    print("Port: 5002")
    print("Endpoints:")
    print("  - GET /recommend/<movie_name>")
    print("  - GET /health")
    print("\nExample usage:")
    print("  curl http://localhost:5002/recommend/Toy%20Story")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5002, debug=True)
