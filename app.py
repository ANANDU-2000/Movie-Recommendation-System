import streamlit as st
import pickle
import pandas as pd
import requests

# Load Data
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))

# Ensure it's a DataFrame
movies = pd.DataFrame(movies)
movies_list = movies['title'].values

# TMDB API to fetch movie posters
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_TMDB_API_KEY"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    return "https://via.placeholder.com/200x300"

# Recommendation Function
def recommend(movie):
    index_list = movies[movies['title'] == movie].index.tolist()
    if not index_list:
        return [], []
    
    index = index_list[0]
    if index >= len(similarity):
        return [], []
    
    distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_posters = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_posters

# Streamlit UI
st.markdown("<h1 style='text-align: center; color: #ff4c4c;'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Find Movies Similar to Your Favorite Ones!</h3>", unsafe_allow_html=True)

# Dropdown
selected_movie = st.selectbox("🎥 Select a Movie", movies_list)

# Show Recommendations
if st.button("Show Recommendations"):
    recommended_movies, recommended_posters = recommend(selected_movie)

    if recommended_movies:
        # Display recommendations in columns
        st.markdown("<h3 style='text-align: center;'>Recommended Movies 🎞️</h3>", unsafe_allow_html=True)
        cols = st.columns(5)
        for i in range(len(recommended_movies)):
            with cols[i]:
                st.image(recommended_posters[i], use_column_width=True)
                st.markdown(f"<h5 style='text-align: center;'>{recommended_movies[i]}</h5>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ No recommendations found. Try another movie!")

# Footer
st.markdown("<br><br><p style='text-align: center; font-size: 14px;'>Made with ❤️ using Machine Learning & Streamlit</p>", unsafe_allow_html=True)
