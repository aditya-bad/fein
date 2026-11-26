#!/usr/bin/env python3
"""Pre-registered test (research_notes/Macro/ey_gsec_gap_test.md): does Nifty earnings yield minus India 10-yr
G-sec yield predict 3-yr / 5-yr Nifty total-return CAGR beyond P/E alone?

Standard library + curl. Data:
  - Nifty 50 month-end close, P/E, div yield: NSE daily index files
    https://archives.nseindia.com/content/indices/ind_close_all_DDMMYYYY.csv (exist from 29-Feb-2012)
  - India 10-yr yield, monthly average: FRED INDIRLTLT01STM (OECD MEI; from 2011-12)
Total return = price + div yield/12 per month (no TRI in the archive files; pre-stated fallback).

  python3 tools/macro/ey_gap_test.py [--cache DIR]   # downloads ~180 month-end files once (cached), ~5 min
  python3 tools/macro/ey_gap_test.py --selftest      # offline: OLS / Newey-West on synthetic data
Writes research_notes/Macro/ey_gap_test_outputs/{monthly.csv,results.json}.
"""
import argparse, calendar, csv, datetime as dt, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import snapshot as S  # noqa: E402

OUT = os.path.join(REPO, "research_notes", "Macro", "ey_gap_test_outputs")
SPLIT = "2016-12"            # Deviation 1: fit <= 2016-12, test >= 2017-01
LAST_START = {36: "2023-10", 60: "2021-10"}


# ---------------------------------------------------------------- data
def month_end_nifty(y, m, cache):
    os.makedirs(cache, exist_ok=True)
    last = calendar.monthrange(y, m)[1]
    for d in range(last, last - 8, -1):
        day = dt.date(y, m, d)
        if day.weekday() >= 5:
            continue
        fn = os.path.join(cache, f"ind_close_all_{day:%d%m%Y}.csv")
        if os.path.exists(fn):
            s = open(fn).read()
        else:
            s = S.fetch(S.URL["nse_idx"].format(f"{day:%d%m%Y}"))
            if not s or "Index Name" not in s:
                continue
            open(fn, "w").write(s)
        r = S.parse_nse_idx(s)
        if r:
            return r
    return None


def build(cache, end=(2026, 10)):
    fred = S.fetch(S.URL["fred"].format("INDIRLTLT01STM"))
    ylds = {}
    for row in csv.reader(fred.splitlines()):
        if len(row) == 2 and row[0][:2] in ("19", "20"):
            try:
                ylds[row[0][:7]] = float(row[1])
            except ValueError:
                pass
    rows, y, m = [], 2012, 2
    while (y, m) <= end:
        r = month_end_nifty(y, m, cache)
        k = f"{y}-{m:02d}"
        if r and k in ylds:
            rows.append({"month": k, "date": r["date"], "close": r["close"], "pe": r["pe"], "dy": r["dy"], "y10": ylds[k]})
        else:
            print("missing", k, file=sys.stderr)
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    tr = 100.0
    for i, r in enumerate(rows):
        if i:
            p = rows[i - 1]
            tr *= (r["close"] / p["close"]) * (1 + p["dy"] / 1200)
        r["tri"] = tr
    return rows


