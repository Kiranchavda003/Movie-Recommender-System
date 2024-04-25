import pickle
import streamlit as st
import requests

# Function to fetch movie poster using OMDB API
def fetch_poster(title):
    url = "http://www.omdbapi.com/"
    params = {'apikey': 'f994b4d6', 't': title}
    data = requests.get(url, params=params).json()
    if data.get('Response') == 'True':
        poster_url = data.get('Poster')
        return poster_url
    else:
        return None

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index
    if len(index) > 0:
        index = index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        for i in distances[1:6]:
            recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names
    else:
        return []

# Load movie list and similarity data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('🎥 Movie Recommender System🌟')
st.write("Welcome to the Movie Recommender System! Select a movie from the dropdown below and click 'Show Recommendation' to see similar movies.")

# Dropdown to select movie for recommendations
selected_movie = st.selectbox("Select a movie:", movies['title'].values, help="Choose a movie from the list.")

if st.button('Show Recommendation'):
    with st.spinner('Fetching recommendations...'):
        recommended_movie_names = recommend(selected_movie)
    
    if len(recommended_movie_names) > 0:
        st.write("Recommended movies with posters:")
        # Display recommended movie posters
        poster_urls = []
        for name in recommended_movie_names:
            # Fetch poster for each recommended movie
            poster_url = fetch_poster(name)
            if poster_url:
                poster_urls.append((name, poster_url))
        
        # Display posters horizontally
        cols = st.columns(len(poster_urls))
        for col, (name, url) in zip(cols, poster_urls):
            with col:
                st.image(url, caption=name, use_column_width=True)
    else:
        st.write("Sorry, we couldn't find recommendations for this movie.")

# Footer
st.markdown("---")