import { Card, CardContent, CardTitle } from '../ui/card'

function Opportunity({ text }) {
  return (
    <div className="rounded-xl border border-emerald-500/25 bg-emerald-500/10 px-3 py-2 text-sm text-emerald-100">{text}</div>
  )
}

function OpportunityCard() {
  return (
    <Card className="bg-slate-900/60">
      <CardContent className="p-5">
        <CardTitle className="text-sm font-medium text-slate-300">Optimization Opportunities</CardTitle>
        <div className="mt-2.5 grid gap-2.5">
          <Opportunity text="Shift travel to Axis Atlas for +₹150/year" />
          <Opportunity text="Use SBI Cashback for utility bills for +₹220/year" />
          <Opportunity text="Consolidate online spends on HDFC Millennia for +₹310/year" />
        </div>
        <div className="mt-2 text-xs text-slate-500">Based on observed spend and current market cards</div>
      </CardContent>
    </Card>
  )
}

export default OpportunityCard
