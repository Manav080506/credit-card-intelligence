import { Button } from '../ui/button'
import { Card, CardContent, CardTitle } from '../ui/card'
import InputField from './InputField'

function SpendInputPanel({
  inputs,
  setInputs,
  focusedInput,
  setFocusedInput,
  sanitize,
  onOptimize,
  loading,
  error,
  hasSpendData,
  maxSpend,
  optimizationPotential = 0,
  className = '',
}) {
  const activeSegments = Math.round((Math.min(100, Math.max(0, optimizationPotential)) / 100) * 20)

  return (
    <Card className={`border-slate-800 bg-slate-900/60 ${className}`.trim()}>
      <CardContent className="p-5">
        <CardTitle className="text-sm font-medium text-slate-300">Spend Input Panel</CardTitle>
        <p className="mb-3 mt-1 text-sm text-slate-400">
          Enter your monthly spend values (₹) and run optimization.
        </p>

        <form onSubmit={onOptimize}>
          <div className="input-grid grid grid-cols-2 gap-3">
            <InputField
              name="amazon"
              label="Amazon"
              value={inputs.amazon}
              onChange={(value) => setInputs((prev) => ({ ...prev, amazon: String(sanitize(value)) }))}
              focusedInput={focusedInput}
              setFocusedInput={setFocusedInput}
              maxSpend={maxSpend}
            />
            <InputField
              name="dining"
              label="Dining"
              value={inputs.dining}
              onChange={(value) => setInputs((prev) => ({ ...prev, dining: String(sanitize(value)) }))}
              focusedInput={focusedInput}
              setFocusedInput={setFocusedInput}
              maxSpend={maxSpend}
            />
            <InputField
              name="travel"
              label="Travel"
              value={inputs.travel}
              onChange={(value) => setInputs((prev) => ({ ...prev, travel: String(sanitize(value)) }))}
              focusedInput={focusedInput}
              setFocusedInput={setFocusedInput}
              maxSpend={maxSpend}
            />
            <InputField
              name="utilities"
              label="Utilities"
              value={inputs.utilities}
              onChange={(value) => setInputs((prev) => ({ ...prev, utilities: String(sanitize(value)) }))}
              focusedInput={focusedInput}
              setFocusedInput={setFocusedInput}
              maxSpend={maxSpend}
            />
          </div>

          <Button
            type="submit"
            disabled={loading || !hasSpendData}
            className="mt-4 h-11 w-full rounded-xl bg-gradient-to-r from-indigo-500 to-cyan-400 text-sm font-semibold text-white"
          >
            {loading ? 'Optimizing...' : hasSpendData ? 'Optimize' : 'Enter spend to optimize'}
          </Button>
        </form>

        {!hasSpendData && <div className="mt-2 text-xs text-amber-300">Add at least one spend value above ₹0 to enable optimization.</div>}

        {loading && (
          <div className="mt-2 flex items-center gap-2 text-sm text-slate-300">
            <span className="h-4 w-4 animate-spin rounded-full border-2 border-slate-500 border-t-emerald-400" />
            <span>Calling AI optimizer...</span>
          </div>
        )}

        {error && (
          <div className="mt-2 rounded-xl border border-rose-400/50 bg-rose-950/40 px-3 py-2 text-sm text-rose-200">
            {error}
          </div>
        )}

        <div className="mt-3 rounded-xl border border-slate-800 bg-slate-950/60 p-3">
          <div className="mb-1 flex items-center justify-between">
            <span className="text-xs text-slate-500">Live optimization score</span>
            <span className="text-sm font-medium text-emerald-400">{optimizationPotential.toFixed(0)}%</span>
          </div>
          <div className="grid grid-cols-[repeat(20,minmax(0,1fr))] gap-0.5">
            {Array.from({ length: 20 }).map((_, index) => (
              <span
                key={`segment-${index}`}
                className={`h-2 rounded-full transition-colors duration-300 ${index < activeSegments ? 'bg-gradient-to-r from-indigo-500 to-cyan-400' : 'bg-slate-800'}`}
              />
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

export default SpendInputPanel
