import { motion, AnimatePresence } from 'framer-motion'

function CardDetailDrawer({ isOpen, onClose, card = null }) {
  if (!card) return null

  const drawer = {
    initial: { x: '100%', opacity: 0 },
    enter: { x: 0, opacity: 1 },
    exit: { x: '100%', opacity: 0 },
    transition: { type: 'spring', damping: 25, stiffness: 200 },
  }

  const overlay = {
    initial: { opacity: 0 },
    enter: { opacity: 1 },
    exit: { opacity: 0 },
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div variants={overlay} initial="initial" animate="enter" exit="exit" className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm" onClick={onClose} />

          <motion.div variants={drawer} initial="initial" animate="enter" exit="exit" className="fixed right-0 z-50 h-full w-full md:w-96 rounded-l-2xl border-l border-slate-700/50 bg-gradient-to-br from-slate-900/95 via-slate-900/90 to-slate-950/95 backdrop-blur-xl shadow-2xl overflow-y-auto">
            {/* Header */}
            <div className="sticky top-0 border-b border-slate-700/50 bg-gradient-to-b from-slate-900/60 to-slate-950/60 backdrop-blur-sm px-6 py-6">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-xs font-bold uppercase tracking-wider text-slate-400">{card.bank || 'Bank'}</p>
                  <h2 className="mt-2 text-lg md:text-xl font-bold text-slate-50">{card.name || 'Card Name'}</h2>
                  {card.segment && (
                    <p className="mt-1 text-xs text-slate-400 capitalize">
                      {card.segment.replace(/_/g, ' ')} • {card.efficiency_score ? `${Math.round(card.efficiency_score * 100)}% efficient` : ''}
                    </p>
                  )}
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
            <div className="px-6 py-6 space-y-6">
              {/* Key Metrics */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-3">Key Metrics</h3>
                <div className="space-y-2.5">
                  <div className="flex items-center justify-between rounded-lg bg-slate-800/40 border border-slate-700/30 p-3">
                    <span className="text-sm text-slate-400">Monthly Reward</span>
                    <span className="text-lg font-bold text-emerald-400">₹{(card.monthly_reward || 0).toLocaleString()}</span>
                  </div>
                  <div className="flex items-center justify-between rounded-lg bg-slate-800/40 border border-slate-700/30 p-3">
                    <span className="text-sm text-slate-400">Annual Fee</span>
                    <span className="text-lg font-bold text-slate-100">₹{(card.annual_fee || 0).toLocaleString()}</span>
                  </div>
                  <div className="flex items-center justify-between rounded-lg bg-slate-800/40 border border-slate-700/30 p-3">
                    <span className="text-sm text-slate-400">Yearly Reward</span>
                    <span className="text-lg font-bold text-cyan-400">₹{(card.yearly_reward || 0).toLocaleString()}</span>
                  </div>
                </div>
              </div>

              {/* Category Rewards */}
              {card.categories && (
                <div>
                  <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-3">Category Multipliers</h3>
                  <div className="space-y-2">
                    {Object.entries(card.categories).map(([category, multiplier]) => (
                      <div key={category} className="flex items-center justify-between rounded-lg bg-slate-800/30 border border-slate-700/30 p-2.5">
                        <span className="text-xs font-medium text-slate-400 capitalize">{category.replace(/_/g, ' ')}</span>
                        <span className={`text-sm font-bold ${multiplier > 2 ? 'text-emerald-400' : multiplier > 1 ? 'text-cyan-400' : 'text-slate-400'}`}>
                          {multiplier}x
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Benefits */}
              {card.lounge_access && (
                <div>
                  <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-3">Key Benefits</h3>
                  <div className="space-y-2">
                    {card.lounge_access && (
                      <div className="flex items-center gap-2.5 rounded-lg bg-purple-500/10 border border-purple-500/30 p-3">
                        <span className="text-lg">🛋️</span>
                        <div>
                          <p className="text-sm font-semibold text-slate-100">Lounge Access</p>
                          <p className="mt-0.5 text-xs text-slate-400">Airport & travel lounges</p>
                        </div>
                      </div>
                    )}
                    {card.forex_markup !== undefined && (
                      <div className="flex items-center gap-2.5 rounded-lg bg-blue-500/10 border border-blue-500/30 p-3">
                        <span className="text-lg">🌍</span>
                        <div>
                          <p className="text-sm font-semibold text-slate-100">Forex Markup</p>
                          <p className="mt-0.5 text-xs text-slate-400">{card.forex_markup}% on international</p>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Pros */}
              {card.pros && card.pros.length > 0 && (
                <div>
                  <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-300 mb-3">Pros</h3>
                  <ul className="space-y-2">
                    {card.pros.map((pro, idx) => (
                      <li key={idx} className="flex gap-2.5 text-sm text-slate-300">
                        <span className="text-emerald-400 flex-shrink-0 font-bold">✓</span>
                        <span>{pro}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Cons */}
              {card.cons && card.cons.length > 0 && (
                <div>
                  <h3 className="text-xs font-bold uppercase tracking-wider text-orange-300 mb-3">Cons</h3>
                  <ul className="space-y-2">
                    {card.cons.map((con, idx) => (
                      <li key={idx} className="flex gap-2.5 text-sm text-slate-400">
                        <span className="text-orange-400 flex-shrink-0 font-bold">×</span>
                        <span>{con}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Footer */}
            <div className="sticky bottom-0 border-t border-slate-700/50 bg-gradient-to-t from-slate-950/60 to-slate-900/60 backdrop-blur-sm px-6 py-4 flex gap-3">
              <button
                onClick={onClose}
                className="flex-1 px-4 py-2.5 rounded-lg border border-slate-600/50 bg-slate-800/50 hover:bg-slate-700/50 text-slate-200 text-sm font-medium transition-colors"
              >
                Close
              </button>
              <button className="flex-1 px-4 py-2.5 rounded-lg bg-gradient-to-r from-emerald-600 to-cyan-600 hover:from-emerald-500 hover:to-cyan-500 text-white text-sm font-semibold transition-all shadow-lg hover:shadow-emerald-500/30">
                Apply Now
              </button>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}

export default CardDetailDrawer
