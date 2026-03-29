-- Production PostgreSQL Schema for Credit Card Intelligence

-- Main credit cards table
CREATE TABLE IF NOT EXISTS credit_cards (
    id TEXT PRIMARY KEY,
    card_name TEXT NOT NULL,
    bank TEXT NOT NULL,
    network TEXT,
    annual_fee NUMERIC DEFAULT 0,
    joining_fee NUMERIC DEFAULT 0,
    reward_type TEXT,
    reward_json JSONB,
    benefits_json JSONB,
    milestone_json JSONB,
    caps_json JSONB,
    source_url TEXT,
    data_confidence NUMERIC DEFAULT 0.0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for fast lookups
CREATE INDEX IF NOT EXISTS idx_credit_cards_bank ON credit_cards(bank);
CREATE INDEX IF NOT EXISTS idx_credit_cards_network ON credit_cards(network);
CREATE INDEX IF NOT EXISTS idx_credit_cards_confidence ON credit_cards(data_confidence DESC);
CREATE INDEX IF NOT EXISTS idx_reward_json ON credit_cards USING GIN (reward_json);
CREATE INDEX IF NOT EXISTS idx_benefits_json ON credit_cards USING GIN (benefits_json);

-- Reward change history
CREATE TABLE IF NOT EXISTS reward_history (
    id SERIAL PRIMARY KEY,
    card_id TEXT NOT NULL REFERENCES credit_cards(id) ON DELETE CASCADE,
    old_reward_json JSONB,
    new_reward_json JSONB,
    change_summary TEXT,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (card_id) REFERENCES credit_cards(id)
);

CREATE INDEX IF NOT EXISTS idx_reward_history_card_id ON reward_history(card_id);
CREATE INDEX IF NOT EXISTS idx_reward_history_detected_at ON reward_history(detected_at DESC);

-- Scraping metadata and health
CREATE TABLE IF NOT EXISTS scrape_sessions (
    id SERIAL PRIMARY KEY,
    worker_name TEXT NOT NULL,
    cards_discovered INTEGER DEFAULT 0,
    cards_scraped INTEGER DEFAULT 0,
    cards_failed INTEGER DEFAULT 0,
    cards_validated INTEGER DEFAULT 0,
    average_confidence NUMERIC DEFAULT 0.0,
    session_status TEXT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    error_log TEXT
);

CREATE INDEX IF NOT EXISTS idx_scrape_sessions_worker ON scrape_sessions(worker_name);
CREATE INDEX IF NOT EXISTS idx_scrape_sessions_completed_at ON scrape_sessions(completed_at DESC);

-- Card discovery registry (new URLs found)
CREATE TABLE IF NOT EXISTS discovery_registry (
    id SERIAL PRIMARY KEY,
    card_url TEXT UNIQUE NOT NULL,
    issuer_bank TEXT NOT NULL,
    card_name TEXT,
    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source TEXT,
    status TEXT DEFAULT 'pending'
);

CREATE INDEX IF NOT EXISTS idx_discovery_registry_bank ON discovery_registry(issuer_bank);
CREATE INDEX IF NOT EXISTS idx_discovery_registry_status ON discovery_registry(status);

-- Raw HTML snapshots metadata
CREATE TABLE IF NOT EXISTS raw_html_snapshots (
    id SERIAL PRIMARY KEY,
    card_id TEXT NOT NULL REFERENCES credit_cards(id) ON DELETE CASCADE,
    html_hash TEXT,
    file_path TEXT,
    snapshot_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_size_bytes INTEGER
);

CREATE INDEX IF NOT EXISTS idx_raw_html_card_id ON raw_html_snapshots(card_id);
CREATE INDEX IF NOT EXISTS idx_raw_html_hash ON raw_html_snapshots(html_hash);

-- Parser confidence tracking
CREATE TABLE IF NOT EXISTS parsing_confidence_log (
    id SERIAL PRIMARY KEY,
    card_id TEXT NOT NULL REFERENCES credit_cards(id) ON DELETE CASCADE,
    parse_session_id INTEGER,
    category_confidence JSONB,
    milestone_confidence NUMERIC,
    benefit_confidence NUMERIC,
    overall_confidence NUMERIC,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_parsing_confidence_card_id ON parsing_confidence_log(card_id);
CREATE INDEX IF NOT EXISTS idx_parsing_confidence_overall ON parsing_confidence_log(overall_confidence DESC);

-- Merchant category classifier training data
CREATE TABLE IF NOT EXISTS merchant_training_data (
    id SERIAL PRIMARY KEY,
    merchant_name TEXT NOT NULL,
    mcc_code TEXT,
    standard_category TEXT,
    reward_category TEXT NOT NULL,
    frequency INTEGER DEFAULT 1,
    verified_by TEXT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_merchant_training_merchant_name ON merchant_training_data(merchant_name);
CREATE INDEX IF NOT EXISTS idx_merchant_training_category ON merchant_training_data(reward_category);

-- Reward simulation dataset
CREATE TABLE IF NOT EXISTS reward_simulation_runs (
    id SERIAL PRIMARY KEY,
    card_id TEXT NOT NULL REFERENCES credit_cards(id) ON DELETE CASCADE,
    annual_spend_json JSONB,
    estimated_yearly_reward NUMERIC,
    estimated_net_reward NUMERIC,
    roi_percent NUMERIC,
    simulation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_reward_simulation_card_id ON reward_simulation_runs(card_id);
CREATE INDEX IF NOT EXISTS idx_reward_simulation_roi ON reward_simulation_runs(roi_percent DESC);

-- Health & observability
CREATE TABLE IF NOT EXISTS pipeline_metrics (
    id SERIAL PRIMARY KEY,
    metric_name TEXT NOT NULL,
    metric_value NUMERIC,
    tags JSONB,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pipeline_metrics_name ON pipeline_metrics(metric_name);
CREATE INDEX IF NOT EXISTS idx_pipeline_metrics_recorded_at ON pipeline_metrics(recorded_at DESC);

-- Views for common queries
CREATE OR REPLACE VIEW high_confidence_cards AS
SELECT 
    id, card_name, bank, annual_fee, data_confidence
FROM credit_cards
WHERE data_confidence >= 0.85
ORDER BY data_confidence DESC;

CREATE OR REPLACE VIEW recent_reward_changes AS
SELECT 
    rh.card_id,
    cc.card_name,
    cc.bank,
    rh.change_summary,
    rh.detected_at
FROM reward_history rh
JOIN credit_cards cc ON rh.card_id = cc.id
WHERE rh.detected_at >= NOW() - INTERVAL '30 days'
ORDER BY rh.detected_at DESC;

CREATE OR REPLACE VIEW portfolio_coverage_by_issuer AS
SELECT 
    bank,
    COUNT(*) as total_cards,
    COUNT(CASE WHEN data_confidence >= 0.85 THEN 1 END) as high_confidence_count,
    ROUND(100.0 * COUNT(CASE WHEN data_confidence >= 0.85 THEN 1 END) / NULLIF(COUNT(*), 0), 2) as coverage_percent
FROM credit_cards
GROUP BY bank
ORDER BY coverage_percent DESC;
