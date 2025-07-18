from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect

_subscribers: Dict[str, Set[WebSocket]] = {}

async def register(survey_id: str, ws: WebSocket):
    await ws.accept()
    _subscribers.setdefault(survey_id, set()).add(ws)

async def unregister(survey_id: str, ws: WebSocket):
    _subscribers.get(survey_id, set()).discard(ws)

async def send_event(survey_id: str, event: dict):
    sockets = list(_subscribers.get(survey_id, []))
    for ws in sockets:
        try:
            await ws.send_json(event)
        except Exception:
            _subscribers[survey_id].discard(ws)


async def events_ws(ws: WebSocket, survey_id: str):
    await register(survey_id, ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        await unregister(survey_id, ws)
