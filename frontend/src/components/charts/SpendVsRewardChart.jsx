import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

function ChartTooltip({ active, payload }) {
  if (!active || !payload?.length) {
    return null
  }

  return (
    <div className="rounded-lg border border-slate-700 bg-slate-950 px-2.5 py-1.5 text-xs text-slate-100 shadow-[0_2px_12px_rgba(0,0,0,0.25)]">
      <div className="font-medium">Projected Reward</div>
      <div className="text-emerald-400">₹ {Number(payload[0].value || 0).toFixed(2)}</div>
    </div>
  )
}

function SpendVsRewardChart({ data, loading, formatCompact, formatMoney }) {
  if (loading) {
    return <div className="h-full w-full animate-pulse rounded-xl bg-slate-800/80" />
  }

  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={data} margin={{ top: 12, right: 10, left: 0, bottom: 8 }}>
        <CartesianGrid strokeDasharray="2 6" stroke="rgba(148,163,184,0.12)" vertical={false} />
        <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#94a3b8' }} />
        <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} tickFormatter={(v) => formatCompact(v)} />
        <Tooltip content={<ChartTooltip />} />
        <Line type="monotone" dataKey="value" stroke="#22c55e" strokeWidth={3} dot={{ r: 3, fill: '#22c55e' }} isAnimationActive animationDuration={600} />
      </LineChart>
    </ResponsiveContainer>
  )
}

export default SpendVsRewardChart
