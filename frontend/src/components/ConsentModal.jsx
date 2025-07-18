import { useState } from 'react'

export default function ConsentModal({ onAccept }) {
  const [loading, setLoading] = useState(false)
  const base = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  const handleAccept = async () => {
    setLoading(true)
    await fetch(`${base}/consent`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ survey_id: 'demo' })
    })
    setLoading(false)
    if (onAccept) onAccept()
  }

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white p-4 rounded space-y-4 max-w-md">
        <p>
          Para continuar debes otorgar consentimiento para el uso de tu micrófono y el almacenamiento de tus datos de acuerdo a la Ley 19.628.
        </p>
        <button onClick={handleAccept} disabled={loading} className="px-4 py-2 bg-blue-600 text-white rounded">
          {loading ? 'Guardando...' : 'Acepto'}
        </button>
      </div>
    </div>
  )
}
