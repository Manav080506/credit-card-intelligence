import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart } from 'recharts'
import { motion } from 'framer-motion'
import { useMemo } from 'react'

function SavingsProjectionChart({ currentCard, recommendedCard, formatMoney = (v) => v, monthlyReward = 0, yearlyReward = 0 }) {
  const data = useMemo(() => {
    const chartData = []
    const monthlyCurrentGain = monthlyReward * 0.6 // Assume 60% savings vs current card
    const monthlyRecommendedGain = monthlyReward

    for (let month = 0; month <= 12; month++) {
      chartData.push({
        month: month === 0 ? 'Now' : `Month ${month}`,
        current: Math.round(monthlyCurrentGain * month),
        recommended: Math.round(monthlyRecommendedGain * month),
        difference: Math.round(monthlyRecommendedGain * month - monthlyCurrentGain * month),
      })
    }

    return chartData
  }, [monthlyReward])

  const maxDifference = Math.max(...data.map((d) => d.difference))

  const containerVariants = {
    initial: { opacity: 0, y: 10 },
    enter: { opacity: 1, y: 0 },
    transition: { duration: 0.4 },
  }

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="rounded-lg border border-slate-600/50 bg-slate-900/95 backdrop-blur-sm p-3 shadow-lg">
          <p className="text-xs font-semibold text-slate-200">{payload[0].payload.month}</p>
          {payload.map((entry, index) => (
            <p key={index} className="mt-1 text-xs" style={{ color: entry.color }}>
              {entry.name}: ₹{formatMoney(entry.value)}
            </p>
          ))}
          <p className="mt-2 text-xs font-bold text-emerald-400">
            Gain: ₹{formatMoney(payload[0].payload.difference)}
          </p>
        </motion.div>
      )
    }
    return null
  }

  return (
    <motion.div variants={containerVariants} initial="initial" animate="enter" className="rounded-xl border border-indigo-500/30 bg-gradient-to-br from-slate-900/60 via-slate-900/50 to-slate-950/60 backdrop-blur-sm p-6 shadow-lg">
      <div className="mb-6">
        <h3 className="text-lg font-bold text-slate-50">Yearly Savings Projection</h3>
        <p className="mt-1 text-sm text-slate-400">Compare your current rewards vs. recommended card</p>
      </div>

      {/* Stats Cards */}
      <div className="mb-6 grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="rounded-lg border border-slate-700/50 bg-slate-800/40 p-3.5 backdrop-blur-sm">
          <p className="text-xs font-medium uppercase tracking-wider text-slate-400">Current Card Yearly</p>
          <p className="mt-2 text-xl md:text-2xl font-bold text-slate-200">₹{formatMoney((monthlyReward * 0.6 * 12).toFixed(0))}</p>
        </div>
        <div className="rounded-lg border border-slate-700/50 bg-slate-800/40 p-3.5 backdrop-blur-sm">
          <p className="text-xs font-medium uppercase tracking-wider text-slate-400">Recommended Card Yearly</p>
          <p className="mt-2 text-xl md:text-2xl font-bold text-emerald-400">₹{formatMoney((monthlyReward * 12).toFixed(0))}</p>
        </div>
        <div className="rounded-lg border border-emerald-500/30 bg-gradient-to-br from-emerald-500/15 to-slate-900/40 p-3.5 backdrop-blur-sm">
          <p className="text-xs font-medium uppercase tracking-wider text-emerald-300">Additional Gain</p>
          <p className="mt-2 text-xl md:text-2xl font-bold text-emerald-400">₹{formatMoney((monthlyReward * 0.4 * 12).toFixed(0))}</p>
        </div>
      </div>

      {/* Chart */}
      <div className="mt-6 rounded-lg border border-slate-700/40 bg-slate-950/40 p-4 overflow-hidden">
        <ResponsiveContainer width="100%" height={320}>
          <AreaChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
            <defs>
              <linearGradient id="colorCurrent" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#94a3b8" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#94a3b8" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorRecommended" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155/50" />
            <XAxis dataKey="month" stroke="#94a3b8" style={{ fontSize: '12px' }} />
            <YAxis stroke="#94a3b8" style={{ fontSize: '12px' }} />
            <Tooltip content={<CustomTooltip />} />
            <Legend wrapperStyle={{ paddingTop: '16px', fontSize: '12px' }} />
            <Area
              type="monotone"
              dataKey="current"
              stroke="#94a3b8"
              fill="url(#colorCurrent)"
              name={`Current Card: ₹${formatMoney((monthlyReward * 0.6).toFixed(0))}/mo`}
              isAnimationActive={true}
            />
            <Area
              type="monotone"
              dataKey="recommended"
              stroke="#10b981"
              fill="url(#colorRecommended)"
              name={`Recommended Card: ₹${formatMoney(monthlyReward.toFixed(0))}/mo`}
              isAnimationActive={true}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Insights */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-3">
        <div className="rounded-lg border border-emerald-500/30 bg-emerald-500/10 p-3.5">
          <p className="text-xs font-bold text-emerald-300 uppercase tracking-wider">Key Insight</p>
          <p className="mt-2 text-sm text-emerald-100">
            Switching saves you <strong>₹{formatMoney((monthlyReward * 0.4 * 12).toFixed(0))}</strong> per year in rewards
          </p>
        </div>
        <div className="rounded-lg border border-cyan-500/30 bg-cyan-500/10 p-3.5">
          <p className="text-xs font-bold text-cyan-300 uppercase tracking-wider">Breakeven Point</p>
          <p className="mt-2 text-sm text-cyan-100">
            Recover annual fee in <strong>{Math.ceil((monthlyReward * 0.4 * 12) / 100) || 1} months</strong>
          </p>
        </div>
      </div>
    </motion.div>
  )
}

export default SavingsProjectionChart
