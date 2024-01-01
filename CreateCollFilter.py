import pandas as pd
import sqlite3
from scipy.sparse import csr_matrix, save_npz
from sklearn.metrics.pairwise import cosine_similarity

# Gather unique Playlist-Track interactions
with sqlite3.connect("Spotify.db") as conn:
    df = pd.read_sql_query(
        "SELECT DISTINCT playlist_id, track_id FROM PlaylistTracks;",
        conn
    )

# Transform into sparse matrix
csr = csr_matrix(([1]*len(df), (df["playlist_id"], df["track_id"])))

# Generate similarity score matrix
sim = cosine_similarity(csr.T, dense_output=False)

# Save sim matrix to hard drive if not run as a subprocess
if __name__ == "__main__":
    print("Saving matrix")
    save_npz("col_fil_spotify.npz", sim)
