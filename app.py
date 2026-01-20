import streamlit as st
import pickle
import pandas as pd
import requests


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
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        url = "https://api.themoviedb.org/3/movie/{}".format(movie_id)
        params = {
            "api_key": "870fea2ca635981ef59ec080f30ef0be",
            "language": "en-US"
        }

        logger.info(f"Fetching movie ID: {movie_id}")
        logger.info(f"URL: {url}")

        response = requests.get(
            url, params=params, timeout=10)  # Increase timeout

        logger.info(f"Response status: {response.status_code}")

        if response.status_code != 200:
            logger.error(
                f"API Error: {response.status_code} - {response.text}")
            raise Exception(f"TMDB API error: {response.status_code}")

        data = response.json()
        logger.info(f"Successfully fetched data for movie ID: {movie_id}")

        poster_path = data.get("poster_path")
        poster_url = (
            f"https://image.tmdb.org/t/p/w500/{poster_path}"
            if poster_path else None
        )

        return {
            "poster": poster_url,
            "overview": data.get("overview", "No description available."),
            "rating": data.get("vote_average", "N/A"),
            "release_date": data.get("release_date", "N/A"),
            "genres": ", ".join(
                genre["name"] for genre in data.get("genres", [])
            ),
            "runtime": data.get("runtime", "N/A")
        }
    except requests.exceptions.Timeout:
        logger.error(f"Timeout error for movie ID: {movie_id}")
        raise Exception("Request timed out")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error for movie ID {movie_id}: {str(e)}")
        raise Exception(f"Network error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error for movie ID {movie_id}: {str(e)}")
        raise


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
        '🎯 Get Recommendations', use_container_width=True)

# Display recommendations
if recommend_button:
    with st.spinner('Finding perfect matches for you...'):
        recommendations = recommend(option, num_recommendations)

        st.markdown("---")
        st.markdown(f"### 🎥 Because you liked **{option}**, you might enjoy:")
        st.markdown("---")

        for idx, rec in enumerate(recommendations, 1):
            movie_id = movies[movies['title'] == rec].movie_id.values[0]

            try:
                details = fetch_movie_details(movie_id)

                col_img, col_info = st.columns([1, 2])

                with col_img:
                    st.image(details['poster'], use_container_width=True)

                with col_info:
                    st.markdown(f"### {idx}. {rec}")

                    # Rating and basic info
                    info_col1, info_col2, info_col3 = st.columns(3)
                    with info_col1:
                        st.markdown(f"⭐ **Rating:** {details['rating']}/10")
                    with info_col2:
                        st.markdown(
                            f"📅 **Released:** {details['release_date'][:4] if details['release_date'] != 'N/A' else 'N/A'}")
                    with info_col3:
                        st.markdown(
                            f"⏱️ **Runtime:** {details['runtime']} min" if details['runtime'] != 'N/A' else "⏱️ **Runtime:** N/A")

                    # Genres
                    if details['genres']:
                        st.markdown(f"🎭 **Genres:** {details['genres']}")

                    # Overview
                    st.markdown(f"**Overview:**")
                    st.markdown(f"{details['overview']}")

                st.markdown("---")

            except Exception as e:
                st.error(f"Could not load details for {rec}")
                st.markdown("---")

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666; font-size: 0.9rem;">Powered by TMDB API | Made with ❤️ using Streamlit</div>',
    unsafe_allow_html=True
)
