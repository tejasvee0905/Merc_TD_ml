"""
FastAPI Application for Spotify Song Recommendation System
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from spotify_model import SpotifyRecommender
import os

# Initialize FastAPI app
app = FastAPI(
    title="Spotify Song Recommender API",
    description="API for recommending similar songs using K-means clustering",
    version="1.0.0"
)

# Setup templates directory
templates = Jinja2Templates(directory="templates")

# Initialize recommender
recommender = None

@app.on_event("startup")
async def startup_event():
    """Initialize the recommender on startup"""
    global recommender
    recommender = SpotifyRecommender('spotify_tracks.csv')
    
    # Load or train model
    if os.path.exists('spotify_recommender_model.pkl'):
        recommender.load_model()
        print("Model loaded successfully")
    else:
        print("Training model...")
        recommender.load_and_prepare_data()
        recommender.save_model()
        print("Model trained and saved")


# Request/Response models
class RecommendationRequest(BaseModel):
    song_name: str
    n_recommendations: int = 10

class SongInfo(BaseModel):
    track_name: str
    artist: str
    genre: str
    cluster: int
    popularity: int

class RecommendationItem(BaseModel):
    track_name: str
    artist: str
    genre: str
    playlist_category: str
    popularity: int
    distance: float

class RecommendationResponse(BaseModel):
    song_info: SongInfo
    recommendations: List[RecommendationItem]
    total_recommendations: int


# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/songs", response_class=JSONResponse)
async def get_all_songs():
    """Get all songs in the dataset"""
    try:
        songs = recommender.get_all_songs()
        songs_list = songs.to_dict('records')
        return {
            "total_songs": len(songs_list),
            "songs": songs_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/songs/random", response_class=JSONResponse)
async def get_random_song():
    """Get a random song from the dataset"""
    try:
        random_song = recommender.get_random_song()
        song_data = recommender.df[recommender.df['track_name'] == random_song].iloc[0]
        return {
            "track_name": song_data['track_name'],
            "artist": song_data['artist'],
            "genre": song_data['genre']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/recommend", response_model=RecommendationResponse)
async def recommend_songs(request: RecommendationRequest):
    """
    Get song recommendations based on a given song name
    
    Parameters:
    - song_name: Name of the song to find recommendations for
    - n_recommendations: Number of recommendations to return (default: 10)
    
    Returns:
    - Song information and list of recommended songs
    """
    try:
        recommendations, song_info = recommender.recommend_songs(
            request.song_name, 
            request.n_recommendations
        )
        
        if recommendations is None:
            raise HTTPException(status_code=404, detail=song_info)
        
        # Convert recommendations to list of dicts
        recommendations_list = recommendations.to_dict('records')
        
        return {
            "song_info": song_info,
            "recommendations": recommendations_list,
            "total_recommendations": len(recommendations_list)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/recommend/{song_name}", response_model=RecommendationResponse)
async def recommend_songs_get(song_name: str, n_recommendations: int = 10):
    """
    Get song recommendations (GET method)
    
    Parameters:
    - song_name: Name of the song to find recommendations for
    - n_recommendations: Number of recommendations to return (default: 10)
    """
    request = RecommendationRequest(song_name=song_name, n_recommendations=n_recommendations)
    return await recommend_songs(request)


@app.get("/api/search/{query}", response_class=JSONResponse)
async def search_songs(query: str, limit: int = 10):
    """
    Search for songs matching the query
    
    Parameters:
    - query: Search query string
    - limit: Maximum number of results to return (default: 10)
    """
    try:
        all_songs = recommender.get_all_songs()
        matching_songs = all_songs[
            all_songs['track_name'].str.contains(query, case=False, na=False)
        ].head(limit)
        
        return {
            "query": query,
            "total_matches": len(matching_songs),
            "results": matching_songs.to_dict('records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats", response_class=JSONResponse)
async def get_stats():
    """Get dataset statistics"""
    try:
        stats = {
            "total_songs": len(recommender.df),
            "total_clusters": recommender.optimal_k,
            "features_used": recommender.features,
            "cluster_distribution": recommender.df['cluster'].value_counts().to_dict(),
            "genres": recommender.df['genre'].unique().tolist(),
            "total_genres": recommender.df['genre'].nunique()
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": recommender is not None,
        "version": "1.0.0"
    }


# Run the app
if __name__ == "__main__":
    print("Starting Spotify Recommendation API...")
    print("API Documentation available at: http://localhost:8000/docs")
    print("Alternative docs at: http://localhost:8000/redoc")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
