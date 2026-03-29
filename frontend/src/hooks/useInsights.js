import { useMemo } from 'react'

export function useInsights({
  inputs,
  toAmount,
  totalSpend,
  hasSpendData,
  filledCategories,
  optimizationPotential,
  bestCardSuggestion,
  backendInsights = [],
  backendOpportunities = [],
}) {
  return useMemo(() => {
    const utilities = toAmount(inputs.utilities)
    const denominator = Math.max(1, totalSpend)
    const utilityShare = Math.round((utilities / denominator) * 100)

    const aiInsight = `You spend ${utilityShare}% on utilities. Consider ${bestCardSuggestion} for higher ROI.`

    let hint = 'Live optimization is active as you type. Tune spend to maximize yearly rewards.'
    if (!hasSpendData) {
      hint = 'Enter your monthly spend to unlock AI insights.'
    } else if (filledCategories === 1) {
      hint = 'Add more categories for better optimization accuracy.'
    } else if (optimizationPotential > 80) {
      hint = 'Optimized setup detected. Your current mix is highly efficient.'
    }

    const state = !hasSpendData ? 'empty' : filledCategories === 1 ? 'partial' : 'full'

    const fallbackChips = [
      'high utility spend',
      'travel heavy profile',
      'balanced spending',
    ]

    const chips = [...backendInsights, ...backendOpportunities].filter(Boolean)

    return {
      state,
      hint,
      aiInsight,
      chips: chips.length > 0 ? chips : fallbackChips,
    }
  }, [
    inputs,
    toAmount,
    totalSpend,
    hasSpendData,
    filledCategories,
    optimizationPotential,
    bestCardSuggestion,
    backendInsights,
    backendOpportunities,
  ])
}
