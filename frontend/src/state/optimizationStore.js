export const initialOptimizationState = {
  loading: false,
  error: '',
  result: null,
  transactions: [],
}

export function createOptimizationSnapshot(state) {
  return {
    ...initialOptimizationState,
    ...state,
    updatedAt: Date.now(),
  }
}
