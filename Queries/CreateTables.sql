PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS RawData (
    pl_pid INTEGER,
    pl_name TEXT,
    pl_num_tracks INTEGER,
    pl_num_albums INTEGER,
    pl_num_artists INTEGER,
    pl_duration_ms INTEGER,
    pl_num_followers INTEGER,
    pl_collaborative TEXT,
    pl_description TEXT,
    pos INTEGER,
    track_name TEXT,
    album_name TEXT,
    artist_name TEXT,
    duration_ms INTEGER,
    track_uri TEXT,
    album_uri TEXT,
    artist_uri TEXT
    );

CREATE TABLE IF NOT EXISTS Playlists (
	playlist_id INTEGER PRIMARY KEY,
	playlist_name TEXT,
	playlist_description TEXT,
	playlist_num_tracks INTEGER,
	playlist_num_albums INTEGER,
	playlist_num_artists INTEGER,
	playlist_duration_ms INTEGER,
	playlist_followers INTEGER
	);

CREATE TABLE IF NOT EXISTS Artists (
	artist_uri TEXT PRIMARY KEY,
	artist_name TEXT
	);

CREATE TABLE IF NOT EXISTS Albums (
    album_uri TEXT,
    artist_uri TEXT,
    album_name TEXT,
    FOREIGN KEY (artist_uri) REFERENCES Artists (artist_uri),
    PRIMARY KEY (album_uri, artist_uri)
    );

CREATE TABLE IF NOT EXISTS Tracks (
    track_id INTEGER PRIMARY KEY AUTOINCREMENT,
	track_uri TEXT,
	album_uri TEXT,
	artist_uri TEXT,
	track_name TEXT,
	track_duration_ms INTEGER,
	FOREIGN KEY (album_uri) REFERENCES Albums (album_uri),
	FOREIGN KEY (artist_uri) REFERENCES Artists (artist_uri)
	);

CREATE TABLE IF NOT EXISTS PlaylistTracks (
    playlist_id INT,
    track_id INT,
    track_position INT,
    FOREIGN KEY (playlist_id) REFERENCES Playlists (playlist_id),
    FOREIGN KEY (track_id) REFERENCES Tracks (track_id),
    PRIMARY KEY (playlist_id, track_id, track_position)
    );
