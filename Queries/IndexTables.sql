CREATE INDEX PlaylistTracks_playlist_id ON PlaylistTracks(playlist_id);

CREATE INDEX PlaylistTracks_track_id ON PlaylistTracks(track_id);

CREATE INDEX PlaylistTracks_playlist_track_id ON PlaylistTracks(playlist_id, track_id);

CREATE INDEX Playlists_playlist_name ON Playlists(playlist_name);

CREATE INDEX Playlists_playlist_num_tracks ON Playlists(playlist_num_tracks);

CREATE INDEX Tracks_artist_uri ON Tracks(artist_uri);

CREATE INDEX Tracks_track_uri ON Tracks(track_uri);

CREATE INDEX Tracks_track_id ON Tracks(track_id);
