# 🎬 Distributed Movie Recommendation Microservice System

A distributed machine learning-based movie recommendation system built with Python and Flask, demonstrating microservices architecture, RESTful APIs, and basic ML using TF-IDF vectorization and cosine similarity.

## 🎯 System Overview

This project consists of two independent Flask microservices that communicate over HTTP:

1. **User Service** (Port 5000) - Frontend API that accepts user requests
2. **Recommender Service** (Port 5001) - ML-powered recommendation engine

## 🧩 Architecture

```
User Request → User Service (Port 5000)
                    ↓ HTTP Request
              Recommender Service (Port 5001)
                    ↓ ML Processing (TF-IDF + Cosine Similarity)
              Top 5 Recommendations
                    ↓ JSON Response
              User Service → User
```

## 📁 Project Structure

```
movie-recommendation-system/
│
├── user_service/
│   ├── app.py              # User-facing Flask API
│   ├── requirements.txt    # Dependencies
│
├── recommender_service/
│   ├── app.py              # Recommender Flask API
│   ├── recommender.py      # ML recommendation engine
│   ├── movies.csv          # Movie dataset
│   ├── requirements.txt    # Dependencies
│
└── README.md               # This file
```

## ⚙️ Tech Stack

- **Language**: Python 3
- **Framework**: Flask
- **ML Libraries**: scikit-learn (TF-IDF, Cosine Similarity)
- **Data Processing**: pandas, numpy
- **HTTP Client**: requests

## 🚀 Setup & Installation

### Prerequisites

- Python 3.8+
- pip package manager

### Installation Steps

1. **Clone or navigate to the project directory**

   ```bash
   cd movie-recommendation-system
   ```

2. **Install User Service dependencies**

   ```bash
   cd user_service
   pip install -r requirements.txt
   cd ..
   ```

3. **Install Recommender Service dependencies**
   ```bash
   cd recommender_service
   pip install -r requirements.txt
   cd ..
   ```

## 🏃 Running the System

You need to run both services in separate terminal windows:

### Terminal 1: Start Recommender Service (Port 5001)

```bash
cd recommender_service
python app.py
```

You should see:

```
Loading movie dataset and computing similarity matrix...
Similarity matrix computed successfully!
 * Running on http://127.0.0.1:5001
```

### Terminal 2: Start User Service (Port 5000)

```bash
cd user_service
python app.py
```

You should see:

```
 * Running on http://127.0.0.1:5000
```

## 📡 API Usage

### Get Movie Recommendations

**Endpoint**: `GET /recommend/<movie_name>`

**Example Request**:

```bash
curl http://localhost:5000/recommend/Toy%20Story
```

**Example Response**:

```json
{
  "movie": "Toy Story",
  "recommendations": [
    "A Bug's Life",
    "Monsters, Inc.",
    "Finding Nemo",
    "The Incredibles",
    "Cars"
  ]
}
```

### Error Handling

**Movie Not Found**:

```json
{
  "error": "Movie 'Unknown Movie' not found in database"
}
```

**Service Unavailable**:

```json
{
  "error": "Recommender service is currently unavailable"
}
```

## 🧠 How It Works

### 1. User Service

- Accepts HTTP GET requests with a movie name
- Forwards the request to the Recommender Service via HTTP
- Returns the recommendation results to the user
- Handles errors gracefully

### 2. Recommender Service

- **Loads Dataset**: Reads `movies.csv` on startup
- **TF-IDF Vectorization**: Converts movie genres into numerical vectors
- **Cosine Similarity**: Computes similarity between all movies (precomputed for efficiency)
- **Recommendation**: Returns top 5 most similar movies based on genre similarity
- **Caching**: Similarity matrix is computed once at startup for fast responses

### ML Pipeline

1. Extract movie genres from the dataset
2. Apply TF-IDF (Term Frequency-Inverse Document Frequency) vectorization
3. Compute pairwise cosine similarity matrix
4. For a given movie, find the 5 most similar movies
5. Return recommendations excluding the input movie itself

## 📊 Dataset

The system includes a sample dataset (`movies.csv`) with 15 popular movies:

- Toy Story
- The Matrix
- Inception
- The Dark Knight
- Pulp Fiction
- And more...

Each movie has:

- `movieId`: Unique identifier
- `title`: Movie name
- `genres`: Pipe-separated genres (e.g., "Adventure|Animation|Children")

## 🔧 Customization

### Adding More Movies

Edit `recommender_service/movies.csv` and add new entries:

```csv
16,Your Movie,Action|Sci-Fi
```

Restart the Recommender Service to reload the dataset.

### Changing Ports

- User Service: Edit `user_service/app.py`, change `port=5000`
- Recommender Service: Edit `recommender_service/app.py`, change `port=5001`
- Also update the RECOMMENDER_URL in `user_service/app.py`

## 💻 System Requirements

- **OS**: macOS , also works on Linux/Windows
- **RAM**: ~200MB (very lightweight)
- **CPU**: No GPU required, runs efficiently on any modern CPU
- **Disk**: <10MB

## 🧪 Testing

Test individual services:

```bash
# Test Recommender Service directly
curl http://localhost:5001/recommend/Inception

# Test User Service (which calls Recommender Service)
curl http://localhost:5000/recommend/The%20Matrix
```

## 🎓 Learning Outcomes

This project demonstrates:

- ✅ Microservices architecture
- ✅ RESTful API design
- ✅ Inter-service communication over HTTP
- ✅ Machine Learning (TF-IDF, Cosine Similarity)
- ✅ Distributed systems basics
- ✅ Error handling and fault tolerance
- ✅ Efficient ML preprocessing and caching

## 📝 License

This is a learning project - feel free to use and modify as needed!

## 🤝 Contributing

Feel free to enhance this project by:

- Adding more sophisticated ML models
- Implementing user ratings-based collaborative filtering
- Adding a web UI
- Implementing service discovery
- Adding containerization (Docker)

---

**Happy Coding! 🚀**
