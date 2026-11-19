"""memdb CLI — long-term memory for the FEIN investing project.

Examples
  python3 -m memdb search "promoter pledge" --type insight
  python3 -m memdb search "" --ticker UNIPARTS            # everything about a ticker
  python3 -m memdb get case_study:radico-khaitan --history
  python3 -m memdb add --type insight --title "..." --body "..." --tag base-rate --source URL
  python3 -m memdb add --json-file records.json           # bulk: list of record dicts
  python3 -m memdb metric add UNIPARTS FY26 pat 158 --unit "INR cr" --source screener
  python3 -m memdb metric get UNIPARTS --field pat
  python3 -m memdb related case_study:radico-khaitan
  python3 -m memdb ingest-md research_notes/**/*.md --tag research
  python3 -m memdb stats | rebuild | compact | types
"""
import argparse
import glob
import json
import sys
import textwrap
from pathlib import Path

from . import core


def _print_rec(r, full=False):
    tick = ",".join(r.get("tickers") or [])
    tags = ",".join(r.get("tags") or [])
    print(f"[{r['id']}] {r.get('title','')}")
    meta = " · ".join(x for x in (r.get("date"), tick, tags, r.get("status"), r.get("confidence")) if x)
    if meta:
        print(f"    {meta}")
    if full:
        if r.get("body"):
            print(textwrap.indent(r["body"], "    "))
        if r.get("data"):
            print("    data: " + json.dumps(r["data"], ensure_ascii=False))
        if r.get("sources"):
            print("    sources: " + " | ".join(r["sources"]))
    else:
        snip = (r.get("snip") or r.get("body") or "").replace("\n", " ")
        if snip:
            print("    " + snip[:220])


def main(argv=None):
    ap = argparse.ArgumentParser(prog="memdb", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search"); s.add_argument("query", nargs="?", default="")
    s.add_argument("--type"); s.add_argument("--ticker"); s.add_argument("--tag")
    s.add_argument("--since"); s.add_argument("--limit", type=int, default=15)
    s.add_argument("--full", action="store_true"); s.add_argument("--json", action="store_true")

    g = sub.add_parser("get"); g.add_argument("id"); g.add_argument("--history", action="store_true")
    g.add_argument("--json", action="store_true")

    a = sub.add_parser("add")
    a.add_argument("--type"); a.add_argument("--id"); a.add_argument("--title")
    a.add_argument("--ticker", action="append", default=[]); a.add_argument("--tag", action="append", default=[])
    a.add_argument("--date"); a.add_argument("--body"); a.add_argument("--body-file")
    a.add_argument("--data", help="JSON object"); a.add_argument("--source", action="append", default=[])
    a.add_argument("--link", action="append", default=[], help="target_id[:rel]")
    a.add_argument("--confidence", help="verified | single-source | unverified | myth")
    a.add_argument("--status"); a.add_argument("--replace", action="store_true", help="don't merge with existing")
    a.add_argument("--json-file", help="bulk add: file with a JSON list of records")

    d = sub.add_parser("delete"); d.add_argument("id")
    r = sub.add_parser("related"); r.add_argument("id")

    m = sub.add_parser("metric"); msub = m.add_subparsers(dest="mcmd", required=True)
    ma = msub.add_parser("add"); ma.add_argument("ticker"); ma.add_argument("period")
    ma.add_argument("field"); ma.add_argument("value", type=float)
    ma.add_argument("--unit", default=""); ma.add_argument("--source", default=""); ma.add_argument("--as-of", default="")
    mg = msub.add_parser("get"); mg.add_argument("ticker"); mg.add_argument("--field")

    i = sub.add_parser("ingest-md"); i.add_argument("paths", nargs="+")
    i.add_argument("--tag", action="append", default=[]); i.add_argument("--ticker", action="append", default=[])
    i.add_argument("--date", default="")

    sub.add_parser("stats"); sub.add_parser("rebuild"); sub.add_parser("compact"); sub.add_parser("types")
    args = ap.parse_args(argv)

    if args.cmd == "types":
        for k, v in core.TYPES.items():
            print(f"{k:11s} {v}")
        return
    if args.cmd == "rebuild":
        print(f"indexed {core.rebuild()} items"); return
    if args.cmd == "compact":
        print(f"kept {core.compact()} items"); return

    con = core.connect()
    if args.cmd == "search":
        res = core.search(con, args.query, args.type, args.ticker, args.tag, args.since, args.limit)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=1)); return
        for x in res:
            _print_rec(x, args.full)
        if not res:
            print("(no matches)")
    elif args.cmd == "get":
        rec = core.get(con, args.id)
        if not rec:
            sys.exit(f"not found: {args.id}")
        if args.json:
            print(json.dumps(rec, ensure_ascii=False, indent=1))
        else:
            _print_rec(rec, full=True)
        if args.history:
            for h in core.history(args.id, rec["type"]):
                print(f"  v{h.get('version')} {h.get('updated')}")
    elif args.cmd == "add":
        if args.json_file:
            recs = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
            for rec in recs:
                core.put(con, rec, merge=not rec.pop("_replace", False), commit=False)
            core.touch(con)
            print(f"added/updated {len(recs)} records"); return
        if not args.type or not (args.title or args.id):
            sys.exit("--type and --title (or --id) required")
        body = Path(args.body_file).read_text(encoding="utf-8") if args.body_file else args.body
        links = []
        for l in args.link:
            to, _, rel = l.rpartition(":") if l.count(":") >= 2 else (l, "", "related")
            links.append({"to": to or l, "rel": rel or "related"})
        rec = core.put(con, {"type": args.type, "id": args.id, "title": args.title,
                             "tickers": [t.upper() for t in args.ticker], "tags": args.tag,
                             "date": args.date, "body": body,
                             "data": json.loads(args.data) if args.data else None,
                             "sources": args.source, "links": links,
                             "confidence": args.confidence, "status": args.status},
                       merge=not args.replace)
        print(f"saved {rec['id']} (v{rec['version']})")
    elif args.cmd == "delete":
        core.delete(con, args.id); print(f"deleted {args.id}")
    elif args.cmd == "related":
        for x in core.related(con, args.id):
            print(f"  {'→' if x['dir']=='out' else '←'} {x['rel']:12s} [{x['id']}] {x['title']}")
    elif args.cmd == "metric":
        if args.mcmd == "add":
            core.add_metric(con, args.ticker, args.period, args.field, args.value,
                            args.unit, args.source, args.as_of)
            print("ok")
        else:
            q = "SELECT * FROM metrics WHERE ticker=?" + (" AND field=?" if args.field else "") + " ORDER BY field, period"
            for row in con.execute(q, (args.ticker.upper(), args.field) if args.field else (args.ticker.upper(),)):
                print(f"  {row['field']:14s} {row['period']:8s} {row['value']:>12,.2f} {row['unit']}  ({row['source']} {row['as_of']})")
    elif args.cmd == "ingest-md":
        files = sorted({f for p in args.paths for f in glob.glob(p, recursive=True)})
        total = sum(core.ingest_markdown(con, Path(f), args.tag, [t.upper() for t in args.ticker], args.date)
                    for f in files)
        print(f"ingested {len(files)} files → {total} passages")
    elif args.cmd == "stats":
        for k, v in sorted(core.stats(con).items()):
            print(f"  {k:12s} {v}")


if __name__ == "__main__":
    main()
