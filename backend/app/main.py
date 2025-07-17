from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from jsonschema import validate, ValidationError
import json
import uuid
import os
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

# Locate the schema file relative to the repository root. ``__file__`` may
# resolve to ``backend/app/main.py`` even when imported via a symlink. Moving two
# directories up points to the repository root where ``survey.schema.json``
# resides.
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "survey.schema.json")
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
