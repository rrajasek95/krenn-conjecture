#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- controls.

Pinned HEAD: see PINNED_HEAD.txt.  Probe output; not a proved project claim.

C1  planted witnesses: W11's stored witnesses are re-audited with this lane's
    code and must be (SC)-admissible, three-constant, zero-singleton; each
    must be FOUND by the per-class encoder (its exact cell pattern satisfies
    the base CNF) and KILLED with a verified certificate.
C2  W8 anchor: W8's 31 m=18 constant-witness-orbit SAT templates are audited
    and killed here; kill-mechanism distribution reported.
C3  equivariance: random g in S_8 x S_3 applied to killed templates preserves
    (SC), the fibre-size multiset, and the kill (this is what licenses the
    orbit propagation of nogoods and blocking clauses).
C4  mutation of the kill checker: a deliberately broken Lemma W18-A search
    (the "the contradiction word must be MIXED" test removed) produces
    certificates, and verify_certificate must REJECT every one of them.
C5  mutation of the reason machinery: dropping a literal from a verified
    minimal reason must make check_reason_sufficient FAIL.
C6  proof replay mutation: a valid DRUP proof, (a) truncated and (b) with one
    lemma corrupted, must be REJECTED by rup18; and rup18 must agree with
    W11's independent rupcheck on the intact proof.
C7  planted survivor: with the kill engines disabled, the driver must report
    SURVIVOR on a class that certainly contains admissible templates.
C8  solver independence: a census class recomputed with glucose4 gives the
    same template count as with cadical195.
"""
from __future__ import annotations

import gzip
import json
import os
import random
import subprocess
import sys
import time
from collections import Counter
from itertools import permutations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import w18_core as C          # noqa: E402
import w18_fast as F          # noqa: E402
import w18_graphs as G        # noqa: E402
import w18_half as H          # noqa: E402
import w18_kill as K          # noqa: E402
import w18_lattice as L       # noqa: E402
import w18_sat as S           # noqa: E402
import w18_sweep as SW        # noqa: E402
import w18_sym as SY          # noqa: E402
from pysat.solvers import Lingeling, Solver     # noqa: E402

W11 = os.path.join(HERE, "..", "unaudited-sat-pair-w11-2026-08-15")
W8 = os.path.join(HERE, "..", "unaudited-template-kill-w8-2026-08-15")
OUT = {}


def load_w11(path):
    obj = json.load(open(path))
    T = []
    for blk in obj["blocks"]:
        mask = 0
        for (i, j) in blk:
            mask |= 1 << (3 * i + j)
        T.append(mask)
    return tuple(T)


def kill_any(T):
    occ = F.occupancy(T)
    compat = F.support_matrix(occ)
    hit = F.find(T, compat)
    if hit is not None:
        cert = F.certificate(T, hit)
        ok, _ = K.verify_certificate(T, cert)
        return ("W18-A", ok, cert)
    cert = H.find_kill_D(T, occ, compat)
    if cert is not None:
        ok, _ = H.verify_D(T, cert)
        return ("W18-D:" + cert["ratio"]["rule"], ok, cert)
    cert = L.find_kill_C(T)
    if cert is not None:
        ok, _ = L.verify_C(T, cert)
        return ("W18-C:" + str(cert.get("rule") or cert["ratio"]["rule"]),
                ok, cert)
    return (None, False, None)


def graph_mask(T):
    m = 0
    for e, mask in enumerate(T):
        if mask:
            m |= 1 << e
    return m


def c1_witnesses():
    wdir = os.path.join(W11, "witnesses")
    rows = []
    for name in sorted(os.listdir(wdir)):
        if not name.endswith(".json") or name == "summary.json":
            continue
        T = load_w11(os.path.join(wdir, name))
        aud = C.audit(T)
        adm = (aud["sc_ok"] and all(aud["constants"].values())
               and aud["mixed_singletons"] == 0)
        mech, ok, _ = kill_any(T)
        found = encoder_accepts(T)
        rows.append({"name": name, "m": aud["m"], "sigma": aud["sigma"],
                     "admissible_zero_singleton": adm,
                     "encoder_accepts": found,
                     "mechanism": mech, "certificate_verified": ok})
    return {"n": len(rows),
            "all_admissible": all(r["admissible_zero_singleton"] for r in rows),
            "all_found_by_encoder": all(r["encoder_accepts"] for r in rows),
            "all_killed_and_verified": all(r["mechanism"] and
                                           r["certificate_verified"]
                                           for r in rows),
            "mechanisms": _tally(r["mechanism"] for r in rows),
            "rows": rows}


def encoder_accepts(T):
    """Does the class encoder for T's own support graph admit exactly T?"""
    mask = graph_mask(T)
    enc = S.ClassEncoder(mask)
    if any(not cl for cl in enc.clauses):
        return False
    units = []
    for e in enc.edges:
        for k in range(9):
            lit = enc.x[(e, k)]
            units.append(lit if (T[e] >> k) & 1 else -lit)
    sol = Solver(name="cadical195", bootstrap_with=enc.clauses + [[u] for u in units])
    ok = sol.solve()
    sol.delete()
    return bool(ok)


