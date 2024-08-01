import streamlit as st
import pickle
import pandas as pd


def placeholder_poster(music_title):
    # Local image file path
    return "image.png"

def recommend(music):
    music_index = new_df[new_df['title'] == music].index[0]
    distances = similarity[music_index]
    music_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_music = []
    recommended_music_poster = []
    for i in music_list:
        music_title = new_df.iloc[i[0]].title
        recommended_music.append(music_title)
        recommended_music_poster.append(placeholder_poster(music_title))
    return recommended_music, recommended_music_poster

# Load the pre-saved music data and similarity matrix
music_dict = pickle.load(open('musicrec.pkl', 'rb'))
new_df = pd.DataFrame(music_dict)
similarity = pickle.load(open('similarities.pkl', 'rb'))

# Streamlit app title
st.title('Music Recommendation System')

# Select box for selecting music
selected_music_name = st.selectbox('Select a music you like', new_df['title'].values)

# Recommend button
if st.button('Recommend'):
    names, posters = recommend(selected_music_name)

    # Display recommended music and their posters
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]
    for idx, (name, poster) in enumerate(zip(names, posters)):
        with columns[idx]:
            st.text(name)
            st.image(poster, width=150)  # Adjust the width as needed
