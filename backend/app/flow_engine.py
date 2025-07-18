import ast
from typing import Any, Dict, Optional


class SafeEvaluator:
    ALLOWED_OPERATORS = {
        ast.Gt: lambda a, b: a > b,
        ast.Lt: lambda a, b: a < b,
        ast.Eq: lambda a, b: a == b,
        ast.NotEq: lambda a, b: a != b,
        ast.GtE: lambda a, b: a >= b,
        ast.LtE: lambda a, b: a <= b,
    }

    ALLOWED_NODES = (
        ast.Expression,
        ast.Compare,
        ast.Name,
        ast.Load,
        ast.Constant,
        ast.BoolOp,
        ast.And,
        ast.Or,
    )

    def eval(self, expr: str, context: Dict[str, Any]) -> Any:
        tree = ast.parse(expr, mode="eval")
        return self._eval_node(tree.body, context)

    def _eval_node(self, node: ast.AST, ctx: Dict[str, Any]):
        if isinstance(node, ast.BoolOp):
            if isinstance(node.op, ast.And):
                return all(self._eval_node(v, ctx) for v in node.values)
            elif isinstance(node.op, ast.Or):
                return any(self._eval_node(v, ctx) for v in node.values)
            else:
                raise ValueError("Unsupported boolean operator")
        if isinstance(node, ast.Compare):
            left = self._eval_node(node.left, ctx)
            result = True
            for op, comp in zip(node.ops, node.comparators):
                right = self._eval_node(comp, ctx)
                op_func = self.ALLOWED_OPERATORS.get(type(op))
                if op_func is None:
                    raise ValueError("Operator not allowed")
                result = result and op_func(left, right)
                left = right
            return result
        if isinstance(node, ast.Name):
            if node.id not in ctx:
                raise ValueError(f"Unknown variable {node.id}")
            return ctx[node.id]
        if isinstance(node, ast.Constant):
            return node.value
        raise ValueError("Unsupported expression element")


eval_safe = SafeEvaluator().eval


class FlowEngine:
    def __init__(self, survey: Dict[str, Any]):
        self.questions = survey.get("questions", [])
        self.index_map = {q["id"]: i for i, q in enumerate(self.questions)}

    def _get_question(self, qid: str) -> Optional[Dict[str, Any]]:
        for q in self.questions:
            if q["id"] == qid:
                return q
        return None

    def next_question(self, current_id: str, answers: Dict[str, Any]) -> Optional[str]:
        current = self._get_question(current_id)
        if not current:
            return None
        expr = current.get("followup_if")
        follow_id = current.get("followup_id")
        if expr and follow_id:
            ctx = {
                "answer": answers.get(current_id),
                "answers": answers,
            }
            try:
                if bool(eval_safe(expr, ctx)):
                    return follow_id
            except Exception:
                pass
        idx = self.index_map.get(current_id, -1)
        if idx >= 0 and idx + 1 < len(self.questions):
            return self.questions[idx + 1]["id"]
        return None

import json
from pathlib import Path

TRANSCRIPTS_DIR = Path("transcripts")
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)


def build_transcript(survey_id: str, token: str, db_engine) -> Path:
    cur = db_engine.cursor()
    cur.execute(
        "SELECT question_id, role, transcript, audio_url, timestamp FROM turns WHERE survey_id=? AND token=? ORDER BY timestamp",
        (survey_id, token),
    )
    rows = [
        {
            "question_id": q,
            "role": r,
            "transcript": t,
            "audio_url": u,
            "timestamp": ts,
        }
        for q, r, t, u, ts in cur.fetchall()
    ]
    data = {"survey_id": survey_id, "turns": rows}
    path = TRANSCRIPTS_DIR / f"{survey_id}_{token}.json"
    with path.open("w") as f:
        json.dump(data, f)
    return path


def load_or_build_transcript(survey_id: str, token: str, db_engine) -> dict:
    path = TRANSCRIPTS_DIR / f"{survey_id}_{token}.json"
    if path.is_file():
        with path.open() as f:
            return json.load(f)
    build_transcript(survey_id, token, db_engine)
    with path.open() as f:
        return json.load(f)
