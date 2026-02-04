# Spotify Song Recommendation System

This project implements a Spotify song recommendation system using K-means clustering. It provides two user interfaces: **Streamlit** and **FastAPI**.

## 📁 Files Created

- `spotify_model.py` - Core recommendation model using K-means clustering
- `streamlit_app.py` - Streamlit web interface
- `fastapi_app.py` - FastAPI REST API with interactive UI
- `templates/index.html` - HTML frontend for FastAPI

## 🚀 Setup

### Install Dependencies

```bash
pip install pandas numpy scikit-learn scipy streamlit fastapi uvicorn jinja2 python-multipart
```

## 🎵 Usage

### Option 1: Run Streamlit App

```bash
streamlit run streamlit_app.py
```

The Streamlit app will open in your browser at `http://localhost:8501`

**Features:**
- Search songs by name
- Pick from dropdown
- Get random song recommendations
- Interactive visualizations
- Download recommendations as CSV

### Option 2: Run FastAPI App

```bash
python fastapi_app.py
```

Or using uvicorn directly:

```bash
uvicorn fastapi_app:app --reload
```

Access the application:
- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

**API Endpoints:**
- `GET /` - Web interface
- `POST /api/recommend` - Get recommendations
- `GET /api/recommend/{song_name}` - Get recommendations (GET method)
- `GET /api/songs` - Get all songs
- `GET /api/songs/random` - Get random song
- `GET /api/search/{query}` - Search songs
- `GET /api/stats` - Get statistics
- `GET /health` - Health check

### Option 3: Use the Model Directly

```python
from spotify_model import SpotifyRecommender

# Initialize recommender
recommender = SpotifyRecommender()
recommender.load_and_prepare_data()

# Get recommendations
recommendations, song_info = recommender.recommend_songs("Fire Beat", n_recommendations=10)

if recommendations is not None:
    print(song_info)
    print(recommendations)
```

## 🔧 Model Details

- **Algorithm**: K-means Clustering
- **Number of Clusters**: 5 (optimal)
- **Features Used**:
  - Danceability
  - Energy
  - Valence
  - Tempo
  - Duration (ms)
  - Popularity

- **Similarity Metric**: Euclidean Distance

## 📊 How It Works

1. Songs are clustered into 5 groups based on audio features
2. When you select a song, the system finds its cluster
3. It then calculates the Euclidean distance to all songs in that cluster
4. Returns the N closest songs (most similar)

## 🎯 Example API Request

### Using curl:

```bash
curl -X POST "http://localhost:8000/api/recommend" \
  -H "Content-Type: application/json" \
  -d '{"song_name": "Fire Beat", "n_recommendations": 10}'
```

### Using Python requests:

```python
import requests

response = requests.post(
    "http://localhost:8000/api/recommend",
    json={"song_name": "Fire Beat", "n_recommendations": 10}
)

data = response.json()
print(data)
```

## 🌟 Features

### Streamlit App
- ✨ Beautiful gradient UI
- 🔍 Multiple search methods
- 📊 Real-time statistics
- 📥 Download recommendations
- 🎲 Random song discovery

### FastAPI App
- 🚀 High-performance REST API
- 📚 Automatic API documentation (Swagger/ReDoc)
- 🎨 Modern web interface
- 🔄 Real-time recommendations
- 📊 Statistics dashboard

## 📝 Notes

- The model is trained automatically on first run
- Model is saved as `spotify_recommender_model.pkl` for faster loading
- Requires `spotify_tracks.csv` in the same directory

## 🎨 UI Preview

Both interfaces feature:
- Clean, modern design with gradient backgrounds
- Responsive layouts
- Easy-to-use search functionality
- Detailed song information
- Popularity scores and similarity distances

Enjoy discovering new music! 🎵
