import streamlit as st
import pandas as pd
import numpy as np
import math

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(stop_words='english', max_features=100)

class MusicExplorer:
    def __init__(self, file_path='data/input_df.csv',
                 X_cols=['danceability','energy','loudness','speechiness','acousticness','liveness','valence'],
                 lyric_col='lyrics',
                 id_col='songurl'):
        self.file_path = file_path
        self.X_cols = X_cols
        self.lyric_col = lyric_col
        self.id_col = id_col
        self.X_count = len(X_cols)
        df = pd.read_csv(self.file_path)
        df = df.drop_duplicates(subset=self.id_col, keep='first')
        self.df = df.copy()
        self.df_no_miss = df.dropna(subset=[self.X_cols[0]])
        self.dev_from_mean_df = None
        self.band_singer = self.df['band_singer'].unique()
        self.lyrics_array = vectorizer.fit_transform(self.df_no_miss['lyrics']).toarray()
    
    def calculate_dev_from_mean(self):
        df = self.df_no_miss
        X = df[self.X_cols]
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)
        center = np.mean(X_scaled, axis=0)
        distances = np.linalg.norm(X_scaled - center, axis=1)
        df['distance_from_center'] = distances
        df['obviouness'] = 1 / distances
        df = df.sort_values('obviouness', ascending=False)
        self.dev_from_mean_df = df
        return df

    def compare_graph(self, df, song_id):
        n_graphs = self.X_count
        n_row = math.ceil(n_graphs / 4)
        fig, axes = plt.subplots(nrows=n_row, ncols=4, figsize=(9, n_row * 2))
        axes = axes.flatten()
        temp = df[df[self.id_col] == song_id]
        song = temp['song'].values[0]
        singer = temp['band_singer'].values[0]
        spotify_uri = temp['uri'].values[0]
        track_id = spotify_uri.split("spotify:track:")[1]
        link_url = f"https://open.spotify.com/track/{track_id}"
        title = f"### [{song} by {singer}]({link_url})"
        for v, ax in zip(self.X_cols, axes):
            sns.histplot(data=df, x=v, ax=ax, kde=True)
            ax.axvline(x=temp[v].values[0], color='red', linestyle='--', linewidth=1.5)
            ax.set_title(v)
            ax.set_xlabel("")
        for ax in axes[n_graphs:]:
            ax.set_visible(False)
        plt.tight_layout()
        return title, fig

    def top_songs(self, n=3, kind="obvious"):
        df = self.dev_from_mean_df if self.dev_from_mean_df is not None else self.calculate_dev_from_mean()
        if kind == "obvious":
            selected = df.head(n)
            st.subheader(f"Top {n} songs closer to the center")
        else:
            selected = df.tail(n).sort_values('obviouness')
            st.subheader(f"Top {n} songs farther from the center")
        for idx, row in selected.iterrows():
            title, fig = self.compare_graph(df, row[self.id_col])
            st.markdown(title)
            st.pyplot(fig)

    def pick_music_by_vibe(self):
        st.subheader("🎧 Pick music based on your vibe")
        user_options = []
        for col in self.X_cols:
            val = st.slider(col, min_value=0.0, max_value=1.0, value=0.5, step=0.01)
            user_options.append(val)

        if st.button("🎶 Suggest a Song"):
            if self.df is None:
                df = self.data_loader()
            else:
                df = self.df
            X = df[self.X_cols]
            scaler = MinMaxScaler()
            X_scaled = scaler.fit_transform(X)
            distances = np.linalg.norm(X_scaled - user_options, axis=1)
            df['distance_from_user'] = distances
            closest = df.sort_values('distance_from_user').iloc[0]
            st.markdown(f"### 🎵 Closest match:")
            title, fig = self.compare_graph(df, closest[self.id_col])
            st.markdown(title)
            st.pyplot(fig)
    
    def songs(self,artist):
        songs_df = self.df[self.df['band_singer']==artist][['song','lyrics']].copy()
        songs_list = songs_df['song'].unique()
        return songs_df, songs_list
    
    def closest_lyrics(self, lyrics):
        pass
