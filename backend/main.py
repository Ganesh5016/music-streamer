const express = require('express');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Initialize SQLite DB
const dbFile = path.resolve(__dirname, 'data', 'music.db');
if (!fs.existsSync(path.dirname(dbFile))) fs.mkdirSync(path.dirname(dbFile));
const db = new sqlite3.Database(dbFile);

// Simple auth simulation middleware
function authMiddleware(req, res, next) {
  const token = req.headers['authorization'];
  if (!token) return res.status(401).json({ error: 'Missing auth token' });
  // In real app verify JWT; here we just set a dummy user
  req.user = { id: 1, username: 'demo_user' };
  next();
}

// Healthcheck
app.get('/health', (req, res) => res.json({ status: 'ok', uptime: process.uptime() }));

// ---------- SONG ROUTES ----------
app.get('/api/songs', (req, res) => {
  db.all('SELECT * FROM songs', [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

app.get('/api/songs/:id', (req, res) => {
  const id = req.params.id;
  db.get('SELECT * FROM songs WHERE id = ?', [id], (err, row) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!row) return res.status(404).json({ error: 'Song not found' });
    res.json(row);
  });
});

// ---------- PLAYLIST ROUTES ----------
app.get('/api/playlists', authMiddleware, (req, res) => {
  const sql = `SELECT p.id, p.name, GROUP_CONCAT(ps.song_id) as songIds
               FROM playlists p LEFT JOIN playlist_songs ps ON p.id = ps.playlist_id
               WHERE p.user_id = ?
               GROUP BY p.id`;
  db.all(sql, [req.user.id], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    const playlists = rows.map(r => ({ id: r.id, name: r.name, songs: r.songIds ? r.songIds.split(',').map(Number) : [] }));
    res.json(playlists);
  });
});

app.post('/api/playlists', authMiddleware, (req, res) => {
  const { name, songIds } = req.body;
  if (!name) return res.status(400).json({ error: 'Playlist name required' });
  db.run('INSERT INTO playlists (name, user_id) VALUES (?, ?)', [name, req.user.id], function(err) {
    if (err) return res.status(500).json({ error: err.message });
    const playlistId = this.lastID;
    if (Array.isArray(songIds) && songIds.length) {
      const placeholders = songIds.map(() => '(?, ?)').join(',');
      const params = [];
      songIds.forEach(sid => { params.push(playlistId, sid); });
      const sql = `INSERT INTO playlist_songs (playlist_id, song_id) VALUES ${placeholders}`;
      db.run(sql, params, err2 => {
        if (err2) return res.status(500).json({ error: err2.message });
        res.status(201).json({ id: playlistId, name, songs: songIds });
      });
    } else {
      res.status(201).json({ id: playlistId, name, songs: [] });
    }
  });
});

app.put('/api/playlists/:id', authMiddleware, (req, res) => {
  const pid = req.params.id;
  const { name, songIds } = req.body;
  db.run('UPDATE playlists SET name = ? WHERE id = ? AND user_id = ?', [name, pid, req.user.id], function(err) {
    if (err) return res.status(500).json({ error: err.message });
    db.run('DELETE FROM playlist_songs WHERE playlist_id = ?', [pid], err2 => {
      if (err2) return res.status(500).json({ error: err2.message });
      if (Array.isArray(songIds) && songIds.length) {
        const placeholders = songIds.map(() => '(?, ?)').join(',');
        const params = [];
        songIds.forEach(sid => { params.push(pid, sid); });
        const sql = `INSERT INTO playlist_songs (playlist_id, song_id) VALUES ${placeholders}`;
        db.run(sql, params, err3 => {
          if (err3) return res.status(500).json({ error: err3.message });
          res.json({ id: pid, name, songs: songIds });
        });
      } else {
        res.json({ id: pid, name, songs: [] });
      }
    });
  });
});

app.delete('/api/playlists/:id', authMiddleware, (req, res) => {
  const pid = req.params.id;
  db.run('DELETE FROM playlists WHERE id = ? AND user_id = ?', [pid, req.user.id], function(err) {
    if (err) return res.status(500).json({ error: err.message });
    db.run('DELETE FROM playlist_songs WHERE playlist_id = ?', [pid]);
    res.status(204).send();
  });
});

// ---------- ERROR HANDLER ----------
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal Server Error' });
});

app.listen(PORT, () => console.log(`Server listening on port ${PORT}`));