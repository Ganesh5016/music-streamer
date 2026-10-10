// test.js - Jest + Supertest integration tests
const request = require('supertest');
const express = require('express');
const fs = require('fs');
const path = require('path');

// Import the server (assuming server exports the app for testing)
const app = require('./server'); // server.js must export the Express app

describe('Healthcheck', () => {
  it('should return status ok', async () => {
    const res = await request(app).get('/health');
    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('ok');
  });
});

describe('Songs API', () => {
  it('should fetch all songs', async () => {
    const res = await request(app).get('/api/songs');
    expect(res.statusCode).toBe(200);
    expect(Array.isArray(res.body)).toBe(true);
  });

  it('should fetch a single song by id', async () => {
    const all = await request(app).get('/api/songs');
    const firstId = all.body[0].id;
    const res = await request(app).get(`/api/songs/${firstId}`);
    expect(res.statusCode).toBe(200);
    expect(res.body.id).toBe(firstId);
  });
});

describe('Playlists API (protected)', () => {
  const authHeader = { Authorization: 'Bearer dummy-token' };

  let createdId;

  it('should create a new playlist', async () => {
    const res = await request(app)
      .post('/api/playlists')
      .set(authHeader)
      .send({ name: 'Test Playlist', songIds: [1, 2] });
    expect(res.statusCode).toBe(201);
    expect(res.body.name).toBe('Test Playlist');
    createdId = res.body.id;
  });

  it('should retrieve playlists for the user', async () => {
    const res = await request(app).get('/api/playlists').set(authHeader);
    expect(res.statusCode).toBe(200);
    const found = res.body.find(p => p.id === createdId);
    expect(found).toBeDefined();
    expect(found.songs).toContain(1);
  });

  it('should update the playlist', async () => {
    const res = await request(app)
      .put(`/api/playlists/${createdId}`)
      .set(authHeader)
      .send({ name: 'Renamed Playlist', songIds: [2, 3] });
    expect(res.statusCode).toBe(200);
    expect(res.body.name).toBe('Renamed Playlist');
    expect(res.body.songs).toContain(3);
  });

  it('should delete the playlist', async () => {
    const res = await request(app).delete(`/api/playlists/${createdId}`).set(authHeader);
    expect(res.statusCode).toBe(204);
  });
});

// To run: add "test": "jest" to package.json scripts and execute npm test