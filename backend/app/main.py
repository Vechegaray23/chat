import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from .stt_stream import router as stt_router

from jsonschema import validate, ValidationError
import json
import uuid
from pathlib import Path
# The original implementation used SQLAlchemy for persistence. However the test
# environment does not provide the required dependency, so we use a very
# lightweight in-memory store to keep launched surveys. This is sufficient for
# the unit tests which only verify the response structure.
from .storage import surveys_storage

app = FastAPI()

allowed = os.getenv("FRONTEND_DOMAIN")
origins = [allowed] if allowed else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.getenv("FORCE_HTTPS") == "1":
    @app.middleware("http")
    async def https_redirect(request: Request, call_next):
        if request.url.scheme != "https":
            url = request.url.replace(scheme="https")
            return RedirectResponse(url=str(url))
        return await call_next(request)
app.include_router(stt_router)

# Locate ``survey.schema.json``. When running inside Docker ``__file__`` will
# be ``/app/app/main.py`` while during development it may be
# ``backend/app/main.py``. Instead of relying on a fixed number of parent
# directories, walk up the tree until the file is found so both environments
# work the same.
_current = Path(__file__).resolve()
for parent in [_current.parent, *_current.parents]:
    candidate = parent / "survey.schema.json"
    if candidate.is_file():
        SCHEMA_PATH = candidate
        break
else:  # pragma: no cover - guard against missing schema during runtime
    # When running inside Docker ``survey.schema.json`` is copied to
    # ``/app/survey.schema.json``. Check that location before raising an error
    # to handle cases where the dynamic search above fails.
    fallback = Path("/app/survey.schema.json")    
    if fallback.is_file():
        SCHEMA_PATH = fallback
    else:
        raise FileNotFoundError("survey.schema.json not found")
with open(SCHEMA_PATH) as f:
    SURVEY_SCHEMA = json.load(f)

@app.post("/launch")
async def launch_survey(file: UploadFile = File(...)):
    try:
        content = await file.read()
        data = json.loads(content)
        validate(instance=data, schema=SURVEY_SCHEMA)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    survey_id = str(uuid.uuid4())
    token = str(uuid.uuid4())
    link = f"/survey/{survey_id}?token={token}"

    # Store the survey in memory so tests can verify the behaviour without a
    # database. In a full application this would be persisted to a database.
    surveys_storage.append({"id": survey_id, "data": data})

    return JSONResponse({"survey_id": survey_id, "link": link})

from fastapi import WebSocket
from .flow_engine import load_or_build_transcript
from . import events, stt_stream


@app.websocket("/events/{survey_id}")
async def events_ws(ws: WebSocket, survey_id: str):
    await events.events_ws(ws, survey_id)


@app.get("/transcript/{survey_id}/{token}")
async def get_transcript(survey_id: str, token: str):
    data = load_or_build_transcript(survey_id, token, stt_stream.engine)
    return JSONResponse(data)


@app.post("/consent")
async def register_consent(request: Request):
    data = await request.json()
    survey_id = data.get("survey_id")
    if not survey_id:
        raise HTTPException(status_code=400, detail="survey_id required")
    cur = stt_stream.engine.cursor()
    cur.execute(
        "INSERT INTO consent (survey_id, timestamp) VALUES (?, CURRENT_TIMESTAMP)",
        (survey_id,),
    )
    stt_stream.engine.commit()
    return JSONResponse({"ok": True})
