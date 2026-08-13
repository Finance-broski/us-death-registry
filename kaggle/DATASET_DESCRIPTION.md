# S&P 500 point-in-time membership, and what free data can't see

Two dated vintages of S&P 500 membership (1 Jan 2010 and 1 Jan 2015), a liveness probe of
every member against free price data (stamped July 2026), and a seed registry of how the
invisible names actually died.

Measured findings this dataset supports:

- Roughly one in four members of the 2010 vintage is invisible in free price data today
  (about one in five for 2015).
- The survivor-filter effect on an equal-weight backtest: +0.39 pp/yr (2010 vintage,
  16.6 years) and +1.02 pp/yr (2015, 11.6 years) — and year-by-year it swings from
  −7.5 to +3.5, netting small only by cancellation.
- Ticker recycling is the trap under the trap: four reanimated tickers (CPWR, EP, COL, MI)
  moved the measured result by 1.7 pp/yr, more than the bias itself. A visible ticker is
  not proof of a continuous company: S was Sprint until 2020 and serves SentinelOne today.

## Files

**sp500_membership_vintages.csv** — one row per (vintage, ticker). Membership as of the
vintage date, rebuilt by walking today's constituent list backwards through the public
dated changelog; endpoint cross-checked against the ETF issuer's published holdings
(503 of 503 match).

**visibility_probe_2026-07.csv** — (vintage, ticker, visible_today). visible_today = 1 if
a five-day recent-history request against the free source returns rows (a liveness test,
deliberately: recycled tickers count as visible, identity is a separate check).

**death_registry_seed.csv** — the invisible names with candidate exit type, acquirer,
year, date, and a source_url column. Entries are marked verified only when they carry a
source URL. This is a living registry being built in public; corrections with receipts
are welcome.

## Method and writeups

Full method, the return-effect measurement, and the identity checks:
https://financebroski.com — the free library behind the checks: `pip install backtest-bias`
(https://github.com/Finance-broski/backtest-bias).

Membership derived from the public dated changelog (Wikipedia), CC BY-SA; probe and
registry are original measurements. If you use this to correct a backtest, that is the
whole point.
