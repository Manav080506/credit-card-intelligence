import { Card, CardContent, CardTitle } from '../components/ui/card'

function InsightItem({ title, value, tone }) {
  const toneClass =
    tone === 'positive' ? 'text-emerald-400' : tone === 'warning' ? 'text-amber-400' : 'text-indigo-300'

  return (
    <Card>
      <CardContent className="p-5">
        <CardTitle className="text-sm font-medium text-slate-300">{title}</CardTitle>
        <p className={`mt-2 text-sm ${toneClass}`}>{value}</p>
      </CardContent>
    </Card>
  )
}

function InsightsPage() {
  return (
    <section className="space-y-6">
      <Card>
        <CardContent className="p-5">
          <CardTitle className="text-sm font-medium text-slate-300">Insights</CardTitle>
          <p className="mt-1 text-sm text-slate-400">Personalized actions to optimize your rewards profile.</p>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <InsightItem title="Top Saving Opportunity" value="Shift utility spend to SBI Cashback to gain ~₹220/year." tone="positive" />
        <InsightItem title="Best Card Switch Suggestion" value="Move dining transactions to HDFC Millennia for better multiplier value." tone="neutral" />
        <InsightItem title="Spend Imbalance Warning" value="Utilities contribute 38% of spend but only 16% of rewards." tone="warning" />
      </div>
    </section>
  )
}

export default InsightsPage
