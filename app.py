import streamlit as st
import pickle
import pandas as pd
import requests
import logging
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TMDB_API_KEY = os.environ.get('TMDB_API_KEY')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def recommend(movie, top_n=5):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    scored = sorted(
        enumerate(distances),
        key=lambda x: x[1],
        reverse=True
    )
    top_matches = scored[1: top_n + 1]
    recommendations = [movies.iloc[i[0]].title for i in top_matches]
    return recommendations


def fetch_movie_details(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}".format(movie_id)
        params = {
            "api_key": TMDB_API_KEY,
            "language": "en-US"
        }

        logger.info(f"Fetching movie ID: {movie_id}")
        logger.info(f"URL: {url}")

        response = requests.get(url, params=params, timeout=10)

        logger.info(f"Response status: {response.status_code}")

        if response.status_code != 200:
            logger.error(
                f"API Error: {response.status_code} - {response.text}")
            return None

        data = response.json()
        logger.info(f"Successfully fetched data for movie ID: {movie_id}")
        logger.info(f"Data keys: {data.keys()}")

        poster_path = data.get("poster_path")
        poster_url = (
            f"https://image.tmdb.org/t/p/w500{poster_path}"
            if poster_path else "https://via.placeholder.com/500x750?text=No+Poster"
        )

        movie_details = {
            "poster": poster_url,
            "overview": data.get("overview", "No description available."),
            "rating": data.get("vote_average", "N/A"),
            "release_date": data.get("release_date", "N/A"),
            "genres": ", ".join(
                genre["name"] for genre in data.get("genres", [])
            ) if data.get("genres") else "N/A",
            "runtime": data.get("runtime", "N/A")
        }

        logger.info(f"Movie details created: {movie_details}")
        return movie_details

    except requests.exceptions.Timeout:
        logger.error(f"Timeout error for movie ID: {movie_id}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error for movie ID {movie_id}: {str(e)}")
        return None
    except Exception as e:
        logger.error(
            f"Unexpected error for movie ID {movie_id}: {str(e)}", exc_info=True)
        return None


# Page configuration
st.set_page_config(page_title="Movie Recommender",
                   page_icon="🎬", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #E50914;
        margin-bottom: 10px;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }
    .movie-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .movie-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 10px;
    }
    .movie-info {
        color: #666;
        margin: 5px 0;
    }
    .rating {
        color: #f5c518;
        font-weight: bold;
        font-size: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🎬 Movie Recommender System</div>',
            unsafe_allow_html=True)
st.markdown('<div class="sub-header">Discover your next favorite movie based on what you love!</div>',
            unsafe_allow_html=True)

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie selection
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    option = st.selectbox(
        '🔍 Select a movie you like:',
        movies['title'].values,
        index=0
    )

    num_recommendations = st.slider('Number of recommendations:', 3, 10, 5)

    recommend_button = st.button(
        '🎯 Get Recommendations', use_container_width=False)

# Display recommendations
if recommend_button:
    with st.spinner('Finding perfect matches for you...'):
        recommendations = recommend(option, num_recommendations)

        st.markdown("---")
        st.markdown(f"### 🎥 Because you liked **{option}**, you might enjoy:")
        st.markdown("---")

        for idx, rec in enumerate(recommendations, 1):
            try:
                movie_id = movies[movies['title'] == rec].movie_id.values[0]
                logger.info(
                    f"Processing recommendation #{idx}: {rec} (ID: {movie_id})")

                details = fetch_movie_details(movie_id)

                if details is None:
                    st.warning(f"⚠️ Could not load details for **{rec}**")
                    st.markdown("---")
                    continue

                col_img, col_info = st.columns([1, 2])

                with col_img:
                    if details['poster']:
                        st.image(details['poster'], use_column_width=True)

                with col_info:
                    st.markdown(f"### {idx}. {rec}")

                    # Rating and basic info
                    info_col1, info_col2, info_col3 = st.columns(3)
                    with info_col1:
                        rating_value = details['rating']
                        if rating_value != "N/A":
                            st.markdown(f"⭐ **Rating:** {rating_value}/10")
                        else:
                            st.markdown(f"⭐ **Rating:** N/A")
                    with info_col2:
                        release_date = details['release_date']
                        year = release_date[:4] if release_date and release_date != 'N/A' and len(
                            release_date) >= 4 else 'N/A'
                        st.markdown(f"📅 **Released:** {year}")
                    with info_col3:
                        runtime = details['runtime']
                        if runtime and runtime != 'N/A':
                            st.markdown(f"⏱️ **Runtime:** {runtime} min")
                        else:
                            st.markdown(f"⏱️ **Runtime:** N/A")

                    # Genres
                    if details['genres'] and details['genres'] != 'N/A':
                        st.markdown(f"🎭 **Genres:** {details['genres']}")

                    # Overview
                    st.markdown(f"**Overview:**")
                    st.markdown(f"{details['overview']}")

                st.markdown("---")

            except Exception as e:
                logger.error(
                    f"Error displaying {rec}: {str(e)}", exc_info=True)
                st.error(f"Could not load details for **{rec}**: {str(e)}")
                st.markdown("---")

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666; font-size: 0.9rem;">Powered by TMDB API | Made with ❤️ using Streamlit</div>',
    unsafe_allow_html=True
)
