import { useMemo, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'

import { fadeUp, hoverCard, stagger } from '../core/motion'
import { useInsights } from '../hooks/useInsights'
import { useOptimization } from '../hooks/useOptimization'

// Card Components
import InsightCard from '../components/cards/InsightCard'
import KpiCard from '../components/cards/KpiCard'
import OpportunityCard from '../components/cards/OpportunityCard'
import RecommendationCard from '../components/cards/RecommendationCard'

// Chart Components
import ContributionPie from '../components/charts/ContributionPie'
import OptimizationGauge from '../components/charts/OptimizationGauge'
import RewardBarChart from '../components/charts/RewardBarChart'
import SpendVsRewardChart from '../components/charts/SpendVsRewardChart'
import SavingsProjectionChart from '../components/charts/SavingsProjectionChart'

// Input Components
import SpendInputPanel from '../components/inputs/SpendInputPanel'
import PersonaSelector from '../components/inputs/PersonaSelector'

// UI Components
import DashboardLayout from '../components/layout/DashboardLayout'
import Header from '../components/layout/Header'
import Sidebar from '../components/layout/Sidebar'
import { Card, CardContent, CardTitle } from '../components/ui/card'
import ComparisonModal from '../components/modals/ComparisonModal'
import CardDetailDrawer from '../components/ui/CardDetailDrawer'
import InsightBadge from '../components/common/InsightBadge'

// Theme & Pages
import { tokens } from '../theme/tokens'
import CardExplorer from './CardExplorer'
import InsightsPage from './InsightsPage'
import RewardSimulator from './RewardSimulator'
import SettingsPage from './SettingsPage'

const MAX_SPEND_PER_INPUT = 50000

function Dashboard() {
  const [activeMenu, setActiveMenu] = useState('Dashboard')
  const [focusedInput, setFocusedInput] = useState('amazon')
  const [isDarkerMode, setIsDarkerMode] = useState(false)
  const [inputs, setInputs] = useState({ amazon: '', dining: '', travel: '', utilities: '' })

  // New state for premium components
  const [selectedPersona, setSelectedPersona] = useState(null)
  const [comparisonOpen, setComparisonOpen] = useState(false)
  const [selectedCard, setSelectedCard] = useState(null)

  const {
    loading,
    error,
    result,
    animatedReward,
    sanitize,
    toAmount,
    totalSpend,
    hasSpendData,
    filledCategories,
    liveProjectedReward,
    liveBestSuggestion,
    confidencePercent,
    optimizationPotential,
    submitOptimization,
  } = useOptimization(inputs, MAX_SPEND_PER_INPUT)

  const insights = useInsights({
    inputs,
    toAmount,
    totalSpend,
    hasSpendData,
    filledCategories,
    optimizationPotential,
    bestCardSuggestion: result?.best_card || liveBestSuggestion,
    backendInsights: result?.insights || [],
    backendOpportunities: result?.opportunities || [],
  })

  const chartData = useMemo(() => {
    const breakdown = result?.category_breakdown || {}
    return [
      { category: 'online_shopping', reward: breakdown.online_shopping?.estimated_reward || 0 },
      { category: 'dining', reward: breakdown.dining?.estimated_reward || 0 },
      { category: 'travel', reward: breakdown.travel?.estimated_reward || 0 },
      { category: 'utilities', reward: breakdown.utilities?.estimated_reward || 0 },
    ]
  }, [result])

  const pieData = useMemo(() => {
    const total = chartData.reduce((sum, item) => sum + Number(item.reward || 0), 0)
    return chartData.map((item) => ({ name: item.category, value: total > 0 ? Number(((item.reward / total) * 100).toFixed(1)) : 0 }))
  }, [chartData])

  const comparisonData = useMemo(() => {
    const monthly = Number(result?.expected_monthly_reward || result?.expected_reward || liveProjectedReward || 0)
    return [
      { name: 'Current', value: Number((monthly * 0.78).toFixed(2)) },
      { name: 'Optimized', value: Number(monthly.toFixed(2)) },
    ]
  }, [result, liveProjectedReward])

  const annualProjection = useMemo(
    () => Number(result?.expected_yearly_reward || Number(animatedReward || liveProjectedReward || 0) * 12),
    [result, animatedReward, liveProjectedReward],
  )

  const categoryLeaders = useMemo(
    () => [
      { category: 'Online Shopping', card: 'SBI Cashback' },
      { category: 'Dining', card: 'HDFC Millennia' },
      { category: 'Travel', card: 'ICICI Amazon' },
      { category: 'Utilities', card: result?.best_card || liveBestSuggestion },
    ],
    [result, liveBestSuggestion],
  )

  const kpiCards = useMemo(
    () => [
      { title: 'Estimated Monthly Reward', value: Number(animatedReward || liveProjectedReward || 0), subtitle: 'Live from your spend mix' },
      { title: 'Best Card Match Score', value: Number(confidencePercent || 0), suffix: '%', subtitle: 'Model confidence' },
      { title: 'Optimization Potential', value: Number(optimizationPotential || 0), suffix: '%', subtitle: 'Untapped rewards' },
      { title: 'Annual Savings Projection', value: Number(annualProjection || 0), subtitle: 'Projected yearly value' },
    ],
    [animatedReward, liveProjectedReward, confidencePercent, optimizationPotential, annualProjection],
  )

  // Build comparison cards list for modal
  const comparisonCards = useMemo(() => {
    if (!result?.best_card) return []
    return [
      {
        id: 'best',
        bank: 'Recommended',
        name: result.best_card,
        monthly_reward: Number(result?.expected_monthly_reward || 0),
        yearly_reward: Number(result?.expected_yearly_reward || 0),
        annual_fee: 3000,
        efficiency_score: confidencePercent / 100,
        lounge_access: true,
        forex_markup: 2,
        pros: insights.chips.slice(0, 3),
        cons: ['Complex point system'],
      },
      {
        id: 'alternative',
        bank: 'Alternative',
        name: result?.second_best_card || 'HDFC Millennia',
        monthly_reward: Number(result?.expected_monthly_reward || 0) * 0.75,
        yearly_reward: Number(result?.expected_yearly_reward || 0) * 0.75,
        annual_fee: 2500,
        efficiency_score: (confidencePercent - 10) / 100,
        lounge_access: true,
        forex_markup: 1.5,
        pros: ['Good dining rewards', 'Travel benefits'],
        cons: ['Moderate annual fee'],
      },
      {
        id: 'budget',
        bank: 'Budget',
        name: 'SBI Cashback',
        monthly_reward: Number(result?.expected_monthly_reward || 0) * 0.6,
        yearly_reward: Number(result?.expected_yearly_reward || 0) * 0.6,
        annual_fee: 0,
        efficiency_score: (confidencePercent - 25) / 100,
        lounge_access: false,
        forex_markup: 3,
        pros: ['Zero annual fee', 'Easy approval'],
        cons: ['Limited lounge access', 'Higher forex markup'],
      },
    ]
  }, [result, confidencePercent, insights])

  const handlePersonaSelect = (personaMetrics) => {
    setSelectedPersona(personaMetrics)
    setInputs({
      amazon: personaMetrics.online_shopping.toString(),
      dining: personaMetrics.dining.toString(),
      travel: personaMetrics.travel.toString(),
      utilities: personaMetrics.utilities.toString(),
    })
  }

  const handleCardClick = (card) => {
    setSelectedCard(card)
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    await submitOptimization()
  }

  const renderDashboardPage = () => (
    <motion.section
      key="Dashboard"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.2 }}
      className="space-y-6 bg-gradient-to-b from-slate-950 to-slate-900"
    >
      <div className="mx-auto max-w-[1280px] space-y-6 px-6">
        <motion.div {...fadeUp} transition={{ ...fadeUp.transition, delay: 0.05 }}>
          <Header isDarkerMode={isDarkerMode} onToggleTheme={() => setIsDarkerMode((prev) => !prev)} />
        </motion.div>

        <motion.header {...fadeUp} transition={{ ...fadeUp.transition, delay: 0.07 }} className="flex items-center justify-between">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-slate-100 to-slate-300 bg-clip-text text-transparent">AI Credit Card Optimizer</h1>
          <div className="rounded-xl border px-3 py-1 text-xs text-slate-300" style={{ borderColor: tokens.colors.border, background: tokens.colors.card }}>
            {insights.hint}
          </div>
        </motion.header>

        {error ? (
          <motion.div
            initial={{ x: 0 }}
            animate={{ x: [0, -8, 8, -6, 6, 0] }}
            transition={{ duration: 0.45 }}
            className="rounded-xl border border-rose-500/50 bg-rose-950/40 px-3 py-2 text-sm text-rose-200"
          >
            {error}
          </motion.div>
        ) : null}

        {/* KPI Row */}
        <motion.section variants={stagger} initial="initial" animate="animate" className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {kpiCards.map((kpi) => (
            <motion.div key={kpi.title} {...fadeUp} transition={{ ...fadeUp.transition, delay: 0.1 }} whileHover={hoverCard}>
              <KpiCard title={kpi.title} value={kpi.value} suffix={kpi.suffix} prefix={kpi.title.includes('Reward') || kpi.title.includes('Projection') ? '₹ ' : ''} subtitle={kpi.subtitle} />
            </motion.div>
          ))}
        </motion.section>

        {/* Quick Impact Preview */}
        <motion.div
          {...fadeUp}
          transition={{ ...fadeUp.transition, delay: 0.12 }}
          className="rounded-2xl border px-4 py-3 text-sm text-slate-300 border-emerald-500/30 bg-emerald-500/5"
        >
          💰 Switch Card Impact: You could earn <strong>₹{formatMoney(Math.max(0, annualProjection * 0.18))}</strong> more per year.
        </motion.div>

        {/* Persona Quick Select */}
        <motion.div {...fadeUp} transition={{ ...fadeUp.transition, delay: 0.13 }}>
          <PersonaSelector onSelect={handlePersonaSelect} selectedPersona={selectedPersona} />
        </motion.div>

        {/* Spend Input & Recommendation Card */}
        <motion.section {...fadeUp} transition={{ ...fadeUp.transition, delay: 0.15 }} className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          <motion.div whileHover={hoverCard}>
            <SpendInputPanel
              inputs={inputs}
              setInputs={setInputs}
              focusedInput={focusedInput}
              setFocusedInput={setFocusedInput}
              sanitize={sanitize}
              onOptimize={handleSubmit}
              loading={loading}
              error={error}
              hasSpendData={hasSpendData}
              maxSpend={MAX_SPEND_PER_INPUT}
              optimizationPotential={optimizationPotential}
            />
          </motion.div>

          <motion.div whileHover={hoverCard} onClick={() => handleCardClick(result?.best_card)}>
            <RecommendationCard
              result={result}
              animatedReward={animatedReward || liveProjectedReward}
              confidencePercent={confidencePercent}
              aiInsight={insights.aiInsight}
              loading={loading}
              formatMoney={formatMoney}
              bestCardSuggestion={result?.best_card || liveBestSuggestion}
            />
          </motion.div>
        </motion.section>

        {/* Savings Projection Chart */}
        <motion.div {...fadeUp} transition={{ ...fadeUp.transition, delay: 0.17 }}>
          <SavingsProjectionChart
            currentCard="Your Current Card"
            recommendedCard={result?.best_card || liveBestSuggestion}
            monthlyReward={animatedReward || liveProjectedReward}
            yearlyReward={annualProjection}
            formatMoney={formatMoney}
          />
        </motion.div>

        {/* Comparison Button */}
        <motion.div {...fadeUp} transition={{ ...fadeUp.transition, delay: 0.18 }}>
          <button
            onClick={() => setComparisonOpen(true)}
            className="w-full px-6 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-cyan-600 hover:from-indigo-500 hover:to-cyan-500 text-white font-semibold transition-all shadow-lg hover:shadow-indigo-500/30 border border-indigo-400/50"
          >
            📊 Compare 3 Top Cards Side-by-Side
          </button>
        </motion.div>

        {/* Charts Grid */}
        <motion.section {...fadeUp} transition={{ ...fadeUp.transition, delay: 0.2 }} className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          <motion.div whileHover={hoverCard}>
            <ChartCard title="Reward Breakdown">
              <RewardBarChart data={chartData} loading={loading} formatCompact={formatCompact} formatMoney={formatMoney} />
            </ChartCard>
          </motion.div>
          <motion.div whileHover={hoverCard}>
            <ChartCard title="Spend vs Reward">
              <SpendVsRewardChart data={comparisonData} loading={loading} formatCompact={formatCompact} formatMoney={formatMoney} />
            </ChartCard>
          </motion.div>
          <motion.div whileHover={hoverCard}>
            <ChartCard title="Optimization Gauge" footer={`${optimizationPotential.toFixed(0)}%`}>
              <OptimizationGauge value={optimizationPotential} loading={loading} />
            </ChartCard>
          </motion.div>
          <motion.div whileHover={hoverCard}>
            <ChartCard title="Reward Contribution">
              <ContributionPie data={pieData} loading={loading} />
            </ChartCard>
          </motion.div>
        </motion.section>

        {/* Insights Section with InsightBadge */}
        <motion.section {...fadeUp} transition={{ ...fadeUp.transition, delay: 0.25 }}>
          <div className="mb-4">
            <h3 className="text-lg font-semibold text-slate-100">Key Insights</h3>
            <p className="text-sm text-slate-400">AI-powered recommendations based on your spending pattern</p>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Array.from({ length: 2 }).map((_, i) => (
                <div key={i} className="h-24 animate-pulse rounded-xl bg-slate-800/60" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <InsightBadge
                type="success"
                title="Perfect Match Found"
                description={`${result?.best_card || liveBestSuggestion} aligns perfectly with your spending pattern.`}
                metric={`${confidencePercent.toFixed(0)}% match confidence`}
                icon="⭐"
              />
              <InsightBadge
                type="opportunity"
                title="Massive Savings Opportunity"
                description={`Switching cards could save you significant rewards.`}
                metric={`₹${formatMoney(Math.max(0, annualProjection * 0.18))}/year potential gain`}
                icon="💰"
              />
              {insights.chips[0] && (
                <InsightBadge
                  type="info"
                  title="Spend Pattern Detected"
                  description={insights.chips[0]}
                  metric={`${Object.values(inputs).filter((v) => Number(v) > 0).length} categories active`}
                  icon="📊"
                />
              )}
              {filledCategories >= 3 && (
                <InsightBadge
                  type="success"
                  title="High Confidence Prediction"
                  description="Your spend data is comprehensive enough for accurate recommendations."
                  metric={`${filledCategories} of 4 categories filled`}
                  icon="✓"
                />
              )}
            </div>
          )}
        </motion.section>

        {/* Additional Insights Card */}
        <motion.section {...fadeUp} transition={{ ...fadeUp.transition, delay: 0.27 }} className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          {!loading && (
            <>
              <motion.div whileHover={hoverCard}>
                <InsightCard title="Smart Insights">
                  <div className="grid gap-2">
                    {insights.chips.map((chip) => (
                      <InsightPill key={chip} text={chip} />
                    ))}
                  </div>
                  <div className="mt-3 rounded-xl border border-emerald-500/35 bg-emerald-500/10 px-3 py-2 text-sm text-emerald-100">
                    {insights.aiInsight}
                  </div>
                </InsightCard>
              </motion.div>

              <motion.div whileHover={hoverCard}>
                <OpportunityCard />
              </motion.div>
            </>
          )}
        </motion.section>

        {/* Category Leaderboard & Goals */}
        <motion.section {...fadeUp} transition={{ ...fadeUp.transition, delay: 0.29 }} className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          <motion.div whileHover={hoverCard}>
            <Card>
              <CardContent className="p-6">
                <CardTitle className="text-sm font-medium text-slate-300">Category Leaderboard</CardTitle>
                <div className="mt-3 grid gap-2.5">
                  {categoryLeaders.map((row) => (
                    <div key={row.category} className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2 hover:bg-slate-800/30 transition-colors">
                      <span className="text-xs text-slate-500">{row.category}</span>
                      <span className="text-sm font-medium text-slate-200">{row.card}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div whileHover={hoverCard}>
            <Card>
              <CardContent className="p-6">
                <CardTitle className="text-sm font-medium text-slate-300">Monthly Goal</CardTitle>
                <div className="mt-2 text-xs text-slate-500">Target ₹{formatMoney(1200)} | Current ₹{formatMoney(animatedReward || liveProjectedReward)}</div>
                <progress className="mt-3 h-2.5 w-full overflow-hidden rounded-full [&::-webkit-progress-bar]:bg-slate-800 [&::-webkit-progress-value]:bg-gradient-to-r [&::-webkit-progress-value]:from-indigo-500 [&::-webkit-progress-value]:to-cyan-400" value={Math.min(100, ((animatedReward || liveProjectedReward) / 1200) * 100)} max="100" />
                <div className="mt-2 text-sm font-medium text-emerald-400">{Math.min(100, ((animatedReward || liveProjectedReward) / 1200) * 100).toFixed(1)}% achieved</div>
              </CardContent>
            </Card>
          </motion.div>
        </motion.section>
      </div>

      {/* Modals */}
      <ComparisonModal isOpen={comparisonOpen} onClose={() => setComparisonOpen(false)} cards={comparisonCards} selectedCard={0} formatMoney={formatMoney} />
      <CardDetailDrawer isOpen={!!selectedCard} onClose={() => setSelectedCard(null)} card={selectedCard} />
    </motion.section>
  )

  return (
    <DashboardLayout sidebar={<Sidebar activeMenu={activeMenu} setActiveMenu={setActiveMenu} />}>
      <AnimatePresence mode="wait" initial={false}>
        {activeMenu === 'Dashboard' ? renderDashboardPage() : null}
        {activeMenu === 'Card Explorer' ? <PageWrapper key="Card Explorer"><CardExplorer /></PageWrapper> : null}
        {activeMenu === 'Reward Simulator' ? <PageWrapper key="Reward Simulator"><RewardSimulator /></PageWrapper> : null}
        {activeMenu === 'Insights' ? <PageWrapper key="Insights"><InsightsPage /></PageWrapper> : null}
        {activeMenu === 'Settings' ? <PageWrapper key="Settings"><SettingsPage /></PageWrapper> : null}
      </AnimatePresence>
    </DashboardLayout>
  )
}

  const {
    loading,
    error,
    result,
    animatedReward,
    sanitize,
    toAmount,
    totalSpend,
    hasSpendData,
    filledCategories,
    liveProjectedReward,
    liveBestSuggestion,
    confidencePercent,
    optimizationPotential,
    submitOptimization,
  } = useOptimization(inputs, MAX_SPEND_PER_INPUT)

  const insights = useInsights({
    inputs,
    toAmount,
    totalSpend,
    hasSpendData,
    filledCategories,
    optimizationPotential,
    bestCardSuggestion: result?.best_card || liveBestSuggestion,
    backendInsights: result?.insights || [],
    backendOpportunities: result?.opportunities || [],
  })

  const chartData = useMemo(() => {
    const breakdown = result?.category_breakdown || {}
    return [
      { category: 'online_shopping', reward: breakdown.online_shopping?.estimated_reward || 0 },
      { category: 'dining', reward: breakdown.dining?.estimated_reward || 0 },
      { category: 'travel', reward: breakdown.travel?.estimated_reward || 0 },
      { category: 'utilities', reward: breakdown.utilities?.estimated_reward || 0 },
    ]
  }, [result])

  const pieData = useMemo(() => {
    const total = chartData.reduce((sum, item) => sum + Number(item.reward || 0), 0)
    return chartData.map((item) => ({ name: item.category, value: total > 0 ? Number(((item.reward / total) * 100).toFixed(1)) : 0 }))
  }, [chartData])

  const comparisonData = useMemo(() => {
    const monthly = Number(result?.expected_monthly_reward || result?.expected_reward || liveProjectedReward || 0)
    return [
      { name: 'Current', value: Number((monthly * 0.78).toFixed(2)) },
      { name: 'Optimized', value: Number(monthly.toFixed(2)) },
    ]
  }, [result, liveProjectedReward])

  const annualProjection = useMemo(
    () => Number(result?.expected_yearly_reward || Number(animatedReward || liveProjectedReward || 0) * 12),
    [result, animatedReward, liveProjectedReward],
  )

  const categoryLeaders = useMemo(
    () => [
      { category: 'Online Shopping', card: 'SBI Cashback' },
      { category: 'Dining', card: 'HDFC Millennia' },
      { category: 'Travel', card: 'ICICI Amazon' },
      { category: 'Utilities', card: result?.best_card || liveBestSuggestion },
    ],
    [result, liveBestSuggestion],
  )

  const kpiCards = useMemo(
    () => [
      { title: 'Estimated Monthly Reward', value: Number(animatedReward || liveProjectedReward || 0), subtitle: 'Live from your spend mix' },
      { title: 'Best Card Match Score', value: Number(confidencePercent || 0), suffix: '%', subtitle: 'Model confidence' },
      { title: 'Optimization Potential', value: Number(optimizationPotential || 0), suffix: '%', subtitle: 'Untapped rewards' },
      { title: 'Annual Savings Projection', value: Number(annualProjection || 0), subtitle: 'Projected yearly value' },
    ],
    [animatedReward, liveProjectedReward, confidencePercent, optimizationPotential, annualProjection],
  )

  const handleSubmit = async (event) => {
    event.preventDefault()
    await submitOptimization()
  }

  const renderDashboardPage = () => (
    <motion.section
      key="Dashboard"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.2 }}
      className="space-y-6"
    >
      <div className="mx-auto max-w-[1280px] space-y-6 px-6">
        <motion.div {...fadeUp} transition={{ ...fadeUp.transition, delay: 0.05 }}>
          <Header isDarkerMode={isDarkerMode} onToggleTheme={() => setIsDarkerMode((prev) => !prev)} />
        </motion.div>

        <motion.header {...fadeUp} transition={{ ...fadeUp.transition, delay: 0.07 }} className="flex items-center justify-between">
          <h1 className="text-2xl font-semibold text-slate-100">AI Credit Card Optimizer</h1>
          <div className="rounded-xl border px-3 py-1 text-xs text-slate-300" style={{ borderColor: tokens.colors.border, background: tokens.colors.card }}>
            {insights.hint}
          </div>
        </motion.header>

        {error ? (
          <motion.div
            initial={{ x: 0 }}
            animate={{ x: [0, -8, 8, -6, 6, 0] }}
            transition={{ duration: 0.45 }}
            className="rounded-xl border border-rose-500/50 bg-rose-950/40 px-3 py-2 text-sm text-rose-200"
          >
            {error}
          </motion.div>
        ) : null}

        <motion.section variants={stagger} initial="initial" animate="animate" className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {kpiCards.map((kpi) => (
            <motion.div key={kpi.title} {...fadeUp} transition={{ ...fadeUp.transition, delay: 0.1 }} whileHover={hoverCard}>
              <KpiCard title={kpi.title} value={kpi.value} suffix={kpi.suffix} prefix={kpi.title.includes('Reward') || kpi.title.includes('Projection') ? '₹ ' : ''} subtitle={kpi.subtitle} />
            </motion.div>
          ))}
        </motion.section>

        <motion.div
          {...fadeUp}
          transition={{ ...fadeUp.transition, delay: 0.12 }}
          className="rounded-2xl border px-4 py-3 text-sm text-slate-300"
          style={{ borderColor: tokens.colors.border, background: tokens.colors.card }}
        >
          Switch card impact preview: You could earn ₹{formatMoney(Math.max(0, annualProjection * 0.18))} more per year.
        </motion.div>

        <motion.section {...fadeUp} transition={{ ...fadeUp.transition, delay: 0.1 }} className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          <motion.div whileHover={hoverCard}>
            <SpendInputPanel
              inputs={inputs}
              setInputs={setInputs}
              focusedInput={focusedInput}
              setFocusedInput={setFocusedInput}
              sanitize={sanitize}
              onOptimize={handleSubmit}
              loading={loading}
              error={error}
              hasSpendData={hasSpendData}
              maxSpend={MAX_SPEND_PER_INPUT}
              optimizationPotential={optimizationPotential}
            />
          </motion.div>

          <motion.div whileHover={hoverCard}>
            <RecommendationCard
              result={result}
              animatedReward={animatedReward || liveProjectedReward}
              confidencePercent={confidencePercent}
              aiInsight={insights.aiInsight}
              loading={loading}
              formatMoney={formatMoney}
              bestCardSuggestion={result?.best_card || liveBestSuggestion}
            />
          </motion.div>
        </motion.section>

        <motion.section {...fadeUp} transition={{ ...fadeUp.transition, delay: 0.2 }} className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          <motion.div whileHover={hoverCard}>
            <ChartCard title="Reward Breakdown">
              <RewardBarChart data={chartData} loading={loading} formatCompact={formatCompact} formatMoney={formatMoney} />
            </ChartCard>
          </motion.div>
          <motion.div whileHover={hoverCard}>
            <ChartCard title="Spend vs Reward">
              <SpendVsRewardChart data={comparisonData} loading={loading} formatCompact={formatCompact} formatMoney={formatMoney} />
            </ChartCard>
          </motion.div>
          <motion.div whileHover={hoverCard}>
            <ChartCard title="Optimization Gauge" footer={`${optimizationPotential.toFixed(0)}%`}>
              <OptimizationGauge value={optimizationPotential} loading={loading} />
            </ChartCard>
          </motion.div>
          <motion.div whileHover={hoverCard}>
            <ChartCard title="Reward Contribution">
              <ContributionPie data={pieData} loading={loading} />
            </ChartCard>
          </motion.div>
        </motion.section>

        <motion.section {...fadeUp} transition={{ ...fadeUp.transition, delay: 0.25 }} className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          {loading ? (
            Array.from({ length: 2 }).map((_, index) => (
              <div key={`insight-skeleton-${index}`} className="h-[188px] animate-pulse rounded-xl bg-slate-800/60" />
            ))
          ) : (
            <>
              <motion.div whileHover={hoverCard}>
                <InsightCard title="Smart Insights">
                  <div className="grid gap-2">
                    {insights.chips.map((chip) => (
                      <InsightPill key={chip} text={chip} />
                    ))}
                  </div>
                  <div className="mt-3 rounded-xl border border-emerald-500/35 bg-emerald-500/10 px-3 py-2 text-sm text-emerald-100">
                    {insights.aiInsight}
                  </div>
                </InsightCard>
              </motion.div>

              <motion.div whileHover={hoverCard}>
                <OpportunityCard />
              </motion.div>
            </>
          )}
        </motion.section>

        <motion.section {...fadeUp} transition={{ ...fadeUp.transition, delay: 0.27 }} className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          <motion.div whileHover={hoverCard}>
            <Card>
              <CardContent className="p-5">
                <CardTitle className="text-sm font-medium text-slate-300">Category Leaderboard</CardTitle>
                <div className="mt-3 grid gap-2.5">
                  {categoryLeaders.map((row) => (
                    <div key={row.category} className="flex items-center justify-between rounded-xl border border-slate-800 px-3 py-2">
                      <span className="text-xs text-slate-500">{row.category}</span>
                      <span className="text-sm font-medium text-slate-200">{row.card}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div whileHover={hoverCard}>
            <Card>
              <CardContent className="p-5">
                <CardTitle className="text-sm font-medium text-slate-300">Monthly Goal</CardTitle>
                <div className="mt-2 text-xs text-slate-500">Target ₹{formatMoney(1200)} | Current ₹{formatMoney(animatedReward || liveProjectedReward)}</div>
                <progress className="mt-3 h-2.5 w-full overflow-hidden rounded-full [&::-webkit-progress-bar]:bg-slate-800 [&::-webkit-progress-value]:bg-gradient-to-r [&::-webkit-progress-value]:from-indigo-500 [&::-webkit-progress-value]:to-cyan-400" value={Math.min(100, ((animatedReward || liveProjectedReward) / 1200) * 100)} max="100" />
                <div className="mt-2 text-sm font-medium text-emerald-400">{Math.min(100, ((animatedReward || liveProjectedReward) / 1200) * 100).toFixed(1)}% achieved</div>
              </CardContent>
            </Card>
          </motion.div>
        </motion.section>
      </div>
    </motion.section>
  )


function PageWrapper({ children }) {
  return (
    <motion.section initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.2 }}>
      {children}
    </motion.section>
  )
}

function SectionCard({ title, subtitle, children, delay }) {
  return (
    <motion.div {...fadeUp} transition={{ ...fadeUp.transition, delay }}>
      <Card>
        <CardContent className="p-6">
          <h2 className="m-0 text-sm font-medium text-slate-300">{title}</h2>
          <p className="mb-4 mt-1 text-sm text-slate-400">{subtitle}</p>
          {children}
        </CardContent>
      </Card>
    </motion.div>
  )
}

function ChartCard({ title, children, footer }) {
  return (
    <Card className="h-[220px]">
      <CardContent className="flex h-full flex-col p-6">
        <CardTitle className="mb-2 text-sm font-medium text-slate-300">{title}</CardTitle>
        <div className="min-h-0 flex-1">{children}</div>
        {footer ? <div className="mt-2 text-center text-2xl font-semibold text-emerald-400">{footer}</div> : null}
      </CardContent>
    </Card>
  )
}

function InsightPill({ text }) {
  return <div className="rounded-xl border border-indigo-500/30 bg-indigo-500/10 px-3 py-2 text-xs text-indigo-200">{text}</div>
}

function formatMoney(value) {
  return new Intl.NumberFormat('en-IN', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(value)
}

function formatCompact(value) {
  return new Intl.NumberFormat('en-IN', {
    notation: 'compact',
    maximumFractionDigits: 1,
  }).format(Number(value || 0))
}

export default Dashboard
