import { useState } from 'react'

const COUNT_OPTIONS = [3, 5, 7, 10]

export default function InputSection({
  description,
  setDescription,
  count,
  setCount,
  onSubmit,
  phase,
  hasResults,
}) {
  const [focused, setFocused] = useState(false)
  const [inputFocused, setInputFocused] = useState(false)
  const [customValue, setCustomValue] = useState('')
  const isLoading = phase === 'loading'

  function handleCustomChange(e) {
    const raw = e.target.value.replace(/\D/g, '')
    setCustomValue(raw)
    const n = parseInt(raw, 10)
    if (!isNaN(n) && n >= 1 && n <= 20) setCount(n)
  }

  function handleCustomBlur() {
    setInputFocused(false)
    const n = parseInt(customValue, 10)
    if (!customValue || isNaN(n) || n < 1) {
      setCustomValue('')
    } else {
      setCount(Math.min(20, Math.max(1, n)))
      setCustomValue(String(Math.min(20, Math.max(1, n))))
    }
  }

  function handleKey(e) {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
      onSubmit()
    }
  }

  return (
    <div style={styles.wrapper}>
      {/* Header — shrinks when results are showing */}
      <div style={{ marginBottom: hasResults ? 16 : 28 }}>
        <h1 style={{ ...styles.title, fontSize: hasResults ? '1.6rem' : '2.4rem' }}>
          MusicTasteMatch
        </h1>
        {!hasResults && (
          <p style={styles.subtitle}>describe your mood. get your music.</p>
        )}
      </div>

      {/* Textarea */}
      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        onKeyDown={handleKey}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        placeholder="I want something late-night and melancholic, acoustic but not too slow..."
        disabled={isLoading}
        rows={hasResults ? 2 : 4}
        style={{
          ...styles.textarea,
          borderColor: focused ? 'var(--blue-dim)' : 'var(--border)',
          boxShadow: focused ? '0 0 0 2px var(--blue-dim)' : 'none',
          minHeight: hasResults ? 60 : 100,
          opacity: isLoading ? 0.6 : 1,
        }}
      />

      {/* Count picker + submit row */}
      <div style={styles.row}>
        <div style={styles.countRow}>
          <span style={styles.countLabel}>songs</span>
          {COUNT_OPTIONS.map((n) => (
            <button
              key={n}
              onClick={() => { setCount(n); setCustomValue('') }}
              disabled={isLoading}
              style={{
                ...styles.pill,
                backgroundColor: count === n && !customValue ? 'var(--green)' : 'var(--surface-2)',
                borderColor: count === n && !customValue ? 'var(--green-bright)' : 'var(--border)',
                color: count === n && !customValue ? '#fff' : 'var(--muted)',
              }}
            >
              {n}
            </button>
          ))}
          <input
            type="text"
            inputMode="numeric"
            placeholder="?"
            value={customValue}
            onChange={handleCustomChange}
            onFocus={() => setInputFocused(true)}
            onBlur={handleCustomBlur}
            disabled={isLoading}
            maxLength={2}
            style={{
              ...styles.customInput,
              borderColor: inputFocused ? 'var(--green)' : customValue ? 'var(--green-bright)' : 'var(--border)',
              backgroundColor: customValue ? 'var(--green)' : 'var(--surface-2)',
              color: customValue ? '#fff' : 'var(--muted)',
            }}
          />
        </div>

        <button
          onClick={onSubmit}
          disabled={isLoading || !description.trim()}
          style={{
            ...styles.submitBtn,
            opacity: (!description.trim() && !isLoading) ? 0.45 : 1,
            cursor: isLoading || !description.trim() ? 'not-allowed' : 'pointer',
          }}
          onMouseEnter={(e) => {
            if (!isLoading && description.trim()) {
              e.currentTarget.style.backgroundColor = 'var(--green-bright)'
            }
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = 'var(--green)'
          }}
        >
          {isLoading ? <LoadingDots /> : 'Find My Music →'}
        </button>
      </div>

      {!hasResults && (
        <p style={styles.hint}>⌘ + Enter to submit</p>
      )}
    </div>
  )
}

function LoadingDots() {
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
      <span style={styles.dotLabel}>analyzing</span>
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          style={{
            ...styles.dot,
            animationDelay: `${i * 160}ms`,
          }}
        />
      ))}
    </span>
  )
}

const styles = {
  wrapper: {
    display: 'flex',
    flexDirection: 'column',
    gap: 12,
  },
  title: {
    fontFamily: "'Fraunces', Georgia, serif",
    fontWeight: 600,
    color: 'var(--text)',
    lineHeight: 1.1,
    letterSpacing: '-0.02em',
    transition: 'font-size 0.3s ease',
  },
  subtitle: {
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '0.85rem',
    color: 'var(--muted)',
    marginTop: 8,
    letterSpacing: '0.03em',
  },
  textarea: {
    width: '100%',
    backgroundColor: 'var(--surface-2)',
    border: '1px solid',
    borderRadius: 8,
    padding: '14px 16px',
    color: 'var(--text)',
    fontFamily: 'system-ui, -apple-system, sans-serif',
    fontSize: '0.95rem',
    lineHeight: 1.6,
    resize: 'vertical',
    outline: 'none',
    transition: 'border-color 0.15s ease, box-shadow 0.15s ease, min-height 0.3s ease',
  },
  row: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: 12,
    flexWrap: 'wrap',
  },
  countRow: {
    display: 'flex',
    alignItems: 'center',
    gap: 6,
  },
  countLabel: {
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '0.75rem',
    color: 'var(--muted)',
    marginRight: 4,
    textTransform: 'uppercase',
    letterSpacing: '0.06em',
  },
  pill: {
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '0.78rem',
    fontWeight: 600,
    padding: '4px 10px',
    border: '1px solid',
    borderRadius: 20,
    cursor: 'pointer',
    transition: 'background-color 0.15s, border-color 0.15s, color 0.15s',
  },
  submitBtn: {
    fontFamily: 'system-ui, -apple-system, sans-serif',
    fontSize: '0.9rem',
    fontWeight: 600,
    padding: '10px 24px',
    backgroundColor: 'var(--green)',
    color: '#fff',
    border: 'none',
    borderRadius: 8,
    transition: 'background-color 0.15s ease',
    flex: '0 0 auto',
  },
  customInput: {
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '0.78rem',
    fontWeight: 600,
    width: 36,
    padding: '4px 0',
    textAlign: 'center',
    border: '1px solid',
    borderRadius: 20,
    outline: 'none',
    transition: 'background-color 0.15s, border-color 0.15s, color 0.15s',
    cursor: 'text',
  },
  hint: {
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '0.7rem',
    color: 'var(--blue-dim)',
    opacity: 0.7,
    textAlign: 'right',
  },
  dotLabel: {
    fontSize: '0.88rem',
    marginRight: 4,
  },
  dot: {
    display: 'inline-block',
    width: 5,
    height: 5,
    borderRadius: '50%',
    backgroundColor: '#fff',
    animation: 'pulse 1.2s ease-in-out infinite',
  },
}