# ---------------------------------------------------------------- stats
def solve(A, b):
    n = len(A)
    M = [A[i][:] + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c:
                f = M[r][c] / M[c][c]
                M[r] = [a - f * bb for a, bb in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def inv(A):
    n = len(A)
    return [list(col) for col in zip(*[solve(A, [1.0 if i == j else 0.0 for i in range(n)]) for j in range(n)])]


def ols(X, y, nw_lag=0):
    """X rows include the constant. Returns coefs, Newey-West t-stats (Bartlett, lag nw_lag), R2."""
    k, n = len(X[0]), len(y)
    XtX = [[sum(X[t][i] * X[t][j] for t in range(n)) for j in range(k)] for i in range(k)]
    b = solve(XtX, [sum(X[t][i] * y[t] for t in range(n)) for i in range(k)])
    e = [y[t] - sum(b[i] * X[t][i] for i in range(k)) for t in range(n)]
    my = sum(y) / n
    r2 = 1 - sum(v * v for v in e) / sum((v - my) ** 2 for v in y)
    Sm = [[0.0] * k for _ in range(k)]
    for lag in range(0, min(nw_lag, n - 1) + 1):
        w = 1.0 if lag == 0 else 1 - lag / (nw_lag + 1)
        for t in range(lag, n):
            for i in range(k):
                for j in range(k):
                    v = X[t][i] * e[t] * X[t - lag][j] * e[t - lag]
                    Sm[i][j] += w * (v if lag == 0 else v)
                    if lag:
                        Sm[j][i] += w * v
    Q = inv(XtX)
    V = [[sum(Q[i][a] * Sm[a][c] * Q[c][j] for a in range(k) for c in range(k)) for j in range(k)] for i in range(k)]
    t = [b[i] / math.sqrt(V[i][i]) if V[i][i] > 0 else float("nan") for i in range(k)]
    return b, t, r2


def predict(b, X):
    return [sum(bi * xi for bi, xi in zip(b, x)) for x in X]


MODELS = {
    "M0_ey": lambda r: [1, 100 / r["pe"]],
    "M0_logpe": lambda r: [1, math.log(r["pe"])],
    "M1_ey_y10": lambda r: [1, 100 / r["pe"], r["y10"]],
    "M2_gap": lambda r: [1, 100 / r["pe"] - r["y10"]],
}
EXPECT = {"M0_ey": [None, +1], "M0_logpe": [None, -1], "M1_ey_y10": [None, +1, -1], "M2_gap": [None, +1]}


def analyse(rows):
    idx = {r["month"]: i for i, r in enumerate(rows)}
    res = {}
    for h in (36, 60):
        S_ = [r for r in rows if r["month"] <= LAST_START[h] and idx[r["month"]] + h < len(rows)]
        for r in S_:
            r[f"fwd{h}"] = ((rows[idx[r['month']] + h]["tri"] / r["tri"]) ** (12 / h) - 1) * 100
        y = [r[f"fwd{h}"] for r in S_]
        tr = [r for r in S_ if r["month"] <= SPLIT]
        te = [r for r in S_ if r["month"] > SPLIT]
        bench = sum(r[f"fwd{h}"] for r in tr) / len(tr)
        sse_b = sum((r[f"fwd{h}"] - bench) ** 2 for r in te)
        H = {"n_starts": len(S_), "first": S_[0]["month"], "last": S_[-1]["month"], "n_train": len(tr), "n_test": len(te),
             "independent_windows_approx": round(len(S_) / h + 1, 1), "mean_fwd": round(sum(y) / len(y), 2),
             "min_fwd": round(min(y), 2), "max_fwd": round(max(y), 2), "models": {}}
        for name, f in MODELS.items():
            b, t, r2 = ols([f(r) for r in S_], y, nw_lag=h - 1)
            btr, _, _ = ols([f(r) for r in tr], [r[f"fwd{h}"] for r in tr])
            bte, _, _ = ols([f(r) for r in te], [r[f"fwd{h}"] for r in te])
            pred = predict(btr, [f(r) for r in te])
            oos = 1 - sum((r[f"fwd{h}"] - p) ** 2 for r, p in zip(te, pred)) / sse_b
            sign_ok = [all(EXPECT[name][i] * bb[i] > 0 for i in range(1, len(b))) for bb in (btr, bte)]
            # non-overlapping subsamples, all phase offsets
            nonov = []
            for off in range(h):
                sub = S_[off::h]
                if len(sub) > len(b) + 1:
                    bs, _, _ = ols([f(r) for r in sub], [r[f"fwd{h}"] for r in sub])
                    nonov.append(bs[1:])
            nm = {"full_coef": [round(v, 3) for v in b], "nw_t": [round(v, 2) for v in t], "r2_full": round(r2, 3),
                  "coef_train": [round(v, 3) for v in btr], "coef_test_half": [round(v, 3) for v in bte],
                  "oos_r2": round(oos, 3), "sign_ok_train_half": sign_ok[0], "sign_ok_test_half": sign_ok[1]}
            if nonov:
                s1 = sorted(c[0] for c in nonov)
                nm["nonoverlap"] = {"offsets": len(nonov), "points_each": len(S_[0::h]),
                                    "median_first_slope": round(s1[len(s1) // 2], 3),
                                    "share_expected_sign": round(sum(1 for c in nonov if EXPECT[name][1] * c[0] > 0) / len(nonov), 2)}
            else:
                nm["nonoverlap"] = f"not estimable: only {len(S_[0::h])} non-overlapping points per offset"
            H["models"][name] = nm
        m0, m1 = H["models"]["M0_ey"], H["models"]["M1_ey_y10"]
        H["H1_pe_predicts"] = bool(abs(m0["nw_t"][1]) >= 2 and m0["nw_t"][1] > 0 and m0["oos_r2"] > 0
                                   and m0["sign_ok_train_half"] and m0["sign_ok_test_half"])
        H["H2_gap_adds_info"] = bool(m1["oos_r2"] - m0["oos_r2"] >= 0.05 and m1["coef_train"][2] < 0 and m1["coef_test_half"][2] < 0)
        H["oos_r2_gain_M1_vs_M0"] = round(m1["oos_r2"] - m0["oos_r2"], 3)
        H["oos_r2_gain_M2_vs_M0"] = round(H["models"]["M2_gap"]["oos_r2"] - m0["oos_r2"], 3)
        res[f"{h // 12}y"] = H
    ys = [r["y10"] for r in rows]
    pes = [r["pe"] for r in rows]
    gaps = [100 / r["pe"] - r["y10"] for r in rows]
    n = len(rows)
    mp, mg = sum(pes) / n, sum(gaps) / n
    corr = (sum((a - mp) * (b - mg) for a, b in zip(pes, gaps))
            / math.sqrt(sum((a - mp) ** 2 for a in pes) * sum((b - mg) ** 2 for b in gaps)))
    res["descriptive"] = {"months": n, "first": rows[0]["month"], "last": rows[-1]["month"],
                          "pe_min_max": [min(pes), max(pes)], "y10_min_max": [min(ys), max(ys)],
                          "gap_min_max": [round(min(gaps), 2), round(max(gaps), 2)], "corr_pe_gap": round(corr, 3)}
    return res


def selftest():
    import random
    random.seed(1)
    X = [[1, random.gauss(0, 1), random.gauss(0, 1)] for _ in range(300)]
    y = [2 + 3 * x[1] - 1 * x[2] + random.gauss(0, 0.5) for x in X]
    b, t, r2 = ols(X, y, nw_lag=5)
    ok = [abs(b[0] - 2) < 0.1, abs(b[1] - 3) < 0.1, abs(b[2] + 1) < 0.1, r2 > 0.95, t[1] > 20]
    # NW t shrinks with strongly autocorrelated errors relative to plain OLS
    e, xs = 0.0, 0.0
    X2, y2 = [], []
    for _ in range(400):
        e = 0.95 * e + random.gauss(0, 1)
        xs = 0.95 * xs + random.gauss(0, 1)
        X2.append([1, xs])
        y2.append(e)
    _, t0, _ = ols(X2, y2, 0)
    _, t30, _ = ols(X2, y2, 30)
    ok.append(abs(t30[1]) < abs(t0[1]))
    print("selftest:", sum(ok), "/", len(ok), "passed")
    return 0 if all(ok) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=os.path.join(os.environ.get("FEIN_DATA", os.path.expanduser("~/fein-data")), "macro", "nse_idx"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    rows = build(a.cache)
    res = analyse(rows)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "monthly.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["month", "date", "close", "pe", "dy", "y10", "tri", "fwd36", "fwd60"])
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
    res["generated"] = dt.date.today().isoformat()
    res["sources"] = [S.URL["nse_idx"].format("DDMMYYYY"), "https://fred.stlouisfed.org/series/INDIRLTLT01STM"]
    json.dump(res, open(os.path.join(OUT, "results.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
