import sqlite3
from fastapi.testclient import TestClient
from app.main import app
from app import stt_stream

client = TestClient(app)


def test_stt_stream_inserts_and_returns(tmp_path, monkeypatch):
    # setup in-memory sqlite
    stt_stream.engine = sqlite3.connect(':memory:', check_same_thread=False)
    stt_stream.engine.execute(
        "CREATE TABLE turns (survey_id TEXT, token TEXT, question_id TEXT, role TEXT, audio_url TEXT, transcript TEXT, timestamp TEXT)"
    )

    stt_stream.UPLOAD_DIR = tmp_path
    monkeypatch.setattr(stt_stream, 'transcribe_audio', lambda data: ("hi", 0.9))

    with client.websocket_connect("/stt-stream?survey_id=s1&token=t1&question_id=q1&role=user") as ws:
        ws.send_bytes(b'abc')
        data = ws.receive_json()
    assert data['transcript'] == 'hi'
    assert data['confidence'] == 0.9

    cur = stt_stream.engine.cursor()
    cur.execute("SELECT survey_id, token, question_id, role, transcript FROM turns")
    row = cur.fetchone()
    assert row == ('s1', 't1', 'q1', 'user', 'hi')


def test_multiple_messages_create_rows(tmp_path, monkeypatch):
    stt_stream.engine = sqlite3.connect(':memory:', check_same_thread=False)
    stt_stream.engine.execute(
        "CREATE TABLE turns (survey_id TEXT, token TEXT, question_id TEXT, role TEXT, audio_url TEXT, transcript TEXT, timestamp TEXT)"
    )
    stt_stream.UPLOAD_DIR = tmp_path
    monkeypatch.setattr(stt_stream, 'transcribe_audio', lambda data: ('hi', 0.9))

    for _ in range(3):
        with client.websocket_connect("/stt-stream?survey_id=s1&token=t1&question_id=q1&role=user") as ws:
            ws.send_bytes(b'abc')
            ws.receive_json()

    cur = stt_stream.engine.cursor()
    cur.execute("SELECT COUNT(*) FROM turns")
    count = cur.fetchone()[0]
    assert count == 3
    assert len(list(tmp_path.iterdir())) == 3
