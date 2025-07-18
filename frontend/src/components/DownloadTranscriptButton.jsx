export default function DownloadTranscriptButton({ surveyId, token }) {
  const base = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  const url = `${base}/transcript/${surveyId}/${token}`
  return (
    <a href={url} className="px-4 py-2 bg-green-600 text-white rounded" download>
      Download transcript
    </a>
  )
}
