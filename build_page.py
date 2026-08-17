"""Build the public registry page (financebroski.com/deaths.html) from registry_seed.csv.

The CSV stays the source of truth: add or fix a row there, re-run this, and the page plus the
on-site CSV copy move together, so the published counts can never drift from the file. Every
number on the page is computed here - none is typed by hand.

Page CSS is scoped to body.registry and lives inside the page. The shared style.css is NEVER
edited for one page (that broke the graveyard twice).

Run: python build_page.py   (writes deaths.html + us_death_registry.csv into the site repo)
"""
import datetime as dt
import html
import os
import shutil
import urllib.parse as up

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = r"C:\dev\financebroski.github.io"
CSV = os.path.join(HERE, "registry_seed.csv")
OUT = os.path.join(SITE, "deaths.html")
CSV_COPY = os.path.join(SITE, "us_death_registry.csv")
REPO = "https://github.com/Finance-broski/us-death-registry"
KAGGLE = ("https://www.kaggle.com/datasets/financebroski/"
          "s-and-p-500-survivorship-bias-point-in-time")

FATE_LABEL = {
    "acquisition": "acquired",
    "merger": "merged",
    "take-private": "taken private",
    "renamed": "renamed",
    "bankruptcy": "bankrupt, gone",
    "bankruptcy-emerged": "bankrupt, re-emerged",
    "split": "split up",
}
FATE_ORDER = ["acquisition", "merger", "take-private", "renamed",
              "bankruptcy-emerged", "bankruptcy", "split"]


def esc(x):
    return html.escape(str(x), quote=True)


def host(url):
    h = up.urlparse(str(url)).netloc.replace("www.", "")
    return {"sec.gov": "SEC filing"}.get(h, h)


