import { motion } from 'framer-motion'

function InsightBadge({ type = 'info', title, description, metric = null, icon = null }) {
  const colorMap = {
    info: 'border-cyan-500/30 bg-cyan-500/10 text-cyan-100 icon-cyan',
    success: 'border-emerald-500/30 bg-emerald-500/10 text-emerald-100 icon-emerald',
    warning: 'border-orange-500/30 bg-orange-500/10 text-orange-100 icon-orange',
    opportunity: 'border-indigo-500/30 bg-indigo-500/10 text-indigo-100 icon-indigo',
  }

  const iconMap = {
    info: '📌',
    success: '✓',
    warning: '⚠',
    opportunity: '💡',
  }

  const colors = colorMap[type] || colorMap.info
  const defaultIcon = iconMap[type] || '•'

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      className={`rounded-lg border ${colors} p-3.5 backdrop-blur-sm`}
    >
      <div className="flex gap-3">
        <div className="flex-shrink-0 text-lg">{icon || defaultIcon}</div>
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-semibold leading-tight">{title}</h4>
          {description && <p className="mt-1 text-xs opacity-90 leading-relaxed">{description}</p>}
          {metric && <p className="mt-2 text-xs font-bold opacity-100">{metric}</p>}
        </div>
      </div>
    </motion.div>
  )
}

export default InsightBadge
