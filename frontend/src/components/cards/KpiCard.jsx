import { Card, CardContent, CardTitle } from '../ui/card'

function MetricIcon({ title }) {
  if (title.includes('Reward')) {
    return <span className="grid h-7 w-7 place-items-center rounded-lg bg-emerald-500/20 text-emerald-300">Rs</span>
  }
  if (title.includes('Confidence')) {
    return <span className="grid h-7 w-7 place-items-center rounded-lg bg-indigo-500/20 text-indigo-300">%</span>
  }
  if (title.includes('Optimization')) {
    return <span className="grid h-7 w-7 place-items-center rounded-lg bg-cyan-500/20 text-cyan-300">Up</span>
  }
  return <span className="grid h-7 w-7 place-items-center rounded-lg bg-amber-500/20 text-amber-300">Yr</span>
}

function metricColorClass(title) {
  if (title.includes('Confidence')) {
    return 'text-indigo-300'
  }
  if (title.includes('Optimization')) {
    return 'text-cyan-300'
  }
  return 'text-emerald-400'
}

function KpiCard({ title, value, subtitle }) {
  return (
    <Card className="h-[110px] border-slate-800 bg-slate-900/60">
      <CardContent className="flex h-full flex-col justify-center p-5">
        <div className="mb-1.5 flex items-center justify-between">
          <CardTitle className="text-sm font-medium text-slate-300">{title}</CardTitle>
          <MetricIcon title={title} />
        </div>
        <div className={`text-2xl font-semibold leading-none ${metricColorClass(title)}`}>
          {value}
        </div>
        <div className="mt-1 text-xs text-slate-500">{subtitle}</div>
      </CardContent>
    </Card>
  )
}

export default KpiCard
