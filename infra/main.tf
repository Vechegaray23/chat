resource "docker_network" "survey" {
  name = "survey_net"
}

resource "docker_image" "backend" {
  name = "survey_backend:latest"
  build {
    context    = "${path.module}/.."
    dockerfile = "backend/Dockerfile"
  }
}

resource "docker_container" "backend" {
  name  = "backend"
  image = docker_image.backend.name
  networks_advanced {
    name = docker_network.survey.name
  }
  env = [
    "DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/postgres"
  ]
  volumes = [
    "${path.module}/../survey.schema.json:/app/survey.schema.json"
  ]
  ports {
    internal = 8000
    external = 8000
  }
  depends_on = [docker_container.db]
}

resource "docker_image" "frontend" {
  name = "survey_frontend:latest"
  build {
    context    = "${path.module}/../frontend"
  }
}

resource "docker_container" "frontend" {
  name  = "frontend"
  image = docker_image.frontend.name
  networks_advanced {
    name = docker_network.survey.name
  }
  ports {
    internal = 5173
    external = 5173
  }
  depends_on = [docker_container.backend]
}

resource "docker_container" "db" {
  name  = "db"
  image = "postgres:15-alpine"
  networks_advanced {
    name = docker_network.survey.name
  }
  env = [
    "POSTGRES_PASSWORD=postgres"
  ]
  ports {
    internal = 5432
    external = 5432
  }
}
