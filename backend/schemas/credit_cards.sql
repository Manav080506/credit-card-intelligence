CREATE TABLE credit_cards (
  id TEXT PRIMARY KEY,
  name TEXT,
  display_name TEXT,
  issuer TEXT,
  annual_fee INT,
  reward_type TEXT,
  reward_online FLOAT,
  reward_dining FLOAT,
  reward_travel FLOAT,
  reward_utilities FLOAT,
  lounge_access BOOLEAN,
  forex_markup FLOAT,
  rating FLOAT
);

CREATE TABLE optimization_logs (
  id SERIAL PRIMARY KEY,
  online_spend FLOAT,
  dining_spend FLOAT,
  travel_spend FLOAT,
  utilities_spend FLOAT,
  recommended_card TEXT,
  monthly_reward FLOAT,
  created_at TIMESTAMP DEFAULT now()
);
