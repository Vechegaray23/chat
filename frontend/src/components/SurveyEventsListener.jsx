import { useEffect } from 'react'

export default function SurveyEventsListener({ surveyId, onEvent }) {
  useEffect(() => {
    const base = import.meta.env.VITE_API_URL || 'ws://localhost:8000'
    const ws = new WebSocket(`${base.replace('http', 'ws')}/events/${surveyId}`)
    ws.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data)
        if (onEvent) onEvent(data)
      } catch {}
    }
    return () => ws.close()
  }, [surveyId, onEvent])

  return null
}
