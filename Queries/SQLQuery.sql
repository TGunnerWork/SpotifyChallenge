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