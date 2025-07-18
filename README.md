# Survey Launcher

This project contains a FastAPI backend and a React frontend for uploading and launching surveys.
Backend dependencies are listed in `backend/requirements.txt`.


## Development

Use Docker Compose to start all services:

```bash
docker-compose up
```

## Configuration

Define environment variables in a `.env` file at the project root. Docker Compose will load this file automatically. An example configuration looks like:

```bash
DATABASE_URL=/tmp/turns.db
VITE_API_URL=http://localhost:8000
UPLOAD_DIR=uploads
OPENAI_API_KEY=sk-your-openai-key
```

**Variables**

- `DATABASE_URL` - path to the SQLite database file used by the backend. Defaults to `:memory:` when not set.
- `VITE_API_URL` - base URL for the backend API. Defaults to `http://backend:8000` during container builds.
- `UPLOAD_DIR` - directory where audio files are stored. Defaults to `uploads`.
- `OPENAI_API_KEY` - key used to access OpenAI's transcription API. Defaults to `test`.
  When left at the default value the backend does not contact the OpenAI service
  and instead returns an empty transcript immediately. This keeps local tests and
  the bundled load test fast even without network access.

The OpenAI key is obtained from the [OpenAI dashboard](https://platform.openai.com/account/api-keys).


The backend exposes `POST /launch` which accepts a JSON survey file and stores it in a local database.

### Testing

Backend tests can be run with `pytest`:

```bash
pytest backend/app/tests
```

Frontend tests are executed from the `frontend` directory using npm:

```bash
npm test
```

These commands mirror the steps defined in the CI workflow.

To run the WebSocket load test locally install the `websockets` package and execute:

```bash
pip install websockets
python scripts/load_test_script.py
```
