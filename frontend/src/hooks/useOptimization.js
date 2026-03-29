import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import { optimizeSpend } from '../core/api/optimizeSpend'
import { useDebounce } from './useDebounce'

export function useOptimization(inputs, maxSpend = 50000) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)
  const [animatedReward, setAnimatedReward] = useState(0)
  const lastOptimizedSignature = useRef('')

  const toAmount = useCallback(
    (value) => {
      const parsed = Number(value)
      if (!Number.isFinite(parsed) || parsed < 0) {
        return 0
      }
      return Math.min(maxSpend, parsed)
    },
    [maxSpend],
  )

  const sanitize = useCallback((value) => Math.min(maxSpend, Math.max(0, Number(value) || 0)), [maxSpend])

  const transactions = useMemo(
    () => [
      { merchant: 'Amazon', amount: toAmount(inputs.amazon) },
      { merchant: 'Swiggy', amount: toAmount(inputs.dining) },
      { merchant: 'Uber', amount: toAmount(inputs.travel) },
      { merchant: 'Electricity', amount: toAmount(inputs.utilities) },
    ],
    [inputs, toAmount],
  )

  const categoryPayload = useMemo(
    () => ({
      online_shopping: toAmount(inputs.amazon),
      dining: toAmount(inputs.dining),
      travel: toAmount(inputs.travel),
      utilities: toAmount(inputs.utilities),
    }),
    [inputs, toAmount],
  )

  const signature = useMemo(() => transactions.map((item) => item.amount).join('|'), [transactions])
  const debouncedSignature = useDebounce(signature, 500)

  const totalSpend = useMemo(
    () => transactions.reduce((sum, item) => sum + item.amount, 0),
    [transactions],
  )
  const hasSpendData = totalSpend > 0
  const filledCategories = useMemo(() => transactions.filter((item) => item.amount > 0).length, [transactions])

  const liveProjectedReward = useMemo(
    () =>
      transactions[0].amount * 0.05 +
      transactions[1].amount * 0.04 +
      transactions[2].amount * 0.035 +
      transactions[3].amount * 0.02,
    [transactions],
  )

  const liveBestSuggestion = useMemo(() => {
    const top = [...transactions].sort((a, b) => b.amount - a.amount)[0]
    if (!top || top.amount <= 0) {
      return 'SBI Cashback'
    }
    if (top.merchant === 'Swiggy') {
      return 'HDFC Millennia'
    }
    if (top.merchant === 'Uber') {
      return 'Axis Atlas'
    }
    return 'SBI Cashback'
  }, [transactions])

  const confidencePercent = useMemo(() => {
    if (result?.confidence_score != null) {
      return Math.max(0, Math.min(100, Number(result.confidence_score) * 100))
    }
    if (result?.confidence != null) {
      return Math.max(0, Math.min(100, Number(result.confidence) * 100))
    }
    return Math.min(95, filledCategories * 24)
  }, [result, filledCategories])

  const optimizationPotential = useMemo(() => {
    if (result?.optimization_score != null) {
      return Math.max(0, Math.min(100, Number(result.optimization_score) * 100))
    }
    if ((!result?.expected_reward && !liveProjectedReward) || totalSpend <= 0) {
      return 0
    }
    const baseline = totalSpend * 0.01
    const gain = Math.max(0, (result?.expected_reward || liveProjectedReward) - baseline)
    return Math.min(100, (gain / Math.max(1, baseline)) * 100)
  }, [result, totalSpend, liveProjectedReward])

  const optimizeTransactions = useCallback(async (payload) => {
    const payloadSignature = payload.map((item) => item.amount).join('|')
    if (!payloadSignature || payloadSignature === '0|0|0|0') {
      setResult(null)
      setLoading(false)
      setError('')
      return
    }

    setLoading(true)
    setError('')

    try {
      const response = await optimizeSpend(categoryPayload, payload)
      setResult(response)
      lastOptimizedSignature.current = payloadSignature
    } catch (requestError) {
      const message = requestError?.response?.data?.detail || requestError?.message || 'Unable to fetch recommendation. Please try again.'
      setError(String(message))
    } finally {
      setLoading(false)
    }
  }, [categoryPayload])

  const submitOptimization = useCallback(async () => {
    await optimizeTransactions(transactions)
  }, [optimizeTransactions, transactions])

  useEffect(() => {
    if (!hasSpendData) {
      setResult(null)
      setError('')
      setLoading(false)
      return
    }

    if (debouncedSignature === lastOptimizedSignature.current) {
      return
    }

    optimizeTransactions(transactions)
  }, [debouncedSignature, hasSpendData, optimizeTransactions, transactions])

  useEffect(() => {
    const target = Number(result?.expected_monthly_reward || result?.expected_reward || 0)
    if (target <= 0) {
      setAnimatedReward(0)
      return
    }

    const duration = 600
    const startTime = performance.now()
    const startValue = 0

    const animate = (timestamp) => {
      const elapsed = timestamp - startTime
      const progress = Math.min(1, elapsed / duration)
      const eased = 1 - Math.pow(1 - progress, 3)
      setAnimatedReward(startValue + (target - startValue) * eased)

      if (progress < 1) {
        requestAnimationFrame(animate)
      }
    }

    requestAnimationFrame(animate)
  }, [result])

  return {
    loading,
    error,
    result,
    animatedReward,
    sanitize,
    toAmount,
    transactions,
    totalSpend,
    hasSpendData,
    filledCategories,
    liveProjectedReward,
    liveBestSuggestion,
    confidencePercent,
    optimizationPotential,
    categoryPayload,
    submitOptimization,
    setResult,
    setError,
    setLoading,
  }
}
