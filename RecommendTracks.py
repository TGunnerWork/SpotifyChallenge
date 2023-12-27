import csv
import os
import re
import json
import sqlite3
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, load_npz

with open('spotify_challenge_results.csv', 'w', newline='') as csv_file:
    csv.writer(csv_file).writerow([
        "team_info",
        "Team Gunner",
        "tgwork11@gmail.com"
    ])

# Load collaborative filter model
sim = load_npz('col_fil_spotify.npz')

# Load challenge dataset
with open(os.path.join(
        os.getcwd(),
        r'SourceData\spotify_million_playlist_dataset_challenge\challenge_set.json'), 'r') as file:
    challenge_playlists = json.load(file)['playlists']

# Get number of tracks
with sqlite3.connect("Spotify.db") as conn:
    csr_matrix_shape = conn.cursor().execute("SELECT COUNT(*) FROM Tracks;").fetchone()[0]

# Define ad-hoc scripts
track_uri_script = "SELECT track_id FROM Tracks WHERE track_uri IN ({});"
track_id_script = "SELECT track_uri FROM Tracks WHERE track_id IN ({});"
with open("Queries/EmptyPlaylistChallengeTracks.sql", "r") as sql_file:
    script = sql_file.read()

# Get tracks from sample playlists that have similar names to challenge playlist
for playlist in challenge_playlists:
    new_tracks = []
    try:
        var = re.sub(r'[^a-zA-Z0-9]', '', playlist['name'].lower())
        with sqlite3.connect("Spotify.db") as conn:
            tracks_from_similar_pl_names = [
                result[0]
                for result
                in conn.cursor().execute(script, (var, var)).fetchall()]
    except KeyError:
        pass

    try:
        uris = [track['track_uri'] for track in playlist['tracks']]
        uri_query = track_uri_script.format(', '.join(['?']*len(uris)))
        with sqlite3.connect("Spotify.db") as conn:
            tracks_in_playlist = [result[0] for result in conn.cursor().execute(uri_query, uris).fetchall()]
    except KeyError:
        pass

    new_tracks = list(set(tracks_from_similar_pl_names + tracks_in_playlist))

    # convert to sparse matrix row
    csr_pl = csr_matrix(list(np.isin(np.arange(csr_matrix_shape), new_tracks).astype(int)))

    # generate 500 new recommendations
    rec_tracks = list(filter(
        lambda x: x not in tracks_in_playlist,
        list(np.argsort(csr_pl.dot(sim).toarray().ravel())[::-1])
    ))[:500]

    # Convert back to URIs
    with sqlite3.connect("Spotify.db") as conn:
        pd.DataFrame(
            {'track_id': rec_tracks}
        ).to_sql('TrackTemp', conn, index=False, if_exists='replace')

        conn.commit()

        recommended_uris = [
            result[0]
            for result
            in conn.cursor().execute(
                "SELECT track_uri FROM TrackTemp JOIN Tracks ON TrackTemp.track_id = Tracks.track_id;"
            ).fetchall()]

        with open('spotify_challenge_results.csv', 'a', newline='') as csv_file:
            csv.writer(csv_file).writerow(
                [playlist['pid']]+recommended_uris
            )
