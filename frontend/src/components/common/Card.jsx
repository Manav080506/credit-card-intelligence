import { radius } from '../../styles/theme'

export function cardVariantStyle(variant, cardBg) {
  if (variant === 'primary') {
    return {
      background: `linear-gradient(160deg, ${cardBg} 0%, #111c33 100%)`,
      border: '1px solid rgba(129, 140, 248, 0.25)',
      borderRadius: `${radius.md}px`,
      boxShadow: '0 2px 10px rgba(0, 0, 0, 0.18)',
    }
  }

  return {
    background: cardBg,
    border: '1px solid rgba(255, 255, 255, 0.05)',
    borderRadius: `${radius.md}px`,
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.18)',
  }
}

function Card({ variant = 'secondary', cardBg, style, children, className = '' }) {
  return (
    <section className={className} style={{ ...cardVariantStyle(variant, cardBg), ...style }}>
      {children}
    </section>
  )
}

export default Card
