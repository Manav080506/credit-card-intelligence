import { motion, AnimatePresence } from 'framer-motion'
import { useEffect, useState } from 'react'

function ComparisonModal({ isOpen, onClose, cards = [], selectedCard = null, formatMoney = (v) => v }) {
  const [selectedIndex, setSelectedIndex] = useState(0)

  useEffect(() => {
    if (!isOpen) return undefined
    const originalOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => {
      document.body.style.overflow = originalOverflow
    }
  }, [isOpen])

  if (!isOpen || !cards.length) return null

  const displayCards = cards.slice(0, 3)

  const cardMetrics = [
    { label: 'Annual Fee', key: 'annual_fee' },
    { label: 'Monthly Reward', key: 'monthly_reward' },
    { label: 'Yearly Reward', key: 'yearly_reward' },
    { label: 'Reward Efficiency', key: 'efficiency_score' },
    { label: 'Lounge Access', key: 'lounge_access' },
    { label: 'Forex Markup', key: 'forex_markup' },
  ]

  const getBestValue = (key) => {
    return displayCards.map((c) => c[key] || 0).reduce((max, val) => Math.max(max, val), 0)
  }

  const isBest = (cardIdx, key) => {
    return displayCards[cardIdx][key] === getBestValue(key)
  }

  const overlay = {
    initial: { opacity: 0 },
    enter: { opacity: 1 },
    exit: { opacity: 0 },
  }

  const modal = {
    initial: { opacity: 0, scale: 0.9, y: 20 },
    enter: { opacity: 1, scale: 1, y: 0 },
    exit: { opacity: 0, scale: 0.9, y: 20 },
  }

  return (
    <AnimatePresence>
      <motion.div
        variants={overlay}
        initial="initial"
        animate="enter"
        exit="exit"
        className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm"
        onClick={onClose}
      >
      <motion.div
        variants={modal}
        initial="initial"
        animate="enter"
        exit="exit"
        className="w-[1100px] max-h-[90vh] max-w-[95vw] overflow-y-auto rounded-2xl border border-white/10 bg-[#0b1120] p-6 shadow-2xl"
        style={{ paddingBottom: '40px' }}
        onClick={(event) => event.stopPropagation()}
      >
        {/* Header */}
        <div className="relative border-b border-slate-700/50 bg-gradient-to-r from-slate-900/40 to-slate-950/40 px-2 py-3 md:px-4 md:py-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg md:text-2xl font-bold text-slate-50">Card Comparison</h2>
              <p className="mt-1 text-xs md:text-sm text-slate-400">Find the card that maximizes your rewards</p>
            </div>
            <button
              onClick={onClose}
              className="flex h-10 w-10 items-center justify-center rounded-lg bg-slate-800/50 hover:bg-slate-700/50 transition-colors text-slate-400 hover:text-slate-200"
              aria-label="Close"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Content */}
          <div className="pt-6 md:pt-8">
            {/* Cards Grid Header */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
              {displayCards.map((card, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.1 }}
                  className={`rounded-xl border ${idx === selectedIndex ? 'border-emerald-500/50 bg-gradient-to-br from-emerald-500/10 to-slate-900/40' : 'border-slate-700/40 bg-slate-800/30'} p-4 transition-all`}
                >
                  <div className="mb-3 flex items-start justify-between">
                    <div>
                      <p className="text-xs font-bold uppercase tracking-wider text-slate-400">{card.bank || 'Bank'}</p>
                      <h3 className="mt-1 text-base md:text-lg font-bold text-slate-100">{card.name || 'Card Name'}</h3>
                    </div>
                    {idx === selectedIndex && (
                      <span className="inline-flex items-center gap-1 rounded-full bg-emerald-500/20 px-2.5 py-1 text-xs font-semibold text-emerald-300 border border-emerald-400/50">
                        ✓ Best Match
                      </span>
                    )}
                  </div>

                  <div className="space-y-2.5">
                    <div className="rounded-lg bg-slate-900/60 p-2.5 border border-slate-700/30">
                      <p className="text-xs text-slate-400">Monthly Reward</p>
                      <p className="mt-1 text-lg font-bold text-cyan-400">₹{formatMoney(card.monthly_reward || 0)}</p>
                    </div>
                    <div className="rounded-lg bg-slate-900/60 p-2.5 border border-slate-700/30">
                      <p className="text-xs text-slate-400">Annual Fee</p>
                      <p className="mt-1 text-lg font-bold text-slate-100">₹{formatMoney(card.annual_fee || 0)}</p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Metrics Table */}
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-700/40">
                    <th className="text-left py-3 px-3 md:px-4 text-xs font-semibold uppercase tracking-wider text-slate-400">Metric</th>
                    {displayCards.map((card, idx) => (
                      <th key={idx} className="text-center py-3 px-3 md:px-4 text-xs font-semibold uppercase tracking-wider text-slate-300">
                        {card.bank}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700/30">
                  {cardMetrics.map((metric) => (
                    <tr key={metric.key} className="hover:bg-slate-800/30 transition-colors">
                      <td className="py-3 px-3 md:px-4 text-slate-300 font-medium">{metric.label}</td>
                      {displayCards.map((card, idx) => {
                        const value = card[metric.key]
                        const isBestVal = isBest(idx, metric.key)
                        return (
                          <td
                            key={idx}
                            className={`py-3 px-3 md:px-4 text-center font-semibold transition-colors ${
                              isBestVal
                                ? 'bg-emerald-500/15 text-emerald-300 border-l-2 border-r-2 border-emerald-500/30'
                                : 'text-slate-300'
                            }`}
                          >
                            {metric.key.includes('fee') || metric.key.includes('reward') ? `₹${formatMoney(value || 0)}` : value || '—'}
                          </td>
                        )
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pros & Cons */}
            <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
              {displayCards.map((card, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.3 + idx * 0.1 }}
                  className="rounded-xl border border-slate-700/40 bg-slate-800/20 p-4"
                >
                  <div className="mb-3">
                    <p className="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-2">Pros</p>
                    <ul className="space-y-1.5">
                      {(card.pros || ['High rewards', 'Good benefits']).slice(0, 3).map((pro, i) => (
                        <li key={i} className="flex gap-2 text-xs text-slate-300">
                          <span className="text-emerald-400 flex-shrink-0">✓</span>
                          <span>{pro}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <p className="text-xs font-bold uppercase tracking-wider text-orange-400 mb-2">Cons</p>
                    <ul className="space-y-1.5">
                      {(card.cons || ['Annual fee', 'Limited categories']).slice(0, 3).map((con, i) => (
                        <li key={i} className="flex gap-2 text-xs text-slate-400">
                          <span className="text-orange-400 flex-shrink-0">✕</span>
                          <span>{con}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

        {/* Footer */}
        <div className="mt-6 flex justify-end gap-3 border-t border-slate-700/50 bg-gradient-to-r from-slate-900/40 to-slate-950/40 px-2 py-4 md:px-4 md:py-5">
          <button
            onClick={onClose}
            className="px-4 py-2.5 rounded-lg border border-slate-600/50 bg-slate-800/50 hover:bg-slate-700/50 text-slate-200 text-sm font-medium transition-colors"
          >
            Close
          </button>
          <button className="px-4 py-2.5 rounded-lg bg-gradient-to-r from-emerald-600 to-cyan-600 hover:from-emerald-500 hover:to-cyan-500 text-white text-sm font-semibold transition-all shadow-lg hover:shadow-emerald-500/30">
            Apply Now
          </button>
        </div>
      </motion.div>
      </motion.div>
    </AnimatePresence>
  )
}

export default ComparisonModal
