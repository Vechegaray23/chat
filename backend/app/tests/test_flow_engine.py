from app.flow_engine import FlowEngine


def test_followup_jump():
    survey = {
        "questions": [
            {"id": "q1", "type": "text", "text": "A", "followup_id": "q3", "followup_if": "answer > 5"},
            {"id": "q2", "type": "text", "text": "B"},
            {"id": "q3", "type": "text", "text": "C"},
        ]
    }
    engine = FlowEngine(survey)
    answers = {"q1": 10}
    assert engine.next_question("q1", answers) == "q3"


def test_followup_none():
    survey = {
        "questions": [
            {"id": "q1", "type": "text", "text": "A", "followup_id": "q3", "followup_if": "answer > 5"},
            {"id": "q2", "type": "text", "text": "B"},
            {"id": "q3", "type": "text", "text": "C"},
        ]
    }
    engine = FlowEngine(survey)
    answers = {"q1": 2}
    assert engine.next_question("q1", answers) == "q2"


def test_end_of_survey():
    survey = {
        "questions": [
            {"id": "q1", "type": "text", "text": "A"},
        ]
    }
    engine = FlowEngine(survey)
    answers = {"q1": "hi"}
    assert engine.next_question("q1", answers) is None
