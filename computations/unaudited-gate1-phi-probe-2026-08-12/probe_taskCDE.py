#!/usr/bin/env python3
"""UNAUDITED PROBE - Tasks C, D, E for Gate I.

C: assemble the largest inventory of source-provenant candidate columns the
   committed checkers know how to construct, in a common augmented row model,
   and decide by exact rational linear algebra whether J(M_v) lies in the span.
D: the three shared-label coherence equations for cutwise fillers.
E: mutation controls for every PASS.

All arithmetic is exact (fractions.Fraction).
"""
from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = {}


def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ------------------------------------------------------------ exact lin alg
def rref(rows):
    work = [list(r) for r in rows]
    if not work:
        return [], []
    ncol = len(work[0])
    piv, r = [], 0
    for c in range(ncol):
        p = next((i for i in range(r, len(work)) if work[i][c]), None)
        if p is None:
            continue
        work[r], work[p] = work[p], work[r]
        v = work[r][c]
        work[r] = [x / v for x in work[r]]
        for i in range(len(work)):
            if i != r and work[i][c]:
                f = work[i][c]
                work[i] = [a - f * b for a, b in zip(work[i], work[r])]
        piv.append(c)
        r += 1
        if r == len(work):
            break
    return work[:r], piv


def col_rank(cols, h):
    return len(rref([[cols[j][i] for j in range(len(cols))] for i in range(h)])[0])


def nullspace(rows, ncol):
    red, piv = rref(rows)
    out = []
    for f in [c for c in range(ncol) if c not in piv]:
        v = [Q(0)] * ncol
        v[f] = Q(1)
        for i, c in enumerate(piv):
            v[c] = -red[i][f]
        out.append(v)
    return out


def membership(cols, target, h):
    """Return (in_span, coefficients or None)."""
    w = len(cols)
    aug = [[Q(cols[j][i]) for j in range(w)] + [Q(target[i])] for i in range(h)]
    red, piv = rref(aug)
    if w in piv:
        return False, None
    coeff = [Q(0)] * w
    for i, c in enumerate(piv):
        coeff[c] = red[i][w]
    chk = [sum((coeff[j] * Q(cols[j][i]) for j in range(w)), Q(0)) for i in range(h)]
    assert chk == [Q(x) for x in target]
    return True, coeff


def left_nullspace(cols, h):
    """All covectors L (length h) with L . col = 0 for every column."""
    rows = [list(map(Q, c)) for c in cols]   # each column is one equation on L
    return nullspace(rows, h)


# ------------------------------------------------------------ union row model
CORNERS = ("P+q00", "P-q00", "P+q11", "P-q11")
ALPHA = (Q(-1), Q(1), Q(1), Q(-1))          # -delta
KINDS = ("private", "Eq", "W", "target", "R", "D")
ROWS = tuple(f"{k}_{c}" for c in CORNERS for k in KINDS) + ("ainc",) + tuple(
    f"eta{f}_constant" for f in range(1, 6)) + ("eta1_U1", "sigma_qpq22")
H = len(ROWS)
RIDX = {r: i for i, r in enumerate(ROWS)}


def vec(**e):
    assert set(e) <= set(ROWS), sorted(set(e) - set(ROWS))
    return tuple(Q(e.get(r, 0)) for r in ROWS)


def vadd(*vs):
    return tuple(sum(x, Q(0)) for x in zip(*vs))


def vscale(a, v):
    return tuple(Q(a) * x for x in v)


def dot(a, b):
    return sum((Q(x) * Q(y) for x, y in zip(a, b)), Q(0))


# ------------------------------------------------------------ the target
def build_target(alpha=ALPHA):
    terminal = {**{f"eta{f}_constant": 1 for f in range(1, 6)},
                "eta1_U1": 1, "sigma_qpq22": -1}
    literal_c = {c: vec(**{f"private_{c}": -1, f"Eq_{c}": -1}) for c in CORNERS}
    JMv = vadd(*(vscale(-alpha[i], literal_c[c]) for i, c in enumerate(CORNERS)),
               vec(**terminal))
    residue_only = vec(**{f"R_{c}": alpha[i] for i, c in enumerate(CORNERS)})
    full = vadd(residue_only, vec(**terminal))
    return JMv, residue_only, full


