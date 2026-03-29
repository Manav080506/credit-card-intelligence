export const fadeUp = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.35, ease: 'easeOut' },
}

export const stagger = {
  animate: {
    transition: {
      staggerChildren: 0.06,
    },
  },
}

export const hoverCard = {
  scale: 1.015,
  boxShadow: '0 8px 30px rgba(0,0,0,0.35)',
}