def c2_w8_anchor():
    path = os.path.join(W8, "results_band_m18_nosingleton.json")
    d = json.load(open(path))
    rows = []
    for r in d["rows"]:
        for T in r.get("survivors", []):
            T = tuple(int(x) for x in T)
            aud = C.audit(T)
            adm = (aud["sc_ok"] and all(aud["constants"].values())
                   and aud["mixed_singletons"] == 0)
            mech, ok, _ = kill_any(T)
            rows.append({"orbit": r["orbit"], "m": aud["m"],
                         "sigma": aud["sigma"],
                         "single_cell_blocks": aud["single_cell_blocks"],
                         "admissible_zero_singleton": adm,
                         "mechanism": mech, "certificate_verified": ok})
    return {"n": len(rows),
            "all_admissible": all(r["admissible_zero_singleton"] for r in rows),
            "all_killed_and_verified": all(r["mechanism"] and
                                           r["certificate_verified"]
                                           for r in rows),
            "sigma_range": [min(r["sigma"] for r in rows),
                            max(r["sigma"] for r in rows)],
            "mechanisms": _tally(r["mechanism"] for r in rows),
            "rows": rows}


def _tally(it):
    out = {}
    for x in it:
        out[str(x)] = out.get(str(x), 0) + 1
    return out


def c3_equivariance(trials=40, seed=7):
    rng = random.Random(seed)
    wdir = os.path.join(W11, "witnesses")
    names = [n for n in sorted(os.listdir(wdir))
             if n.endswith(".json") and n != "summary.json"]
    bad = []
    for t in range(trials):
        T = load_w11(os.path.join(wdir, rng.choice(names)))
        pi = tuple(rng.sample(range(8), 8))
        sig = tuple(rng.sample(range(3), 3))
        T2 = C.apply_perm(T, pi, sig)
        a1, a2 = C.audit(T), C.audit(T2)
        same = (a1["m"] == a2["m"] and a1["sigma"] == a2["sigma"]
                and a1["sc_ok"] == a2["sc_ok"]
                and a1["fibre_histogram"] == a2["fibre_histogram"]
                and sorted(a1["constants"].values())
                == sorted(a2["constants"].values()))
        m1, ok1, cert1 = kill_any(T)
        m2, ok2, _ = kill_any(T2)
        # the reason set must transport too
        rok = True
        if cert1 is not None and cert1.get("lemma") == "W18-A":
            img = [list(SY.map_literal(tuple(l), pi, sig))
                   for l in cert1["reason"]]
            cert1b = dict(cert1)
            cert1b["reason"] = img
            cert1b["cut_L"] = sorted(pi[p] for p in cert1["cut_L"])
            cert1b["cut_R"] = sorted(pi[p] for p in cert1["cut_R"])
            w = [0] * 8
            for p in range(8):
                w[pi[p]] = sig[cert1["word"][p]]
            cert1b["word"] = w
            cert1b["u"] = [w[p] for p in cert1b["cut_L"]]
            cert1b["y"] = [w[p] for p in cert1b["cut_R"]]
            vok, _ = K.verify_certificate(T2, cert1b)
            sok, _ = K.check_reason_sufficient(T2, cert1b)
            rok = vok and sok
        if not (same and bool(m1) == bool(m2) and ok1 == ok2 and rok):
            bad.append({"trial": t, "pi": pi, "sig": sig, "same": same,
                        "m1": m1, "m2": m2, "reason_transports": rok})
    return {"trials": trials, "failures": len(bad), "examples": bad[:3]}


def c4_mutated_checker():
    """A broken W18-A search that forgets the MIXED test must be rejected."""
    wdir = os.path.join(W11, "witnesses")
    T = load_w11(os.path.join(wdir, "m18_1048445_0.json"))
    occ = F.occupancy(T)
    compat = F.support_matrix(occ)
    made = 0
    rejected = 0
    for cut in F.CUTS:
        if len(cut.crossing_pms) == 0:
            continue
        split = ~compat[cut.crossing_pms].any(axis=0)
        cl = [c for c in range(3) if split[F.CONST_WORD_IDX[c]]]
        for c in cl:
            widx = int(cut.sideR.fullidx[c][cut.sideR.const_index[c]])
            if not split[widx]:
                continue
            hit = (cut.L, cut.R, (c,) * len(cut.L), (c,) * len(cut.R),
                   "P2", "P2")          # the CONSTANT word: not a kill
            cert = F.certificate(T, hit)
            made += 1
            ok, notes = K.verify_certificate(T, cert)
            if not ok:
                rejected += 1
    return {"bogus_certificates_made": made, "rejected_by_verifier": rejected,
            "control_passes": made > 0 and rejected == made}


