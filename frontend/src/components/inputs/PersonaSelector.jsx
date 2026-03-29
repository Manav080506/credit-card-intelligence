import { motion } from 'framer-motion'
import { useState } from 'react'

const PERSONAS = [
  {
    id: 'student',
    label: 'Student',
    emoji: '🎓',
    description: 'Low spend, online-heavy',
    metrics: { online_shopping: 5000, dining: 2000, travel: 1000, utilities: 1500 },
  },
  {
    id: 'professional',
    label: 'Professional',
    emoji: '💼',
    description: 'Balanced spend, everyday cards',
    metrics: { online_shopping: 10000, dining: 5000, travel: 8000, utilities: 3000 },
  },
  {
    id: 'traveler',
    label: 'Frequent Traveler',
    emoji: '✈️',
    description: 'Travel-focused, premium benefits',
    metrics: { online_shopping: 8000, dining: 4000, travel: 20000, utilities: 2000 },
  },
  {
    id: 'foodie',
    label: 'Foodie',
    emoji: '🍽️',
    description: 'Dining-focused, high spend',
    metrics: { online_shopping: 6000, dining: 12000, travel: 3000, utilities: 2000 },
  },
  {
    id: 'shopper',
    label: 'Online Shopper',
    emoji: '🛍️',
    description: 'E-commerce heavy, cashback',
    metrics: { online_shopping: 18000, dining: 3000, travel: 2000, utilities: 2000 },
  },
  {
    id: 'high_net_worth',
    label: 'Premium Lifestyle',
    emoji: '👑',
    description: 'High spend, luxury benefits',
    metrics: { online_shopping: 15000, dining: 10000, travel: 15000, utilities: 5000 },
  },
]

function PersonaSelector({ onSelect, selectedPersona }) {
  const [hoveredId, setHoveredId] = useState(null)

  const containerVariants = {
    initial: { opacity: 0 },
    enter: { opacity: 1, transition: { staggerChildren: 0.05 } },
  }

  const itemVariants = {
    initial: { opacity: 0, y: 10 },
    enter: { opacity: 1, y: 0 },
  }

  return (
    <motion.div variants={containerVariants} initial="initial" animate="enter">
      <div className="mb-4">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-300">Quick Personas</h3>
        <p className="mt-1 text-xs text-slate-400">Select your spending profile for instant recommendations</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {PERSONAS.map((persona, idx) => (
          <motion.button
            key={persona.id}
            variants={itemVariants}
            onClick={() => onSelect(persona.metrics)}
            onMouseEnter={() => setHoveredId(persona.id)}
            onMouseLeave={() => setHoveredId(null)}
            className={`relative p-4 rounded-xl border-2 transition-all text-left ${
              selectedPersona?.online_shopping === persona.metrics.online_shopping
                ? 'border-emerald-500/50 bg-gradient-to-br from-emerald-500/15 to-slate-900/40'
                : 'border-slate-700/40 bg-slate-800/20 hover:border-slate-600/60'
            }`}
          >
            {/* Hover glow */}
            {hoveredId === persona.id && (
              <motion.div
                layoutId="glow"
                className="absolute inset-0 rounded-xl bg-gradient-to-r from-emerald-500/10 to-cyan-500/10"
              />
            )}

            <div className="relative">
              <div className="text-2xl mb-2">{persona.emoji}</div>
              <h4 className="text-sm font-bold text-slate-100">{persona.label}</h4>
              <p className="text-xs mt-1 text-slate-400">{persona.description}</p>

              {/* Metric preview */}
              <div className="mt-2.5 space-y-0.5">
                <p className="text-xs font-medium text-slate-300">
                  💰 ₹{(persona.metrics.online_shopping + persona.metrics.dining + persona.metrics.travel + persona.metrics.utilities).toLocaleString()}/mo
                </p>
                {selectedPersona?.online_shopping === persona.metrics.online_shopping && (
                  <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-xs text-emerald-400 font-semibold">
                    ✓ Selected
                  </motion.p>
                )}
              </div>
            </div>
          </motion.button>
        ))}
      </div>
    </motion.div>
  )
}

export default PersonaSelector
