import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts'

const COLORS = ['#22c55e', '#6366f1', '#14b8a6', '#f59e0b']

function ChartTooltip({ active, payload }) {
  if (!active || !payload?.length) {
    return null
  }

  return (
    <div className="rounded-lg border border-slate-700 bg-slate-950 px-2.5 py-1.5 text-xs text-slate-100 shadow-[0_2px_12px_rgba(0,0,0,0.25)]">
      <div className="font-medium">{payload[0].name}</div>
      <div className="text-cyan-300">{Number(payload[0].value || 0).toFixed(1)}%</div>
    </div>
  )
}

function ContributionPie({ data, loading }) {
  if (loading) {
    return <div className="h-full w-full animate-pulse rounded-xl bg-slate-800/80" />
  }

  return (
    <div className="flex h-full flex-col">
      <div className="min-h-0 flex-1">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="48%" outerRadius={62} innerRadius={36} isAnimationActive animationDuration={600}>
              {data.map((entry, index) => (
                <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip content={<ChartTooltip />} />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-2 grid grid-cols-2 gap-x-3 gap-y-1 text-xs text-slate-400">
        {data.map((item, index) => (
          <div key={item.name} className="flex items-center gap-1.5">
            <span
              className={`h-2.5 w-2.5 rounded-full ${
                index === 0
                  ? 'bg-emerald-500'
                  : index === 1
                    ? 'bg-indigo-500'
                    : index === 2
                      ? 'bg-teal-500'
                      : 'bg-amber-500'
              }`}
            />
            <span className="truncate">{item.name}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ContributionPie
