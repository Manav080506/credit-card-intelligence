import { Button } from '../ui/button'
import { Card, CardContent } from '../ui/card'

function DashboardIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <rect x="3" y="3" width="8" height="8" rx="2" stroke="currentColor" strokeWidth="2" />
      <rect x="13" y="3" width="8" height="5" rx="2" stroke="currentColor" strokeWidth="2" />
      <rect x="13" y="10" width="8" height="11" rx="2" stroke="currentColor" strokeWidth="2" />
      <rect x="3" y="13" width="8" height="8" rx="2" stroke="currentColor" strokeWidth="2" />
    </svg>
  )
}

function CardIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <rect x="2" y="5" width="20" height="14" rx="3" stroke="currentColor" strokeWidth="2" />
      <path d="M2 10h20" stroke="currentColor" strokeWidth="2" />
    </svg>
  )
}

function SparkIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M13 2L4 14h7l-1 8 10-13h-7l0-7z" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" />
    </svg>
  )
}

function InsightIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M4 18V6m8 12V10m8 8V4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
    </svg>
  )
}

function GearIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M12 15a3 3 0 100-6 3 3 0 000 6z" stroke="currentColor" strokeWidth="2" />
      <path d="M19.4 15a1.7 1.7 0 00.34 1.87l.06.06a2 2 0 11-2.83 2.83l-.06-.06A1.7 1.7 0 0015 19.4a1.7 1.7 0 00-1 .6 1.7 1.7 0 00-.4 1.1V22a2 2 0 11-4 0v-.1a1.7 1.7 0 00-.4-1.1 1.7 1.7 0 00-1-.6 1.7 1.7 0 00-1.87.34l-.06.06a2 2 0 11-2.83-2.83l.06-.06A1.7 1.7 0 004.6 15a1.7 1.7 0 00-.6-1 1.7 1.7 0 00-1.1-.4H2a2 2 0 110-4h.1a1.7 1.7 0 001.1-.4 1.7 1.7 0 00.6-1 1.7 1.7 0 00-.34-1.87l-.06-.06a2 2 0 112.83-2.83l.06.06A1.7 1.7 0 009 4.6a1.7 1.7 0 001-.6 1.7 1.7 0 00.4-1.1V2a2 2 0 114 0v.1a1.7 1.7 0 00.4 1.1 1.7 1.7 0 001 .6 1.7 1.7 0 001.87-.34l.06-.06a2 2 0 112.83 2.83l-.06.06A1.7 1.7 0 0019.4 9c.26.32.44.7.5 1.1H22a2 2 0 110 4h-.1a1.7 1.7 0 00-1.1.4 1.7 1.7 0 00-.6 1z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

function Sidebar({ activeMenu, setActiveMenu }) {
  const menuItems = [
    { label: 'Dashboard', icon: DashboardIcon },
    { label: 'Card Explorer', icon: CardIcon },
    { label: 'Reward Simulator', icon: SparkIcon },
    { label: 'Insights', icon: InsightIcon },
    { label: 'Settings', icon: GearIcon },
  ]

  return (
    <Card className="w-full border-slate-800 bg-slate-900/60 backdrop-blur">
      <CardContent className="p-5">
        <div className="mb-4 border-b border-slate-800 pb-3">
          <div className="text-lg font-semibold text-slate-100">AI Card Intelligence</div>
        </div>

        <nav className="grid gap-2">
        {menuItems.map((item) => {
          const Icon = item.icon
          const active = activeMenu === item.label
          return (
            <Button
              key={item.label}
              type="button"
              onClick={() => setActiveMenu(item.label)}
              variant={active ? 'secondary' : 'ghost'}
              className={`menu-item h-10 justify-start gap-2.5 rounded-xl border px-3 text-left ${
                active
                  ? 'border-indigo-400/45 bg-indigo-500/20 text-slate-100 hover:bg-indigo-500/25'
                  : 'border-slate-700/60 bg-slate-950/40 text-slate-400 hover:border-indigo-400/35 hover:bg-slate-800/70 hover:text-slate-100'
              }`}
            >
              <Icon />
              <span className="font-medium">{item.label}</span>
            </Button>
          )
        })}
        </nav>
      </CardContent>
    </Card>
  )
}

export default Sidebar
