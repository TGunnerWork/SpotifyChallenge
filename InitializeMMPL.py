import json
import pandas as pd
import os
import sqlite3

source = r"C:\Users\Gunner\PycharmProjects\SpotifyMMPL\SourceData\spotify_million_playlist_dataset\data"
db = r"C:\sqlite\Databases\SpotifyMMPL.db"

conn = sqlite3.connect(db)

for file in os.listdir(source):
    with open(os.path.join(source, file), "r") as json_file:
        for playlist in json.load(json_file)['playlists']:

            if (playlist['pid']+1) % 50 == 0:
                print(f"Processing Playlist {playlist['pid']+1} out of 1,000,000.")

            pl_track_uris = [track['track_uri'] for track in playlist['tracks']]
            pl_track_names = [track['track_name'] for track in playlist['tracks']]
            pl_track_times = [track['duration_ms'] for track in playlist['tracks']]
            pl_album_uris = [track['album_uri'] for track in playlist['tracks']]
            pl_album_names = [track['album_name'] for track in playlist['tracks']]
            pl_artist_uris = [track['artist_uri'] for track in playlist['tracks']]
            pl_artist_names = [track['artist_name'] for track in playlist['tracks']]

            # Add playlist tracks to fact table
            pd.DataFrame(data={
                'TrackID': pl_track_uris,
                'PlaylistID': [playlist['pid']] * len(pl_track_uris)
            }).to_sql("PlaylistsTracks", conn, if_exists='append', index=False)

            # Add playlist to playlist table
            pd.Series({
                'ID': playlist['pid'],
                'Playlist': playlist['name'],
                'Followers': playlist['num_followers']
            }).to_frame().T.to_sql("Playlists", conn, if_exists='append', index=False)

            # Add tracks to tracks table
            pd.DataFrame(data={
                'ID': pl_track_uris,
                'Track': pl_track_names,
                'Duration': pl_track_times,
                'Album': pl_album_uris
            }).to_sql("Tracks", conn, if_exists='append', index=False)

            # Add albums to album table
            pd.DataFrame(data={
                'ID': pl_album_uris,
                'Album': pl_album_names,
                'Artist': pl_artist_uris
            }).to_sql("Albums", conn, if_exists='append', index=False)

            # Add artists to artists table
            pd.DataFrame(data={
                'ID': pl_artist_uris,
                'Artist': pl_artist_names
            }).to_sql("Artists", conn, if_exists='append', index=False)

            conn.commit()

conn.close()