def c5_reason_mutation(trials=25, seed=11):
    rng = random.Random(seed)
    wdir = os.path.join(W11, "witnesses")
    names = [n for n in sorted(os.listdir(wdir))
             if n.endswith(".json") and n != "summary.json"]
    checked = 0
    survived = 0
    for _ in range(trials):
        T = load_w11(os.path.join(wdir, rng.choice(names)))
        hit = F.find(T)
        if hit is None:
            continue
        cert = K.minimise_reason(T, F.certificate(T, hit))
        for k in range(len(cert["reason"])):
            trial = dict(cert)
            trial["reason"] = cert["reason"][:k] + cert["reason"][k + 1:]
            ok, _ = K.check_reason_sufficient(T, trial)
            checked += 1
            if ok:
                survived += 1
    return {"literal_drops_tested": checked,
            "still_sufficient_after_drop": survived,
            "control_passes": checked > 0 and survived == 0}


def c6_proof_mutation():
    """Build an UNSAT instance with a nontrivial proof, then break the proof.

    Three mutations, matching the recorded pysat/cadical hazard and the two
    obvious corruptions: (a) the file cut at a byte boundary in the middle of
    a clause, (b) only the first two lemmas kept, (c) one lemma corrupted by
    an extra literal.  All three must be REJECTED.
    """
    # The class encodings are SAT before any kill clause is added, so the
    # fixture is a pigeonhole formula: UNSAT for sure, and with a proof long
    # enough that a truncation really does stop short of the empty clause.
    def php(npig, nhole):
        var = {}
        cls = []
        for p in range(npig):
            for h in range(nhole):
                var[(p, h)] = len(var) + 1
        for p in range(npig):
            cls.append([var[(p, h)] for h in range(nhole)])
        for h in range(nhole):
            for p in range(npig):
                for q in range(p + 1, npig):
                    cls.append([-var[(p, h)], -var[(q, h)]])
        return len(var), cls

    proof = []
    for n in (8, 9, 10):
        nv, cls = php(n, n - 1)
        s = Lingeling(bootstrap_with=cls, with_proof=True)
        assert not s.solve(), "pigeonhole fixture is not UNSAT"
        proof = s.get_proof()
        s.delete()
        if len(proof) >= 200:
            break
    if len(proof) < 200:
        return {"control_passes": False, "note": "no suitable instance"}
    mask = "PHP(%d,%d)" % (n, n - 1)
    tmp = os.path.join(HERE, "_control_tmp")
    os.makedirs(tmp, exist_ok=True)
    cnf = os.path.join(tmp, "c6.cnf")
    S.write_cnf(cnf, nv, cls)
    good = os.path.join(tmp, "c6.drup")
    text = "\n".join(proof) + "\n"
    open(good, "w").write(text)
    midcut = os.path.join(tmp, "c6_midcut.drup")
    cut = len(text) // 2
    while cut < len(text) and text[cut] not in " \n":
        cut += 1
    open(midcut, "w").write(text[:cut] + " 17")      # unterminated clause
    short = os.path.join(tmp, "c6_short.drup")
    open(short, "w").write("\n".join(proof[:2]) + "\n")
    corrupt = os.path.join(tmp, "c6_corrupt.drup")
    lines = list(proof)
    for i, line in enumerate(lines):
        parts = line.split()
        if len(parts) >= 3 and parts[0] != "d":
            lines[i] = " ".join(["999"] + parts)
            break
    open(corrupt, "w").write("\n".join(lines) + "\n")
    res = {"mask": mask, "proof_lemmas": len(proof)}
    for tag, path in (("intact", good), ("midcut", midcut),
                      ("first_two_lemmas", short), ("corrupted", corrupt)):
        r = subprocess.run([SW.RUP, cnf, path], capture_output=True, text=True)
        res[tag] = {"rc": r.returncode, "out": (r.stdout or r.stderr).strip()}
    w11rup = os.path.join(W11, "rupcheck")
    if os.path.exists(w11rup):
        for tag, path in (("intact", good), ("corrupted", corrupt)):
            r = subprocess.run([w11rup, cnf, path], capture_output=True,
                               text=True)
            res["w11_rupcheck_" + tag] = {"rc": r.returncode,
                                          "out": (r.stdout or r.stderr).strip()}
    res["control_passes"] = (res["intact"]["rc"] == 0
                             and res["midcut"]["rc"] != 0
                             and res["first_two_lemmas"]["rc"] != 0
                             and res["corrupted"]["rc"] != 0
                             and res.get("w11_rupcheck_intact",
                                         {"rc": 1})["rc"] == 0)
    return res


