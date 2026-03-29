import { PolarAngleAxis, RadialBar, RadialBarChart, ResponsiveContainer, Tooltip } from 'recharts'

function OptimizationGauge({ value, loading }) {
  if (loading) {
    return <div className="h-full w-full animate-pulse rounded-xl bg-slate-800/80" />
  }

  const score = Math.max(0, Math.min(100, value))
  const data = [{ name: 'potential', value: score, fill: '#22c55e' }]

  return (
    <div className="relative h-full w-full">
      <ResponsiveContainer width="100%" height="100%">
        <RadialBarChart data={data} startAngle={180} endAngle={0} innerRadius="60%" outerRadius="95%" barSize={14}>
          <PolarAngleAxis type="number" domain={[0, 100]} tick={false} />
          <RadialBar background dataKey="value" cornerRadius={10} isAnimationActive animationDuration={600} />
          <Tooltip formatter={(v) => [`${Number(v).toFixed(0)}%`, 'Potential']} />
        </RadialBarChart>
      </ResponsiveContainer>
      <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
        <div className="text-2xl font-semibold text-emerald-400">{score.toFixed(0)}%</div>
      </div>
    </div>
  )
}

export default OptimizationGauge
