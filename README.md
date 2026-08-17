# US Corporate Death Registry (seed)
Every S&P 500 member invisible to free data, with how and when it actually died.
Schema: ticker, exit_type (acquisition/merger/take-private/bankruptcy/delisting/reverse-merger),
acquirer_or_note, exit_year, exit_date, source_url, verified (bool), ticker_recycled, notes.
RULE: verified=True requires a source_url (press release, SEC filing, or exchange notice).
Candidate info is seeded from research sessions and MUST be sourced before flipping the flag.
Started 2026-08-13. Feeds backtest-bias v0.2, the Kaggle dataset, and the FOSS grant milestones.

## Field definitions (audited 2026-08-17)
- **verified**: True only when source_url is a primary source (SEC filing, company/acquirer
  press release, or major wire story) directly documenting the event. All 139 rows verified.
- **exit_date**: the event the source dates - deal completion for M&A/take-privates,
  petition date for bankruptcies (emergence noted where applicable), rename effective date.
- **ticker_recycled**: True if the symbol was LATER REUSED by a different issuer at any
  point (14 of 139) - the trap under the trap: a visible ticker is not a continuous company.
- Source-link note: SEC links require a declared User-Agent per SEC policy; newswire hosts
  (businesswire/prnewswire/globenewswire) block scripted clients but open normally in a
  browser. Every URL was live-checked 2026-08-17 (one replaced: YHOO, Altaba's press page
  died with the company - which is itself the registry's thesis in action).
