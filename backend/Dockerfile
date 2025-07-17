FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt

COPY backend/app /app/app
COPY survey.schema.json /app/survey.schema.json
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
