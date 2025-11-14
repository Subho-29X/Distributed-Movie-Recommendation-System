<!-- <<<<<<< HEAD:README.md -->

# 🎬 Distributed Movie Recommendation Microservice System

<!-- =======

# Distributed Movie Recommendation System -->

<!-- >>>>>>> dbbd4ed (Revamp):movie-recommendation-system/README.md -->

A lightweight microservices-based movie recommendation system built with Python and Flask. The system uses TF-IDF vectorization and cosine similarity to recommend movies based on genre similarities.

## Overview

This project demonstrates a simple distributed architecture where two independent services communicate via HTTP APIs:

- **User Service**: Acts as the API gateway, handling user requests
- **Recommender Service**: Contains the ML logic for generating recommendations

## Architecture

```
┌─────────────┐         HTTP Request          ┌──────────────────────┐
│             │ ──────────────────────────────>│                      │
│   User      │         Port 5000              │   User Service       │
│             │ <──────────────────────────────│   (API Gateway)      │
└─────────────┘         JSON Response          └──────────────────────┘
                                                          │
                                                          │ HTTP
                                                          │
                                                          ▼
                                                ┌──────────────────────┐
                                                │                      │
                                                │  Recommender Service │
                                                │  (ML Engine)         │
                                                │  Port 5001           │
                                                └──────────────────────┘
                                                          │
                                                          │
                                                          ▼
                                                    ┌──────────┐
                                                    │ movies.csv│
                                                    └──────────┘
```

## Tech Stack

- **Python 3.x**: Programming language
- **Flask**: Web framework for building REST APIs
- **Pandas**: Data manipulation and CSV handling
- **Scikit-learn**: TF-IDF vectorization and cosine similarity
- **Requests**: HTTP client for inter-service communication

## Folder Structure

```
movie-recommendation-system/
│
├── user_service/
│   ├── app.py                    # User-facing API (Port 5000)
│   └── requirements.txt
│
├── recommender_service/
│   ├── app.py                    # Recommendation API (Port 5001)
│   ├── recommender.py            # ML logic
│   ├── movies.csv                # Movie dataset
│   └── requirements.txt
│
└── README.md
```

## Setup Instructions

### 1. Install Dependencies

Open two terminal windows/tabs.

**Terminal 1 - Recommender Service:**

```bash
cd recommender_service
pip install -r requirements.txt
```

**Terminal 2 - User Service:**

```bash
cd user_service
pip install -r requirements.txt
```

### 2. Start the Services

**Important**: Start the recommender service first!

**Terminal 1:**

```bash
cd recommender_service
python app.py
```

_Output: Service running on http://localhost:5001_

**Terminal 2:**

```bash
cd user_service
python app.py
```

_Output: Service running on http://localhost:5000_

## Usage

### Example Request

```bash
curl http://localhost:5000/recommend/Inception
```

### Example Response

```json
{
  "input_movie": "Inception",
  "recommendations": [
    "The Matrix",
    "Interstellar",
    "Avatar",
    "Jurassic Park",
    "The Dark Knight"
  ]
}
```

### Try More Movies

```bash
curl http://localhost:5000/recommend/Toy%20Story
curl http://localhost:5000/recommend/The%20Matrix
curl http://localhost:5000/recommend/Titanic
```

### Health Check

```bash
curl http://localhost:5000/health
curl http://localhost:5001/health
```

## Error Handling

The system handles multiple error scenarios:

### 1. Movie Not Found

```bash
curl http://localhost:5000/recommend/InvalidMovie
```

**Response (404):**

```json
{
  "error": "Movie not found",
  "message": "The movie \"InvalidMovie\" was not found in our database",
  "suggestion": "Please check the movie name and try again"
}
```

### 2. Recommender Service Offline

If recommender service is not running:
**Response (503):**

```json
{
  "error": "Service unavailable",
  "message": "Recommender service is currently offline",
  "suggestion": "Please ensure the recommender service is running on port 5001"
}
```

### 3. Invalid Input

```bash
curl http://localhost:5000/recommend/
```

**Response (400):**

```json
{
  "error": "Invalid movie name",
  "message": "Movie name cannot be empty"
}
```

## How It Works

### Recommender Service

1. **Startup**: Loads `movies.csv` and precomputes the similarity matrix using TF-IDF on genres
2. **TF-IDF Vectorization**: Converts genre strings (e.g., "Action|Sci-Fi") into numerical vectors
3. **Cosine Similarity**: Computes similarity scores between all movie pairs
4. **Recommendation**: Returns top 5 most similar movies based on precomputed scores

### User Service

1. Receives user requests on port 5000
2. Forwards requests to recommender service on port 5001
3. Returns formatted responses to the user
4. Handles timeouts and connection errors gracefully

## Learning Outcomes

This project demonstrates:

✅ **Microservices Architecture**: Separation of concerns between services  
✅ **REST API Design**: Clean endpoint design with proper HTTP methods  
✅ **Error Handling**: Comprehensive error responses with meaningful messages  
✅ **Machine Learning**: TF-IDF vectorization and cosine similarity  
✅ **Inter-Service Communication**: HTTP-based service-to-service calls  
✅ **Data Processing**: Using Pandas for CSV operations  
✅ **Service Independence**: Each service can be developed and deployed independently

## Dataset

The system includes 15 movies across various genres:

- Action, Sci-Fi: The Matrix, Inception, Avatar, Jurassic Park
- Animation: Toy Story, The Lion King, Finding Nemo
- Drama: The Godfather, Forrest Gump, The Shawshank Redemption
- And more...

## Extending the System

To add more movies, simply edit `recommender_service/movies.csv`:

```csv
movieId,title,genres
16,Your Movie,Action|Drama|Thriller
```

Restart the recommender service to reload the dataset.

---

**Built with ❤️ using Python and Flask**
