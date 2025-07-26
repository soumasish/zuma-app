# Zuma App - Docker Setup

This project contains a React TypeScript frontend and FastAPI backend containerized with Docker.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. **Start the entire application:**
   ```
   docker-compose up
   ```

2. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:9000
   - API Docs: http://localhost:9000/redoc

## Ascertain Accuracy
server/seed.py has the data used to seed the database. Please check that data to ascertain accuracy of response.

## Caveats
Chat history isn't persisted(yet) so the system as it stands now is transactional - one time use - for every conversation.


## Database

The SQLite database (`zuma.db`) is automatically created and seeded when the server starts. The database file is persisted in a Docker volume, so your data will survive container restarts.

## Network

Both services communicate over a custom Docker network (`zuma-network`). The frontend can reach the backend at `http://localhost:9000` from the host machine. 