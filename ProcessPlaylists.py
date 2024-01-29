import csv
import json
import sqlite3
from find_tracks import using_title, using_artists
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

# Set named constants
challenge_json = "SourceData/Spotify_million_playlist_dataset_challenge/challenge_set.json"
database = "Spotify.db"
challenge_solution_csv = "spotify_challenge_results.csv"
max_tracks = 500
track_order = np.arange(max_tracks) + 1

# Queries
save_query = "SELECT track_uri FROM TrackTemp JOIN Tracks ON TrackTemp.track_id = Tracks.track_id ORDER BY track_order;"
gather_playlist_tracks = "SELECT DISTINCT playlist_id, track_id FROM PlaylistTracks;"
seed_query = "SELECT track_id FROM Tracks WHERE track_uri IN ({});"

# Gather unique Playlist-Track interactions
with sqlite3.connect("Spotify.db") as connection:
    print("Collecting seed playlist-tracks...")
    df = pd.read_sql_query(
        gather_playlist_tracks,
        connection
    )


# Creates a sparse binary matrix of tracks vs playlists (csr_matrix)
# and calculates the cosine similarity scores
print("Generating COS Sim Matrix...")
similar_tracks = cosine_similarity(
    csr_matrix(
        ([1]*len(df),
         (df["track_id"], df["playlist_id"])
         )
    ),
    dense_output=False)

# Write team information on first row of solution
with open(challenge_solution_csv, "w", newline="") as csv_file:
    csv.writer(csv_file).writerow(["team_info", "Team Gunner", "tgwork11@gmail.com"])

# Open solution file
with open(challenge_solution_csv, "a", newline="") as csv_file:

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
                        using_title(challenge_playlist, connection))

                # Add playlist tracks to input tracks
                if challenge_playlist["tracks"]:

                    # Check if the playlist favors artists. If so, add each artist's top 5 to input tracks
                    derived_tracks = np.append(
                        derived_tracks,
                        using_artists(challenge_playlist, connection))

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
                    ).dot(similar_tracks).toarray().ravel()
                )[::-1]

                # Save track_ids to temp table in order
                pd.DataFrame(
                    {"track_id": rec_array[~np.isin(rec_array, seed_tracks)][:max_tracks],
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
                        connection.cursor().execute(save_query).fetchall()
                    ).ravel().tolist()
                )
