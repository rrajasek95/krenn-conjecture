#!/usr/bin/env python3
"""A5 / claim 1 mutation controls, repaired (h=4 where the factorials bite)."""
from __future__ import annotations
import json, random, sys
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15")
import a5_core as A

out = []
rng = random.Random(11)
for h in (3, 4):
    src = A.random_source(h, rng)
    w = tuple((i % 3) for i in range(2 * h))
    base = A.poly_vec(A.cap_error_raw(src, h, w), h)
    assert any(base), "base error is zero -- control battery would be vacuous"
    cfg = A.poly_vec(A.cap_error_config(src, h, w), h)
    checks = [
        ("C0 raw == config (positive control)", base == cfg, True),
        ("C1 drop k=h term", base != A.poly_vec(A.cap_error_raw_partial(src, h, w, h - 1), h), True),
        ("C2 factorials 1/k! only", base != A.poly_vec(A.cap_error_raw_badfact(src, h, w), h), True),
        ("C3 one-sided R", base != A.poly_vec(A.cap_error_config_oneR(src, h, w), h), True),
        ("C4 |J| up to h-1", base != A.poly_vec(A.cap_error_config(src, h, w, jmax=h - 1), h), True),
    ]
    # C5: perturb an entry the word actually reads (an x-edge)
    s2 = {k: [r[:] for r in v] for k, v in src.items()}
    s2[(2, 3)][w[0]][w[1]] += 1
    checks.append(("C5 perturb x-edge entry used by w",
                   base != A.poly_vec(A.cap_error_raw(s2, h, w), h), True))
    # C6: perturb an A_{p|a} entry the word reads
    s3 = {k: [r[:] for r in v] for k, v in src.items()}
    s3[(0, 2)][1][w[0]] += 1
    checks.append(("C6 perturb A_{p|a} entry used by w",
                   base != A.poly_vec(A.cap_error_raw(s3, h, w), h), True))
    # C7: perturb an A_pq entry (moves s) -- only visible for h>=3
    s4 = {k: [r[:] for r in v] for k, v in src.items()}
    s4[(0, 1)][2][2] += 1
    checks.append(("C7 perturb A_pq (s) entry",
                   base != A.poly_vec(A.cap_error_raw(s4, h, w), h), h >= 3))
    # C8: swap the p and q roles in R (should change the answer)
    s5 = {k: [r[:] for r in v] for k, v in src.items()}
    for u in range(2, 2 + 2 * h):
        s5[(0, u)], s5[(1, u)] = src[(1, u)], src[(0, u)]
    checks.append(("C8 swap p/q source rows", base != A.poly_vec(A.cap_error_raw(s5, h, w), h), True))
    for name, got, want in checks:
        ok = (bool(got) == bool(want))
        print(f"h={h} {name}: {'OK' if ok else '*** FAIL ***'} (got {bool(got)}, want {want})")
        out.append({"h": h, "control": name, "got": bool(got), "want": bool(want), "pass": ok})
json.dump(out, open("/Users/rishi/workplace/krenn-conjecture/computations/"
                    "unaudited-audit-a5-w13-2026-08-15/results_t1_controls.json", "w"), indent=1)
print("all controls pass:", all(c["pass"] for c in out))
