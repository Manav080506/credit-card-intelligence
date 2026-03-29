-- Optimization logs for analytics and ML training

CREATE TABLE optimization_logs (
  id SERIAL PRIMARY KEY,
  user_id TEXT,
  spend_online FLOAT DEFAULT 0,
  spend_dining FLOAT DEFAULT 0,
  spend_travel FLOAT DEFAULT 0,
  spend_utilities FLOAT DEFAULT 0,
  recommended_card TEXT,
  expected_monthly_reward FLOAT,
  confidence_score FLOAT,
  created_at TIMESTAMP DEFAULT now()
);

-- Performance indexes
CREATE INDEX idx_optimization_logs_user_id ON optimization_logs(user_id);
CREATE INDEX idx_optimization_logs_created_at ON optimization_logs(created_at);
CREATE INDEX idx_optimization_logs_recommended_card ON optimization_logs(recommended_card);