# ------------------------------------------------------------ inventories
def build_inventories():
    inv = {}

    # F1  literal mapping-cone gate: the 20 committed old columns.
    f1 = []
    for c in CORNERS:
        r0 = vec(**{f"private_{c}": 1, f"Eq_{c}": 1, f"target_{c}": 1, "ainc": -1})
        f1 += [("r0_pq@" + c, r0),
               ("r0_pr@" + c, r0),                       # identical physical column
               ("T@" + c, vec(**{f"W_{c}": -1, f"target_{c}": 1})),
               ("rho@" + c, vec(**{f"W_{c}": 1, f"R_{c}": 1})),
               ("C_projected@" + c, vec(**{f"Eq_{c}": -1}))]
    inv["F1_mapping_cone_old_columns"] = f1

    # F2  KS standard transport graph: corner columns D_w+R_w and tail edges.
    f2 = [("stdcorner@" + c, vec(**{f"D_{c}": 1, f"R_{c}": 1})) for c in CORNERS]
    edges = (("P+q00", "P-q00"), ("P-q00", "P-q11"),
             ("P+q00", "P+q11"), ("P+q11", "P-q11"))
    d = dict(f2)
    for a, b in edges:
        f2.append((f"stdedge {a}->{b}",
                   vadd(d["stdcorner@" + b], vscale(-1, d["stdcorner@" + a]))))
    inv["F2_KS_standard_transport_graph"] = f2

    # F3  clean-separator typed inventory, projected to the physical rows
    #     (Omega/Q/ridge/chart forgotten) and placed at EVERY corner.  Dropping
    #     the auxiliary rows and allowing free corner placement is strictly
    #     more generous than any faithful corner resolution of those columns.
    f3 = []
    for c in CORNERS:
        f3 += [("endpoint_route@" + c, vec(**{f"R_{c}": 1})),
               ("pp_left_coarse@" + c, vec(**{f"R_{c}": 1})),
               ("pp_right_coarse@" + c, vec(**{f"R_{c}": -1})),
               ("pp_left_lifted@" + c, vec(**{f"R_{c}": 1})),
               ("pp_right_lifted@" + c, vec(**{f"R_{c}": -1})),
               ("normal_face@" + c, vec(**{f"Eq_{c}": -1})),
               ("old_r0@" + c, vec(**{f"Eq_{c}": 1, f"target_{c}": 1, "ainc": -1})),
               ("old_T@" + c, vec(**{f"W_{c}": -1, f"target_{c}": 1})),
               ("old_rho@" + c, vec(**{f"W_{c}": 1, f"R_{c}": 1})),
               ("matching_switch@" + c, vec()),
               ("tate_edge@" + c, vec())]
    inv["F3_clean_typed_inventory_projected"] = f3

    # F3f  FAITHFUL embedding of the same corner-FORGETTING families: each
    #      column enters once, with its readout spread equally over the four
    #      corners (the 9-row model only certifies the corner aggregate).
    #      Every such column is endpoint-EVEN by construction.
    def agg(**per_corner_rows):
        e = {}
        for k, val in per_corner_rows.items():
            for c in CORNERS:
                e[f"{k}_{c}"] = val
        return e

    f3f = [("endpoint_route_AGG", vec(**agg(R=1))),
           ("pp_left_coarse_AGG", vec(**agg(R=1))),
           ("pp_right_coarse_AGG", vec(**agg(R=-1))),
           ("pp_left_lifted_AGG", vec(**agg(R=1))),
           ("normal_face_AGG", vec(**agg(Eq=-1))),
           ("old_r0_AGG", vec(**agg(Eq=1, target=1), ainc=-1)),
           ("old_T_AGG", vec(**agg(W=-1, target=1))),
           ("old_rho_AGG", vec(**agg(W=1, R=1))),
           ("matching_switch_AGG", vec()),
           ("tate_edge_AGG", vec())]
    inv["F3f_clean_typed_inventory_FAITHFUL_aggregate"] = f3f

    # F4  endpoint-odd Cartan prism K=(1-s)H_w.  Its mixed boundary is exactly
    #     -delta on the four corners with D/W/target/anchor/pure-Eq zero.  NOT
    #     yet descended to the physical labelled source complex.
    inv["F4_endpoint_odd_cartan_prism"] = [
        ("cartan_prism_K", vec(**{f"R_{c}": ALPHA[i]
                                  for i, c in enumerate(CORNERS)}))]

    # F5  ULTRA over-generous closure: a free unit column on every non-private,
    #     non-terminal row.  This dominates every conceivable further
    #     source family whose readouts avoid private full-nine pivots and the
    #     eta/sigma terminal.
    f5 = []
    for c in CORNERS:
        for k in ("Eq", "W", "target", "R", "D"):
            f5.append((f"unit_{k}_{c}", vec(**{f"{k}_{c}": 1})))
    f5.append(("unit_ainc", vec(ainc=1)))
    inv["F5_ULTRA_free_units_on_nonprivate_nonterminal_rows"] = f5

    # X1 FABRICATED CONTROL: a bare private column with no physical readout.
    inv["X1_FABRICATED_bare_private"] = [
        (f"FAB_private_{c}", vec(**{f"private_{c}": 1})) for c in CORNERS]
    # X2 FABRICATED CONTROL: bare terminal columns.
    x2 = [(f"FAB_eta{f}", vec(**{f"eta{f}_constant": 1})) for f in range(1, 6)]
    x2 += [("FAB_eta1_U1", vec(eta1_U1=1)), ("FAB_sigma", vec(sigma_qpq22=1))]
    inv["X2_FABRICATED_bare_terminal"] = x2
    return inv


