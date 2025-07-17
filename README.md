# Survey Launcher

This project contains a FastAPI backend and a React frontend for uploading and launching surveys.
Backend dependencies are listed in `backend/requirements.txt`. If you use Postgres, install a compatible driver such as `psycopg2-binary` separately.


## Development

Use Docker Compose to start all services:

```bash
docker-compose up
```

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