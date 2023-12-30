WITH pls AS (SELECT playlist_id
FROM PlaylistTracks
WHERE playlist_id IN
	(SELECT playlist_id
	FROM Playlists
	WHERE TRIM(LOWER(REPLACE(playlist_name, ' ', ''))) LIKE '%' || ? || '%' 
	OR ? LIKE '%' || TRIM(LOWER(REPLACE(playlist_name, ' ', ''))) || '%')
GROUP BY playlist_id
ORDER BY COUNT(*) DESC
LIMIT 5)

SELECT DISTINCT track_id
FROM PlaylistTracks
WHERE playlist_id IN
	(SELECT playlist_id
	FROM Playlists
	WHERE LOWER(REPLACE(playlist_name, ' ', '')) LIKE '%' || ? || '%'
	OR ? LIKE '%' || LOWER(REPLACE(playlist_name, ' ', '')) || '%')