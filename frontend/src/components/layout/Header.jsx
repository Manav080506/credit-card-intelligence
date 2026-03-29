import { Button } from '../ui/button'
import { Card, CardContent } from '../ui/card'

function Header({ isDarkerMode, onToggleTheme }) {
  return (
    <Card className="border-slate-800 bg-gradient-to-br from-slate-900/70 via-slate-900/60 to-slate-900/60">
      <CardContent className="flex flex-col items-start justify-between gap-3 p-5 md:flex-row md:items-center">
        <div>
          <h1 className="m-0 text-2xl font-semibold tracking-tight text-slate-50">AI Credit Card Optimizer</h1>
          <p className="mt-1 text-sm text-slate-400">
            SaaS reward intelligence dashboard with live optimization.
          </p>
        </div>
        <Button
          type="button"
          onClick={onToggleTheme}
          variant="outline"
          className="h-10 border-white/10 bg-slate-900/70 text-slate-300 hover:bg-slate-800/70 hover:text-slate-100"
        >
          {isDarkerMode ? 'Theme: Darker' : 'Theme: Dark'}
        </Button>
      </CardContent>
    </Card>
  )
}

export default Header
