PRAGMA foreign_keys = ON;

CREATE TABLE RawData (
    pl_pid INTEGER,
    pl_name TEXT,
    pos INTEGER,
    track_name TEXT,
    artist_name TEXT,
    track_uri TEXT,
    artist_uri TEXT
    );

CREATE TABLE Playlists (
	playlist_id INTEGER PRIMARY KEY,
	playlist_name TEXT
	);

CREATE TABLE Artists (
	artist_uri TEXT PRIMARY KEY,
	artist_name TEXT
	);

CREATE TABLE Tracks (
    track_id INTEGER PRIMARY KEY AUTOINCREMENT,
    track_uri TEXT,
	artist_uri TEXT,
	track_name TEXT,
	FOREIGN KEY (artist_uri) REFERENCES Artists (artist_uri)
	);

CREATE TABLE PlaylistTracks (
    playlist_id INT,
    track_id INT,
    track_position INT,
    FOREIGN KEY (playlist_id) REFERENCES Playlists (playlist_id),
    FOREIGN KEY (track_id) REFERENCES Tracks (track_id),
    PRIMARY KEY (playlist_id, track_id, track_position)
    );
