#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- SECOND, INDEPENDENT DECOMPOSITION.

Pinned HEAD: see PINNED_HEAD.txt.  Probe output; not a proved project claim.

The primary sweep splits the exhaustion over isomorphism classes of the
SUPPORT GRAPH.  This module splits it over CONSTANT-WITNESS TRIPLES instead
(the decomposition W8 used), which is a completely different cut of the same
space, so agreement between the two lanes is a real cross-check.

WHY THE SPLIT IS COMPLETE.  An admissible template has a nonempty fibre for
each of the three constant words, i.e. for each colour c a perfect matching
M_c of K_8 all of whose edges carry the cell (c,c).  Relabelling sites and
colours moves the ordered triple (M_0, M_1, M_2) onto one of the orbit
representatives computed here, so forcing a representative's twelve diagonal
cells is sound and complete (the cases overlap, which is harmless).

The kill hierarchy, the certificate checks and the proof emission are exactly
the primary sweep's; only the case split and the encoder differ (here the
support graph is free and the support size is pinned by a cardinality
constraint).
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import sys
import time
from collections import Counter
from itertools import permutations

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import w18_core as C            # noqa: E402
import w18_fast as F            # noqa: E402
import w18_graphs as G          # noqa: E402
import w18_half as Hf           # noqa: E402
import w18_kill as K            # noqa: E402
import w18_lattice as L         # noqa: E402
import w18_sat as S             # noqa: E402
import w18_sweep as SW          # noqa: E402
from pysat.card import CardEnc, EncType      # noqa: E402
from pysat.formula import IDPool             # noqa: E402
from pysat.solvers import Solver             # noqa: E402


# ------------------------------------------------- the witness triples

def _perm_matching_table():
    """(40320, 105) table: image index of each matching under each site perm."""
    bits = np.zeros((len(C.PMS), C.NE), dtype=np.float64)
    for n, M in enumerate(C.PM_EIDX):
        for e in M:
            bits[n, e] = 1.0
    masks = bits @ G._WT                      # (105, 40320) image masks
    base = np.array([sum(1 << e for e in M) for M in C.PM_EIDX],
                    dtype=np.int64)
    order = np.argsort(base)
    sortedbase = base[order]
    idx = np.searchsorted(sortedbase, masks.astype(np.int64))
    return order[idx].T                        # (40320, 105)


_PMTAB = None


def pmtab():
    global _PMTAB
    if _PMTAB is None:
        _PMTAB = _perm_matching_table()
    return _PMTAB


def witness_orbits():
    """Orbit representatives of ordered triples of perfect matchings."""
    tab = pmtab()
    canon = C.PM_EIDX.index(tuple(C.EIDX[(2 * k, 2 * k + 1)] for k in range(4)))
    reps = {}
    for b in range(len(C.PMS)):
        for c in range(len(C.PMS)):
            triple = (canon, b, c)
            best = None
            for sig in permutations(range(3)):
                t = tuple(triple[sig[k]] for k in range(3))
                x = tab[:, t[0]].astype(np.int64) * 105 * 105 \
                    + tab[:, t[1]] * 105 + tab[:, t[2]]
                v = int(x.min())
                best = v if best is None else min(best, v)
            reps.setdefault(best, triple)
    return [reps[k] for k in sorted(reps)]


def triple_stabiliser(triple):
    """(site perm, colour perm) pairs fixing the ordered triple setwise."""
    tab = pmtab()
    out = []
    for sig in permutations(range(3)):
        want = tuple(triple[sig[k]] for k in range(3))
        ok = np.ones(tab.shape[0], dtype=bool)
        for k in range(3):
            ok &= (tab[:, triple[k]] == want[k])
        for p in np.nonzero(ok)[0]:
            # sites permuted by G.PERMS[p]; colour k -> position of k in sig
            colour = [0] * 3
            for k in range(3):
                colour[k] = sig.index(k)
            out.append((tuple(G.PERMS[int(p)]), tuple(colour)))
    return out


# --------------------------------------------------------- the encoder

