import re
import numpy as np
from collections import Counter


def using_title(playlist, conn):

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


def using_artists(playlist, conn):
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
