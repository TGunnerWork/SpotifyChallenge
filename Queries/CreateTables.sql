CREATE TABLE IF NOT EXISTS PlaylistTracks (
	track_id INT,
	pl_id INT	
);

CREATE TABLE IF NOT EXISTS Playlists (
	pl_id INT PRIMARY KEY AUTOINCREMENT,
	pl_name TEXT,
	pl_followers INT,
	pl_spotify_id TEXT
);

CREATE TABLE IF NOT EXISTS Tracks (
	track_id INT PRIMARY KEY AUTOINCREMENT,
	track_name TEXT,
	track_duration INT,
	track_album INT,
	track_spotify_id TEXT
);

CREATE TABLE IF NOT EXISTS Albums (
	album_id INT PRIMARY KEY AUTOINCREMENT,
	album_name TEXT,
	album_artist INT,
	album_spotify_id TEXT
);

CREATE TABLE IF NOT EXISTS Artists (
	artist_id INT PRIMARY KEY AUTOINCREMENT,
	artist_name TEXT,
	artist_spotify_id TEXT
);

