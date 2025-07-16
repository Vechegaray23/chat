FROM python:3.12-slim
WORKDIR /app
COPY ./app /app/app
COPY survey.schema.json /app/survey.schema.json
RUN pip install fastapi uvicorn[standard] sqlalchemy jsonschema
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
