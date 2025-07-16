# Survey Launcher

This project contains a FastAPI backend and a React frontend for uploading and launching surveys.

## Development

Use Docker Compose to start all services:

```bash
docker-compose up
```

The backend exposes `POST /launch` which accepts a JSON survey file and stores it in Postgres.
