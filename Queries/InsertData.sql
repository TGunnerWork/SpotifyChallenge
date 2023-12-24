INSERT INTO Playlists (
    playlist_id, playlist_name, playlist_num_tracks, playlist_num_albums,
    playlist_num_artists, playlist_duration_ms, playlist_followers)
SELECT DISTINCT pl_pid, pl_name, pl_num_tracks, pl_num_albums, pl_num_artists, pl_duration_ms, pl_num_followers
FROM RawData;

CREATE INDEX IF NOT EXISTS RawData_track_uri ON RawData (track_uri);
CREATE INDEX IF NOT EXISTS RawData_album_uri ON RawData (album_uri);
CREATE INDEX IF NOT EXISTS RawData_artist_uri ON RawData (artist_uri);
CREATE INDEX IF NOT EXISTS RawData_track_artist_album ON RawData (track_uri, artist_uri, album_uri);
CREATE INDEX IF NOT EXISTS RawData_pl_track ON RawData (pl_pid, track_uri);

INSERT INTO Tracks (track_name, track_duration_ms, track_uri)
SELECT DISTINCT track_name, duration_ms, track_uri
FROM RawData;

INSERT INTO Albums (album_name, album_uri)
SELECT DISTINCT album_name, album_uri
FROM RawData;

INSERT INTO Artists (artist_name, artist_uri)
SELECT DISTINCT artist_name, artist_uri
FROM RawData;

CREATE INDEX IF NOT EXISTS Tracks_track_uri ON Tracks (track_uri);
CREATE INDEX IF NOT EXISTS Albums_album_uri ON Albums (album_uri);
CREATE INDEX IF NOT EXISTS Artists_artist_uri ON Artists (artist_uri);

INSERT INTO TracksFactTable (track_id, album_id, artist_id)
SELECT track_id, album_id, artist_id
FROM (
    SELECT DISTINCT track_uri, album_uri, artist_uri
    FROM RawData) AS Raw
JOIN Tracks, Albums, Artists
ON Tracks.track_uri = Raw.track_uri
AND Albums.album_uri = Raw.album_uri
AND Artists.artist_uri = Raw.artist_uri;

INSERT INTO PlaylistsFactTable (playlist_id, track_id)
SELECT pl_pid as playlist_id, track_id
FROM (SELECT DISTINCT pl_pid, track_uri FROM RawData) AS Raw
JOIN Tracks
ON Tracks.track_uri = Raw.track_uri;

CREATE INDEX PFT_pl_track ON PlaylistsFactTable (playlist_id, track_id);
CREATE INDEX PFT_track_pl ON PlaylistsFactTable (track_id, playlist_id);
