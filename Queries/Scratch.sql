WITH PopularTrack AS (
    SELECT track_id
    FROM PlaylistsFactTable
    GROUP BY track_id
    ORDER BY COUNT(playlist_id) DESC
    LIMIT 1
)

SELECT DISTINCT ft.track_id
FROM PlaylistsFactTable ft
JOIN PlaylistsFactTable pt ON ft.playlist_id = pt.playlist_id
WHERE pt.track_id IN (SELECT * FROM PopularTrack)
AND ft.track_id NOT IN (SELECT * FROM PopularTrack);

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
