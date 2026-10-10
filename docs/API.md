## REST API Documentation

### Authentication (Simulation)
All protected routes require an `Authorization` header with any non‑empty token value. The middleware injects a dummy user `{ id: 1, username: 'demo_user' }`.

### Health Check
- **GET** `/health`
  - **Response**: `{ status: 'ok', uptime: <seconds> }`
  - **Status**: `200`

### Songs
- **GET** `/api/songs`
  - **Description**: Retrieve the full catalog of songs.
  - **Response**: `[{ id, title, artist, album, genre, duration, url, artwork, created_at }, ...]`
  - **Status**: `200`

- **GET** `/api/songs/:id`
  - **Params**: `id` – song identifier.
  - **Response**: Single song object.
  - **Status**: `200` or `404` if not found.

### Playlists (Protected)
All playlist routes require the `Authorization` header.

- **GET** `/api/playlists`
  - **Response**: `[{ id, name, songs: [songId, ...] }, ...]`
  - **Status**: `200`

- **POST** `/api/playlists`
  - **Body**: `{ name: string, songIds?: number[] }`
  - **Response**: Created playlist object with generated `id`.
  - **Status**: `201` or `400` for validation errors.

- **PUT** `/api/playlists/:id`
  - **Params**: `id` – playlist identifier.
  - **Body**: `{ name?: string, songIds?: number[] }`
  - **Response**: Updated playlist object.
  - **Status**: `200` or `400`/`404`.

- **DELETE** `/api/playlists/:id`
  - **Params**: `id` – playlist identifier.
  - **Response**: No content.
  - **Status**: `204` or `404`.

### Error Responses
All error responses follow the shape:
```json
{ "error": "Human readable message" }
```
Typical status codes: `400` (bad request), `401` (unauthorized), `404` (not found), `500` (internal server error).