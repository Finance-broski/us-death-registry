# US Corporate Death Registry (seed)
What actually happened to every S&P 500 name that goes missing from free membership data.
Schema: ticker, exit_type (acquisition/merger/take-private/bankruptcy/bankruptcy-emerged/
renamed/split), acquirer_or_note, exit_year, exit_date, source_url, verified (bool),
ticker_recycled, notes.
RULE: verified=True requires a source_url (press release, SEC filing, or exchange notice).
Candidate info is seeded from research sessions and MUST be sourced before flipping the flag.
Started 2026-08-13. Feeds backtest-bias v0.2, the Kaggle dataset, and the FOSS grant milestones.
Browsable version (sortable, searchable, same CSV): https://financebroski.com/deaths.html

## What is in it (regenerated from the CSV 2026-08-17)
143 rows, all 143 verified against a primary source, covering exits from 2010 to 2026, of
which 21 happened in 2024 or later. 38 rows rest on SEC filings, the rest on company press
releases or exchange notices. Exit types: 87 acquisition, 18 take-private, 18 merger, 6
renamed, 6 bankruptcy-emerged, 4 bankruptcy, 4 split.

139 of the rows are names that are INVISIBLE in free membership data. The other 4 (CPWR, EP,
COL, MI) are the opposite failure and the reason the registry exists: their tickers are
perfectly visible today because a different issuer reuses them, and the free source serves the
replacement's history stitched onto the dead company with no gap. Those four moved a measured
survivorship number by 1.7pp/yr, which was larger than the survivorship bias being measured.

## Field definitions (audited 2026-08-17)
- **verified**: True only when source_url is a primary source (SEC filing, company/acquirer
  press release, or major wire story) directly documenting the event. All 143 rows verified.
- **exit_date**: the event the source dates - deal completion for M&A/take-privates,
  petition date for bankruptcies (emergence noted where applicable), rename effective date.
- **ticker_recycled**: True if the symbol was LATER REUSED by a different issuer at any
  point (14 of 143) - the trap under the trap: a visible ticker is not a continuous company.
  This is the superset. Which of the 14 actually contaminate a panel depends on the sample
  window and the data source; four did in mine.
- Source-link note: SEC links require a declared User-Agent per SEC policy; newswire hosts
  (businesswire/prnewswire/globenewswire) block scripted clients but open normally in a
  browser. Every URL was live-checked 2026-08-17 (one replaced: YHOO, Altaba's press page
  died with the company - which is itself the registry's thesis in action).

## Corrections
A wrong row is a bug report worth having. Open an issue with a primary source and it gets
fixed with the source credited. The file is append-only; corrections are noted, not silently
overwritten.
