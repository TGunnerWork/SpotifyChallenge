INSERT INTO Artists (artist_name, artist_spotify_id)
SELECT DISTINCT artist_name, artist_uri
FROM RawData;

INSERT INTO Albums (album_name, album_artist, album_spotify_id)
SELECT DISTINCT album_name, Artists.artist_id, album_uri
FROM RawData
JOIN Artists
ON Artists.artist_spotify_id = RawData.artist_uri;

INSERT INTO Tracks (track_name, track_duration, track_album, track_spotify_id)
SELECT track_name, duration_ms, Albums.album_id, track_uri
FROM (
    SELECT DISTINCT track_name, duration_ms, track_uri, album_uri
    FROM RawData
    ) AS Raw
JOIN Albums
ON Raw.album_uri = Albums.album_spotify_id
LIMIT 10;