import axios from 'axios'

const API_BASE = 'http://127.0.0.1:8001'

export async function predictCard(transactions) {
  const response = await axios.post(`${API_BASE}/predict-card`, {
    transactions,
  })
  return response.data
}

export async function optimizeSpendApi(spendPayload) {
  const response = await axios.post(`${API_BASE}/optimize-spend`, spendPayload)
  return response.data
}
