import os
import io
import uuid
import importlib
import sqlite3
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

DATABASE_URL = os.getenv("DATABASE_URL", ":memory:")
engine = sqlite3.connect(DATABASE_URL, check_same_thread=False)
engine.execute(
    "CREATE TABLE IF NOT EXISTS turns (survey_id TEXT, token TEXT, question_id TEXT, role TEXT, audio_url TEXT, transcript TEXT, timestamp TEXT)"
)

router = APIRouter()

MAX_CHUNK_BYTES = 64000  # approx 2s of 16kHz 16bit audio


def get_supabase_client():
    try:
        supabase_mod = importlib.import_module("supabase")
    except ModuleNotFoundError as e:  # pragma: no cover - handled in tests via mock
        raise RuntimeError("supabase module not installed") from e
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    return supabase_mod.create_client(url, key)


def transcribe_audio(data: bytes):
    try:
        openai = importlib.import_module("openai")
    except ModuleNotFoundError as e:  # pragma: no cover - handled in tests via mock
        raise RuntimeError("openai module not installed") from e
    openai.api_key = os.environ.get("OPENAI_API_KEY", "test")
    file_obj = io.BytesIO(data)
    file_obj.name = "audio.wav"
    resp = openai.audio.transcriptions.create(model="whisper-1", file=file_obj)
    text_out = getattr(resp, "text", "") if not isinstance(resp, dict) else resp.get("text", "")
    confidence = getattr(resp, "confidence", 1.0) if not isinstance(resp, dict) else resp.get("confidence", 1.0)
    return text_out, float(confidence)


@router.websocket("/stt-stream")
async def stt_stream(ws: WebSocket, survey_id: str, token: str, question_id: str, role: str):
    await ws.accept()
    supabase = get_supabase_client()
    bucket = os.getenv("SUPABASE_BUCKET", "audio")

    while True:
        try:
            data = await ws.receive_bytes()
        except WebSocketDisconnect:
            break

        if len(data) > MAX_CHUNK_BYTES:
            await ws.close(code=1003)
            break

        audio_name = f"{uuid.uuid4()}.wav"
        supabase.storage.from_(bucket).upload(audio_name, data)
        signed = supabase.storage.from_(bucket).create_signed_url(audio_name, 604800)
        audio_url = signed["signedURL"] if isinstance(signed, dict) else signed

        transcript, confidence = transcribe_audio(data)

        cur = engine.cursor()
        cur.execute(
            "INSERT INTO turns (survey_id, token, question_id, role, audio_url, transcript, timestamp)"
            " VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
            (survey_id, token, question_id, role, audio_url, transcript),
        )
        engine.commit()

        await ws.send_json({"transcript": transcript, "confidence": confidence})
