export default function LiveTranscript({ transcript, confirmed }) {
  return (
    <p className={confirmed ? 'text-green-600' : 'text-gray-800'}>
      {transcript}
    </p>
  )
}
