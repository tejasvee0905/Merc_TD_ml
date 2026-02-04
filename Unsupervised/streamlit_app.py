"""
Professional Spotify Song Recommendation System
Powered by Machine Learning - K-means Clustering Algorithm
"""

import streamlit as st
import pandas as pd
from spotify_model import SpotifyRecommender
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="🎵 Spotify AI Recommender | ML-Powered Music Discovery",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Custom CSS with animations and modern design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background-color: #0e1117;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Header styling */
    .app-header {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        text-align: center;
    }
    
    .app-title {
        color: white;
        font-size: 3em;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .app-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2em;
        margin-top: 10px;
        font-weight: 300;
    }
    
    /* Card styling */
    .recommendation-card {
        background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border-left: 5px solid #1DB954;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    
    .recommendation-card:hover {
        transform: translateX(10px);
        box-shadow: 0 8px 25px rgba(29, 185, 84, 0.4);
    }
    
    .song-info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        color: white;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(29, 185, 84, 0.5);
    }
    
    /* Input styling */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #1DB954;
        padding: 12px;
        font-size: 16px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #2d2d2d 0%, #1e1e1e 100%);
    }
    
    /* Success/Info boxes */
    .success-box {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
        animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 30px;
        color: rgba(255,255,255,0.7);
        font-size: 14px;
        margin-top: 50px;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.1);
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize the recommender
@st.cache_resource
def load_recommender():
    """Load the recommender model"""
    recommender = SpotifyRecommender('spotify_tracks.csv')
    
    # Check if model exists, otherwise train
    if os.path.exists('spotify_recommender_model.pkl'):
        recommender.load_model()
    else:
        with st.spinner('Training model... This may take a moment.'):
            recommender.load_and_prepare_data()
            recommender.save_model()
    
    return recommender

