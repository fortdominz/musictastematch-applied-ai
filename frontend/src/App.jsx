import { useState } from 'react'
import InputSection from './components/InputSection.jsx'
import ProfilePills from './components/ProfilePills.jsx'
import SongCard from './components/SongCard.jsx'
import ConfidenceBar from './components/ConfidenceBar.jsx'
import CritiqueBlock from './components/CritiqueBlock.jsx'

const API_BASE = import.meta.env.VITE_API_URL || ''

export default function App() {
  const [phase, setPhase] = useState('idle')      // idle | loading | results
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [description, setDescription] = useState('')
  const [count, setCount] = useState(5)

  async function handleSubmit() {
    if (!description.trim()) return
    setPhase('loading')
    setError(null)
    try {
      const res = await fetch(`${API_BASE}/api/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description, count }),
      })
      const data = await res.json()
      if (data.error) throw new Error(data.error)
      setResult(data)
      setPhase('results')
    } catch (e) {
      setError(e.message)
      setPhase('idle')
    }
  }

  return (
    <div style={styles.app}>
      <div style={styles.container}>

        {/* Input is always at top */}
        <InputSection
          description={description}
          setDescription={setDescription}
          count={count}
          setCount={setCount}
          onSubmit={handleSubmit}
          phase={phase}
          hasResults={phase === 'results'}
        />

        {/* Error message */}
        {error && (
          <div style={styles.error}>
            <span style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '0.8rem' }}>error</span>
            <p style={{ marginTop: 6, lineHeight: 1.6 }}>{error}</p>
          </div>
        )}

        {/* Results section */}
        {phase === 'results' && result && (
          <div style={styles.results}>
            <ProfilePills profile={result.profile} count={count} />

            <div style={styles.songsSection}>
              {result.recommendations.map((song, i) => (
                <SongCard key={`${song.title}-${i}`} song={song} index={i} rank={i + 1} />
              ))}
            </div>

            <ConfidenceBar confidence={result.confidence} />
            <CritiqueBlock critique={result.critique} />
          </div>
        )}

      </div>
    </div>
  )
}

const styles = {
  app: {
    minHeight: '100vh',
    backgroundColor: 'var(--bg)',
    padding: '48px 24px 80px',
  },
  container: {
    maxWidth: 720,
    margin: '0 auto',
    display: 'flex',
    flexDirection: 'column',
    gap: 32,
  },
  error: {
    backgroundColor: 'rgba(180, 60, 60, 0.1)',
    border: '1px solid rgba(180, 60, 60, 0.35)',
    borderRadius: 8,
    padding: '16px 20px',
    color: '#e07070',
    animation: 'fadeUp 0.4s ease both',
  },
  results: {
    display: 'flex',
    flexDirection: 'column',
    gap: 24,
  },
  songsSection: {
    display: 'flex',
    flexDirection: 'column',
    gap: 12,
  },
}
