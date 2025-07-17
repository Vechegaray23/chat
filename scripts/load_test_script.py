import asyncio
import statistics
import time
import sys
import websockets

URL = 'ws://localhost:8000/stt-stream?survey_id=test&token=tok&question_id=q1&role=user'
AUDIO_CHUNK = b'0' * 32000

async def run_session(latencies):
    async with websockets.connect(URL) as ws:
        start = time.perf_counter()
        await ws.send(AUDIO_CHUNK)
        await ws.recv()
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
