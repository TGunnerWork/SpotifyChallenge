import json
import pandas as pd
import os
import sqlite3

# Set directories/file paths
source_data = "SourceData/spotify_million_playlist_dataset/data"

columns = [
    'pl_pid',
    'pl_name',
    'pl_num_tracks',
    'pl_num_albums',
    'pl_num_artists',
    'pl_duration_ms',
    'pl_num_followers',
    'pl_collaborative',
    'pl_description',
    'pos',
    'track_name',
    'album_name',
    'artist_name',
    'duration_ms',
    'track_uri',
    'album_uri',
    'artist_uri'
]
meta = [
    'name',
    'collaborative',
    'pid',
    'num_tracks',
    'num_albums',
    'num_followers',
    'duration_ms',
    'num_artists',
    'description'
]
dtypes = {
    'pl_pid': int,
    'pl_name': str,
    'pl_num_tracks': int,
    'pl_num_albums': int,
    'pl_num_artists': int,
    'pl_duration_ms': int,
    'pl_num_followers': int,
    'pl_collaborative': str,
    'pl_description': str,
    'pos': int,
    'track_name': str,
    'album_name': str,
    'artist_name': str,
    'duration_ms': int,
    'track_uri': str,
    'album_uri': str,
    'artist_uri': str
}

# Create Tables
with sqlite3.connect("Spotify.db") as conn:
    cursor = conn.cursor()
    with open("Queries/CreateTables.sql", 'r') as script_file:
        cursor.executescript(script_file.read())
        conn.commit()

    # Import data into DB
    for json_file in os.listdir(source_data):
        with open(os.path.join(source_data, json_file), 'r') as file:
            pd.json_normalize(
                json.load(file)['playlists'],
                record_path='tracks', meta=meta, meta_prefix='pl_', errors='ignore'
            )[columns].to_sql("RawData", conn, if_exists='append', index=False)

