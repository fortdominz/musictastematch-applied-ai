import { useState } from 'react'

export default function SongCard({ song, index, rank }) {
  const [expanded, setExpanded] = useState(false)
  const [hovered, setHovered] = useState(false)

  const delay = `${index * 80}ms`

  return (
    <div
      onClick={() => setExpanded((v) => !v)}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        ...styles.card,
        borderColor: hovered ? 'var(--border-bright)' : 'var(--border)',
        transform: hovered ? 'translateY(-2px)' : 'translateY(0)',
        animationDelay: delay,
        cursor: 'pointer',
      }}
      className="fade-up"
    >
      <div style={styles.main}>
        {/* Rank */}
        <span style={styles.rank}>{String(rank).padStart(2, '0')}</span>

        {/* Song info */}
        <div style={styles.info}>
          <span style={styles.title}>{song.title}</span>
          <span style={styles.artist}>{song.artist}</span>
          <div style={styles.tags}>
            {song.genre && <Tag>{song.genre}</Tag>}
            {song.mood && <Tag>{song.mood}</Tag>}
          </div>
        </div>

        {/* Score */}
        <div style={styles.scoreBox}>
          <span style={styles.score}>{song.score.toFixed(2)}</span>
          <span style={styles.scoreLabel}>score</span>
        </div>

        {/* Expand indicator */}
        <span style={styles.chevron}>{expanded ? '▲' : '▼'}</span>
      </div>

      {/* Expanded reasons */}
      {expanded && (
        <div style={styles.reasons}>
          <span style={styles.reasonsLabel}>why this song</span>
          <ul style={styles.reasonList}>
            {song.reasons.map((r, i) => (
              <li key={i} style={styles.reasonItem}>{r}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

function Tag({ children }) {
  return <span style={tagStyle}>{children}</span>
}

const tagStyle = {
  fontFamily: 'JetBrains Mono, monospace',
  fontSize: '0.65rem',
  color: 'var(--muted)',
  backgroundColor: 'rgba(94, 122, 97, 0.15)',
  border: '1px solid var(--border)',
  borderRadius: 4,
  padding: '2px 7px',
  textTransform: 'lowercase',
}

const styles = {
  card: {
    backgroundColor: 'var(--surface-2)',
    border: '1px solid',
    borderRadius: 8,
    padding: '14px 18px',
    transition: 'border-color 0.15s ease, transform 0.15s ease',
    userSelect: 'none',
  },
  main: {
    display: 'flex',
    alignItems: 'center',
    gap: 14,
  },
  rank: {
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '0.78rem',
    color: 'var(--green)',
    fontWeight: 600,
    flex: '0 0 auto',
    width: 26,
  },
  info: {
    flex: 1,
    minWidth: 0,
    display: 'flex',
    flexDirection: 'column',
    gap: 3,
  },
  title: {
    fontSize: '0.97rem',
    fontWeight: 600,
    color: 'var(--text)',
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  artist: {
    fontSize: '0.84rem',
    color: 'var(--muted)',
  },
  tags: {
    display: 'flex',
    gap: 6,
    flexWrap: 'wrap',
    marginTop: 4,
  },
  scoreBox: {
    flex: '0 0 auto',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-end',
    gap: 2,
  },
  score: {
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '1.05rem',
    fontWeight: 600,
    color: 'var(--blue)',
  },
  scoreLabel: {
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '0.62rem',
    color: 'var(--muted)',
    textTransform: 'uppercase',
    letterSpacing: '0.06em',
  },
  chevron: {
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '0.6rem',
    color: 'var(--muted)',
    flex: '0 0 auto',
  },
  reasons: {
    marginTop: 12,
    paddingTop: 12,
    borderTop: '1px solid var(--border)',
  },
  reasonsLabel: {
    fontFamily: 'JetBrains Mono, monospace',
    fontSize: '0.65rem',
    color: 'var(--muted)',
    textTransform: 'uppercase',
    letterSpacing: '0.06em',
    display: 'block',
    marginBottom: 8,
  },
  reasonList: {
    listStyle: 'none',
    display: 'flex',
    flexDirection: 'column',
    gap: 5,
    paddingLeft: 0,
  },
  reasonItem: {
    fontSize: '0.85rem',
    color: 'var(--muted)',
    lineHeight: 1.5,
    paddingLeft: 12,
    position: 'relative',
  },
}
