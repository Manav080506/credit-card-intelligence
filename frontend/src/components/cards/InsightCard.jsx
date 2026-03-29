import { Card, CardContent, CardTitle } from '../ui/card'

function InsightCard({ title, children }) {
  return (
    <Card className="bg-slate-900/60">
      <CardContent className="p-5">
        <CardTitle className="text-sm font-medium text-slate-300">{title}</CardTitle>
        <div className="mt-2">{children}</div>
        <div className="mt-2 text-xs text-slate-500">Realtime AI-driven spend intelligence</div>
      </CardContent>
    </Card>
  )
}

export default InsightCard
