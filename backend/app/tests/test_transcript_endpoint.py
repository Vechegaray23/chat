import sqlite3
from fastapi.testclient import TestClient
from app.main import app
from app import stt_stream
from app import flow_engine

client = TestClient(app)


def setup_test_env(tmp_path):
    stt_stream.engine = sqlite3.connect(':memory:', check_same_thread=False)
    stt_stream.engine.execute(
        "CREATE TABLE turns (survey_id TEXT, token TEXT, question_id TEXT, role TEXT, audio_url TEXT, transcript TEXT, timestamp TEXT)"
    )
    flow_engine.TRANSCRIPTS_DIR = tmp_path


def test_transcript_generation(tmp_path):
    setup_test_env(tmp_path)
    cur = stt_stream.engine.cursor()
    cur.execute(
        "INSERT INTO turns (survey_id, token, question_id, role, audio_url, transcript, timestamp) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
        ("s1", "t1", "q1", "user", "file.wav", "hello"),
    )
    stt_stream.engine.commit()

    response = client.get("/transcript/s1/t1")
    assert response.status_code == 200
    data = response.json()
    assert data["survey_id"] == "s1"
    assert len(data["turns"]) == 1
    assert data["turns"][0]["transcript"] == "hello"
