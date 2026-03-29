import { optimizeSpendApi, predictCard } from '../../api/cardApi'

function transformLegacyResponse(response, categoryPayload) {
  const expectedMonthlyReward = Number(response?.expected_reward || 0)
  const totalSpend = Object.values(categoryPayload).reduce((sum, value) => sum + Number(value || 0), 0)
  const baseline = totalSpend * 0.01
  const optimization = expectedMonthlyReward > 0 ? Math.max(0, Math.min(1, (expectedMonthlyReward - baseline) / expectedMonthlyReward)) : 0

  return {
    best_card: response?.best_card || 'SBI Cashback Card',
    expected_monthly_reward: expectedMonthlyReward,
    expected_yearly_reward: expectedMonthlyReward * 12,
    second_best_card: '',
    confidence_score: Number(response?.confidence || 0),
    optimization_score: optimization,
    insights: [],
    opportunities: [],
    category_breakdown: response?.category_breakdown || {},
  }
}

export async function optimizeSpend(categoryPayload, fallbackTransactions = []) {
  try {
    return await optimizeSpendApi(categoryPayload)
  } catch (error) {
    const status = error?.response?.status
    if (status && status !== 404 && status !== 405) {
      throw error
    }

    const legacyResponse = await predictCard(fallbackTransactions)
    return transformLegacyResponse(legacyResponse, categoryPayload)
  }
}