class OrbitEncoder:
    """Cells on all 28 edges, support pinned to m, a witness triple forced."""

    def __init__(self, m, triple):
        self.m = m
        self.triple = triple
        self.pool = IDPool()
        self.clauses = []
        self.x = {}
        for e in range(C.NE):
            for k in range(9):
                self.x[(e, k)] = self.pool.id(("c", e, k))
        self.present = {e: self.pool.id(("p", e)) for e in range(C.NE)}
        for e in range(C.NE):
            self.clauses.append([-self.present[e]]
                                + [self.x[(e, k)] for k in range(9)])
            for k in range(9):
                self.clauses.append([-self.x[(e, k)], self.present[e]])
        card = CardEnc.equals(lits=[self.present[e] for e in range(C.NE)],
                              bound=m, vpool=self.pool,
                              encoding=EncType.seqcounter)
        self.clauses.extend([list(cl) for cl in card.clauses])
        self.t = {}
        for e in range(C.NE):
            for side in range(2):
                for r in range(3):
                    v = self.pool.id(("t", e, side, r))
                    self.t[(e, side, r)] = v
                    self.clauses.append([-v, self.present[e]])
                    for k in range(9):
                        i, j = divmod(k, 3)
                        if (j if side == 1 else i) != r:
                            self.clauses.append([-v, -self.x[(e, k)]])
        for p in range(C.N):
            for r in range(3):
                lits = []
                for e in C.INCIDENT[p]:
                    u, v = C.EDGES[e]
                    lits.append(self.t[(e, 1 if u == p else 0, r)])
                self.clauses.append(lits)
        for colour, mi in enumerate(triple):
            for e in C.PM_EIDX[mi]:
                self.clauses.append([self.x[(e, 4 * colour)]])
        self.nv = self.pool.top
        self.word_done = set()
        self.kill_clauses = 0
        self.edge_set = set(range(C.NE))

    def add_word_constraint(self, w):
        if w in self.word_done:
            return
        self.word_done.add(w)
        cells = {}
        for n in range(len(C.PMS)):
            sel = []
            for e in C.PM_EIDX[n]:
                u, v = C.EDGES[e]
                sel.append(self.x[(e, 3 * w[u] + w[v])])
            cells[n] = sel
        z = {}
        for n in range(len(C.PMS)):
            self.nv += 1
            z[n] = self.nv
            for lit in cells[n]:
                self.clauses.append([-z[n], lit])
            self.clauses.append([-lit for lit in cells[n]] + [z[n]])
        for n in range(len(C.PMS)):
            self.clauses.append([-lit for lit in cells[n]]
                                + [z[k] for k in z if k != n])
        self.pool.top = max(self.pool.top, self.nv)

    def add_kill_clause(self, reason):
        cl = []
        for (kind, e, i, j) in reason:
            lit = self.x[(e, 3 * i + j)]
            cl.append(-lit if kind == "on" else lit)
        assert cl
        self.clauses.append(cl)
        self.kill_clauses += 1
        return cl

    def block_template(self, T):
        cl = []
        for e in range(C.NE):
            for k in range(9):
                lit = self.x[(e, k)]
                cl.append(-lit if (T[e] >> k) & 1 else lit)
        self.clauses.append(cl)
        return cl

    def decode(self, model):
        pos = set(l for l in model if l > 0)
        T = []
        for e in range(C.NE):
            mask = 0
            for k in range(9):
                if self.x[(e, k)] in pos:
                    mask |= 1 << k
            T.append(mask)
        return tuple(T)


