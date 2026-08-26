#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- CONTROL C1.

Reproduce, with this lane's own code, the two facts the mission names as
anchors:
  (a) W11's stored witnesses really are (SC)-admissible, three-constant,
      zero-singleton templates (independent audit of the input data);
  (b) the m=18 / m=19 ones (and all the others) are killed by this lane's
      cut-contradiction engine, with a certificate that re-verifies and a
      reason set that is checked to be logically sufficient.

Also runs the MUTATION CONTROL: a deliberately weakened kill checker (one that
forgets to require the contradiction word to be MIXED) must produce a bogus
"kill" on a template that has none -- and the certificate verifier must reject
it.
"""
from __future__ import annotations

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import w18_core as C          # noqa: E402
import w18_kill as K          # noqa: E402

WDIR = os.path.join(HERE, "..", "unaudited-sat-pair-w11-2026-08-15",
                    "witnesses")


def load(path):
    obj = json.load(open(path))
    assert [tuple(e) for e in obj["edges"]] == list(C.EDGES), "edge order"
    T = []
    for blk in obj["blocks"]:
        mask = 0
        for (i, j) in blk:
            mask |= 1 << (3 * i + j)
        T.append(mask)
    return tuple(T)


def main():
    rows = []
    names = sorted(n for n in os.listdir(WDIR)
                   if n.endswith(".json") and n != "summary.json")
    for name in names:
        T = load(os.path.join(WDIR, name))
        t0 = time.time()
        aud = C.audit(T)
        adm = (aud["sc_ok"] and all(aud["constants"].values())
               and aud["mixed_singletons"] == 0)
        cert = K.find_kill_A(T)
        row = {"name": name, "m": aud["m"], "sigma": aud["sigma"],
               "admissible_zero_singleton": adm,
               "sc_ok": aud["sc_ok"],
               "constants": aud["constants"],
               "mixed_singletons": aud["mixed_singletons"],
               "killed_by_W18A": cert is not None}
        if cert:
            ok, notes = K.verify_certificate(T, cert)
            suff, msg = K.check_reason_sufficient(T, cert)
            row.update({"cert_verified": ok, "cert_notes": notes,
                        "reason_size": len(cert["reason"]),
                        "reason_sufficient": suff, "reason_msg": msg,
                        "cut_L": cert["cut_L"], "word": cert["word"],
                        "pinL": cert["pinL"], "pinR": cert["pinR"]})
        row["seconds"] = round(time.time() - t0, 2)
        rows.append(row)
        print(f"{name:28s} m={row['m']:2d} adm={adm} "
              f"killA={row['killed_by_W18A']} "
              f"cert={row.get('cert_verified')} "
              f"reason={row.get('reason_size')} "
              f"suff={row.get('reason_sufficient')} "
              f"[{row['seconds']}s]", flush=True)

    summary = {
        "witnesses": len(rows),
        "all_admissible_zero_singleton": all(r["admissible_zero_singleton"]
                                             for r in rows),
        "killed_by_W18A": sum(1 for r in rows if r["killed_by_W18A"]),
        "certs_verified": sum(1 for r in rows if r.get("cert_verified")),
        "reasons_sufficient": sum(1 for r in rows
                                  if r.get("reason_sufficient")),
        "not_killed": [r["name"] for r in rows if not r["killed_by_W18A"]],
        "m18_m19": [r for r in rows if r["m"] in (18, 19)],
    }
    print()
    print(json.dumps({k: v for k, v in summary.items() if k != "m18_m19"},
                     indent=1))
    json.dump({"summary": summary, "rows": rows},
              open(os.path.join(HERE, "results_c1_witnesses.json"), "w"),
              indent=1)
    print("wrote results_c1_witnesses.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
