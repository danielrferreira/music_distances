import streamlit as st
from utils.music_explorer import MusicExplorer

# Streamlit App
st.set_page_config(page_title="Music Explorer", layout="wide")
st.title("🎶 Music Explorer")

explorer = MusicExplorer()

if st.sidebar.button("Load Data"):
    explorer.data_loader()
    st.success("Data loaded successfully.")

if st.sidebar.button("Calculate Distances"):
    explorer.calculate_dev_from_mean()
    st.success("Distances calculated.")

st.sidebar.markdown("---")

tab1, tab2, tab3 = st.tabs(["Top Obvious", "Top Weird", "Pick by Vibe"])

with tab1:
    n = st.slider("Number of songs", 1, 10, 3, key="obvious_slider")
    explorer.top_songs(n=n, kind="obvious")

with tab2:
    n = st.slider("Number of songs", 1, 10, 3, key="weird_slider")
    explorer.top_songs(n=n, kind="weird")

with tab3:
    explorer.pick_music_by_vibe()
