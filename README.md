# Survey Launcher

This project contains a FastAPI backend and a React frontend for uploading and launching surveys.
Backend dependencies are listed in `backend/requirements.txt`. A Postgres driver
(for example `psycopg2-binary`) is required when using a Postgres database.


## Development

Use Docker Compose to start all services:

```bash
docker-compose up
```

## Configuration

Define environment variables in a `.env` file at the project root. Docker Compose will load this file automatically and you can `source .env` before running Terraform so the same values are used. An example configuration looks like:

```bash
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/postgres
POSTGRES_PASSWORD=postgres
VITE_API_URL=http://localhost:8000
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-api-key
SUPABASE_BUCKET=audio
OPENAI_API_KEY=sk-your-openai-key
```

**Variables**

- `DATABASE_URL` - connection string used by the backend to store speech transcription data. Defaults to `:memory:` when not set.
- `POSTGRES_PASSWORD` - password for the Postgres container, default `postgres`.
- `VITE_API_URL` - base URL for the backend API. Defaults to `http://backend:8000` during container builds.
- `SUPABASE_URL` - REST endpoint for your Supabase project.
- `SUPABASE_KEY` - API key from Supabase.
- `SUPABASE_BUCKET` - bucket for uploaded audio files. Defaults to `audio`.
- `OPENAI_API_KEY` - key used to access OpenAI's transcription API. Defaults to `test`.

Supabase credentials can be generated after creating a project at [Supabase](https://app.supabase.com). The OpenAI key is obtained from the [OpenAI dashboard](https://platform.openai.com/account/api-keys).


### Infrastructure as Code

Terraform configuration is provided in the `infra` directory. It replicates the
Docker Compose setup using the Docker provider.

To provision the environment with Terraform:

```bash
cd infra
terraform init
terraform apply
```

The backend exposes `POST /launch` which accepts a JSON survey file and stores it in Postgres.

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