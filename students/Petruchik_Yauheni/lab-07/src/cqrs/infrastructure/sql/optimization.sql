-- Оптимизация таблицы представлений бюджетов
CREATE INDEX IF NOT EXISTS idx_budget_summary_budget_id ON budget_summary (budget_id);
