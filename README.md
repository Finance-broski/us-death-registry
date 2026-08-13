# US Corporate Death Registry (seed)
Every S&P 500 member invisible to free data, with how and when it actually died.
Schema: ticker, exit_type (acquisition/merger/take-private/bankruptcy/delisting/reverse-merger),
acquirer_or_note, exit_year, exit_date, source_url, verified (bool), ticker_recycled, notes.
RULE: verified=True requires a source_url (press release, SEC filing, or exchange notice).
Candidate info is seeded from research sessions and MUST be sourced before flipping the flag.
Started 2026-08-13. Feeds backtest-bias v0.2, the Kaggle dataset, and the FOSS grant milestones.
