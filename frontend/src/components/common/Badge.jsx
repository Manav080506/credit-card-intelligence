function Badge({ children, background = 'rgba(99,102,241,0.2)', color = '#c7d2fe', style }) {
  return (
    <span
      style={{
        display: 'inline-grid',
        placeItems: 'center',
        padding: '4px 8px',
        borderRadius: '999px',
        background,
        color,
        fontSize: '0.78rem',
        fontWeight: 600,
        ...style,
      }}
    >
      {children}
    </span>
  )
}

export default Badge
