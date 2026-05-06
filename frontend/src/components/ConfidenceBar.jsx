export default function ConfidenceBar({ confidence }) {
  const score = confidence.confidence_score
  const pct = Math.round(score * 100)

  let fillColor
  if (score < 0.5) {
    fillColor = '#c0504a'
  } else if (score < 0.75) {
    fillColor = '#c8a030'
  } else {
    fillColor = 'var(--blue)'
  }

  return (
    <div style={styles.wrapper} className="fade-up">
      <div style={styles.header}>
        <span style={styles.label}>Confidence</span>
        <span style={styles.score}>
          {score.toFixed(2)} <span style={styles.outOf}>/ 1.0</span>
        </span>
      </div>

      <div style={styles.track}>
        <div
          style={{
            ...styles.fill,
            width: `${pct}%`,
            backgroundColor: fillColor,
          }}
        />
      </div>

      {confidence.flags && confidence.flags.length > 0 && (
        <ul style={styles.flags}>
          {confidence.flags.map((flag, i) => (
            <li key={i} style={styles.flag}>
              <span style={styles.flagIcon}>⚠</span>
              {flag}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

const styles = {
  wrapper: {
    display: 'flex',
    flexDirection: 'column',
    gap: 10,
    padding: '16px 0',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  label: {
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '0.75rem',
    color: 'var(--blue)',
    textTransform: 'uppercase',
    letterSpacing: '0.07em',
  },
  score: {
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '0.85rem',
    color: 'var(--text)',
    fontWeight: 600,
  },
  outOf: {
    color: 'var(--muted)',
    fontWeight: 400,
  },
  track: {
    width: '100%',
    height: 6,
    backgroundColor: 'var(--surface-2)',
    borderRadius: 3,
    overflow: 'hidden',
    border: '1px solid var(--border)',
  },
  fill: {
    height: '100%',
    borderRadius: 3,
    transition: 'width 0.7s ease',
  },
  flags: {
    listStyle: 'none',
    display: 'flex',
    flexDirection: 'column',
    gap: 5,
    marginTop: 4,
    padding: 0,
  },
  flag: {
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '0.72rem',
    color: '#b8943a',
    lineHeight: 1.5,
    display: 'flex',
    gap: 7,
    alignItems: 'flex-start',
  },
  flagIcon: {
    flex: '0 0 auto',
    marginTop: 1,
  },
}