def describe(v):
    return {r: str(x) for r, x in zip(ROWS, v) if x}


def run_taskC():
    inv = build_inventories()
    JMv, residue_only, full = build_target()

    levels = [
        ("INV0 = F1 (note's committed columns)", ["F1_mapping_cone_old_columns"]),
        ("INV1 = F1+F2", ["F1_mapping_cone_old_columns",
                          "F2_KS_standard_transport_graph"]),
        ("INV2f = F1+F2+F3f (FAITHFUL corner-aggregate coarse families)",
         ["F1_mapping_cone_old_columns", "F2_KS_standard_transport_graph",
          "F3f_clean_typed_inventory_FAITHFUL_aggregate"]),
        ("INV3f = F1+F2+F3f+F4 (faithful + endpoint-odd Cartan prism)",
         ["F1_mapping_cone_old_columns", "F2_KS_standard_transport_graph",
          "F3f_clean_typed_inventory_FAITHFUL_aggregate",
          "F4_endpoint_odd_cartan_prism"]),
        ("INV2 = F1+F2+F3", ["F1_mapping_cone_old_columns",
                             "F2_KS_standard_transport_graph",
                             "F3_clean_typed_inventory_projected"]),
        ("INV3 = F1+F2+F3+F4 (adds Cartan prism)",
         ["F1_mapping_cone_old_columns", "F2_KS_standard_transport_graph",
          "F3_clean_typed_inventory_projected", "F4_endpoint_odd_cartan_prism"]),
        ("INV4 = ULTRA (INV3 + free units on all non-private non-terminal rows)",
         ["F1_mapping_cone_old_columns", "F2_KS_standard_transport_graph",
          "F3_clean_typed_inventory_projected", "F4_endpoint_odd_cartan_prism",
          "F5_ULTRA_free_units_on_nonprivate_nonterminal_rows"]),
        ("CTRL-A = ULTRA + fabricated bare private columns",
         ["F1_mapping_cone_old_columns", "F2_KS_standard_transport_graph",
          "F3_clean_typed_inventory_projected", "F4_endpoint_odd_cartan_prism",
          "F5_ULTRA_free_units_on_nonprivate_nonterminal_rows",
          "X1_FABRICATED_bare_private"]),
        ("CTRL-B = ULTRA + fabricated bare terminal columns",
         ["F1_mapping_cone_old_columns", "F2_KS_standard_transport_graph",
          "F3_clean_typed_inventory_projected", "F4_endpoint_odd_cartan_prism",
          "F5_ULTRA_free_units_on_nonprivate_nonterminal_rows",
          "X2_FABRICATED_bare_terminal"]),
        ("CTRL-C = everything incl. both fabrications",
         list(inv.keys())),
    ]

    note_sep = {c: vec(**{f"private_{c}": 1, f"W_{c}": -1,
                          f"target_{c}": -1, f"R_{c}": 1}) for c in CORNERS}

    results = []
    for name, keys in levels:
        cols = [v for k in keys for _n, v in inv[k]]
        names = [n for k in keys for n, _v in inv[k]]
        r = col_rank(cols, H)
        rec = {"inventory": name, "families": keys, "columns": len(cols),
               "rank": r}
        J_phys = list(JMv)
        for rr in ROWS:
            if rr.startswith("eta") or rr.startswith("sigma"):
                J_phys[RIDX[rr]] = Q(0)
        J_phys = tuple(J_phys)
        for tname, tvec in (("J(M_v)", JMv),
                            ("J(M_v)_physical_part_only", J_phys),
                            ("desired_residue_only", residue_only),
                            ("desired_full_fiber_target", full)):
            ok, coeff = membership(cols, tvec, H)
            entry = {"in_span": ok}
            if ok:
                entry["combination"] = {names[j]: str(coeff[j])
                                        for j in range(len(cols)) if coeff[j]}
                # EVERY signature row is verified, not only the nonzero ones.
                recon = [sum((coeff[j] * cols[j][i] for j in range(len(cols))),
                             Q(0)) for i in range(H)]
                entry["row_by_row_check"] = {
                    ROWS[i]: {"combination": str(recon[i]),
                              "target": str(tvec[i]),
                              "match": recon[i] == tvec[i]} for i in range(H)}
                entry["all_32_rows_match"] = all(
                    recon[i] == tvec[i] for i in range(H))
            rec[tname] = entry
        # separators
        ln = left_nullspace(cols, H)
        rec["left_null_dimension"] = len(ln)
        rec["left_null_support_rows"] = sorted({ROWS[i] for v in ln
                                                for i in range(H) if v[i]})
        sep = None
        for v in ln:
            if dot(v, JMv):
                sep = [x / dot(v, JMv) for x in v]
                break
        if sep is None and ln:
            # try combinations: the pairing map on ln
            vals = [dot(v, JMv) for v in ln]
            sep = None
        rec["separator_reading_1_on_J(M_v)"] = (
            describe(sep) if sep else "NONE (J(M_v) in span)")
        # does the note's primitive separator survive?
        rec["note_primitive_separator_status"] = {
            c: {"kills_every_column": all(dot(note_sep[c], col) == 0
                                          for col in cols),
                "value_on_J(M_v)": str(dot(note_sep[c], JMv))}
            for c in CORNERS}
        results.append(rec)

    OUT["taskC"] = {
        "row_model": list(ROWS),
        "J(M_v)": describe(JMv),
        "levels": results,
    }
    return inv, JMv, residue_only, full


