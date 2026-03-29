import { useState } from 'react'

import { Card, CardContent, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'

function ToggleRow({ label, value, onToggle }) {
  return (
    <div className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950/60 px-4 py-3">
      <span className="text-sm text-slate-300">{label}</span>
      <Button type="button" variant={value ? 'secondary' : 'outline'} className="h-8 px-3" onClick={onToggle}>
        {value ? 'On' : 'Off'}
      </Button>
    </div>
  )
}

function SettingsPage() {
  const [darkTheme, setDarkTheme] = useState(true)
  const [currency, setCurrency] = useState('INR')
  const [notifications, setNotifications] = useState(true)

  return (
    <section className="space-y-6">
      <Card>
        <CardContent className="space-y-4 p-5">
          <div>
            <CardTitle className="text-sm font-medium text-slate-300">Settings</CardTitle>
            <p className="mt-1 text-sm text-slate-400">Control your dashboard preferences.</p>
          </div>

          <ToggleRow label="Theme Toggle" value={darkTheme} onToggle={() => setDarkTheme((prev) => !prev)} />

          <div className="rounded-xl border border-slate-800 bg-slate-950/60 px-4 py-3">
            <div className="mb-2 text-sm text-slate-300">Currency Selector</div>
            <select
              value={currency}
              onChange={(event) => setCurrency(event.target.value)}
              className="h-10 w-full rounded-lg border border-slate-700 bg-slate-900 px-3 text-sm text-slate-100 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
            >
              <option value="INR">INR</option>
              <option value="USD">USD</option>
              <option value="EUR">EUR</option>
            </select>
          </div>

          <ToggleRow
            label="Notification Toggle"
            value={notifications}
            onToggle={() => setNotifications((prev) => !prev)}
          />
        </CardContent>
      </Card>
    </section>
  )
}

export default SettingsPage