def c7_planted_survivor():
    """Disable the kill engines: the driver must report SURVIVOR."""
    classes = json.load(open(os.path.join(HERE, "graph_classes.json")))
    mask = classes["18"][436]
    import w18_deep as DP
    saved = (F.find, H.find_kill_D, L.find_kill_C, DP.find_kill_B)
    F.find = lambda T, compat=None: None
    H.find_kill_D = lambda T, occ=None, compat=None, side_sizes=(4,): None
    L.find_kill_C = lambda T, fibres=None: None
    DP.find_kill_B = lambda T, timeout=60, cuts=None, verbose=False: (None, None)
    try:
        row = SW.run_class(mask, 18, seconds=300, outdir=None,
                           store_certs=False, deep_timeout=1)
    finally:
        (F.find, H.find_kill_D, L.find_kill_C, DP.find_kill_B) = saved
    return {"status": row["status"], "rounds": row["rounds"],
            "control_passes": row["status"] == "SURVIVOR",
            "survivor": row.get("survivors", [None])[0]}


def c8_solver_independence():
    import run_census as RC
    classes = json.load(open(os.path.join(HERE, "graph_classes.json")))
    out = []
    for mask in [6233982, 6224126]:
        a = RC.census_class(mask, 17, seconds=600)
        saved = RC.Solver
        n_a = len(a["templates"])
        b = _census_with(mask, 17, "glucose4")
        out.append({"mask": mask, "cadical195": n_a, "glucose4": b,
                    "agree": n_a == b})
    return {"rows": out, "control_passes": all(r["agree"] for r in out)}


def _census_with(mask, m, solver):
    enc = S.ClassEncoder(mask)
    eng = S.FibreEngine(enc.edges)
    sol = Solver(name=solver, bootstrap_with=enc.clauses)
    ptr = len(enc.clauses)
    n = 0
    while True:
        if sol.solve() is False:
            break
        T = enc.decode(sol.get_model())
        sing, _ = eng.singleton_words(T)
        if sing:
            for w in sing[:24]:
                enc.add_word_constraint(w)
            for cl in enc.clauses[ptr:]:
                sol.add_clause(cl)
            ptr = len(enc.clauses)
            continue
        n += 1
        cl = enc.block_template(T)
        sol.add_clause(cl)
        ptr = len(enc.clauses)
    sol.delete()
    return n


def c9_excluded_classes(ms=(18, 19)):
    """The classes dropped by the min-degree/perfect-matching filters must be
    UNSAT for the encoder too -- otherwise the filters were not sound."""
    allc = json.load(open(os.path.join(HERE, "graph_classes_all.json")))
    keep = json.load(open(os.path.join(HERE, "graph_classes.json")))
    out = {}
    for m in ms:
        kept = set(keep[str(m)])
        dropped = [x for x in allc[str(m)] if x not in kept]
        statuses = Counter()
        bad = []
        for mask in dropped:
            row = SW.run_class(mask, m, seconds=120, outdir=None,
                               store_certs=False)
            statuses[row["status"]] += 1
            if row["status"] not in ("UNSAT", "TRIVIAL-UNSAT"):
                bad.append({"mask": mask, "status": row["status"]})
        out[str(m)] = {"dropped_classes": len(dropped),
                       "statuses": dict(statuses), "bad": bad}
    out["control_passes"] = all(not v["bad"] for k, v in out.items()
                                if k != "control_passes")
    return out


if __name__ == "__main__":
    which = sys.argv[1:] or ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8",
                             "C9"]
    res = {}
    for tag in which:
        t0 = time.time()
        fn = {"C1": c1_witnesses, "C2": c2_w8_anchor, "C3": c3_equivariance,
              "C4": c4_mutated_checker, "C5": c5_reason_mutation,
              "C6": c6_proof_mutation, "C7": c7_planted_survivor,
              "C8": c8_solver_independence,
              "C9": c9_excluded_classes}[tag]
        res[tag] = fn()
        res[tag]["seconds"] = round(time.time() - t0, 1)
        brief = {k: v for k, v in res[tag].items() if k != "rows"}
        print(tag, json.dumps(brief)[:1200], flush=True)
    json.dump(res, open(os.path.join(HERE, "results_controls.json"), "w"),
              indent=1)
    print("wrote results_controls.json")
