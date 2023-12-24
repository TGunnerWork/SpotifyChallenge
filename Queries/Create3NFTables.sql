CREATE TABLE IF NOT EXISTS Playlists (
	playlist_id INTEGER PRIMARY KEY,
	playlist_name TEXT,
	playlist_num_tracks INTEGER,
	playlist_num_albums INTEGER,
	playlist_num_artists INTEGER,
	playlist_duration_ms INTEGER,
	playlist_followers INTEGER);

INSERT INTO Playlists (playlist_id, playlist_name, playlist_num_tracks, playlist_num_albums, playlist_num_artists, playlist_duration_ms, playlist_followers)
SELECT DISTINCT pid, name, num_tracks, num_albums, num_artists, pl_duration_ms, num_followers
FROM RawData;

CREATE TABLE IF NOT EXISTS Tracks (
	track_id INTEGER PRIMARY KEY AUTOINCREMENT,
	track_name TEXT,
	track_duration_ms INTEGER,
	track_uri TEXT);

INSERT INTO Tracks (track_name, track_duration_ms, track_uri)
SELECT DISTINCT track_name, duration_ms, track_uri
FROM RawData;

CREATE TABLE IF NOT EXISTS Albums (
	album_id INTEGER PRIMARY KEY AUTOINCREMENT,
	album_name TEXT,
	album_uri TEXT);

INSERT INTO Albums (album_name, album_uri)
SELECT DISTINCT album_name, album_uri
FROM RawData;

CREATE TABLE IF NOT EXISTS Artists (
	artist_id INTEGER PRIMARY KEY AUTOINCREMENT,
	artist_name TEXT,
	artist_uri TEXT);

INSERT INTO Artists (artist_name, artist_uri)
SELECT DISTINCT artist_name, artist_uri
FROM RawData;

CREATE TABLE IF NOT EXISTS TracksFactTable (
	track_id INTEGER,
	album_id INTEGER,
	artist_id INTEGER);

CREATE INDEX IF NOT EXISTS TFT_track_index
ON TracksFactTable(track_id);

CREATE INDEX IF NOT EXISTS TFT_album_index
ON TracksFactTable(album_id);

CREATE INDEX IF NOT EXISTS TFT_artist_index
ON TracksFactTable(artist_id);

INSERT INTO TracksFactTable (track_id, album_id, artist_id)
SELECT DISTINCT track_id, album_id, artist_id
FROM RawData
JOIN Tracks ON Tracks.track_uri = RawData.track_uri
JOIN Albums ON Albums.album_uri = RawData.album_uri
JOIN Artists ON Artists.artist_uri = RawData.artist_uri

CREATE TABLE IF NOT EXISTS PlaylistsFactTable (
    playlist_id INTEGER,
    track_id INTEGER);

CREATE INDEX IF NOT EXISTS PLFT_playlist_track_index
ON PlaylistsFactTable(playlist_id, track_id);

CREATE INDEX IF NOT EXISTS PLFT_track_playlist_index
ON PlaylistsFactTable(playlist_id, track_id);

INSERT INTO PlaylistsFactTable (playlist_id, track_id)
SELECT DISTINCT pid as playlist_id, track_id
FROM RawData
JOIN Tracks ON Tracks.track_uri = RawData.track_uri;