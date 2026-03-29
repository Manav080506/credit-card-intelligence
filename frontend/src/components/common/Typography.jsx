import { typography } from '../../styles/theme'

export function PageTitle({ children, style }) {
  return <h1 style={{ ...typography.pageTitle, ...style }}>{children}</h1>
}

export function SectionTitle({ children, style }) {
  return <h2 style={{ ...typography.sectionTitle, ...style }}>{children}</h2>
}

export function CardTitle({ children, style }) {
  return <h3 style={{ ...typography.cardTitle, ...style }}>{children}</h3>
}
