import json
from jsonschema import validate, ValidationError
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parents[2] / 'survey.schema.json'
with open(SCHEMA_PATH) as f:
    SCHEMA = json.load(f)

def test_valid_survey():
    data = {
        "title": "Customer Feedback",
        "questions": [
            {"id": "q1", "type": "text", "text": "What do you think?"}
        ]
    }
    validate(instance=data, schema=SCHEMA)

def test_invalid_survey():
    data = {"title": "Invalid"}
    try:
        validate(instance=data, schema=SCHEMA)
        assert False, 'Should raise ValidationError'
    except ValidationError:
        pass