# ------------------------------------------------------------ Task D
def run_taskD():
    tangent = load("computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
                   "probeD_tangent")

    def lower_labels(cut):
        cs = set(cut)
        out = []
        for mi, m in enumerate(tangent.MATCHINGS):
            if tangent.crosses_cut(m, cut):
                continue
            rep = tuple(e for e in m if set(e) <= cs)
            out.append((tuple(cut), mi, rep[0]))
        return tuple(out)

    base_cut, other_cut = tangent.CUTS[0], tangent.CUTS[5]
    ol, bl = lower_labels(other_cut), lower_labels(base_cut)
    key = lambda L: (L[1], L[2])
    shared = tuple(sorted(set(map(key, ol)) & set(map(key, bl))))

    # (1) the lower chain itself, read separately from each cut copy
    chain_defect = {}
    for p in shared:
        v024 = Q(1) if any(key(L) == p for L in ol) else Q(0)      # +1 on 024 cube
        v012 = Q(-1) if any(key(L) == p for L in bl) else Q(0)     # -1 on 012 cube
        chain_defect[str(p)] = {"value_from_024_cube": str(v024),
                                "value_from_012_cube": str(v012),
                                "defect_024_minus_012": str(v024 - v012),
                                "sum_descends_to": str(v024 + v012)}

    # (2) exact general characterisation: cutwise maps Phi_0,Phi_1 into any
    #     L descend iff Phi_1(e_p) - Phi_0(e_p) = 0 for the three shared p.
    #     Verify: the space of coherent maps k^18 -> k^1 has codimension 3.
    phys = tuple(sorted({key(L) for L in ol + bl}))
    pidx = {p: i for i, p in enumerate(phys)}
    dl = ol + bl
    F = [[Q(0)] * 18 for _ in range(15)]
    for j, L in enumerate(dl):
        F[pidx[key(L)]][j] = Q(1)
    chart = []
    for p in shared:
        v = [Q(0)] * 18
        v[next(j for j in range(9) if key(dl[j]) == p)] = Q(1)
        v[next(j for j in range(9, 18) if key(dl[j]) == p)] = Q(-1)
        chart.append(v)
    # scalar rows on k^18 that factor through F  <=>  annihilate chart
    coherent_rows = nullspace(chart, 18)
    pullback = [[F[i][j] for j in range(18)] for i in range(15)]
    codim = 18 - len(coherent_rows)
    same = (len(rref(coherent_rows)[0]) == len(rref(pullback)[0])
            == len(rref(coherent_rows + pullback)[0]) == 15)

    OUT["taskD"] = {
        "shared_labels_(matching_index, repeated_edge)":
            [[p[0], list(p[1])] for p in shared],
        "lower_chain_cutwise_readings": chain_defect,
        "coherent_scalar_row_space_dimension": len(coherent_rows),
        "codimension_of_coherence_condition": codim,
        "coherent_rows_equal_pullbacks_from_the_15_label_quotient": same,
        "constructor_availability": (
            "no committed checker exposes a cutwise filler Phi_0 / Phi_1 on the "
            "collision-label module, so the three equations cannot be evaluated "
            "on a real candidate filler; what is evaluated exactly here is (a) "
            "the signed lower chain itself and (b) the exact codimension-3 "
            "characterisation of the coherence condition"),
    }


