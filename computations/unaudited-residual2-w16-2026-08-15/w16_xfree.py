#!/usr/bin/env python3
"""W16 -- X_free-only forcing: does the 4x81 clean rectangle force a VERTEX
FACTORISATION on the R side?  (m = 25..28, gauge-fixed, lam_x free.)

For x in X_free every one of the 81 R-words is clean, so Phi(x,.) = 0 is the
full 3^4 identity.  Target polynomials are the 2x2 minors of the matrix M_t
whose columns are the t-vectors of all Gamma blocks at site t: rank M_t = 1
is exactly "vertex t factors", which kills the instance whenever a
(clean, k=1) pair differing only at t exists (mechanism W16-B).
"""
import sys, json, itertools, time
sys.path.insert(0, '/Users/rishi/workplace/krenn-conjecture/computations/unaudited-residual2-w16-2026-08-15')
import w16_gen as G
from w16_sing import run_singular

XFREE = [(x0, 2, 0, x3) for x0 in (1, 2) for x3 in (0, 1)]


def t_columns(M, t):
    """columns of M_t: for every Gamma-neighbour s and colour c_s, the
    3-vector (A_ts[c_t][c_s])_{c_t}."""
    cols = []
    for s in range(8):
        if s == t or not M.ing(t, s):
            continue
        for cs in range(3):
            cols.append([M.name(t, s, ct, cs) for ct in range(3)])
    return cols


def run(m, site, timeout=2400, extraX=()):
    M = G.Model(m)
    X = list(XFREE) + [tuple(x) for x in extraX]
    eqs = []
    for x in X:
        for y in G.clean_ys(M, x):
            if len(set(tuple(x) + tuple(y))) > 1:
                eqs.append(M.phi(x, y))
    cols = t_columns(M, site)
    tgts = []
    for i, j in itertools.combinations(range(len(cols)), 2):
        for a, b in itertools.combinations(range(3), 2):
            tgts.append("(%s)*(%s)-(%s)*(%s)" % (cols[i][a], cols[j][b],
                                                 cols[i][b], cols[j][a]))
    allv = M.variables(eqs + tgts)
    cells = [v for v in allv if v.startswith("a")]
    ll = ['LIB "elim.lib";', "ring r = 0,(%s),dp;" % ",".join(allv)]
    for i, e in enumerate(eqs, 1):
        ll.append("poly g%d = %s;" % (i, e))
    ll.append("ideal Iid = %s;" % ",".join("g%d" % i
                                           for i in range(1, len(eqs) + 1)))
    ll.append("poly PP = %s;" % "*".join(cells))
    ll.append("ideal Jid = PP;")
    ll.append("list LL = sat(Iid,Jid);")
    ll.append("ideal GS = groebner(LL[1]);")
    ll.append("int bad = 0;")
    for t in tgts:
        ll.append("if (reduce(%s,GS) != 0) { bad = bad + 1; }" % t)
    ll.append('"NBAD:"; bad;')
    ll.append('"NTGT:"; %d;' % len(tgts))
    ll.append('"UNIT:"; (GS[1]==1);')
    ll.append("quit;")
    t0 = time.time()
    out, st = run_singular("\n".join(ll) + "\n", timeout=timeout)
    if st == "TIMEOUT":
        return dict(m=m, site=site, verdict=None, n_eqs=len(eqs),
                    n_vars=len(allv), n_targets=len(tgts), secs=timeout)
    nbad = int(out.split("NBAD:")[1].strip().split()[0])
    return dict(m=m, site=site, n_eqs=len(eqs), n_vars=len(allv),
                n_targets=len(tgts), n_not_forced=nbad,
                vertex_factors_forced=(nbad == 0),
                unit=out.split("UNIT:")[1].strip().split()[0] == "1",
                secs=round(time.time() - t0, 1))


if __name__ == "__main__":
    m = int(sys.argv[1])
    sites = [int(s) for s in sys.argv[2].split(",")]
    res = []
    for s in sites:
        r = run(m, s, timeout=int(sys.argv[3]) if len(sys.argv) > 3 else 2400)
        print(r, flush=True)
        res.append(r)
    json.dump(res, open('/Users/rishi/workplace/krenn-conjecture/computations/'
                        'unaudited-residual2-w16-2026-08-15/'
                        'results_xfree_m%d.json' % m, 'w'), indent=1)
