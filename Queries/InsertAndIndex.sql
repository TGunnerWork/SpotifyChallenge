INSERT INTO PlayLists
SELECT DISTINCT
	pl_pid AS playlist_id,
	pl_name AS playlist_name,
	pl_description AS playlist_description,
	pl_num_tracks AS playlist_num_tracks,
	pl_num_albums AS playlist_num_albums,
	pl_num_artists AS playlist_num_artists,
	pl_duration_ms AS playlist_duration_ms,
	pl_num_followers AS playlist_followers
FROM RawData;

INSERT INTO Artists
SELECT DISTINCT
    artist_uri,
    artist_name
FROM RawData;

INSERT INTO Albums
SELECT DISTINCT
    album_uri,
    artist_uri,
    album_name
FROM RawData;

INSERT INTO Tracks
SELECT DISTINCT
    track_uri,
    album_uri,
    artist_uri,
    track_name,
    duration_ms AS track_duration_ms
FROM RawData;

INSERT INTO PlaylistTracks
SELECT pl_pid AS playlist_id, track_uri, pos AS track_position
FROM RawData;
