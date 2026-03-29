const CARD_CATALOG = [
  { name: 'SBI Cashback', rewardType: 'Cashback', annualFee: '₹999', bestCategory: 'Online Shopping', rating: 4.8 },
  { name: 'HDFC Millennia', rewardType: 'Cashback', annualFee: '₹1,000', bestCategory: 'Dining', rating: 4.6 },
  { name: 'ICICI Amazon Pay', rewardType: 'Co-branded', annualFee: '₹0', bestCategory: 'E-commerce', rating: 4.7 },
  { name: 'Axis Atlas', rewardType: 'Travel', annualFee: '₹5,000', bestCategory: 'Travel', rating: 4.5 },
  { name: 'Amex MRCC', rewardType: 'Reward Points', annualFee: '₹4,500', bestCategory: 'Rewards', rating: 4.4 },
]

export function getCardsCatalog() {
  return CARD_CATALOG
}

export async function getCardsCatalogAsync() {
  return CARD_CATALOG
}
