from flask import Flask, jsonify, request, render_template
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Configuration
RECOMMENDER_SERVICE_URL = 'http://localhost:5003'


@app.route('/')
def home():
    """Serve the web UI"""
    return render_template('index.html')


@app.route('/recommend/<movie_name>', methods=['GET'])
def recommend(movie_name):
    """
    Get movie recommendations by calling the recommender service
    """
    try:
        # Validate input
        if not movie_name or movie_name.strip() == "":
            return jsonify({
                'error': 'Invalid movie name',
                'message': 'Movie name cannot be empty'
            }), 400
        
        # Call recommender service
        app.logger.info(f"Requesting recommendations for: {movie_name}")
        
        try:
            response = requests.get(
                f"{RECOMMENDER_SERVICE_URL}/recommend/{movie_name}",
                timeout=5
            )
            
            # Forward the response from recommender service
            return jsonify(response.json()), response.status_code
            
        except requests.exceptions.ConnectionError:
            app.logger.error("Recommender service is offline")
            return jsonify({
                'error': 'Service unavailable',
                'message': 'Recommender service is currently offline',
                'suggestion': 'Please ensure the recommender service is running on port 5001'
            }), 503
            
        except requests.exceptions.Timeout:
            app.logger.error("Request to recommender service timed out")
            return jsonify({
                'error': 'Request timeout',
                'message': 'Recommender service took too long to respond'
            }), 504
            
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred while processing your request'
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        # Check if recommender service is available
        response = requests.get(f"{RECOMMENDER_SERVICE_URL}/health", timeout=2)
        recommender_healthy = response.status_code == 200
    except:
        recommender_healthy = False
    
    return jsonify({
        'status': 'healthy',
        'service': 'user_service',
        'recommender_service_status': 'up' if recommender_healthy else 'down'
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)
