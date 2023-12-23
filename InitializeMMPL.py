import json
import pandas as pd
import os
import sqlite3

# Set directories/file paths
wd = r"C:\Users\Gunner\PycharmProjects\SpotifyMMPL"
source = wd + r"\SourceData\spotify_million_playlist_dataset\data"
db = wd + r"SpotifyMMPL.db"

# Establish DB connection / cursor
conn = sqlite3.connect(db)
cursor = conn.cursor()

# Import CreateTables script
with open(os.path.join(wd, "Queries", "CreateTables.sql"), 'r') as script_file:
    create_tables = script_file.read()

# Execute CreateTables script
cursor.executescript(create_tables)
conn.commit()

# Columns of interest
columns = [
    'pid', 'name', 'num_followers', 'track_name', 'duration_ms',
    'album_name', 'artist_name', 'track_uri', 'album_uri', 'artist_uri']

progress = 1

# Iterate over all JSON files and import data
for file in os.listdir(source):
    with open(os.path.join(source, file), "r") as json_file:
        for playlist in json.load(json_file)['playlists']:
            # 'Progress' bar
            if progress % 100 == 0:
                print(f"Processing Playlist {progress} out of 1,000,000.")

            pd.json_normalize(
                playlist,
                'tracks',
                ['pid', 'name', 'num_followers'])[columns].to_sql(
                "RawData", conn, if_exists='append', index=False)

            progress += 1
            conn.commit()

conn.close()
