FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt

COPY backend/app /app/app
COPY backend/start.sh /app/start.sh
COPY survey.schema.json /app/survey.schema.json
RUN pip install -r requirements.txt
RUN chmod +x /app/start.sh
RUN mkdir -p /var/log
CMD /app/start.sh | tee /var/log/backend.log
