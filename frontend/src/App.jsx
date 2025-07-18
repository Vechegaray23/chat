import { useState } from 'react'
import ConsentModal from './components/ConsentModal'
import SurveyUploader from './components/SurveyUploader'
import LiveTranscript from './components/LiveTranscript'
import DownloadTranscriptButton from './components/DownloadTranscriptButton'
import SurveyEventsListener from './components/SurveyEventsListener'
import useSttStream from './hooks/useSttStream'

export default function App() {
  const stt = useSttStream({ surveyId: 'demo', token: 'demo', questionId: 'q1', role: 'user' })
  const [completed, setCompleted] = useState(false)
  const [consent, setConsent] = useState(false)

  if (!consent) {
    return <ConsentModal onAccept={() => setConsent(true)} />
  }

  return (
    <div className="container mx-auto space-y-4">
      <h1 className="text-2xl font-bold mb-4">Launch Survey</h1>
      <SurveyUploader />
      <LiveTranscript transcript={stt.transcript} confirmed={stt.confirmed} />
      {completed && (
        <DownloadTranscriptButton surveyId="demo" token="demo" />
      )}
      <SurveyEventsListener surveyId="demo" onEvent={(e) => {
        if (e.type === 'survey_completed') setCompleted(true)
      }} />
    </div>
  )
}
