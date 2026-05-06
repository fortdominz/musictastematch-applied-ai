export default function ProfilePills({ profile, count }) {
  return (
    <div style={styles.wrapper} className="fade-up">
      <p style={styles.meta}>
        <span style={styles.metaLabel}>catalog</span>
        <span style={{ color: 'var(--blue)' }}>{count} songs selected</span>
      </p>

      <div style={styles.pills}>
        <Pill label="genre" value={profile.genre} mono />
        <Pill label="mood" value={profile.mood} mono />
        <Pill label="energy" value={
          <EnergyBar value={profile.energy} color="var(--green)" border="var(--green)" />
        } />
        <Pill label="valence" value={
          <EnergyBar value={profile.valence} color="var(--blue)" border="var(--blue-dim)" />
        } borderColor="var(--blue-dim)" />
        <Pill label="tempo" value={`${Math.round(profile.tempo_bpm)} bpm`} mono />
      </div>
    </div>
  )
}

function Pill({ label, value, mono, borderColor }) {
  return (
    <div style={{ ...styles.pill, ...(borderColor ? { borderColor } : {}) }}>
      <span style={styles.pillLabel}>{label}</span>
      {mono ? (
        <span style={styles.pillValue}>{value}</span>
      ) : (
        <div style={{ marginTop: 4 }}>{value}</div>
      )}
    </div>
  )
}

function EnergyBar({ value, color = 'var(--green)' }) {
  const pct = Math.round(value * 100)
  return (
    <div style={styles.barWrapper}>
      <div style={styles.barTrack}>
        <div
          style={{
            width: `${pct}%`,
            height: '100%',
            backgroundColor: color,
          }}
        />
      </div>
      <span style={styles.barValue}>{value.toFixed(2)}</span>
    </div>
  )
}

const styles = {
  wrapper: {
    display: 'flex',
    flexDirection: 'column',
    gap: 12,
  },
  meta: {
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '0.72rem',
    color: 'var(--muted)',
    display: 'flex',
    alignItems: 'center',
    gap: 8,
  },
  metaLabel: {
    backgroundColor: 'var(--surface-2)',
    border: '1px solid var(--blue-dim)',
    borderRadius: 4,
    padding: '2px 7px',
    fontSize: '0.65rem',
    textTransform: 'uppercase',
    letterSpacing: '0.06em',
    color: 'var(--blue)',
  },
  pills: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: 10,
  },
  pill: {
    backgroundColor: 'var(--surface-2)',
    border: '1px solid var(--border)',
    borderRadius: 8,
    padding: '10px 14px',
    minWidth: 90,
    animation: 'fadeUp 0.5s ease both',
  },
  pillLabel: {
    display: 'block',
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '0.65rem',
    color: 'var(--muted)',
    textTransform: 'uppercase',
    letterSpacing: '0.07em',
    marginBottom: 5,
  },
  pillValue: {
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '0.88rem',
    color: 'var(--text)',
    fontWeight: 500,
  },
  barWrapper: {
    display: 'flex',
    alignItems: 'center',
    gap: 6,
    marginTop: 2,
  },
  barTrack: {
    width: 60,
    height: 4,
    borderRadius: 2,
    backgroundColor: 'var(--border)',
    overflow: 'hidden',
    flexShrink: 0,
  },
  barValue: {
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '0.78rem',
    color: 'var(--text)',
  },
}
