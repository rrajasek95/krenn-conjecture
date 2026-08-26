#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- batch decision over every available target.

Targets: W8's 77 killed m=17 classes (POSITIVE control), W11's 44 verified
admissible witnesses (m = 16..28), W8's immune family (m = 20..28), the m=20
CEGAR survivor, and the negative controls.
"""

from __future__ import annotations

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w12_core as C          # noqa: E402
import w12_decide as D        # noqa: E402
import w12_split as S         # noqa: E402
import w12_targets as TG      # noqa: E402
from run_t4_calibration import load_survivor, load_immunity  # noqa: E402


def one(geo, name, template, timeout, extra=None):
    t0 = time.time()
    a = C.audit(geo, template)
    scp_ok, scp_bad = TG.sc_plus(geo, template)
    cert = S.split_certificate(geo, template)
    if cert is not None:
        checks = S.verify_split_certificate(geo, template, cert)
        cert["verified"] = all(checks.values())
        cert["failed_clauses"] = [k for k, v in checks.items() if not v]
    verdict = D.decide(template, geo, timeout=timeout)
    row = {"name": name, "audit": a, "sc_plus_ok": scp_ok,
           "sc_plus_failures": scp_bad,
           "split_certificate": cert,
           "decision": verdict, "seconds": round(time.time() - t0, 2)}
    if extra:
        row.update(extra)
    print(f"{name:22s} m={a['m']:2d} S={a['sigma']:3d} "
          f"minfib={a['min_mixed_fibre']:2d} live={a['mixed_words_live']:5d} "
          f"SC+={'Y' if scp_ok else 'N'} "
          f"split={'Y' if cert else '-'} "
          f"-> {verdict['verdict']:15s} {verdict.get('reason','') or ''} "
          f"({row['seconds']}s)", flush=True)
    return row


def main():
    geo = C.geometry()
    out = {"targets": []}
    which = sys.argv[1] if len(sys.argv) > 1 else "all"

    if which in ("all", "m17"):
        print("=== POSITIVE CONTROL: W8's 77 killed m=17 classes ===",
              flush=True)
        for name, tmpl, w8v in TG.load_w8_m17_classes():
            out["targets"].append(
                one(geo, name, tmpl, 600, {"w8_verdict": w8v}))

    if which in ("all", "w11"):
        print("=== W11's 44 admissible witnesses ===", flush=True)
        for name, tmpl in TG.load_w11_witnesses():
            out["targets"].append(one(geo, name, tmpl, 900))

    if which in ("all", "core"):
        print("=== W8's immune family + the CEGAR survivor ===", flush=True)
        out["targets"].append(one(geo, "survivor_m20", load_survivor(), 1800))
        for m, tmpl, _ in load_immunity():
            out["targets"].append(one(geo, f"immunity_m{m}", tmpl, 1800))

    stem = "results_t5_batch" + ("" if which == "all" else f"_{which}")
    with open(os.path.join(HERE, stem + ".json"), "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print("wrote", stem + ".json")


if __name__ == "__main__":
    main()
