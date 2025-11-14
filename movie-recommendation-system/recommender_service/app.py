from flask import Flask, jsonify, request
from recommender import load_dataset, build_similarity_matrix, get_recommendations
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Precompute similarity matrix at startup
try:
    movies_df = load_dataset()
    similarity_matrix = build_similarity_matrix(movies_df)
    app.logger.info("Similarity matrix built successfully")
except Exception as e:
    app.logger.error(f"Error during initialization: {str(e)}")
    movies_df = None
    similarity_matrix = None


@app.route('/recommend/<movie_name>', methods=['GET'])
def recommend(movie_name):
    """
    Get movie recommendations based on similarity
    """
    try:
        # Validate input
        if not movie_name or movie_name.strip() == "":
            return jsonify({
                'error': 'Invalid movie name',
                'message': 'Movie name cannot be empty'
            }), 400
        
        # Check if data is loaded
        if movies_df is None or similarity_matrix is None:
            return jsonify({
                'error': 'Service initialization error',
                'message': 'Recommendation system not properly initialized'
            }), 500
        
        # Get recommendations
        recommendations = get_recommendations(movie_name, movies_df, similarity_matrix)
        
        if recommendations is None:
            return jsonify({
                'error': 'Movie not found',
                'message': f'The movie "{movie_name}" was not found in our database',
                'suggestion': 'Please check the movie name and try again'
            }), 404
        
        return jsonify({
            'input_movie': movie_name,
            'recommendations': recommendations
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred while processing your request'
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'recommender_service',
        'movies_loaded': len(movies_df) if movies_df is not None else 0
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=False)
