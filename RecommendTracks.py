import csv
import re
import json
import sqlite3
import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import Counter
from scipy.sparse import csr_matrix, load_npz


def find_tracks_using_title(playlist, conn):

    # fetches the 5 most popular tracks among playlists that share a similar name with the challenge playlist name
    similar_playlist_tracks = (
            "SELECT track_id FROM PlaylistTracks " +
            "WHERE playlist_id = " +
            "(SELECT playlist_id FROM Playlists WHERE {} ORDER BY playlist_num_tracks DESC) " +
            "GROUP BY track_id ORDER BY COUNT(*) DESC LIMIT 5;")

    playlist_name = playlist['name'].replace("'", "")

    # 'Exact' match playlist names with challenge playlist name
    added_tracks = [
        record[0]
        for record
        in conn.cursor().execute(
            similar_playlist_tracks.format(
                "LOWER(REPLACE(playlist_name, ' ', '')) = '{}'".format(
                    playlist_name.lower().replace(" ", "")
                )
            )).fetchall()]

    # 'Fuzzy' match
    if not (added_tracks or playlist['tracks']):
        added_tracks = [
            record[0]
            for record
            in conn.cursor().execute(
                similar_playlist_tracks.format(
                    "'%' || LOWER(REPLACE(playlist_name, ' ', '')) || '%' LIKE '%{}%'".format(
                        playlist_name.lower().replace(" ", "")
                    )
                )).fetchall()]

        # Very fuzzy match
        if not added_tracks:
            added_tracks = [
                record[0]
                for record
                in conn.cursor().execute(
                    similar_playlist_tracks.format(
                        "'%' || LOWER(REPLACE(playlist_name, ' ', '')) || '%' LIKE '%{}%'".format(
                            re.sub(pattern=r'[^a-z0-9]', repl='', string=playlist_name)
                        )
                    )).fetchall()]

    return added_tracks


def find_tracks_using_artists(playlist, conn):
    artist_query = "SELECT track_id " + \
                   "FROM PlaylistTracks " + \
                   "WHERE track_id IN " + \
                        "(SELECT track_id" + \
                        " FROM Tracks" + \
                        " WHERE artist_uri = '{}') " + \
                   "GROUP BY track_id " + \
                   "ORDER BY COUNT(*) DESC " + \
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

            # Fetch tracks from DB playlists that 'match' playlist names
            if 'name' in challenge_playlist.keys():
                derived_tracks += find_tracks_using_title(challenge_playlist, connection)

            # Add playlist tracks to input tracks
            if challenge_playlist['tracks']:

                # Check if the playlist favors artists. If so, add each artist's top 5 to input tracks
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
                    "SELECT track_uri FROM TrackTemp LEFT JOIN Tracks ON TrackTemp.track_id = Tracks.track_id;"
                ).fetchall()]

            # Save recommendations to csv output file
            csv.writer(csv_file).writerow([challenge_playlist['pid']] + recommended_uris)
