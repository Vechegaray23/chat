from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from jsonschema import validate, ValidationError
import json
import uuid
import os
from sqlalchemy import create_engine, Table, Column, MetaData, String, JSON

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
engine = create_engine(DATABASE_URL, future=True)
metadata = MetaData()

surveys_table = Table(
    "surveys",
    metadata,
    Column("id", String, primary_key=True),
    Column("data", JSON),
)

metadata.create_all(engine)

app = FastAPI()

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "survey.schema.json")
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

    with engine.begin() as conn:
        conn.execute(surveys_table.insert().values(id=survey_id, data=data))

    return JSONResponse({"survey_id": survey_id, "link": link})