def main():
    d = pd.read_csv(CSV)
    d["exit_date"] = pd.to_datetime(d["exit_date"])
    d = d.sort_values("exit_date", ascending=False).reset_index(drop=True)

    n = len(d)
    n_sourced = int(d["verified"].sum())
    n_recycled = int(d["ticker_recycled"].sum())
    recycled = sorted(d.loc[d["ticker_recycled"], "ticker"].tolist())
    n_recent = int((d["exit_date"].dt.year >= 2024).sum())
    n_sec = int(d["source_url"].str.contains("sec.gov").sum())
    y0, y1 = int(d["exit_date"].dt.year.min()), int(d["exit_date"].dt.year.max())
    counts = d["exit_type"].value_counts()

    rows = []
    for _, r in d.iterrows():
        badge = ('<span class="recyc" title="this ticker was later used by a different '
                 'issuer">reused</span>' if r["ticker_recycled"] else "")
        fate = FATE_LABEL.get(r["exit_type"], r["exit_type"])
        rows.append(
            f'<tr><td class="mono tick">{esc(r["ticker"])}{badge}</td>'
            f'<td><span class="fate f-{esc(r["exit_type"])}">{esc(fate)}</span></td>'
            f'<td class="who">{esc(r["acquirer_or_note"])}'
            f'<span class="note">{esc(r["notes"])}</span></td>'
            f'<td class="mono">{r["exit_date"].date()}</td>'
            f'<td class="mono src"><a href="{esc(r["source_url"])}" rel="nofollow noopener" '
            f'target="_blank">{esc(host(r["source_url"]))}</a></td></tr>')

    fate_rows = "".join(
        f'<tr><td>{esc(FATE_LABEL.get(k, k))}</td><td class="mono">{int(counts[k])}</td></tr>'
        for k in FATE_ORDER if k in counts)

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The US Death Registry &middot; what happened to every company missing from free S&amp;P 500 data</title>
<meta name="description" content="{n} S&amp;P 500 names that vanished from free membership data, each with the actual fate (acquired, taken private, merged, renamed, bankrupt), the date it stopped trading, and a primary source. Free CSV, no signup.">
<meta property="og:title" content="The US Death Registry">
<meta property="og:description" content="Every company missing from free S&amp;P 500 data, and what actually happened to it. {n} sourced exits, {y0}-{y1}.">
<meta property="og:type" content="website">
<link rel="icon" href="mark.png">
<link rel="stylesheet" href="style.css">
<style>
body.registry{{background:var(--bg);color:var(--fg)}}
body.registry .wrap{{max-width:1020px;margin:0 auto;padding:3.2rem 1.2rem 4rem}}
body.registry h1{{font-family:var(--serif);font-size:clamp(1.9rem,4.5vw,2.7rem);margin:.2rem 0 .6rem;letter-spacing:-.01em}}
body.registry .kick{{font-family:var(--mono);font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--accent-hi)}}
body.registry .sub{{color:var(--muted);max-width:66ch;line-height:1.65;margin:.4rem 0 0}}
body.registry .statrow{{display:flex;gap:2.2rem;flex-wrap:wrap;margin:1.7rem 0 0}}
body.registry .stat .n{{font-family:var(--mono);font-size:1.5rem;color:var(--fg)}}
body.registry .stat .l{{font-size:.82rem;color:var(--faint);margin-top:.15rem}}
body.registry h2{{font-family:var(--serif);font-size:1.35rem;margin:2.6rem 0 .5rem}}
body.registry p{{color:var(--muted);line-height:1.65;max-width:70ch}}
body.registry ul{{color:var(--muted);line-height:1.65;max-width:70ch;padding-left:1.1rem}}
body.registry li{{margin:.3rem 0}}
body.registry code{{font-family:var(--mono);font-size:.86rem;color:var(--fg)}}
body.registry .tablewrap{{overflow-x:auto;margin-top:.9rem;border-top:1px solid var(--line)}}
body.registry table{{border-collapse:collapse;width:100%;font-size:.92rem}}
body.registry th{{text-align:left;font-family:var(--mono);font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);padding:.5rem .8rem;border-bottom:2px solid var(--line);white-space:nowrap}}
body.registry th.sortable{{cursor:pointer;user-select:none}}
body.registry th.sortable:hover{{color:var(--accent-hi)}}
body.registry th.sortable::after{{content:" \\2195";opacity:.35}}
body.registry td{{padding:.55rem .8rem;border-bottom:1px solid var(--line);vertical-align:top}}
body.registry td.mono{{font-family:var(--mono);font-size:.88rem;white-space:nowrap}}
body.registry td.tick{{font-weight:600;color:var(--fg)}}
body.registry .recyc{{font-family:var(--mono);font-size:.62rem;letter-spacing:.06em;text-transform:uppercase;color:var(--flag);border:1px solid var(--flag);border-radius:4px;padding:0 .25rem;margin-left:.4rem;vertical-align:1px;cursor:help}}
body.registry .fate{{font-family:var(--mono);font-size:.78rem;white-space:nowrap;color:var(--muted)}}
body.registry .fate.f-bankruptcy,body.registry .fate.f-bankruptcy-emerged{{color:var(--flag)}}
body.registry .who{{min-width:19rem;color:var(--fg)}}
body.registry .note{{display:block;color:var(--faint);font-size:.82rem;line-height:1.45;margin-top:.15rem}}
body.registry td.src a{{color:var(--accent-hi);font-size:.82rem}}
body.registry .tools{{display:flex;gap:.8rem;align-items:center;flex-wrap:wrap;margin:1.1rem 0 .2rem}}
body.registry input[type=search]{{background:var(--panel-hi);border:1px solid var(--line);border-radius:8px;color:var(--fg);font-family:var(--mono);font-size:.86rem;padding:.5rem .7rem;min-width:15rem}}
body.registry .count{{font-family:var(--mono);font-size:.82rem;color:var(--faint)}}
body.registry .rules{{background:var(--panel-hi);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:10px;padding:1.1rem 1.3rem;margin-top:1rem}}
body.registry .rules p{{margin:.35rem 0;font-size:.92rem}}
body.registry a{{color:var(--accent-hi)}}
body.registry .dl{{display:inline-block;margin-top:.8rem;font-family:var(--mono);font-size:.85rem}}
body.registry .fine{{font-size:.85rem;color:var(--faint);line-height:1.55;margin-top:2.4rem}}
body.registry .mini{{max-width:26rem}}
body.registry .mini td{{padding:.4rem .8rem}}
</style>
</head>
<body class="registry">
<div class="wrap">
  <div class="kick">The US Death Registry</div>
  <h1>Every company missing from free S&amp;P 500 data, and what happened to it.</h1>
  <p class="sub">Download a free list of S&amp;P 500 members from a few years back and the names
  that were acquired, taken private, or went bankrupt are simply absent. Nothing marks the hole,
  so a backtest built on that list quietly tests only the survivors and reports their returns as
  the index's. This page fills the holes: {n} tickers, the actual fate of each one, the date it
  stopped trading, and a primary source for every single row.</p>

  <div class="statrow">
    <div class="stat"><div class="n">{n}</div><div class="l">exits recorded</div></div>
    <div class="stat"><div class="n">{n_sourced}/{n}</div><div class="l">with a source opened by hand</div></div>
    <div class="stat"><div class="n">{n_recycled}</div><div class="l">tickers later reused by a different issuer</div></div>
    <div class="stat"><div class="n">{n_recent}</div><div class="l">left in 2024 or later</div></div>
  </div>

  <h2>What is in each row</h2>
  <p><code>ticker</code>, <code>exit_type</code>, <code>acquirer_or_note</code> (who bought it or
  what it became), <code>exit_year</code>, <code>exit_date</code> (the last day it traded under
  that ticker), <code>source_url</code>, <code>verified</code>, <code>ticker_recycled</code>, and
  a <code>notes</code> line recording what the source actually says. Range covered:
  {y0} to {y1}.</p>

  <h2>How the names leave</h2>
  <div class="tablewrap"><table class="mini">{fate_rows}</table></div>
  <p>Most of the missing names are not failures. They were bought at a premium, so a survivors-only
  backtest usually drops the good outcomes as well as the bad ones. That is why the direction of
  survivorship error is not predictable from theory: it depends on which names your source lost.</p>

  <h2>The trap that survives a careful join</h2>
  <p>{n_recycled} of these tickers were later used by a different issuer. Join old prices to new
  prices on ticker alone and you can splice two unrelated companies into one continuous series
  with no warning anywhere in the data: {", ".join(f"<code>{esc(t)}</code>" for t in recycled)}.
  "Reused" here means strictly that: the same letters appeared later under a different issuer.
  It does not claim the ticker belongs to that other company today.</p>

  <h2>The registry</h2>
  <div class="tools">
    <input type="search" id="q" placeholder="filter: ticker, buyer, year..." aria-label="filter the registry">
    <span class="count" id="cnt">{n} of {n} rows</span>
  </div>
  <div class="tablewrap"><table id="reg">
    <thead><tr>
      <th class="sortable" data-k="0">ticker</th>
      <th class="sortable" data-k="1">what happened</th>
      <th class="sortable" data-k="2">who / what it became</th>
      <th class="sortable" data-k="3">last traded</th>
      <th>source</th>
    </tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table></div>
  <a class="dl" href="us_death_registry.csv">download the registry (csv)</a> &middot;
  <a class="dl" href="{REPO}">repo and revision history</a> &middot;
  <a class="dl" href="{KAGGLE}">point-in-time membership dataset</a>

  <h2>How it was verified</h2>
  <p>Every row was checked against a primary document and the note records what that document
  says: {n_sec} rows rest on SEC filings, the rest on company press releases or exchange notices.
  Where a source had rotted, it was replaced with the filing rather than left as a dead link, and
  where a host blocks automated fetches the page was confirmed in a browser instead of trusting a
  script's status code.</p>
  <p>Two honest limits. First, this is the set of names that go missing from the free membership
  sources being probed, not the complete set of every S&amp;P 500 change ever; it grows as more
  vintages are compared. Second, an exit date is the last day the ticker traded, which for a
  merger closing intraday is the day of the close.</p>

  <h2>What to do with it</h2>
  <ul>
    <li>Take your own universe file, anti-join it against this list, and count how many exits your
    source silently dropped. That number is the size of your survivorship hole, measured rather
    than assumed.</li>
    <li>Before joining price histories on ticker, check the reused list. A splice there is
    invisible in returns and fatal in a backtest.</li>
    <li>If your data vendor claims point-in-time membership, ask them what happened to a handful of
    these tickers. The answers separate a real PIT panel from a current-members list.</li>
  </ul>

  <h2>The rules this page runs on</h2>
  <div class="rules">
    <p>1. The file is the source of truth and this page is generated from it, so the counts here
    cannot drift from the data.</p>
    <p>2. Append-only. Corrections happen in the open and are noted, not quietly overwritten.</p>
    <p>3. Free, CSV, no signup, no email wall.</p>
    <p>4. A wrong row is a bug report I want. If you can point at a document, send it and it gets
    fixed with the source credited.</p>
  </div>

  <p class="fine">Built while auditing backtests for survivorship damage; this is the reference
  list that work needed. The rest of the record: <a href="index.html">the audit practice</a>
  &middot; <a href="graveyard.html">the graveyard</a> &middot;
  <a href="auction.html">the auction ledger</a>. Generated {dt.date.today().isoformat()} from
  registry_seed.csv.</p>
