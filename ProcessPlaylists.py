import csv
import re
import json
import sqlite3
import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import Counter
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity


def find_tracks_using_title(playlist, conn):

    # fetches the 5 most popular tracks among playlists that share a similar name with the challenge playlist name
    similar_playlist_tracks = (
            "SELECT track_id FROM PlaylistTracks " +
            "WHERE playlist_id = " +
            "(SELECT playlist_id FROM Playlists WHERE {}) " +
            "GROUP BY track_id ORDER BY COUNT(*) DESC LIMIT 5;")

    playlist_name = playlist["name"].replace("'", "")

    # "Exact" match playlist names with challenge playlist name
    added_tracks = np.array(
        conn.cursor().execute(
            similar_playlist_tracks.format(
                "LOWER(REPLACE(playlist_name, ' ', '')) = '{}'".format(
                    playlist_name.lower().replace(" ", "")))
        ).fetchall()
    ).ravel()

    # "Fuzzy" match
    if not (added_tracks.any() or playlist["tracks"]):
        added_tracks = np.array(
            conn.cursor().execute(
                similar_playlist_tracks.format(
                    "'%' || LOWER(REPLACE(playlist_name, ' ', '')) || '%' LIKE '%{}%'".format(
                        playlist_name.lower().replace(" ", "")))
            ).fetchall()
        ).ravel()

        # Very fuzzy match
        if not added_tracks.any():
            added_tracks = np.array(
                conn.cursor().execute(
                    similar_playlist_tracks.format(
                        "'%' || LOWER(REPLACE(playlist_name, ' ', '')) || '%' LIKE '%{}%'".format(
                            re.sub(pattern=r"[^a-z0-9]", repl="", string=playlist_name)))
                ).fetchall()
            ).ravel()

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
    artist_counts = Counter([track["artist_uri"] for track in playlist["tracks"]])
    added_tracks = np.empty(0)

    # Only add artist if it has more than 10% of the playlist
    artists = [
        artist
        for artist, count
        in artist_counts.items()
        if count * 10 >= sum(artist_counts.values())
    ]

    # Get 5 most popular tracks of each chosen artists
    for artist in artists:
        added_tracks = np.append(
            added_tracks,
            np.array(conn.cursor().execute(
                artist_query.format(artist)
            ).fetchall()).ravel())

    return added_tracks


challenge_json = "SourceData/Spotify_million_playlist_dataset_challenge/challenge_set.json"
database = "Spotify.db"
challenge_solution_csv = "spotify_challenge_results.csv"
track_order = np.arange(1, 501)

# Gather unique Playlist-Track interactions
with sqlite3.connect("Spotify.db") as connection:
    print("Collecting seed playlist-tracks...")
    df = pd.read_sql_query(
        "SELECT DISTINCT playlist_id, track_id FROM PlaylistTracks;",
        connection
    )

# Generate similarity score matrix
print("Generating COS Sim Matrix...")
sim = cosine_similarity(csr_matrix(([1]*len(df), (df["playlist_id"], df["track_id"]))).T, dense_output=False)

# Write team information on first row of solution
with open(challenge_solution_csv, "w", newline="") as csv_file:
    csv.writer(csv_file).writerow(["team_info", "Team Gunner", "tgwork11@gmail.com"])

# Open solution file
with (open(challenge_solution_csv, "a", newline="") as csv_file):

    # Connect to database
    with sqlite3.connect(database) as connection:

        # Open challenge dataset
        with open(challenge_json, "r") as challenge_file:

            # Iterate over the playlists
            for challenge_playlist in tqdm(
                    json.load(challenge_file)["playlists"],
                    desc="Processing playlists...",
                    unit="playlist"):

                derived_tracks = np.empty(0)
                seed_tracks = np.empty(0)

                # Fetch tracks from DB playlists that "match" playlist names
                if "name" in challenge_playlist.keys():
                    derived_tracks = np.append(
                        derived_tracks,
                        find_tracks_using_title(challenge_playlist, connection))

                # Add playlist tracks to input tracks
                if challenge_playlist["tracks"]:

                    # Check if the playlist favors artists. If so, add each artist's top 5 to input tracks
                    derived_tracks = np.append(
                        derived_tracks,
                        find_tracks_using_artists(challenge_playlist, connection))

                    seed_query = "SELECT track_id FROM Tracks WHERE track_uri IN ({});"
                    seed_uris = [track["track_uri"] for track in challenge_playlist["tracks"]]

                    seed_tracks = np.append(
                        seed_tracks,
                        np.array(
                            connection.cursor().execute(
                                seed_query.format(",".join(["?"] * len(seed_uris))),
                                seed_uris
                            ).fetchall()).ravel())

                # Generate 500 ordered track_id recommendations based on seed
                # tracks and added tracks, but not including seed tracks
                rec_array = np.argsort(
                    csr_matrix(
                        np.isin(
                            np.arange(
                                np.array(connection.cursor().execute("SELECT COUNT(*) FROM Tracks;").fetchone())[0]+1
                            ),
                            np.union1d(
                                seed_tracks,
                                derived_tracks
                            )
                        ).astype(int)
                    ).dot(sim).toarray().ravel()
                )[::-1]

                # Save track_ids to temp table in order
                pd.DataFrame(
                    {"track_id": rec_array[~np.isin(rec_array, seed_tracks)][:500],
                     "track_order": track_order}
                ).to_sql(
                    "TrackTemp",
                    connection,
                    index=False,
                    if_exists="replace"
                )

                # Save recommendations to csv output file
                csv.writer(csv_file).writerow(
                    [challenge_playlist["pid"]] +
                    np.array(
                        connection.cursor().execute(
                            "SELECT track_uri " +
                            "FROM TrackTemp " +
                            "JOIN Tracks " +
                            "ON TrackTemp.track_id = Tracks.track_id " +
                            "ORDER BY track_order;"
                        ).fetchall()).ravel().tolist())
