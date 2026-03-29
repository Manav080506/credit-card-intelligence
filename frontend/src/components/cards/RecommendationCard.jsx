import { Badge } from '../ui/badge'
import { Card, CardContent } from '../ui/card'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '../ui/tooltip'
import { motion } from 'framer-motion'
import { useMemo } from 'react'

function CardLogoBadge({ cardName }) {
  const lower = String(cardName || '').toLowerCase()
  let label = 'C'
  let bgClass = 'bg-slate-500/30'
  let borderClass = 'border-slate-400/30'

  if (lower.includes('hdfc')) {
    label = 'H'
    bgClass = 'bg-sky-500/40'
    borderClass = 'border-sky-400/50'
  } else if (lower.includes('sbi')) {
    label = 'S'
    bgClass = 'bg-indigo-500/40'
    borderClass = 'border-indigo-400/50'
  } else if (lower.includes('icici')) {
    label = 'I'
    bgClass = 'bg-orange-500/40'
    borderClass = 'border-orange-400/50'
  } else if (lower.includes('axis')) {
    label = 'A'
    bgClass = 'bg-pink-500/40'
    borderClass = 'border-pink-400/50'
  }

  return (
    <motion.span
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.3 }}
      className={`grid h-12 w-12 place-items-center rounded-full text-lg font-bold text-slate-50 border ${bgClass} ${borderClass} backdrop-blur-sm`}
    >
      {label}
    </motion.span>
  )
}

function InsightBullet({ icon, text, metric = null }) {
  return (
    <motion.div
      initial={{ x: -10, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="flex items-start gap-2.5"
    >
      <div className="mt-1 flex h-5 w-5 items-center justify-center rounded-full bg-emerald-500/30 text-emerald-300 text-xs font-bold flex-shrink-0">
        {icon}
      </div>
      <div className="min-w-0 flex-1">
        <p className="text-sm text-slate-200">{text}</p>
        {metric && <p className="mt-0.5 text-xs text-emerald-400 font-medium">{metric}</p>}
      </div>
    </motion.div>
  )
}

function ConfidenceMeter({ percent }) {
  return (
    <div className="space-y-1.5">
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-slate-300">Optimization Score</span>
        <span className="text-sm font-bold text-emerald-400">{percent.toFixed(0)}%</span>
      </div>
      <div className="h-2.5 w-full rounded-full bg-slate-800/60 border border-slate-700/50 overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percent}%` }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          className="h-full bg-gradient-to-r from-emerald-500 to-cyan-400 rounded-full"
        />
      </div>
    </div>
  )
}

function AlternativeCard({ cardName, monthlyGain, formatMoney }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.2 }}
      className="mt-4 rounded-xl border border-slate-700/40 bg-gradient-to-br from-slate-800/40 via-slate-800/20 to-slate-900/40 p-3.5 backdrop-blur-sm hover:border-slate-600/60 transition-colors"
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Alternative</p>
          <p className="mt-1 text-sm font-semibold text-slate-100">{cardName}</p>
        </div>
        <div className="text-right">
          <p className="text-xs text-slate-400">Potential gain</p>
          <p className="mt-0.5 text-sm font-bold text-emerald-400">₹{formatMoney(monthlyGain)}/mo</p>
        </div>
      </div>
    </motion.div>
  )
}

