# How to write memdb seed files (for research agents)

Output a JSON **list** of record objects to `memdb/seeds/<date>_<topic>.json`.
Claude ingests with `python3 -m memdb add --json-file <file>`. Validate your JSON parses
(`python3 -c "import json;json.load(open('FILE'))"`). Do NOT run the add yourself unless told.

## Record fields
| field | required | notes |
|---|---|---|
| `type` | yes | one of: company, case_study, strategy, analysis, thesis, promise, event, insight, decision, person, theme, source, note |
| `id` | yes | `<type>:<slug>` lowercase-hyphen, e.g. `case_study:bajaj-finance-2008-2021`, `person:stanley-druckenmiller`, `company:BAJFINANCE` (company ids use the NSE ticker in caps; US: `company:US-NVDA`) |
| `title` | yes | short, specific |
| `body` | yes | dense facts: numbers with years, causes, early signals, outcome, lesson. 80–300 words. |
| `tickers` | if any | NSE ticker caps (US prefix `US-`), list |
| `tags` | yes | lowercase; reuse: india, us, global, multibagger, blowup, fraud, redflag, turnaround, cyclical, rerating, premiumisation, deleveraging, policy, sector-<name>, base-rate, myth, process, alt-data, governance |
| `date` | yes | date the episode refers to or YYYY-MM-DD of research |
| `data` | optional | structured JSON: e.g. {"start_year":2009,"end_year":2021,"start_price":..., "end_price":..., "multiple":"~x", "max_drawdown":"-x%", "early_signals":"...", "lesson":"..."} |
| `sources` | yes | list of URLs actually used |
| `confidence` | yes | verified (2+ sources) / single-source / unverified / myth |
| `links` | optional | [{"to":"<existing id>","rel":"illustrates|contradicts|about|similar_to|caused_by|part_of"}] |

## Existing ids you may link to
insight:twin-engine, insight:hidden-segment, insight:multibagger-patterns, insight:winners-drawdowns,
insight:disqualifiers, insight:avoid-ruin, insight:bessembinder, insight:sebi-fo-losses,
insight:behavior-gap, insight:luck-vs-skill, insight:founders-not-investors, insight:ai-picking-evidence,
strategy:buffett-munger, strategy:lynch, strategy:fisher-scuttlebutt, strategy:qglp, strategy:marcellus-cc,
strategy:variant-perception, strategy:position-sizing, case_study:radico-khaitan, case_study:nvidia,
case_study:suzlon, person:warren-buffett, person:peter-lynch, person:radhakishan-damani,
person:rakesh-jhunjhunwala.

## Quality bar
- Split-/bonus-adjust prices and say so. Mark anything unchecked as `unverified`.
- Every case study must state the **early signal that was visible at the time** and the **lesson**.
- No investment recommendations. This is a knowledge base.
