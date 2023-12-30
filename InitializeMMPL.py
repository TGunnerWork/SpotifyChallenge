import json
import pandas as pd
import os
import sqlite3
# from send_email import send_email
# import time
# from datetime import timedelta


# Iterate over all JSON files and load data to RawData table
def process_json(file):
    with sqlite3.connect("Spotify.db") as connection:
        with open(file, "r") as proc_file:
            pd.json_normalize(
                json.load(proc_file)['playlists'],
                record_path='tracks', meta=meta, meta_prefix='pl_', errors='ignore'
            )[columns].to_sql("RawData", connection, if_exists='append', index=False)


# Set directories/file paths
wd = os.getcwd()
source_data = os.path.join(os.getcwd(), r'SourceData\spotify_million_playlist_dataset\data')

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
progress = 1

# start = time.time()

# Create Tables
with sqlite3.connect(os.path.join(wd, "Spotify.db")) as conn:
    cursor = conn.cursor()
    with open(os.path.join(wd, "Queries", "CreateTables.sql"), 'r') as script_file:
        cursor.executescript(script_file.read())
        conn.commit()

# send_email("CreateTables.sql has completed.",
#           f'Process completed at {time.strftime("%H:%M:%S", time.localtime(time.time()))}.' +
#           f'\nProcess took {str(timedelta(seconds=time.time()-start))}')

# start = time.time()

# Import data into DB
for json_file in os.listdir(os.path.join(wd, source_data)):
    print(f"Processing JSON {progress} of 1,000.")
    process_json(os.path.join(os.path.join(wd, source_data), json_file))
    progress += 1

# send_email("JSON Import has completed.",
#           'All JSON files have been imported into database.\n' +
#           f'Process completed at {time.strftime("%H:%M:%S", time.localtime(time.time()))}.' +
#           f'\nProcess took {str(timedelta(seconds=time.time()-start))}')
