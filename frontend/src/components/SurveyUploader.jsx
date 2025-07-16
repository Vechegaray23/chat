import { useState } from 'react'

export default function SurveyUploader() {
  const [error, setError] = useState(null)
  const [link, setLink] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLink(null)
    const formData = new FormData(e.target)
    try {
      const res = await fetch('/launch', {
        method: 'POST',
        body: formData
      })
      if (!res.ok) {
        const data = await res.json()
        throw new Error(data.detail)
      }
      const data = await res.json()
      setLink(data.link)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input type="file" name="file" accept="application/json" required />
      <button type="submit" className="px-4 py-2 bg-blue-500 text-white rounded">
        Upload
      </button>
      {error && <p className="text-red-600">{error}</p>}
      {link && (
        <p>
          Link: <a href={link} className="text-blue-600 underline">{link}</a>
        </p>
      )}
    </form>
  )
}
