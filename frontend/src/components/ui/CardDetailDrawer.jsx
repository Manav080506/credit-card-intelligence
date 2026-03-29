import { motion, AnimatePresence } from 'framer-motion'
import { Card, CardContent, CardTitle } from './card'

function CardDetailDrawer({ isOpen, onClose, card = null, reward_breakdown = {} }) {
  if (!card) return null

  const entries = Object.entries(reward_breakdown || {}).map(([category, value]) => ({
    category,
    value: Number(value || 0),
  }))

  const topCategories = [...entries].sort((a, b) => b.value - a.value).slice(0, 3)
  const fallbackBenefits = ['High reward efficiency', 'Optimized for your spend mix', 'Strong yearly return profile']

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

          <motion.div variants={drawer} initial="initial" animate="enter" exit="exit" className="fixed right-0 z-50 h-full w-full md:w-[460px] rounded-l-2xl border-l border-slate-700/50 bg-gradient-to-br from-slate-900/95 via-slate-900/90 to-slate-950/95 backdrop-blur-xl shadow-2xl overflow-y-auto">
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
              <Card>
                <CardContent className="space-y-3 p-4">
                  <CardTitle className="text-xs uppercase tracking-wider text-slate-300">Key Metrics</CardTitle>
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
                </CardContent>
              </Card>

              {/* Reward Structure table */}
              <Card>
                <CardContent className="p-4">
                  <CardTitle className="mb-3 text-xs uppercase tracking-wider text-slate-300">Reward Structure</CardTitle>
                  <div className="overflow-hidden rounded-lg border border-slate-700/40">
                    <table className="w-full text-xs">
                      <thead>
                        <tr className="bg-slate-800/40 text-slate-300">
                          <th className="px-3 py-2 text-left">Category</th>
                          <th className="px-3 py-2 text-right">Monthly Contribution</th>
                        </tr>
                      </thead>
                      <tbody>
                        {(entries.length ? entries : [{ category: 'other', value: 0 }]).map((row) => (
                          <tr key={row.category} className="border-t border-slate-700/30 text-slate-300">
                            <td className="px-3 py-2 capitalize">{row.category.replace(/_/g, ' ')}</td>
                            <td className="px-3 py-2 text-right">₹{row.value.toLocaleString()}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </CardContent>
              </Card>

              {/* Key Benefits */}
              <Card>
                <CardContent className="p-4">
                  <CardTitle className="mb-3 text-xs uppercase tracking-wider text-slate-300">Key Benefits</CardTitle>
                  <ul className="space-y-2">
                    {(card.pros && card.pros.length ? card.pros : fallbackBenefits).slice(0, 5).map((item, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm text-slate-300">
                        <span className="mt-0.5 text-emerald-400">•</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              {/* Milestone Bonuses */}
              <Card>
                <CardContent className="p-4">
                  <CardTitle className="mb-3 text-xs uppercase tracking-wider text-slate-300">Milestone Bonuses</CardTitle>
                  <div className="rounded-lg border border-slate-700/30 bg-slate-800/30 p-3 text-sm text-slate-300">
                    {Number(card.milestone_bonus || 0) > 0 ? `Bonus value ₹${Number(card.milestone_bonus).toLocaleString()} available on threshold completion.` : 'No active milestone bonus configured.'}
                  </div>
                </CardContent>
              </Card>

              {/* Lounge access */}
              <Card>
                <CardContent className="p-4">
                  <CardTitle className="mb-3 text-xs uppercase tracking-wider text-slate-300">Lounge Access</CardTitle>
                  <div className="rounded-lg border border-slate-700/30 bg-slate-800/30 p-3 text-sm text-slate-300">
                    {card.lounge_access ? 'Included for this card.' : 'Not included for this card.'}
                  </div>
                </CardContent>
              </Card>

              {/* Best spend categories */}
              <Card>
                <CardContent className="p-4">
                  <CardTitle className="mb-3 text-xs uppercase tracking-wider text-slate-300">Best Spend Categories</CardTitle>
                  <div className="flex flex-wrap gap-2">
                    {(topCategories.length ? topCategories : [{ category: 'general', value: 0 }]).map((row) => (
                      <span key={row.category} className="rounded-full border border-cyan-500/35 bg-cyan-500/10 px-2.5 py-1 text-xs text-cyan-200">
                        {row.category.replace(/_/g, ' ')}
                      </span>
                    ))}
                  </div>
                </CardContent>
              </Card>

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
