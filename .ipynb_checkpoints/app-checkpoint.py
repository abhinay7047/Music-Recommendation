

import streamlit as st
import pickle
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
client_id = 'd6029d356c024733bac70ac38dd848fc'
client_secret = 'ac5e06b52bd9466ca92fa5f469d41fcf'
redirect_uri = 'http://localhost:8501/'  # The redirect URI you set in the Spotify Developer Dashboard

# Initialize Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-library-read"
))

def fetch_poster(music_title):
    try:
        result = sp.search(q=music_title, limit=1, type='track')
        if result['tracks']['items']:
            album_cover_url = result['tracks']['items'][0]['album']['images'][0]['url']
            return album_cover_url
        else:
            st.warning(f"Poster not found for the song: {music_title}")
            return "https://via.placeholder.com/150"  # Placeholder image if not found
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/150"  # Placeholder image if error occurs

def recommend(musics):
    music_index = music[music['title'] == musics].index[0]
    distances = similarity[music_index]
    music_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_music = []
    recommended_music_poster = []
    for i in music_list:
        music_title = music.iloc[i[0]].title
        recommended_music.append(music_title)
        recommended_music_poster.append(fetch_poster(music_title))
    return recommended_music, recommended_music_poster

# Load the pre-saved music data and similarity matrix
music_dict = pickle.load(open('Downloads/Music Recommendation/musicrec.pkl', 'rb'))
music = pd.DataFrame(music_dict)
similarity = pickle.load(open('Downloads/Music Recommendation/similarities.pkl', 'rb'))

# Streamlit app title
st.title('Music Recommendation System')

# Select box for selecting music
selected_music_name = st.selectbox('Select a music you like', music['title'].values)

# Recommend button
if st.button('Recommend'):
    names, posters = recommend(selected_music_name)

    # Display recommended music and their posters
    col1, col2, col3, col4, col5 = st.columns(5)
    for idx, (name, poster) in enumerate(zip(names, posters)):
        with [col1, col2, col3, col4, col5][idx]:
            st.text(name)
            st.image(poster)

