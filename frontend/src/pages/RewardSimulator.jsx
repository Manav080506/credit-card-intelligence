import { useMemo, useState } from 'react'

import { Card, CardContent, CardTitle } from '../components/ui/card'

function SliderRow({ label, value, onChange }) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-slate-300">{label}</span>
        <span className="text-xs text-slate-500">₹ {value.toLocaleString('en-IN')}</span>
      </div>
      <input
        type="range"
        min="0"
        max="50000"
        step="500"
        value={value}
        onChange={(event) => onChange(Number(event.target.value))}
        className="h-2 w-full cursor-pointer appearance-none rounded-lg bg-slate-800 accent-indigo-500"
      />
    </div>
  )
}

function RewardSimulator() {
  const [shopping, setShopping] = useState(12000)
  const [dining, setDining] = useState(4500)
  const [travel, setTravel] = useState(7000)
  const [utilities, setUtilities] = useState(3500)

  const total = shopping + dining + travel + utilities

  const projectedReward = useMemo(() => {
    return shopping * 0.05 + dining * 0.04 + travel * 0.035 + utilities * 0.02
  }, [shopping, dining, travel, utilities])

  return (
    <section className="space-y-6">
      <Card>
        <CardContent className="space-y-5 p-5">
          <div>
            <CardTitle className="text-sm font-medium text-slate-300">Reward Simulator</CardTitle>
            <p className="mt-1 text-sm text-slate-400">Adjust monthly spend sliders to simulate projected rewards.</p>
          </div>

          <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
            <SliderRow label="Shopping" value={shopping} onChange={setShopping} />
            <SliderRow label="Dining" value={dining} onChange={setDining} />
            <SliderRow label="Travel" value={travel} onChange={setTravel} />
            <SliderRow label="Utilities" value={utilities} onChange={setUtilities} />
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-5">
            <div className="text-xs text-slate-500">Total Monthly Spend</div>
            <div className="mt-1 text-2xl font-semibold text-slate-100">₹ {total.toLocaleString('en-IN')}</div>
            <div className="mt-4 text-xs text-slate-500">Projected Monthly Reward</div>
            <div className="mt-1 text-2xl font-semibold text-emerald-400">₹ {projectedReward.toFixed(2)}</div>
          </div>
        </CardContent>
      </Card>
    </section>
  )
}

export default RewardSimulator