# ------------------------------------------------------------ Task E
def run_taskE(inv, JMv, residue_only, full):
    muts = []

    # E1 mutate the lower chain: flip one sign in u -> J_col(u) != -v.
    tangent = load("computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
                   "probeE_tangent")

    def lower_labels(cut):
        cs = set(cut)
        return tuple((tuple(cut), mi, tuple(e for e in m if set(e) <= cs)[0])
                     for mi, m in enumerate(tangent.MATCHINGS)
                     if not tangent.crosses_cut(m, cut))

    ol, bl = lower_labels(tangent.CUTS[5]), lower_labels(tangent.CUTS[0])
    dl = ol + bl
    key = lambda L: (L[1], L[2])
    phys = tuple(sorted({key(L) for L in dl}))
    pidx = {p: i for i, p in enumerate(phys)}
    F = [[Q(0)] * 18 for _ in range(15)]
    for j, L in enumerate(dl):
        F[pidx[key(L)]][j] = Q(1)
    perms = [tangent.cut_permanent(c) for c in tangent.CUTS]
    minus_v = [-(Q(a) - Q(b)) for a, b in zip(perms[5], perms[0])]

    def shadow(lower_vec, permute=None):
        u = [sum((F[i][j] * lower_vec[j] for j in range(18)), Q(0))
             for i in range(15)]
        order = list(range(15))
        if permute:
            a, b = permute
            order[a], order[b] = order[b], order[a]
        s = [Q(0)] * 15
        for j, (mi, _e) in enumerate(phys):
            s[mi] += u[order[j]]
        return u, s

    honest = [Q(1)] * 9 + [Q(-1)] * 9
    u0, s0 = shadow(honest)
    muts.append({"mutation": "none (control)",
                 "u_support": sum(1 for x in u0 if x),
                 "J_col(u)==-v": s0 == minus_v, "expected": True})
    for flip in (0, 4, 9, 17):
        m = list(honest)
        m[flip] = -m[flip]
        u1, s1 = shadow(m)
        muts.append({"mutation": f"flip sign of lower-chain entry {flip}",
                     "u_support": sum(1 for x in u1 if x),
                     "J_col(u)==-v": s1 == minus_v, "expected": False})
    # Only label swaps that actually change the chain are informative: a swap
    # of two labels carrying equal coefficients is a null mutation.
    for a in range(15):
        for b in range(a + 1, 15):
            if u0[a] == u0[b]:
                continue
            _u2, s2 = shadow(honest, permute=(a, b))
            muts.append({
                "mutation": f"permute collision labels ({a},{b}) "
                            f"[u={u0[a]},{u0[b]}]",
                "J_col(u)==-v": s2 == minus_v, "expected": False})
    informative = [m for m in muts if m["mutation"].startswith("permute")]
    muts.append({"summary_of_informative_label_permutations": {
        "count": len(informative),
        "all_broke_the_identity": all(not m["J_col(u)==-v"]
                                      for m in informative),
        "null_swaps_excluded_(equal coefficients)":
            sum(1 for a in range(15) for b in range(a + 1, 15)
                if u0[a] == u0[b])}})

    # E2 mutate the target signature alpha and re-run the ULTRA membership.
    keys = ["F1_mapping_cone_old_columns", "F2_KS_standard_transport_graph",
            "F3_clean_typed_inventory_projected", "F4_endpoint_odd_cartan_prism",
            "F5_ULTRA_free_units_on_nonprivate_nonterminal_rows"]
    cols = [v for k in keys for _n, v in inv[k]]
    sig_muts = []
    for label, alpha in (("honest alpha=-delta=(-1,1,1,-1)", ALPHA),
                         ("MUTATED alpha=(1,1,1,-1)", (Q(1),) * 3 + (Q(-1),)),
                         ("MUTATED alpha=(0,0,0,0)", (Q(0),) * 4)):
        J, ro, fu = build_target(alpha)
        sig_muts.append({
            "alpha": label,
            "J(M_v)_in_ULTRA_span": membership(cols, J, H)[0],
            "residue_only_in_ULTRA_span": membership(cols, ro, H)[0],
        })
    # E3 strip the terminal rows from J(M_v): does it then enter the span?
    J_noterm = list(JMv)
    for r in ROWS:
        if r.startswith("eta") or r.startswith("sigma"):
            J_noterm[RIDX[r]] = Q(0)
    ok_nt, coeff_nt = membership(cols, tuple(J_noterm), H)
    names = [n for k in keys for n, _v in inv[k]]

    # E4 separator sensitivity: does the persistent separator depend on the
    #    endpoint-odd signature, or only on the terminal packet?
    sep = [Q(0)] * H
    sep[RIDX["eta1_constant"]] = Q(1)
    sens = []
    for label, alpha in (("honest alpha=-delta", ALPHA),
                         ("alpha=(1,1,1,-1)", (Q(1),) * 3 + (Q(-1),)),
                         ("alpha=0", (Q(0),) * 4)):
        J, _ro, _fu = build_target(alpha)
        sens.append({"alpha": label,
                     "terminal_separator_value_on_J(M_v)": str(dot(sep, J)),
                     "kills_every_ULTRA_column":
                         all(dot(sep, c) == 0 for c in cols)})
    # E5 zero the terminal packet inside J(M_v): the separator must then die.
    J_noterm_t = tuple(J_noterm)
    sens.append({"mutation": "terminal packet zeroed inside J(M_v)",
                 "terminal_separator_value_on_J(M_v)": str(dot(sep, J_noterm_t)),
                 "separator_still_detects": bool(dot(sep, J_noterm_t))})

    OUT["taskE"] = {
        "input_side_mutations": muts,
        "target_signature_mutations": sig_muts,
        "separator_sensitivity": sens,
        "J(M_v)_with_terminal_rows_zeroed_in_ULTRA_span": ok_nt,
        "that_combination": ({names[j]: str(coeff_nt[j])
                              for j in range(len(cols)) if coeff_nt[j]}
                             if ok_nt else None),
    }


if __name__ == "__main__":
    inv, JMv, ro, fu = run_taskC()
    run_taskD()
    run_taskE(inv, JMv, ro, fu)
    print(json.dumps(OUT, indent=1, sort_keys=False))