function RecommendationCard({ result, animatedReward, confidencePercent, aiInsight, loading, formatMoney, bestCardSuggestion, className = '' }) {
  const bestCard = result?.best_card || bestCardSuggestion || 'SBI Cashback'

  const secondBestCard = useMemo(() => {
    if (result?.second_best_card) {
      return result.second_best_card
    }
    if (bestCard.includes('SBI')) {
      return 'HDFC Millennia'
    }
    if (bestCard.includes('HDFC')) {
      return 'ICICI Amazon Pay'
    }
    return 'Axis MyX Credit Card'
  }, [bestCard, result])

  const monthlyGain = Number(result?.expected_monthly_reward || animatedReward || 0)
  const yearlyGain = Number(result?.expected_yearly_reward || monthlyGain * 12)

  const insights = useMemo(() => {
    const rules = []
    if (result?.online_ratio > 0.45) {
      rules.push({ icon: '🛒', text: 'High online spending detected', metric: `${(result.online_ratio * 100).toFixed(0)}% of transactions` })
    }
    if (result?.travel_ratio > 0.35) {
      rules.push({ icon: '✈️', text: 'Travel-heavy profile identified', metric: `${(result.travel_ratio * 100).toFixed(0)}% travel spend` })
    }
    if (!result?.online_ratio && !result?.travel_ratio) {
      rules.push({ icon: '⚖️', text: 'Balanced spend pattern detected', metric: 'Multi-category optimization' })
    }
    rules.push({ icon: '💰', text: 'High reward efficiency score', metric: `${confidencePercent.toFixed(0)}% match accuracy` })
    return rules.slice(0, 3)
  }, [result, confidencePercent])

  if (loading) {
    return (
      <Card className={`min-h-[380px] border-indigo-500/20 bg-gradient-to-br from-slate-900/50 to-slate-950/50 backdrop-blur-sm ${className}`.trim()}>
        <CardContent className="p-6">
          <div className="space-y-4">
            <div className="h-12 w-12 rounded-full bg-slate-800/60 animate-pulse" />
            <div className="h-8 w-3/4 rounded-lg bg-slate-800/60 animate-pulse" />
            <div className="space-y-2">
              <div className="h-4 w-full rounded-md bg-slate-800/60 animate-pulse" />
              <div className="h-4 w-4/5 rounded-md bg-slate-800/60 animate-pulse" />
            </div>
            <div className="h-6 w-1/2 rounded-lg bg-slate-800/60 animate-pulse" />
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className={`relative overflow-hidden min-h-[420px] border border-gradient-to-r from-indigo-500/30 via-slate-700/30 to-cyan-500/30 bg-gradient-to-br from-slate-900/60 via-slate-900/50 to-slate-950/60 backdrop-blur-xl shadow-xl ${className}`.trim()}>
      {/* Animated gradient background */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute inset-x-4 top-4 h-32 rounded-3xl bg-gradient-to-r from-indigo-500/5 via-cyan-500/5 to-indigo-500/5 blur-2xl" />
        <div className="absolute right-0 -top-20 h-40 w-40 rounded-full bg-indigo-500/10 blur-3xl" />
      </div>

      <CardContent className="relative p-6">
        {/* Hero Section */}
        <div className="mb-6">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3 }}
            className="flex items-start gap-4"
          >
            <CardLogoBadge cardName={bestCard} />
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <motion.span
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.1, type: 'spring', stiffness: 200 }}
                >
                  <Badge className="bg-emerald-500/30 text-emerald-200 border border-emerald-400/50 hover:bg-emerald-500/40">
                    ⭐ BEST MATCH
                  </Badge>
                </motion.span>
              </div>
              <motion.h2
                initial={{ opacity: 0, y: 4 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="text-2xl font-bold text-slate-50 truncate"
              >
                {bestCard}
              </motion.h2>
            </div>
          </motion.div>
        </div>

        {/* Reward Metrics */}
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-6 grid grid-cols-2 gap-3"
        >
          <div className="rounded-lg bg-slate-800/40 border border-slate-700/50 p-3 backdrop-blur-sm">
            <p className="text-xs font-medium text-slate-400">Monthly Reward</p>
            <p className="mt-1.5 text-xl font-bold text-emerald-400">₹{formatMoney(monthlyGain)}</p>
          </div>
          <div className="rounded-lg bg-slate-800/40 border border-slate-700/50 p-3 backdrop-blur-sm">
            <p className="text-xs font-medium text-slate-400">Yearly Reward</p>
            <p className="mt-1.5 text-xl font-bold text-cyan-400">₹{formatMoney(yearlyGain)}</p>
          </div>
        </motion.div>

        {/* Confidence Meter */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="mb-6"
        >
          <ConfidenceMeter percent={confidencePercent} />
        </motion.div>

        {/* Insights */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.35 }}
          className="mb-6 space-y-2.5"
        >
          <p className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Why this card?</p>
          {insights.map((insight, idx) => (
            <InsightBullet key={idx} icon={insight.icon} text={insight.text} metric={insight.metric} />
          ))}
        </motion.div>

        {/* Alternative Card */}
        <AlternativeCard cardName={secondBestCard} monthlyGain={monthlyGain * 0.75} formatMoney={formatMoney} />

        {/* AI Insight */}
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.4 }}
          className="mt-4 rounded-xl border border-cyan-400/30 bg-gradient-to-r from-cyan-500/10 to-indigo-500/10 p-3.5 backdrop-blur-sm"
        >
          <p className="text-xs font-semibold text-cyan-200 uppercase tracking-wider mb-1">AI Insight</p>
          <p className="text-sm text-cyan-100 leading-relaxed">{aiInsight || 'Analyzing your spend pattern...'}</p>
        </motion.div>
      </CardContent>
    </Card>
  )
}

export default RecommendationCard
