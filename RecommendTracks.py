import re
import csv
import json
import sqlite3
import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import Counter
from scipy.sparse import csr_matrix, load_npz


def find_tracks_using_title(playlist, conn):

    no_tracks_script = "SELECT DISTINCT track_id " + \
                       "FROM PlaylistTracks " + \
                       "WHERE playlist_id = " + \
                            "(SELECT playlist_id " + \
                            "FROM Playlists " + \
                            "WHERE {} " + \
                            "ORDER BY playlist_num_tracks DESC " + \
                            "LIMIT 1);"
    eq_pl = "LOWER(REPLACE(playlist_name, ' ', '')) = '{}'"
    like_pl = "'%' || LOWER(REPLACE(playlist_name, ' ', '')) || '%' LIKE '%{}%'"
    playlist_name = playlist['name'].replace("'", "")

    added_tracks = [
        record[0]
        for record
        in conn.cursor().execute(no_tracks_script.format(eq_pl.format(
            playlist_name.lower().replace(" ", "")
        ))).fetchall()]

    if len(added_tracks) == 0 and playlist['num_samples'] == 0:
        added_tracks = [
            record[0]
            for record
            in conn.cursor().execute(
                no_tracks_script.format(like_pl.format(
                    playlist_name.lower().replace(" ", "")
                ))).fetchall()]

        if len(added_tracks) == 0:
            added_tracks = [
                record[0]
                for record
                in conn.cursor().execute(
                    no_tracks_script.format(like_pl.format(
                        re.sub(pattern=r'[^a-z0-9]', repl='', string=playlist_name)
                    ))).fetchall()]

    return added_tracks


def find_tracks_using_artists(playlist, conn):
    artist_query = "SELECT track_id " + \
                   "FROM PlaylistTracks " + \
                   "WHERE track_id IN " + \
                        "(SELECT track_id" + \
                        " FROM Tracks" + \
                        " WHERE artist_uri = '{}') " + \
                   "GROUP BY track_id " + \
                   "ORDER BY COUNT(*) " + \
                   "LIMIT 5;"
    artist_counts = Counter([track['artist_uri'] for track in playlist['tracks']])
    added_tracks = []

    # Only add artist if it has more than 10% of the playlist
    artists = [
        artist
        for artist, count
        in artist_counts.items()
        if count * 10 >= sum(artist_counts.values())
    ]

    # Get 5 most popular tracks of each chosen artists
    for artist in artists:
        added_tracks += [
            result[0]
            for result
            in conn.cursor().execute(
                artist_query.format(artist)
            ).fetchall()
        ]

    return added_tracks


challenge_json = "SourceData/Spotify_million_playlist_dataset_challenge/challenge_set.json"
database = "Spotify.db"

# Load challenge dataset
with open(challenge_json, 'r') as file:
    challenge_playlists = json.load(file)['playlists']

# Load collaborative filter matrix if not already in memory
if __name__ == '__main__':
    print("Loading matrix")
    sim = load_npz('col_fil_spotify.npz')

with open('spotify_challenge_results.csv', 'w', newline='') as csv_file:
    csv.writer(csv_file).writerow(["team_info", "Team Gunner", "tgwork11@gmail.com"])

with open('spotify_challenge_results.csv', 'a', newline='') as csv_file:

    with sqlite3.connect(database) as connection:

        csr_matrix_shape = connection.cursor().execute("SELECT COUNT(*) FROM Tracks;").fetchone()[0] + 1

        for challenge_playlist in tqdm(challenge_playlists, desc="Processing Playlists", unit=" playlists"):

            derived_tracks = []
            seed_tracks = []

            # Check if the playlist has a name, if so, add tracks
            if 'name' in challenge_playlist.keys():
                derived_tracks += find_tracks_using_title(challenge_playlist, connection)

            # Check if existing tracks favor certain artists
            if len(challenge_playlist['tracks']) > 0:
                derived_tracks += find_tracks_using_artists(challenge_playlist, connection)

                seed_query = "SELECT track_id FROM Tracks WHERE track_uri IN ({});"
                seed_uris = [track['track_uri'] for track in challenge_playlist['tracks']]

                seed_tracks += [
                    result[0]
                    for result
                    in connection.cursor().execute(
                        seed_query.format(
                            ','.join(['?'] * len(seed_uris))),
                        seed_uris
                    ).fetchall()
                ]

            # Only one of each track
            tracks = list(set(seed_tracks + derived_tracks))

            # Convert tracks into a 1D sparse matrix
            csr_pl = csr_matrix(list(np.isin(np.arange(csr_matrix_shape), tracks).astype(int)))

            # Generate 500 ordered track_id recommendations based on seed
            # tracks and added tracks, but not including seed tracks
            recommended_tracks = list(filter(
                lambda x: x not in seed_tracks,
                list(np.argsort(csr_pl.dot(sim).toarray().ravel())[::-1])
            ))[:500]

            # Save track_ids to temp table
            pd.DataFrame(
                {'track_id': recommended_tracks}
            ).to_sql(
                'TrackTemp',
                connection,
                index=False,
                if_exists='replace'
            )

            # Get track_uris from track_ids
            recommended_uris = [
                result[0]
                for result
                in connection.cursor().execute(
                    "SELECT track_uri FROM TrackTemp JOIN Tracks ON TrackTemp.track_id = Tracks.track_id;"
                ).fetchall()]

            # Save recommendations to csv output file
            csv.writer(csv_file).writerow([challenge_playlist['pid']] + recommended_uris)