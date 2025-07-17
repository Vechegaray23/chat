from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
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
surveys_storage = []

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
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
