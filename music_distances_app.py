import streamlit as st
from utils.music_explorer import MusicExplorer

st.set_page_config(page_title="Music Distance", layout="wide")
st.title("🎶 ↔️ 🎶 Music Distances")

st.markdown("""
This app plays with different distance calculations. It uses euclidean distance to recommend music and cosine distance to understand lyrics similarity
""")

st.markdown("---")

explorer = MusicExplorer()

tab1, tab2, tab3, tab4 = st.tabs(["Top Obvious", "Top Weird", "Pick by Feature", "Lyrics Distance"])

with tab1:
    st.markdown("This tab shows the musics that are closer to the center. Choose the number of songs")
    st.markdown("---")
    n = st.number_input("Number of songs", min_value=1, max_value=10, value=3, step=1, key="obvious_input")
    if st.button("Show Top Obvious Songs"):
        explorer.top_songs(n=n, kind="obvious")

with tab2:
    st.markdown("This tab shows the musics that are far to the center. Choose the number of songs")
    st.markdown("---")
    n = st.number_input("Number of songs", min_value=1, max_value=10, value=3, step=1, key="weird_input")
    if st.button("Show Top Weird Songs"):
        explorer.top_songs(n=n, kind="weird")

with tab3:
    st.markdown("Here you can use the sliders and then find the music closer to the selection")
    st.markdown("---")
    explorer.pick_music_by_vibe()

with tab4:
    st.markdown("Pick a song and see what is the closest lyric")
    st.markdown("---")
    artist = st.selectbox('Select a Band/Singer:',explorer.band_singer)
    _, songs = explorer.songs(artist)
    song = st.selectbox('Select a Song:', songs)

    

    
