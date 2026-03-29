import { Input } from '../ui/input'

function InputField({ name, label, value, onChange, focusedInput, setFocusedInput, maxSpend }) {
  const isFocused = focusedInput === name

  return (
    <label className="grid gap-1.5 text-left">
      <span className="text-sm font-medium text-slate-400">{label}</span>
      <div className="relative">
        <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-sm text-slate-500">₹</span>
        <Input
          type="number"
          min="0"
          max={maxSpend}
          step="1"
          value={value}
          placeholder="0"
          onChange={(event) => onChange(event.target.value)}
          onFocus={() => setFocusedInput(name)}
          onBlur={() => setFocusedInput('')}
          className={`pl-8 ${isFocused ? 'border-indigo-500 ring-2 ring-indigo-500/40' : ''}`}
        />
      </div>
    </label>
  )
}

export default InputField
