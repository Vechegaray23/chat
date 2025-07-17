import { useEffect, useRef, useState } from 'react'

export default function useSttStream({ surveyId, token, questionId, role }) {
  const [transcript, setTranscript] = useState('')
  const [confidence, setConfidence] = useState(0)
  const wsRef = useRef(null)

  useEffect(() => {
    const base = import.meta.env.VITE_API_URL || 'ws://localhost:8000'
    const url = `${base.replace('http', 'ws')}/stt-stream?survey_id=${surveyId}&token=${token}&question_id=${questionId}&role=${role}`
    const ws = new WebSocket(url)
    wsRef.current = ws

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        setTranscript((t) => t + data.transcript)
        setConfidence(data.confidence)
      } catch {}
    }

    return () => ws.close()
  }, [surveyId, token, questionId, role])

  const sendChunk = (blob) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(blob)
    }
  }

  const confirmed = confidence >= 0.85

  return { transcript, confidence, confirmed, sendChunk }
}
