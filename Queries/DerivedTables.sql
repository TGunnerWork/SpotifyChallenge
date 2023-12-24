CREATE TABLE IF NOT EXISTS Tracks (
	track_id INTEGER PRIMARY KEY AUTOINCREMENT,
	track_name TEXT,
	track_duration_ms INTEGER,
	track_uri TEXT);

CREATE TABLE IF NOT EXISTS Albums (
	album_id INTEGER PRIMARY KEY AUTOINCREMENT,
	album_name TEXT,
	album_uri TEXT);

CREATE TABLE IF NOT EXISTS Artists (
	artist_id INTEGER PRIMARY KEY AUTOINCREMENT,
	artist_name TEXT,
	artist_uri TEXT);

CREATE TABLE IF NOT EXISTS Playlists (
	playlist_id INTEGER PRIMARY KEY,
	playlist_name TEXT,
	playlist_num_tracks INTEGER,
	playlist_num_albums INTEGER,
	playlist_num_artists INTEGER,
	playlist_duration_ms INTEGER,
	playlist_followers INTEGER);

CREATE TABLE IF NOT EXISTS TracksFactTable (
	track_id INTEGER,
	album_id INTEGER,
	artist_id INTEGER);

CREATE TABLE IF NOT EXISTS PlaylistsFactTable (
    playlist_id INTEGER,
    track_id INTEGER);