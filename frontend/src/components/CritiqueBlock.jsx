export default function CritiqueBlock({ critique }) {
  return (
    <div style={styles.wrapper} className="fade-up">
      <span style={styles.label}>AI Critique</span>
      <p style={styles.text}>{critique}</p>
    </div>
  )
}

const styles = {
  wrapper: {
    backgroundColor: 'var(--blue-bg)',
    border: '1px solid var(--blue-dim)',
    borderLeft: '3px solid var(--blue)',
    borderRadius: 8,
    padding: '20px 24px',
    display: 'flex',
    flexDirection: 'column',
    gap: 10,
  },
  label: {
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '0.68rem',
    color: 'var(--blue)',
    textTransform: 'uppercase',
    letterSpacing: '0.1em',
    fontWeight: 600,
  },
  text: {
    color: 'var(--text)',
    lineHeight: 1.7,
    fontSize: '0.92rem',
  },
}
