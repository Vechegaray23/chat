import os
import sqlite3

DATABASE_URL = os.getenv('DATABASE_URL', ':memory:')
conn = sqlite3.connect(DATABASE_URL, check_same_thread=False)

cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS turns (survey_id TEXT, token TEXT, question_id TEXT, role TEXT, audio_url TEXT, transcript TEXT, timestamp TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS consent (survey_id TEXT, timestamp TEXT)")

cur.execute("SELECT COUNT(*) FROM turns")
turns = cur.fetchone()[0]
cur.execute("SELECT AVG(LENGTH(transcript)) FROM turns")
avg_len = cur.fetchone()[0] or 0
cur.execute("SELECT COUNT(*) FROM consent")
consents = cur.fetchone()[0]

print(f'KPI-1 total turns: {turns}')
print(f'KPI-2 avg transcript length: {avg_len:.2f}')
print(f'KPI-3 consents registrados: {consents}')
