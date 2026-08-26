#!/usr/bin/env python3
"""UNAUDITED PROBE (W8) -- the band-closing CEGAR: is there an admissible
template of support <= m that survives BOTH O2 and the value-level closure?

Pinned HEAD: a1196b4dca9f83452483734a3273c0c43d5cf3b5

Loop.
  solve the SAT model of {support <= m, FIE, constants supported}
    * model has a mixed singleton  -> add the exact "fibre(w) != 1" constraint
      for the offending words (a logical consequence of O2 + exactness);
    * model is zero-singleton but the closure engine kills it -> extract the
      certificate, VERIFY it independently, and add the nogood
          NOT( fibre(w_1) = F_1  and ... and  fibre(w_k) = F_k ),
      which is licensed because any template with those exact fibres carries
      the same certificate and therefore admits no nonzero complex values;
    * model is zero-singleton and survives -> STOP: a concrete counterexample
      candidate for the whole route.
  UNSAT  ->  every exact N = 8 source of support <= m is refuted by
             O2 + the closure engine.

Run: python3 w8_close.py --m 19 --seconds 3600
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter

import numpy as np

import w8_core as C
import w8_cert as K
from w8_sat import Encoding, near_constant_words


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--m", type=int, default=19)
    parser.add_argument("--seconds", type=float, default=3600.0)
    parser.add_argument("--seed-radius", type=int, default=2)
    parser.add_argument("--solver", default="cadical153")
    parser.add_argument("--verify-every", type=int, default=1)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    geo = C.geometry(8)
    enc = Encoding(geo, args.m, args.solver)
    for w in near_constant_words(geo, args.seed_radius):
        enc.word_constraint(w)
    print(f"UNAUDITED PROBE (W8) -- closing CEGAR at support <= {args.m}; "
          f"seeded {len(enc.added_words)} words", flush=True)

    start = time.time()
    verdicts = Counter()
    survivors = []
    kills = []
    unverified = []
    rounds = 0
    status = "?"
    while True:
        if time.time() - start > args.seconds:
            status = "timeout"
            break
        if enc.solver.solve() is False:
            status = "UNSAT"
            break
        rounds += 1
        template = enc.decode(enc.solver.get_model())
        compat = C.compat_matrix(geo, template)
        assert C.fie_ok(geo, template) and C.constants_ok(geo, template, compat)
        assert C.support(template) <= args.m
        sizes = compat.sum(axis=0, dtype=np.int64)
        bad = np.nonzero((sizes == 1) & geo.mixed)[0]
        if len(bad):
            verdicts["O2-literal-singleton"] += 1
            for w in sorted(int(x) for x in bad)[:32]:
                enc.word_constraint(w)
        else:
            cert = K.certify(geo, template, compat=compat)
            verdicts[cert["verdict"]] += 1
            if cert["verdict"] == "survivor":
                survivors.append(list(template))
                print(f"  [{time.time()-start:7.1f}s] round {rounds}: "
                      f"SURVIVOR at support {C.support(template)} "
                      f"Sigma {C.sigma(template)}", flush=True)
                status = "survivor"
                break
            if rounds % args.verify_every == 0:
                ok, notes = K.verify(geo, template, cert)
                if not ok:
                    unverified.append({"template": list(template),
                                       "notes": notes})
                    print("  CERTIFICATE FAILED VERIFICATION", notes[-2:],
                          flush=True)
                    status = "certificate-failure"
                    break
            pairs = K.certificate_words(cert)
            size = enc.fibre_nogood(pairs)
            kills.append({"round": rounds, "verdict": cert["verdict"],
                          "words": len(pairs), "clause": size,
                          "support": C.support(template),
                          "sigma": C.sigma(template)})
        if rounds % 25 == 0:
            print(f"  [{time.time()-start:7.1f}s] round {rounds}: "
                  f"{dict(verdicts)}, {len(enc.added_words)} words, "
                  f"{len(kills)} nogoods", flush=True)
    elapsed = round(time.time() - start, 1)
    out = {"m": args.m, "status": status, "rounds": rounds,
           "seconds": elapsed, "verdicts": dict(verdicts),
           "words_constrained": len(enc.added_words),
           "nogoods": len(kills), "kill_log": kills[-50:],
           "survivors": survivors, "unverified": unverified}
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("kill_log", "survivors")}, indent=1))
    name = args.out or f"results_close_m{args.m}.json"
    with open(name, "w") as handle:
        json.dump(out, handle, indent=1)
    print(f"wrote {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
