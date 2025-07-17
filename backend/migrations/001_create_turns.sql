CREATE TABLE IF NOT EXISTS turns (
    id SERIAL PRIMARY KEY,
    survey_id UUID NOT NULL,
    token UUID NOT NULL,
    question_id TEXT NOT NULL,
    role TEXT NOT NULL,
    audio_url TEXT,
    transcript TEXT,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
