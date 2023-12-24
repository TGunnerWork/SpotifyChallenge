import json
import pandas as pd
import os
import sqlite3

# Set directories/file paths
wd = r"C:\Users\Gunner\PycharmProjects\SpotifyMMPL"
source = wd + r"\SourceData\spotify_million_playlist_dataset\data"

# Establish DB connection / cursor
conn = sqlite3.connect(os.path.join(wd, "SpotifyMMPL.db"))
cursor = conn.cursor()

# Import CreateTables script
with open(os.path.join(wd, "Queries", "CreateTables.sql"), 'r') as script_file:
    create_tables = script_file.read()

# Execute CreateTables script
cursor.executescript(create_tables)
conn.commit()

columns = ['pl_pid', 'pl_name', 'pl_num_tracks', 'pl_num_albums', 'pl_num_artists', 'pl_duration_ms',
           'pl_num_followers', 'pl_collaborative', 'pos', 'track_name', 'album_name', 'artist_name',
           'duration_ms', 'track_uri', 'album_uri', 'artist_uri']
meta = ['name', 'collaborative', 'pid', 'num_tracks', 'num_albums', 'num_followers', 'duration_ms', 'num_artists']
path = 'tracks'
prefix = "pl_"

progress = 1

# Iterate over all JSON files and load data to RawData table
for file in os.listdir(source):
    with open(os.path.join(source, file), "r") as json_file:
        print(f"Processing JSON {progress} of 1,000.")
        for playlist in json.load(json_file)['playlists']:

            pd.json_normalize(
                playlist, record_path=path, meta=meta, meta_prefix=prefix)[columns].to_sql(
                "RawData", conn, if_exists='append', index=False)

            conn.commit()
        progress += 1

conn.close()
# About 2 hours
