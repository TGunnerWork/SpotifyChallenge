CREATE TABLE IF NOT EXISTS RawData (
    pid INTEGER,
    name TEXT,
    num_followers INTEGER,
    track_name TEXT,
    duration_ms INTEGER,
    album_name TEXT,
    artist_name TEXT,
    track_uri TEXT,
    album_uri TEXT,
    artist_uri TEXT
);

CREATE TABLE IF NOT EXISTS PlaylistTracks (
	playlist_id INTEGER,
	track_id INTEGER
);

CREATE TABLE IF NOT EXISTS Playlists (
	playlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
	playlist_name TEXT,
	playlist_followers INTEGER,
	playlist_spotify_id TEXT
);

CREATE TABLE IF NOT EXISTS Tracks (
	track_id INTEGER PRIMARY KEY AUTOINCREMENT,
	track_name TEXT,
	track_duration INTEGER,
	track_album INTEGER,
	track_spotify_id TEXT
);

CREATE TABLE IF NOT EXISTS Albums (
	album_id INTEGER PRIMARY KEY AUTOINCREMENT,
	album_name TEXT,
	album_artist INTEGER,
	album_spotify_id TEXT
);

CREATE TABLE IF NOT EXISTS Artists (
	artist_id INTEGER PRIMARY KEY AUTOINCREMENT,
	artist_name TEXT,
	artist_spotify_id TEXT
);

