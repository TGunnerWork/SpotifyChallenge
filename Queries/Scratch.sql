SELECT DISTINCT track_id
FROM PlaylistTracks
WHERE playlist_id =
    (SELECT playlist_id
    FROM Playlists
    WHERE LOWER(REPLACE(playlist_name, ' ', '')) = '{}'
    ORDER BY playlist_num_tracks DESC
    LIMIT 1);

SELECT DISTINCT track_id
FROM PlaylistTracks
WHERE playlist_id =
    (SELECT playlist_id
    FROM Playlists
    WHERE '%' || LOWER(REPLACE(playlist_name, ' ', '')) || '%' LIKE '%{}%'
    ORDER BY playlist_num_tracks DESC
    LIMIT 1);

SELECT track_id
FROM Tracks
WHERE artist_uri
IN ({});

SELECT COUNT(*)
FROM Tracks;

SELECT track_id
FROM Tracks
WHERE track_uri
IN ({});

SELECT track_uri
FROM TrackTemp
JOIN Tracks
ON TrackTemp.track_id = Tracks.track_id;