</div>
<script>
(function () {{
  var tb = document.querySelector('#reg tbody'), q = document.getElementById('q'),
      cnt = document.getElementById('cnt'), rows = Array.prototype.slice.call(tb.rows), dir = {{}};
  q.addEventListener('input', function () {{
    var s = q.value.toLowerCase(), shown = 0;
    rows.forEach(function (r) {{
      var hit = r.textContent.toLowerCase().indexOf(s) > -1;
      r.style.display = hit ? '' : 'none';
      if (hit) shown++;
    }});
    cnt.textContent = shown + ' of ' + rows.length + ' rows';
  }});
  document.querySelectorAll('#reg th.sortable').forEach(function (th) {{
    th.addEventListener('click', function () {{
      var k = +th.dataset.k, asc = !(dir[k] = !dir[k]);
      rows.sort(function (a, b) {{
        var x = a.cells[k].textContent.trim(), y = b.cells[k].textContent.trim();
        return (x < y ? -1 : x > y ? 1 : 0) * (asc ? 1 : -1);
      }});
      rows.forEach(function (r) {{ tb.appendChild(r); }});
    }});
  }});
}})();
</script>
</body>
</html>
"""
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    shutil.copyfile(CSV, CSV_COPY)
    print(f"wrote {OUT} ({len(page):,} bytes) from {n} rows")
    print(f"copied csv -> {CSV_COPY}")
    print(f"stats: {n_sourced}/{n} sourced, {n_recycled} reused, {n_recent} since 2024, "
          f"{n_sec} SEC-filing rows, span {y0}-{y1}")


if __name__ == "__main__":
    main()
