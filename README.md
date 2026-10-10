# Music Streamer

A modern, single‑page music streaming web app with a full‑stack Node.js backend, SQLite storage, and a glassmorphism dark‑mode UI.

## Architecture Overview
- **Frontend**: Vanilla HTML5, CSS (custom variables, dark mode, glass effect) and JavaScript for state management, CRUD operations, and audio playback.
- **Backend**: Node.js + Express exposing a RESTful JSON API, SQLite for persistence, CORS, body parsing, simple auth simulation, and robust error handling.
- **Database**: SQLite with tables for users, songs, playlists, playlist‑song junction, and activity logs.
- **Containerization**: Multi‑stage Docker build, non‑root user, health‑check endpoint.

## Setup & Run
1. **Clone the repo**
   ```bash
   git clone <repo-url>
   cd music-streamer
   ```
2. **Run with Docker**
   ```bash
   docker build -t music-streamer .
   docker run -p 3000:3000 music-streamer
   ```
   The app will be reachable at `http://localhost:3000`.
3. **Run locally (without Docker)**
   ```bash
   npm install
   node server.js
   ```
   Ensure the `data` folder exists; the SQLite DB will be created automatically.

## Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Port on which the Express server listens | `3000` |
| `NODE_ENV` | Node environment (`development`/`production`) | `production` |

## API Documentation
See the dedicated **API.md** file for a complete reference of all endpoints, request/response schemas, and status codes.

## Development
- Frontend code lives in `public/index.html` (single‑page app).
- Backend code in `server.js`.
- Database schema in `schema.sql`.
- Tests in `test.js` (run with `npm test`).

## License
MIT © 2026 Music Streamer Team