def run_orbit(m, triple, seconds=1800, outdir=None, store_certs=True,
              sing_batch=16, cert_cap=2000):
    t0 = time.time()
    enc = OrbitEncoder(m, triple)
    group = triple_stabiliser(triple)
    sol = Solver(name="cadical195", bootstrap_with=enc.clauses)
    ptr = len(enc.clauses)
    tally = Counter()
    certs = {"O2": [], "A": [], "D": [], "C": [], "B": []}
    survivors = []
    rounds = 0
    status = "timeout"
    eng = S.FibreEngine(list(range(C.NE)))

    def push():
        nonlocal ptr
        for cl in enc.clauses[ptr:]:
            sol.add_clause(cl)
        ptr = len(enc.clauses)

    def orbit_reasons(reason):
        out = []
        seen = set()
        for (pi, sig) in group:
            img = tuple(sorted(SWmap(l, pi, sig) for l in reason))
            if img not in seen:
                seen.add(img)
                out.append([list(x) for x in img])
        return out

    def SWmap(lit, pi, sig):
        import w18_sym as SY
        return SY.map_literal(tuple(lit), pi, sig)

    while time.time() - t0 < seconds:
        if sol.solve() is False:
            status = "UNSAT"
            break
        rounds += 1
        T = enc.decode(sol.get_model())
        assert C.support(T) == m, "encoding unsound: support"
        assert C.sc_ok(T), "encoding unsound: (SC)"
        assert C.constants_ok(T), "encoding unsound: constants"
        sing, _ = eng.singleton_words(T)
        if sing:
            tally["O2-singleton"] += 1
            for w in sing[:sing_batch]:
                cert = K.singleton_reason(T, w)
                ok, _ = K.verify_singleton(T, cert)
                ok2, _ = K.singleton_reason_sufficient(
                    T, K.minimise_singleton_reason(T, cert))
                cert = K.minimise_singleton_reason(T, cert)
                if not (ok and ok2):
                    status = "O2-FAILURE"
                    survivors.append([int(x) for x in T])
                    break
                for r in orbit_reasons(cert["reason"]):
                    enc.add_kill_clause(r)
                if store_certs and len(certs["O2"]) < cert_cap:
                    certs["O2"].append(cert)
            push()
            if status != "timeout":
                break
            continue
        occ = F.occupancy(T)
        compat = F.support_matrix(occ)
        hit = F.find(T, compat)
        if hit is not None:
            cert = F.certificate(T, hit)
            ok, _ = K.verify_certificate(T, cert)
            cert = K.minimise_reason(T, cert)
            ok2, _ = K.check_reason_sufficient(T, cert)
            if not (ok and ok2):
                status = "A-FAILURE"
                survivors.append([int(x) for x in T])
                break
            for r in orbit_reasons(cert["reason"]):
                enc.add_kill_clause(r)
            push()
            tally["W18-A"] += 1
            if store_certs and len(certs["A"]) < cert_cap:
                certs["A"].append(cert)
            continue
        cert = Hf.find_kill_D(T, occ, compat)
        if cert is not None:
            ok, _ = Hf.verify_D(T, cert)
            if not ok:
                status = "D-FAILURE"
                survivors.append([int(x) for x in T])
                break
            reason = Hf.reason_D(T, cert)
            ok2, _ = Hf.reason_D_sufficient(T, cert, reason)
            if ok2:
                reason = Hf.minimise_reason_D(T, cert, reason)
                for r in orbit_reasons(reason):
                    enc.add_kill_clause(r)
                cert["reason"] = reason
                tally["W18-D:" + cert["ratio"]["rule"]] += 1
            else:
                enc.block_template(T)
                tally["W18-D-blocked"] += 1
            push()
            cert["template"] = [int(x) for x in T]
            if store_certs and len(certs["D"]) < cert_cap:
                certs["D"].append(cert)
            continue
        cert = L.find_kill_C(T)
        if cert is not None:
            ok, _ = L.verify_C(T, cert)
            if not ok:
                status = "C-FAILURE"
                survivors.append([int(x) for x in T])
                break
            enc.block_template(T)
            push()
            cert["template"] = [int(x) for x in T]
            tally["W18-C"] += 1
            if store_certs and len(certs["C"]) < cert_cap:
                certs["C"].append(cert)
            continue
        survivors.append([int(x) for x in T])
        status = "SURVIVOR"
        break
    sol.delete()
    row = {"m": m, "triple": list(triple), "status": status, "rounds": rounds,
           "tally": dict(tally), "stabiliser": len(group),
           "nclauses": len(enc.clauses), "nvars": enc.nv,
           "seconds": round(time.time() - t0, 2)}
    if survivors:
        row["survivors"] = survivors
    if status == "UNSAT" and outdir is not None:
        row["proof"] = SW.emit_and_check_proof(
            enc.pool.top, enc.clauses,
            "orbit_m%d_t%d_%d_%d" % ((m,) + tuple(triple)), outdir)
    row["certificates"] = certs if store_certs else None
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, required=True)
    ap.add_argument("--stride", type=int, default=1)
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--seconds", type=float, default=1800.0)
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    reps = witness_orbits()
    print("witness-triple orbits:", len(reps), flush=True)
    idxs = list(range(len(reps)))[args.offset::args.stride]
    outdir = os.path.join(HERE, "certificates", "orbit_m%d" % args.m)
    certdir = os.path.join(HERE, "certificates", "orbit_m%d_kills" % args.m)
    os.makedirs(certdir, exist_ok=True)
    rows = []
    t0 = time.time()
    for i in idxs:
        row = run_orbit(args.m, reps[i], seconds=args.seconds, outdir=outdir)
        row["orbit"] = i
        certs = row.pop("certificates", None)
        if certs:
            with gzip.open(os.path.join(certdir, "o%d.json.gz" % i), "wt") as fh:
                json.dump({"orbit": i, "triple": list(reps[i]),
                           "m": args.m, "certificates": certs}, fh)
        rows.append(row)
        print(f"[{time.time()-t0:8.1f}s] orbit {i:3d} {row['status']:<12s} "
              f"rounds={row['rounds']:6d} stab={row['stabiliser']:4d} "
              f"{row['seconds']:8.1f}s "
              f"proof_rc={row.get('proof', {}).get('rup18_rc')} "
              f"tally={row['tally']}", flush=True)
        if row["status"] != "UNSAT":
            print("  !!!!! NON-UNSAT:", row["status"], flush=True)
    json.dump({"m": args.m, "orbits": len(rows), "rows": rows},
              open(os.path.join(HERE, "results_orbit_m%d%s.json"
                                % (args.m, args.tag)), "w"))
    print("done", flush=True)


if __name__ == "__main__":
    sys.exit(main())
