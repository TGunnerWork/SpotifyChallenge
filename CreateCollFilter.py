import pandas as pd
import sqlite3
from scipy.sparse import csr_matrix, save_npz
from sklearn.metrics.pairwise import cosine_similarity

# gather information
with sqlite3.connect('Spotify.db') as conn:
    df = pd.read_sql_query(
        "SELECT DISTINCT playlist_id, track_id FROM PlaylistTracks;",
        conn
    )

# create sparse matrix
csr = csr_matrix(([1]*len(df), (df['playlist_id'], df['track_id'])))

# generate similarity scores
sim = cosine_similarity(csr.T, dense_output=False)

# If this script is being run on its own, save the matrix.
if __name__ == '__main__':
    print("Saving matrix")
    save_npz("col_fil_spotify.npz", sim)
