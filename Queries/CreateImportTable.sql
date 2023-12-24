CREATE TABLE IF NOT EXISTS RawData (
    pid INTEGER,
    name TEXT,
    num_tracks INTEGER,
    num_albums INTEGER,
    num_artists INTEGER,
    pl_duration_ms INTEGER,
    num_followers INTEGER,
    collaborative TEXT,
    pos INTEGER,
    track_name TEXT,
    album_name TEXT,
    artist_name TEXT,
    duration_ms INTEGER,
    track_uri TEXT,
    album_uri TEXT,
    artist_uri TEXT);

CREATE INDEX IF NOT EXISTS RawData_pid
ON RawData (pid);

CREATE INDEX IF NOT EXISTS RawData_tracks
ON RawData (track_uri);

CREATE INDEX IF NOT EXISTS RawData_artists
ON RawData (artist_uri);

CREATE INDEX IF NOT EXISTS RawData_albums
ON RawData (album_uri);
