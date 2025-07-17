import SurveyUploader from './components/SurveyUploader'
import LiveTranscript from './components/LiveTranscript'
import useSttStream from './hooks/useSttStream'

export default function App() {
  const stt = useSttStream({ surveyId: 'demo', token: 'demo', questionId: 'q1', role: 'user' })

  return (
    <div className="container mx-auto space-y-4">
      <h1 className="text-2xl font-bold mb-4">Launch Survey</h1>
      <SurveyUploader />
      <LiveTranscript transcript={stt.transcript} confirmed={stt.confirmed} />
    </div>
  )
}
