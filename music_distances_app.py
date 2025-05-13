import streamlit as st
from utils.music_explorer import MusicExplorer

st.set_page_config(page_title="Music Distance", layout="wide")
st.title("🎶 ↔️ 🎶 Music Distances")

st.markdown("""
This app plays with different distance calculations. It uses euclidean distance to recommend music and cosine distance to understand lyrics similarity
""")

st.markdown("---")

explorer = MusicExplorer()

tab1, tab2, tab3 = st.tabs(["Top Obvious", "Top Weird", "Pick by Feature"])

with tab1:
    n = st.number_input("Number of songs", min_value=1, max_value=10, value=3, step=1, key="obvious_input")
    if st.button("Show Top Obvious Songs"):
        explorer.top_songs(n=n, kind="obvious")

with tab2:
    n = st.number_input("Number of songs", min_value=1, max_value=10, value=3, step=1, key="weird_input")
    if st.button("Show Top Weird Songs"):
        explorer.top_songs(n=n, kind="weird")

with tab3:
    explorer.pick_music_by_vibe()
    
