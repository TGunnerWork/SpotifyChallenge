CREATE INDEX idx_RD_track_uri ON RawData(track_uri);
CREATE INDEX idx_RD_album_uri ON RawData(album_uri);
CREATE INDEX idx_RD_artist_uri ON RawData(artist_uri);
CREATE INDEX midx_RD_playlist_track ON RawData(pl_id, track_uri);

INSERT INTO Playlists (playlist_id, playlist_name)
SELECT DISTINCT
	pl_pid AS playlist_id,
	pl_name AS playlist_name
FROM RawData;

CREATE INDEX idx_P_playlist_name ON Playlists(playlist_name);

INSERT INTO Artists (artist_uri, artist_name)
SELECT DISTINCT
    artist_uri,
    artist_name
FROM RawData;

INSERT INTO Albums (album_uri, artist_uri, album_name)
SELECT DISTINCT
    album_uri,
    artist_uri,
    album_name
FROM RawData;

INSERT INTO Tracks (track_uri, album_uri, artist_uri, track_name, track_duration_ms)
SELECT DISTINCT
    track_uri,
    album_uri,
    artist_uri,
    track_name
FROM RawData;

CREATE INDEX idx_T_track_uri ON Tracks(track_uri);
CREATE INDEX idx_T_artist_uri ON Tracks(artist_uri);
CREATE INDEX idx_T_track_id ON Tracks(track_id);

INSERT INTO PlaylistTracks (playlist_id, track_id, track_position)
SELECT pl_pid, track_id, pos
FROM RawData
JOIN Tracks ON Tracks.track_uri = RawData.track_uri;

CREATE INDEX idx_PT_playlist_id ON PlaylistTracks(playlist_id);
CREATE INDEX idx_PT_track_id ON PlaylistTracks(track_id);
CREATE INDEX midx_PT_playlist_track ON PlaylistTracks(playlist_id, track_id);

DROP INDEX idx_RD_track_uri;
DROP INDEX idx_RD_album_uri;
DROP INDEX idx_RD_artist_uri;
DROP INDEX midx_RD_playlist_track;