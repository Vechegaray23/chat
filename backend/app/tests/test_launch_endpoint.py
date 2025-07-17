from fastapi.testclient import TestClient
from pathlib import Path
import json

from app.main import app

client = TestClient(app)

SCHEMA_PATH = Path(__file__).resolve().parents[3] / 'survey.schema.json'

with open(SCHEMA_PATH) as f:
    VALID_SURVEY = json.load(f)


def test_launch_success(tmp_path):
    survey = {
        "title": "Test",
        "questions": [
            {"id": "q1", "type": "text", "text": "Hello"}
        ]
    }
    file = tmp_path / "survey.json"
    file.write_text(json.dumps(survey))
    with file.open('rb') as f:
        response = client.post('/launch', files={'file': ('survey.json', f, 'application/json')})
    assert response.status_code == 200
    data = response.json()
    assert 'survey_id' in data
    assert 'link' in data

def test_launch_invalid(tmp_path):
    file = tmp_path / "bad.json"
    file.write_text(json.dumps({"title": "Invalid"}))
    with file.open('rb') as f:
        response = client.post('/launch', files={'file': ('bad.json', f, 'application/json')})
    assert response.status_code == 422
