# Survey Launcher

This project contains a FastAPI backend and a React frontend for uploading and launching surveys.
Backend dependencies are listed in `backend/requirements.txt`.


## Development

Use Docker Compose to start all services:

```bash
docker-compose up
```

### Deployment on Railway

Build and deploy containers using the included GitHub Actions workflow. Set the `RAILWAY_TOKEN` secret in your repository and push to `main`:

```bash
git push origin main
```

The workflow runs tests and security scans and then executes `railway up` to deploy the backend.

## Configuration

Define environment variables in a `.env` file at the project root. Docker Compose will load this file automatically. An example configuration looks like:

```bash
DATABASE_URL=/tmp/turns.db
VITE_API_URL=http://localhost:8000
UPLOAD_DIR=uploads
OPENAI_API_KEY=sk-your-openai-key
FRONTEND_DOMAIN=https://your-frontend.example
FORCE_HTTPS=1
SSL_CERTFILE=/path/cert.pem
SSL_KEYFILE=/path/key.pem
```

**Variables**

- `DATABASE_URL` - database URL for storing transcripts and consent. Uses SQLite locally.
- `VITE_API_URL` - base URL for the backend API. Defaults to `http://backend:8000` during container builds.
- `UPLOAD_DIR` - directory where audio files are stored. Defaults to `uploads`.
- `OPENAI_API_KEY` - key used to access OpenAI's transcription API. Defaults to `test`.
- `FRONTEND_DOMAIN` - domain allowed via CORS and used when deploying.
- `FORCE_HTTPS` - set to `1` to redirect all requests to HTTPS.
- `SSL_CERTFILE`/`SSL_KEYFILE` - paths to TLS certificate and key passed to `uvicorn`.
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

Promtail is configured via `promtail.yaml` and started automatically with Docker Compose to forward logs to Grafana Loki.

### Metrics and KPIs

Run the reporting script to obtain basic KPIs from the database:

```bash
python scripts/kpi_report.py
```

The script outputs:
- **KPI-1** total turns processed
- **KPI-2** average transcript length
- **KPI-3** number of recorded consents

Logs from both services are shipped to Grafana Loki using Promtail. Import the provided dashboard JSON in Grafana to visualise errors and request rates.
