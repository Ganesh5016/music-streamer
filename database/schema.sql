-- Database Schema for Music Streamer
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE songs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  artist TEXT NOT NULL,
  album TEXT,
  genre TEXT,
  duration INTEGER, -- seconds
  url TEXT NOT NULL,
  artwork TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE playlists (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  user_id INTEGER NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE playlist_songs (
  playlist_id INTEGER NOT NULL,
  song_id INTEGER NOT NULL,
  position INTEGER,
  PRIMARY KEY (playlist_id, song_id),
  FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
  FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
);

CREATE TABLE activity_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  action TEXT NOT NULL,
  details TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Indexes for performance
CREATE INDEX idx_songs_artist ON songs(artist);
CREATE INDEX idx_playlist_user ON playlists(user_id);

-- Sample seed data
INSERT INTO users (username, password_hash) VALUES ('demo_user', 'hashed_dummy');

INSERT INTO songs (title, artist, album, genre, duration, url, artwork) VALUES
('Song One', 'Artist A', 'Album X', 'Pop', 210, 'https://example.com/audio/song1.mp3', 'https://example.com/artwork/art1.jpg'),
('Song Two', 'Artist B', 'Album Y', 'Rock', 185, 'https://example.com/audio/song2.mp3', 'https://example.com/artwork/art2.jpg'),
('Song Three', 'Artist C', 'Album Z', 'Jazz', 240, 'https://example.com/audio/song3.mp3', 'https://example.com/artwork/art3.jpg');

INSERT INTO playlists (name, user_id) VALUES ('My Favorites', 1);
INSERT INTO playlist_songs (playlist_id, song_id, position) VALUES (1, 1, 1), (1, 3, 2);