# Main app
def main():
    # Professional Header
    st.markdown("""
        <div class="app-header">
            <h1 class="app-title">🎵 Spotify AI Music Recommender</h1>
            <p class="app-subtitle">Discover Your Next Favorite Songs | Powered by Machine Learning</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Load recommender
    try:
        with st.spinner('🔄 Loading AI Model...'):
            recommender = load_recommender()
        st.success("✅ AI Model Ready!")
    except Exception as e:
        st.error(f"❌ Error loading recommender: {e}")
        return
    
    # Tabs for better organization
    tab1, tab2, tab3, tab4 = st.tabs(["🎵 Recommendations", "📊 Analytics", "ℹ️ About", "🔧 Settings"])
    
    with tab1:
        # Get all songs for dropdown
        all_songs = recommender.get_all_songs()
        song_list = all_songs['track_name'].tolist()
        
        # Main content layout
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 🔍 Find Similar Songs")
            
            # Search method selection
            search_method = st.radio(
                "Choose your search method:",
                ["🔎 Search by Name", "📋 Browse All Songs", "🎲 Surprise Me!"],
                horizontal=True
            )
            
            selected_song = None
            
            if search_method == "🔎 Search by Name":
                song_input = st.text_input(
                    "Enter song name:",
                    placeholder="Type any song name...",
                    help="Start typing to search for songs"
                )
                if song_input:
                    # Find matching songs
                    matching_songs = all_songs[all_songs['track_name'].str.contains(song_input, case=False, na=False)]
                    if len(matching_songs) > 0:
                        st.success(f"✨ Found {len(matching_songs)} matching song(s)")
                        selected_song = st.selectbox("Select your song:", matching_songs['track_name'].tolist())
                    else:
                        st.warning(f"🔍 No songs found matching '{song_input}'. Try a different search!")
            
            elif search_method == "📋 Browse All Songs":
                # Add search filter
                filter_text = st.text_input("🔍 Quick filter:", placeholder="Type to filter songs...")
                if filter_text:
                    filtered_songs = [s for s in song_list if filter_text.lower() in s.lower()]
                else:
                    filtered_songs = song_list
                
                selected_song = st.selectbox(
                    "Browse and select a song:",
                    filtered_songs,
                    index=0,
                    help=f"Showing {len(filtered_songs)} of {len(song_list)} songs"
                )
            
            else:  # Surprise Me!
                col_a, col_b = st.columns([1, 3])
                with col_a:
                    if st.button("🎲 Get Random Song", use_container_width=True):
                        selected_song = recommender.get_random_song()
                        st.session_state['random_song'] = selected_song
                        st.balloons()
                
                if 'random_song' in st.session_state:
                    selected_song = st.session_state['random_song']
                    st.info(f"🎵 Random selection: **{selected_song}**")
            
            # Number of recommendations slider
            st.markdown("---")
            n_recommendations = st.slider(
                "📊 Number of recommendations:",
                min_value=5,
                max_value=25,
                value=10,
                step=1,
                help="Choose how many similar songs you want to discover"
            )
        
        with col2:
            st.markdown("### 📈 Quick Stats")
            if recommender.df is not None:
                st.metric("Total Songs", f"{len(recommender.df):,}")
                st.metric("Clusters", recommender.optimal_k)
                st.metric("Genres", recommender.df['genre'].nunique())
                
                # Mini cluster distribution
                cluster_counts = recommender.df['cluster'].value_counts().sort_index()
                fig = px.pie(
                    values=cluster_counts.values,
                    names=[f"Cluster {i}" for i in cluster_counts.index],
                    hole=0.4,
                    color_discrete_sequence=px.colors.sequential.Viridis
                )
                fig.update_layout(
                    height=250,
                    margin=dict(l=0, r=0, t=30, b=0),
                    showlegend=False,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
    
        # Get recommendations
        if selected_song:
            st.markdown("---")
            st.markdown("### 🎯 Generating Recommendations...")
            
            # Progress bar for better UX
            progress_bar = st.progress(0)
            for i in range(100):
                progress_bar.progress(i + 1)
            
            recommendations, song_info = recommender.recommend_songs(selected_song, n_recommendations)
            progress_bar.empty()
            
            if recommendations is not None:
                # Display song info in a beautiful card
                st.markdown("""
                    <div class="song-info-box">
                        <h2 style="margin-top:0;">🎵 Selected Song Details</h2>
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.metric("🎵 Track", song_info['track_name'])
                
                with col2:
                    st.metric("👤 Artist", song_info['artist'])
                
                with col3:
                    st.metric("🎸 Genre", song_info['genre'])
                
                with col4:
                    st.metric("🔢 Cluster", f"#{song_info['cluster']}")
                
                with col5:
                    st.metric("⭐ Popularity", f"{song_info['popularity']}/100")
                
                # Display recommendations
                st.markdown("---")
                st.markdown(f"### 🎧 Your Top {n_recommendations} Recommendations")
                st.markdown("*Ranked by similarity to your selected song*")
                
                # Add filtering options
                col_filter1, col_filter2, col_filter3 = st.columns(3)
                with col_filter1:
                    sort_by = st.selectbox(
                        "Sort by:",
                        ["Similarity (Distance)", "Popularity", "Track Name"],
                        index=0
                    )
                with col_filter2:
                    genre_filter = st.multiselect(
                        "Filter by Genre:",
                        options=recommendations['genre'].unique().tolist(),
                        default=recommendations['genre'].unique().tolist()
                    )
                with col_filter3:
                    min_popularity = st.slider("Min Popularity:", 0, 100, 0)
                
                # Apply filters
                filtered_recs = recommendations[
                    (recommendations['genre'].isin(genre_filter)) &
                    (recommendations['popularity'] >= min_popularity)
                ]
                
                # Apply sorting
                if sort_by == "Popularity":
                    filtered_recs = filtered_recs.sort_values('popularity', ascending=False)
                elif sort_by == "Track Name":
                    filtered_recs = filtered_recs.sort_values('track_name')
                
                if len(filtered_recs) == 0:
                    st.warning("🔍 No songs match your filter criteria. Try adjusting the filters!")
                else:
                    st.success(f"✨ Showing {len(filtered_recs)} recommendations")
                    
                    # Display as enhanced cards
                    for idx, (_, row) in enumerate(filtered_recs.iterrows(), 1):
                        with st.container():
                            col1, col2, col3, col4, col5, col6 = st.columns([0.5, 3, 2, 2, 1.5, 1])
                            
                            with col1:
                                st.markdown(f"### {idx}")
                            
                            with col2:
                                st.markdown(f"**🎵 {row['track_name']}**")
                            
                            with col3:
                                st.markdown(f"👤 *{row['artist']}*")
                            
                            with col4:
                                st.markdown(f"🎸 {row['genre']}")
                            
                            with col5:
                                # Popularity bar
                                pop_color = "🟢" if row['popularity'] >= 70 else "🟡" if row['popularity'] >= 40 else "🔴"
                                st.markdown(f"{pop_color} **{row['popularity']}**")
                            
                            with col6:
                                st.markdown(f"📏 {row['distance']:.3f}")
                            
                            st.markdown("---")
                    
                    # Download recommendations with timestamp
                    csv = filtered_recs.to_csv(index=False)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.download_button(
                        label="📥 Download Recommendations as CSV",
                        data=csv,
                        file_name=f"spotify_recommendations_{selected_song.replace(' ', '_')}_{timestamp}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    
                    # Visualization of recommendations
                    with st.expander("📊 View Recommendations Visualization"):
                        viz_col1, viz_col2 = st.columns(2)
                        
                        with viz_col1:
                            # Genre distribution
                            genre_counts = filtered_recs['genre'].value_counts()
                            fig1 = px.bar(
                                x=genre_counts.index,
                                y=genre_counts.values,
                                title="Genre Distribution in Recommendations",
                                labels={'x': 'Genre', 'y': 'Count'},
                                color=genre_counts.values,
                                color_continuous_scale='Viridis'
                            )
                            fig1.update_layout(
                                showlegend=False,
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)'
                            )
                            st.plotly_chart(fig1, use_container_width=True)
                        
                        with viz_col2:
                            # Popularity vs Distance scatter
                            fig2 = px.scatter(
                                filtered_recs,
                                x='distance',
                                y='popularity',
                                title="Popularity vs Similarity",
                                labels={'distance': 'Distance (Lower = More Similar)', 'popularity': 'Popularity Score'},
                                hover_data=['track_name', 'artist'],
                                color='popularity',
                                color_continuous_scale='Viridis',
                                size='popularity'
                            )
                            fig2.update_layout(
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)'
                            )
                            st.plotly_chart(fig2, use_container_width=True)
            else:
                st.error(f"❌ {song_info}")  # song_info contains the error message if recommendations is None
    
    # Analytics Tab
    with tab2:
        st.markdown("### 📊 Dataset Analytics & Insights")
        
        if recommender.df is not None:
            # Overall statistics
            st.markdown("#### 📈 Overall Statistics")
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            
            with stat_col1:
                st.metric("Total Songs", f"{len(recommender.df):,}")
            
            with stat_col2:
                st.metric("Unique Artists", f"{recommender.df['artist'].nunique():,}")
            
            with stat_col3:
                st.metric("Genres", recommender.df['genre'].nunique())
            
            with stat_col4:
                avg_popularity = recommender.df['popularity'].mean()
                st.metric("Avg Popularity", f"{avg_popularity:.1f}/100")
            
            st.markdown("---")
            
            # Visualizations
            viz_row1_col1, viz_row1_col2 = st.columns(2)
            
            with viz_row1_col1:
                # Cluster distribution
                st.markdown("#### 🎯 Cluster Distribution")
                cluster_counts = recommender.df['cluster'].value_counts().sort_index()
                fig = px.bar(
                    x=[f"Cluster {i}" for i in cluster_counts.index],
                    y=cluster_counts.values,
                    title="Songs per Cluster",
                    labels={'x': 'Cluster', 'y': 'Number of Songs'},
                    color=cluster_counts.values,
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with viz_row1_col2:
                # Genre distribution
                st.markdown("#### 🎸 Top Genres")
                top_genres = recommender.df['genre'].value_counts().head(10)
                fig = px.pie(
                    values=top_genres.values,
                    names=top_genres.index,
                    title="Top 10 Genres",
                    hole=0.4
                )
                st.plotly_chart(fig, use_container_width=True)
            
            viz_row2_col1, viz_row2_col2 = st.columns(2)
            
            with viz_row2_col1:
                # Popularity distribution
                st.markdown("#### ⭐ Popularity Distribution")
                fig = px.histogram(
                    recommender.df,
                    x='popularity',
                    nbins=30,
                    title="Song Popularity Distribution",
                    labels={'popularity': 'Popularity Score', 'count': 'Number of Songs'},
                    color_discrete_sequence=['#1DB954']
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with viz_row2_col2:
                # Feature correlations
                st.markdown("#### 🔗 Feature Analysis")
                feature_means = recommender.df[recommender.features].mean()
                fig = px.bar(
                    x=feature_means.index,
                    y=feature_means.values,
                    title="Average Feature Values",
                    labels={'x': 'Feature', 'y': 'Average Value'},
                    color=feature_means.values,
                    color_continuous_scale='Plasma'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Cluster characteristics
            st.markdown("#### 🎯 Cluster Characteristics")
            cluster_stats = recommender.df.groupby('cluster')[recommender.features].mean()
            st.dataframe(
                cluster_stats.style.background_gradient(cmap='viridis').format("{:.2f}"),
                use_container_width=True
            )
    
    # About Tab
    with tab3:
        st.markdown("### ℹ️ About This Application")
        
        st.markdown("""
        <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; margin: 10px 0;'>
        <h4>🎵 What is this?</h4>
        <p>This is an AI-powered music recommendation system that uses <strong>Machine Learning</strong> to find songs similar to your favorites. 
        The system analyzes various audio features to cluster songs and recommend the most similar tracks.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background: rgba(29, 185, 84, 0.2); padding: 20px; border-radius: 15px; margin: 10px 0;'>
            <h4>🤖 Technology Stack</h4>
            <ul>
                <li><strong>Algorithm:</strong> K-means Clustering</li>
                <li><strong>Clusters:</strong> 5 optimal groups</li>
                <li><strong>Similarity Metric:</strong> Euclidean Distance</li>
                <li><strong>Frontend:</strong> Streamlit</li>
                <li><strong>ML Library:</strong> Scikit-learn</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: rgba(118, 75, 162, 0.2); padding: 20px; border-radius: 15px; margin: 10px 0;'>
            <h4>📊 Features Analyzed</h4>
            <ul>
                <li>🎵 <strong>Danceability:</strong> How suitable for dancing</li>
                <li>⚡ <strong>Energy:</strong> Intensity and activity</li>
                <li>😊 <strong>Valence:</strong> Musical positiveness</li>
                <li>🎼 <strong>Tempo:</strong> Speed (BPM)</li>
                <li>⏱️ <strong>Duration:</strong> Track length</li>
                <li>⭐ <strong>Popularity:</strong> User engagement</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; margin: 20px 0;'>
        <h4>🔍 How It Works</h4>
        <ol>
            <li><strong>Data Processing:</strong> Songs are analyzed based on audio features</li>
            <li><strong>Clustering:</strong> K-means algorithm groups similar songs together</li>
            <li><strong>Recommendation:</strong> When you select a song, the system finds songs in the same cluster</li>
            <li><strong>Ranking:</strong> Results are sorted by similarity distance (closer = more similar)</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("💡 **Tip:** Try different songs and explore various genres to discover new music you might love!")
    
    # Settings Tab
    with tab4:
        st.markdown("### 🔧 Application Settings")
        
        st.markdown("#### 🎨 Display Options")
        col1, col2 = st.columns(2)
        
        with col1:
            show_distance = st.checkbox("Show similarity distance", value=True)
            show_category = st.checkbox("Show playlist category", value=True)
        
        with col2:
            enable_animations = st.checkbox("Enable animations", value=True)
            auto_play = st.checkbox("Auto-play on selection", value=False)
        
        st.markdown("---")
        
        st.markdown("#### 📊 Model Information")
        if recommender:
            info_data = {
                "Parameter": ["Dataset Size", "Number of Clusters", "Features Used", "Model Type", "Scaler"],
                "Value": [
                    f"{len(recommender.df):,} songs",
                    str(recommender.optimal_k),
                    ", ".join(recommender.features),
                    "K-means Clustering",
                    "StandardScaler"
                ]
            }
            st.table(pd.DataFrame(info_data))
        
        st.markdown("---")
        
        st.markdown("#### 🔄 Model Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Reload Model", use_container_width=True):
                st.cache_resource.clear()
                st.rerun()
        
        with col2:
            if st.button("💾 Save Current State", use_container_width=True):
                recommender.save_model()
                st.success("✅ Model saved successfully!")
        
        with col3:
            if st.button("📊 Show Model Stats", use_container_width=True):
                st.write(f"Model loaded at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div class="footer">
            <p><strong>🎵 Spotify AI Music Recommender</strong></p>
            <p>Powered by Machine Learning | K-means Clustering Algorithm</p>
            <p>Made with ❤️ using Streamlit, Scikit-learn, and Plotly</p>
            <p style="font-size: 12px; margin-top: 10px;">
                © 2026 | Data Science Project | 
                <a href="https://github.com" style="color: #1DB954;">GitHub</a> | 
                <a href="https://linkedin.com" style="color: #1DB954;">LinkedIn</a>
            </p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
