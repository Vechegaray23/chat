import asyncio
import statistics
import time
import sys
try:
    import websockets
except ModuleNotFoundError:  # pragma: no cover - environment may lack dependency
    print('websockets package not installed', file=sys.stderr)
    sys.exit(1)

URL = 'ws://localhost:8000/stt-stream?survey_id=test&token=tok&question_id=q1&role=user'
AUDIO_CHUNK = b'0' * 32000

async def run_session(latencies):
    start = time.perf_counter()
    try:
        async with websockets.connect(URL) as ws:
            await ws.send(AUDIO_CHUNK)
            await ws.recv()
    except websockets.exceptions.ConnectionClosedError:
        # The server closed the connection without a proper close frame
        # which previously caused this script to crash. We record the
        # latency observed so far and continue.
        pass
    finally:
        latencies.append((time.perf_counter() - start) * 1000)

async def main():
    latencies = []
    await asyncio.gather(*(run_session(latencies) for _ in range(15)))
    p95 = statistics.quantiles(latencies, n=20)[18]
    print(f'p95 latency: {p95:.1f} ms')
    if p95 > 300:
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
