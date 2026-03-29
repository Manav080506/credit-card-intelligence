-- Production cards schema with reward rules and audit trail

CREATE TABLE cards (
  id TEXT PRIMARY KEY,
  bank TEXT NOT NULL,
  network TEXT,
  segment TEXT,
  annual_fee INT DEFAULT 0,
  joining_fee INT DEFAULT 0,
  forex_markup FLOAT DEFAULT 0,
  reward_currency TEXT DEFAULT 'INR',
  reward_conversion_value FLOAT DEFAULT 1.0,
  lounge_domestic INT DEFAULT 0,
  lounge_international INT DEFAULT 0,
  min_income INT DEFAULT 0,
  credit_score INT DEFAULT 0,
  tags TEXT[],
  last_updated TIMESTAMP DEFAULT now()
);

-- Reward rules per card and category
CREATE TABLE reward_rules (
  id SERIAL PRIMARY KEY,
  card_id TEXT REFERENCES cards(id) ON DELETE CASCADE,
  category TEXT NOT NULL,
  reward_rate FLOAT NOT NULL,
  cap FLOAT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT now()
);

-- Card update audit trail
CREATE TABLE card_updates (
  id SERIAL PRIMARY KEY,
  card_id TEXT REFERENCES cards(id) ON DELETE CASCADE,
  change_type TEXT NOT NULL,
  old_value TEXT,
  new_value TEXT,
  detected_at TIMESTAMP DEFAULT now()
);

-- Indexes for performance
CREATE INDEX idx_cards_bank ON cards(bank);
CREATE INDEX idx_cards_segment ON cards(segment);
CREATE INDEX idx_reward_rules_card_id ON reward_rules(card_id);
CREATE INDEX idx_card_updates_card_id ON card_updates(card_id);
CREATE INDEX idx_card_updates_detected_at ON card_updates(detected_at);
