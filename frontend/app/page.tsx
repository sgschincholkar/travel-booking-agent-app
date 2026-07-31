'"'"'use client'"'"'

import { useState } from '"'"'react'"'"'
import axios from '"'"'axios'"'"'

interface QueryResponse {
  thread_id: string
  response: string
}

interface EmailResponse {
  status: string
}

export default function Home() {
  const [query, setQuery] = useState('"'"''"'"')
  const [threadId, setThreadId] = useState('"'"''"'"')
  const [response, setResponse] = useState('"'"''"'"')
  const [loading, setLoading] = useState(false)
  const [emailLoading, setEmailLoading] = useState(false)
  const [error, setError] = useState('"'"''"'"')

  const [senderEmail, setSenderEmail] = useState('"'"''"'"')
  const [receiverEmail, setReceiverEmail] = useState('"'"''"'"')
  const [subject, setSubject] = useState('"'"'Your Travel Plan'"'"')
  const [emailStatus, setEmailStatus] = useState('"'"''"'"')

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || '"'"'http://localhost:8000'"'"'

  const handleQuery = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    setError('"'"''"'"')
    setResponse('"'"''"'"')

    try {
      const res = await axios.post<QueryResponse>(`${apiUrl}/api/query`, {
        query: query,
      })
      setThreadId(res.data.thread_id)
      setResponse(res.data.response)
    } catch (err) {
      setError(`Error: ${err instanceof Error ? err.message : '"'"'Failed to get response'"'"'}`)
    } finally {
      setLoading(false)
    }
  }

  const handleSendEmail = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!threadId || !senderEmail || !receiverEmail) {
      setError('"'"'Please fill all email fields and get travel info first'"'"')
      return
    }

    setEmailLoading(true)
    setEmailStatus('"'"''"'"')

    try {
      const res = await axios.post<EmailResponse>(`${apiUrl}/api/send-email`, {
        thread_id: threadId,
        sender: senderEmail,
        receiver: receiverEmail,
        subject: subject,
      })
      setEmailStatus(res.data.status)
    } catch (err) {
      setError(`Email error: ${err instanceof Error ? err.message : '"'"'Failed to send email'"'"'}`)
    } finally {
      setEmailLoading(false)
    }
  }

  return (
    <div className="page">
      <div className="container">
        <div className="header">
          <h1>✈️ Travel Booking Agent</h1>
          <p>Find flights and hotels with AI assistance</p>
        </div>

        <div className="main-content">
          <div className="card query-section">
            <h2>Find Flights & Hotels</h2>
            <form onSubmit={handleQuery}>
              <div className="input-group">
                <label htmlFor="query">Travel Query</label>
                <textarea
                  id="query"
                  placeholder="E.g., Flights from NYC to LA next week, 3-star hotels in downtown LA"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  disabled={loading}
                />
              </div>
              <button type="submit" disabled={loading || !query.trim()}>
                {loading ? '"'"'Searching...'"'"' : '"'"'Get Travel Info'"'"'}
              </button>
            </form>

            {threadId && (
              <div className="email-section">
                <h3>Send Results via Email</h3>
                <form onSubmit={handleSendEmail}>
                  <div className="input-group">
                    <label htmlFor="sender">From Email</label>
                    <input
                      id="sender"
                      type="email"
                      placeholder="your@email.com"
                      value={senderEmail}
                      onChange={(e) => setSenderEmail(e.target.value)}
                      disabled={emailLoading}
                    />
                  </div>
                  <div className="input-group">
                    <label htmlFor="receiver">To Email</label>
                    <input
                      id="receiver"
                      type="email"
                      placeholder="recipient@email.com"
                      value={receiverEmail}
                      onChange={(e) => setReceiverEmail(e.target.value)}
                      disabled={emailLoading}
                    />
                  </div>
                  <div className="input-group">
                    <label htmlFor="subject">Subject</label>
                    <input
                      id="subject"
                      type="text"
                      placeholder="Email subject"
                      value={subject}
                      onChange={(e) => setSubject(e.target.value)}
                      disabled={emailLoading}
                    />
                  </div>
                  <button type="submit" disabled={emailLoading}>
                    {emailLoading ? '"'"'Sending...'"'"' : '"'"'Send Email'"'"'}
                  </button>
                </form>
                {emailStatus && <p className="success">{emailStatus}</p>}
              </div>
            )}
          </div>

          <div className="card results-section">
            <h2>Results</h2>
            <div className="results-container">
              {loading && <p className="loading">Searching for flights and hotels...</p>}
              {error && <p className="error">{error}</p>}
              {response && <p>{response}</p>}
              {!loading && !response && !error && (
                <p style={{ color: '"'"'#999'"'"' }}>Your travel information will appear here...</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
