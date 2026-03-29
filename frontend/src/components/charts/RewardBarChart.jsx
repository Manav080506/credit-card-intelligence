import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

function ChartTooltip({ active, payload }) {
  if (!active || !payload?.length) {
    return null
  }

  return (
    <div className="rounded-lg border border-slate-700 bg-slate-950 px-2.5 py-1.5 text-xs text-slate-100 shadow-[0_2px_12px_rgba(0,0,0,0.25)]">
      <div className="font-medium">Reward</div>
      <div className="text-emerald-400">₹ {Number(payload[0].value || 0).toFixed(2)}</div>
    </div>
  )
}

function RewardBarChart({ data, loading, formatCompact, formatMoney }) {
  if (loading) {
    return <div className="h-full w-full animate-pulse rounded-xl bg-slate-800/80" />
  }

  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data} margin={{ top: 8, right: 10, left: 0, bottom: 20 }}>
        <defs>
          <linearGradient id="rewardBarGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#7c83ff" stopOpacity={0.95} />
            <stop offset="95%" stopColor="#4954dd" stopOpacity={0.8} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="2 6" stroke="rgba(148,163,184,0.12)" vertical={false} />
        <XAxis dataKey="category" tick={{ fontSize: 11, fill: '#94a3b8' }} angle={-15} textAnchor="end" />
        <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} tickFormatter={(v) => formatCompact(v)} />
        <Tooltip content={<ChartTooltip />} />
        <Bar dataKey="reward" fill="url(#rewardBarGradient)" radius={[8, 8, 0, 0]} isAnimationActive animationDuration={600} />
      </BarChart>
    </ResponsiveContainer>
  )
}

export default RewardBarChart
