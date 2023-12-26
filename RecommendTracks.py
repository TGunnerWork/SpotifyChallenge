import numpy as np
import pandas as pd
import sqlite3
from sklearn.metrics.pairwise import cosine_similarity
import scipy.sparse as sp


with sqlite3.connect('Spotify.db') as conn:
    df = pd.read_sql_query(
        "SELECT DISTINCT playlist_id, track_id FROM PlaylistTracks;",
        conn)

# create sparse matrix
csr = sp.csr_matrix(([1]*len(df), (df['playlist_id'], df['track_id'])))

# generate similarity scores
sim = cosine_similarity(csr.T, dense_output=False)

sp.save_npz("col_fil_spotify.npz", sim)

# Using 'new' playlist

## get track IDs
new_playlist = [1, 2, 3]

## convert to sparse matrix row
csr_pl = sp.csr_matrix(list(np.isin(np.arange(csr.shape[1]), new_playlist).astype(int)))

## generate 500 new recommonedations
rec_tracks = list(filter(lambda x: x not in test_list, list(np.argsort(csr_pl.dot(sim).toarray().ravel())[::-1])))[:500]



