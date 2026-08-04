#!/usr/bin/env python3
"""Reset-lane ordinary-residue descent lock (h=3).

Imports the committed machinery of
computations/verify_h3_full_hasse_koszul_cap_totalization.py (file digest
pinned below) and verifies, in exact Fraction arithmetic:

  S1  reconstruction on all fifteen (v,N) literal objects: top(N)=r_0-T,
      (d,tgt,ores)(n_I)=(Y*w,0,0), the kappa-normalized cap identity
      top(kappa(N-tau(H_m)Y*rho))=kappa(r_0-T-Y*rho) with ores=-kappa*Y,
      and the diagonal commutator [d,pi_top]N=(H_0-u)*eq.

  S2  the two per-face identities on all sixteen Hasse faces,
         [d,pi_U]N   = (1-delta_{U,empty}) * d_U(H_m) * (H_0-u) * eq,
         ores(pi_U Z)= -kappa*Y*d_U(H_m),
      and THEOREM D: every chain-map readout rho=sum_U g_U pi_U with
      arbitrary polynomial coefficients has ores(rho Z)=-kappa*Y*g_empty*H_m.

  S3  THEOREM E on the fifteen denominator columns: defect functional and
      ores functional coincide (checked on all twenty face/column pairs);
      rho is a chain map on column s iff ores(rho Z_s)=0; the -kappa*Y
      readout is attainable only with eq-defect (H_0-u)*eq.  Leak ledger:
      rank 12 over 22 monomials, one-edge leaks pairwise disjoint.

  S4  RESET-LANE LOCK: in the physical module (sum_c R r_c)+RT+R rho no
      element has (d,tgt,ores)=(kappa*Y*w,0,0) with kappa a unit.  Proof by
      extraction of the edge-degree-zero u-monomial: u occurs in F_0 alone
      with coefficient -1, and every hafnian row over all 3^8=6561
      colourings is a sum of exactly-four-edge monomials.  A fabricated
      module in which u occurs in two rows is exhibited and shown NOT to be
      killed by the same extraction, so the probe discriminates.

  S5  the prolonged escape kappa(s_I-T) exists upstairs, and NO R-linear
      chain map Lambda from the prolonged totalization to the committed
      physical module preserves target and ordinary residue, for ANY
      polynomial normalization Lambda(w) = c*w + q*e_Eq.  The scalar-only
      inference "transported boundary c*kappa*Y*w => c = 0" is FALSE for
      polynomial c: the counterexample c = H_m (the bottom Koszul cell) is
      exhibited and shown to pass the old extraction while dying on the
      transport constraints.  Transporting T forces eps(c) = 1 and
      transporting the escape forces eps(c) = 0 (eps = evaluation at
      edges = 0); the wider q-form dies via the rho-transport on the
      Y-free monomial -kappa*u.  Totalization note section 6 Option 1 is
      refuted for every comparison landing in the committed module; the
      reading whose codomain is an uncommitted "actual filtered source
      resolution" remains a scope caveat (note, section 9).

  S6  parity transport: the chart-odd object has zero w-boundary and zero
      ores; the cap target is chart-even; word-parity classification of the
      four reset tags.

  S7  indeterminacy: the second direct-free tag 12212 has the same top
      chain; the difference of the two descended objects has top face
      exactly zero and bottom face H_m-H_m' (180 monomials, vanishing at
      edges=0).

Hypothesis HYP-L (the syzygy coefficients are polynomial in the labelled
edge variables) and the audit flags A1/A2/CONV-1/CONV-2 scoping this
theorem are stated in notes/h3-reset-lane-ores-descent-lock.md.  The
checker freezes a sha256 ledger over the computed identity values (leak
polynomials, per-face derivatives, lock extraction coefficients), not over
booleans.
"""

from __future__ import annotations

import importlib.util
import io
import json
from contextlib import redirect_stdout
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path

Q = Fraction
HERE = Path(__file__).resolve().parent

COMMITTED_DIGESTS = {
    "verify_h3_full_hasse_koszul_cap_totalization.py":
        "51940ce0ac8387b68e7725508db6da1a1c055ea036335bbf19750580c69e13fb",
    "verify_h3_mixed_word_reset_cross_quotient_chain_lift_no_go.py":
        "2e59e0c6e434fa3afec5e0e8fcbfb19f6b8e9e6188dc7310e0daa994d8caa102",
    "verify_h3_reynolds_attach_coupled_obstruction.py":
        "c37ae0188febbde82196a297307b55d03833a2adee87a0e9f12733eef006110b",
}
REYNOLDS_CERTIFICATE_DIGEST = (
    "ee3699d5267fa63c896a50304f6548f565e6a09986fc5c54a9b6455928b3d5aa"
)
MIXED_WORD_CERTIFICATE_DIGEST = (
    "e6cdf0ba736f7444637967d4eeb18966cdc42ca721ea79d4cb2f5262bbaa8063"
)
EXPECTED_LEDGER_DIGEST = (
    "07a9b589df4b4708133c0849d64bf9e98d7d53d4a4aeeed2f6103a2a3945a828"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_fresh(filename, alias):
    """Fresh module instance per load: the imported checkers keep only pure
    lru_cache state (matchings), but a fresh instance per configuration
    guards against any hidden module-level chart state."""
    path = HERE / filename
    spec = importlib.util.spec_from_file_location(alias, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_digests():
    for filename, expected in COMMITTED_DIGESTS.items():
        digest = sha256((HERE / filename).read_bytes()).hexdigest()
        require(digest == expected,
                f"committed checker {filename} changed: digest {digest}")


def rerun_baseline(filename, alias, expected_digest):
    module = load_fresh(filename, alias)
    captured = io.StringIO()
    with redirect_stdout(captured):
        module.main()
    require(expected_digest in captured.getvalue(),
            f"baseline re-run of {filename} lost its certificate digest")


pin_digests()
tot = load_fresh("verify_h3_full_hasse_koszul_cap_totalization.py",
                 "reset_lock_tot")
tot_probe = load_fresh("verify_h3_full_hasse_koszul_cap_totalization.py",
                       "reset_lock_tot_probe")
require(tot_probe is not tot and tot_probe.H_MIXED == tot.H_MIXED,
        "totalization module is not reproducible across fresh loads")
require(not hasattr(tot, "SUPPORT_STABILIZER"),
        "unexpected module-level stabilizer state in totalization checker")

ONE, ZERO = tot.ONE, tot.ZERO
ODD, SITES = tot.ODD, tot.SITES
MIXED = tot.MIXED
MIXED2 = (0, 1, 2, 2, 1, 2, 2, 2)          # odd part 12212
X, R_, P, QSITE = tot.X, tot.R, tot.P, tot.QSITE
H_MIXED, H_PURE, F_PURE = tot.H_MIXED, tot.H_PURE, tot.F_PURE
CAP_Y, KAPPA, HOM_U = tot.CAP_Y, tot.KAPPA, tot.HOMOGENIZING_U
U_ITEM = ("homogenizing", "u")

add, scale, multiply = tot.add, tot.scale, tot.multiply
constant, variable = tot.constant, tot.variable
derivative, translate = tot.derivative, tot.translate
module_add = tot.module_add
module_multiply = tot.module_multiply
module_coefficient = tot.module_coefficient
module_external_face = tot.module_external_face
apply_module_map = tot.apply_module_map


def eps(name):
    return ("eps", name)


EPS_U, EPS_T, EPS_E, EPS_F = eps("u"), eps("t"), eps("e"), eps("f")
ALL_EPS = (EPS_U, EPS_T, EPS_E, EPS_F)

DIFFERENTIAL_ORIG = {
    "r_0": {"eq": F_PURE},
    "r_m": {"eq": H_MIXED},
    "T": {"w": scale(-ONE, CAP_Y)},
    "rho": {"w": constant()},
}
TARGET = {"r_0": {"target": constant()}, "r_m": {},
          "T": {"target": constant()}, "rho": {}}
ORES = {"r_0": {}, "r_m": {}, "T": {}, "rho": {"ores": constant()}}
ORES_FABRICATED = {"r_0": {}, "r_m": {}, "T": {"ores": constant()},
                   "rho": {"ores": constant()}}

LEDGER = {"committed_digests": COMMITTED_DIGESTS,
          "baseline_certificates": [REYNOLDS_CERTIFICATE_DIGEST,
                                    MIXED_WORD_CERTIFICATE_DIGEST]}


def face(deleted):
    return tuple(site for site in ODD if site != deleted)


def row_for_word(word):
    return tot.polynomial_from_matching(SITES, dict(enumerate(word)))


def face_hafnian_for(word, deleted):
    colouring = {site: word[site] for site in face(deleted)}
    return tot.polynomial_from_matching(face(deleted), colouring,
                                        direct_free=False)


def endpoint_variables_for(word, deleted):
    return (tot.edge(X, deleted, word[X], word[deleted]),
            tot.edge(P, QSITE, word[P], word[QSITE]))


def internal_variables_for(word, matching):
    return tuple(tot.edge(a, b, word[a], word[b]) for a, b in matching)


def directions_for(word, deleted, matching):
    marked_u, marked_t = endpoint_variables_for(word, deleted)
    internal = internal_variables_for(word, matching)
    return {marked_u: EPS_U, marked_t: EPS_T,
            internal[0]: EPS_E, internal[1]: EPS_F}


def totalization(word, deleted, matching):
    """N = tau(H_m)(r_0-T) - tau(H_0-u) r_m with its structural data."""
    directions = directions_for(word, deleted, matching)
    hm = row_for_word(word)
    tau_hm = translate(hm, directions)
    tau_f0 = translate(F_PURE, directions)
    require(tau_f0 == F_PURE, "pure row moved under mixed Hasse directions")
    chain = {"r_0": tau_hm, "r_m": scale(-ONE, F_PURE),
             "T": scale(-ONE, tau_hm)}
    differential = {
        "r_0": {"eq": tau_f0},
        "r_m": {"eq": tau_hm},
        "T": {"w": scale(-ONE, CAP_Y)},
        "rho": {"w": constant()},
    }
    boundary = apply_module_map(chain, differential)
    require(boundary == {"w": multiply(tau_hm, CAP_Y)},
            "dN is not tau(H_m)*Y*w")
    require(not apply_module_map(chain, TARGET), "N retained target")
    require(not apply_module_map(chain, ORES), "N retained ordinary residue")
    response = module_multiply(
        KAPPA, module_add(chain, {"rho": scale(-ONE,
                                               multiply(tau_hm, CAP_Y))}))
    require(not apply_module_map(response, differential),
            "response chain Z is not closed")
    require(not apply_module_map(response, TARGET), "Z retained target")
    require(apply_module_map(response, ORES) ==
            {"ores": scale(-ONE, multiply(KAPPA, multiply(tau_hm, CAP_Y)))},
            "Z has the wrong totalized ordinary residue")
    return dict(directions=directions, tau_hm=tau_hm, chain=chain,
                boundary=boundary, response=response)


def serialize(polynomial):
    items = sorted(polynomial.items(),
                   key=lambda kv: (len(kv[0]), str(kv[0])))
    return [[[list(item) for item in term], str(coefficient)]
            for term, coefficient in items]


def face_label(subset):
    return "".join(item[1] for item in subset) or "1"


def base_variables(directions, subset):
    return tuple(key for key, value in directions.items() if value in subset)


def matrix_rank(matrix):
    work = [list(row) for row in matrix]
    rank = 0
    for column in range(len(work[0]) if work else 0):
        pivot = next((row for row in range(rank, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = work[rank][column]
        work[rank] = [entry / inverse for entry in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][column]:
                factor = work[row][column]
                work[row] = [entry - factor * pivot_entry
                             for entry, pivot_entry
                             in zip(work[row], work[rank])]
        rank += 1
    return rank


def evaluate_edges_zero(polynomial):
    return {term: coefficient for term, coefficient in polynomial.items()
            if not any(item[0] == "w" for item in term)}


def u_part(polynomial):
    """Edge-degree-zero part containing the homogenizing variable u."""
    return {term: coefficient
            for term, coefficient in evaluate_edges_zero(polynomial).items()
            if any(item[0] == "homogenizing" for item in term)}


def readout(g_coefficients, chain, boundary, all_epsilons,
            differential):
    total = {}
    total_boundary = {}
    for subset, g in g_coefficients.items():
        piece = module_coefficient(chain, subset, all_epsilons)
        total = module_add(total, module_multiply(g, piece))
        piece_boundary = module_coefficient(boundary, subset, all_epsilons)
        for key, polynomial in piece_boundary.items():
            total_boundary[key] = add(total_boundary.get(key, {}),
                                      multiply(g, polynomial))
    total_boundary = {key: polynomial
                      for key, polynomial in total_boundary.items()
                      if polynomial}
    image = apply_module_map(total, differential)
    defect = {key: add(image.get(key, {}),
                       scale(-ONE, total_boundary.get(key, {})))
              for key in set(image) | set(total_boundary)}
    return total, {key: polynomial for key, polynomial in defect.items()
                   if polynomial}


# ==========================================================================
# S0  sanity of the committed model
# ==========================================================================

def stage0():
    require(len(H_MIXED) == len(H_PURE) == 90, "direct-free row size changed")
    require(MIXED == (0, 1, 2, 1, 1, 2, 2, 2), "committed mixed word changed")
    require(all(len(term) == 4 and all(item[0] == "w" for item in term)
                for term in H_MIXED),
            "H_m is not a sum of exactly-four-edge monomials")
    require(all(len(term) == 4 and all(item[0] == "w" for item in term)
                for term in H_PURE),
            "H_0 is not a sum of exactly-four-edge monomials")
    require(F_PURE.get((U_ITEM,)) == -ONE,
            "the u-monomial coefficient in F_0 is not -1")
    require(all(term == (U_ITEM,) or
                (len(term) == 4 and all(item[0] == "w" for item in term))
                for term in F_PURE),
            "F_0 has a monomial other than -u and four-edge terms")
    rerun_baseline("verify_h3_reynolds_attach_coupled_obstruction.py",
                   "reset_lock_reynolds", REYNOLDS_CERTIFICATE_DIGEST)
    rerun_baseline(
        "verify_h3_mixed_word_reset_cross_quotient_chain_lift_no_go.py",
        "reset_lock_mixed_word", MIXED_WORD_CERTIFICATE_DIGEST)


# ==========================================================================
# S1  reconstruction on all fifteen (v, N)
# ==========================================================================

def stage1():
    fifteen = [(deleted, matching) for deleted in ODD
               for matching in tot.matchings(face(deleted))]
    require(len(fifteen) == 15, "fifteen objects are five faces x 3 matchings")
    for deleted, matching in fifteen:
        data = totalization(MIXED, deleted, matching)
        top = module_coefficient(data["chain"], ALL_EPS, ALL_EPS)
        require(top == {"r_0": constant(), "T": constant(-ONE)},
                f"top of N is not r_0-T at (v={deleted}, N={matching})")
        require(module_coefficient(data["boundary"], ALL_EPS, ALL_EPS)
                == {"w": CAP_Y}, "top boundary of N is not Y*w")
        require(not apply_module_map(top, TARGET), "tgt(n_I) is not zero")
        require(not apply_module_map(top, ORES), "ores(n_I) is not zero")
        # discrimination probes: the typing requires can fail.
        fabricated_top = {"r_0": constant()}
        require("w" not in apply_module_map(fabricated_top,
                                            DIFFERENTIAL_ORIG),
                "dropping T from the top chain still produced a w-boundary")
        require(apply_module_map(fabricated_top, TARGET)
                == {"target": constant()},
                "target probe cannot see the fabricated top chain")
        require(apply_module_map(top, ORES_FABRICATED)
                == {"ores": constant(-ONE)},
                "ores probe cannot distinguish a fabricated ores map")
        top_response = module_coefficient(data["response"], ALL_EPS, ALL_EPS)
        require(top_response == {"r_0": KAPPA, "T": scale(-ONE, KAPPA),
                                 "rho": scale(-ONE, multiply(KAPPA, CAP_Y))},
                "top response cycle is not kappa*(r_0-T-Y*rho)")
        top_ores = apply_module_map(top_response, ORES)
        require(top_ores == {"ores": scale(-ONE, multiply(KAPPA, CAP_Y))}
                and top_ores["ores"],
                "top response ores is not the nonzero value -kappa*Y")
        # diagonal commutator (11a) under the ORIGINAL differential.
        projected = apply_module_map(top, DIFFERENTIAL_ORIG)
        require(projected == {"eq": F_PURE, "w": CAP_Y} and F_PURE,
                "[d, pi_top]N is not the nonzero defect (H_0-u)*eq")
    data0 = totalization(MIXED, fifteen[0][0], fifteen[0][1])
    top_last = module_coefficient(data0["chain"], ALL_EPS, ALL_EPS)
    LEDGER["top_chain"] = {generator: serialize(polynomial)
                           for generator, polynomial in top_last.items()}
    LEDGER["reconstruction_objects"] = len(fifteen)
    return fifteen, data0


# ==========================================================================
# S2  per-face identities and THEOREM D
# ==========================================================================

def stage2(data0):
    directions = data0["directions"]
    per_face = {}
    for subset in tot.subsets(ALL_EPS):
        piece = module_coefficient(data0["chain"], subset, ALL_EPS)
        piece_boundary = module_coefficient(data0["boundary"], subset,
                                            ALL_EPS)
        image = apply_module_map(piece, DIFFERENTIAL_ORIG)
        defect = {key: add(image.get(key, {}),
                           scale(-ONE, piece_boundary.get(key, {})))
                  for key in set(image) | set(piece_boundary)}
        defect = {key: polynomial for key, polynomial in defect.items()
                  if polynomial}
        du_hm = derivative(H_MIXED, base_variables(directions, subset))
        require(du_hm, f"d_U(H_m) vanished at U={face_label(subset)}; "
                       "the per-face identity would be vacuous")
        predicted = {} if not subset else {"eq": multiply(du_hm, F_PURE)}
        require(defect == predicted,
                f"per-face commutator mismatch at U={face_label(subset)}")
        if subset:
            require(defect, "nonempty-face defect unexpectedly vanished")
        piece_response = module_coefficient(data0["response"], subset,
                                            ALL_EPS)
        ores_value = apply_module_map(piece_response, ORES)
        require(ores_value ==
                {"ores": scale(-ONE, multiply(KAPPA,
                                              multiply(du_hm, CAP_Y)))}
                and ores_value["ores"],
                f"per-face ores mismatch at U={face_label(subset)}")
        per_face[face_label(subset)] = serialize(du_hm)
    LEDGER["per_face_dU_Hm"] = per_face

    # THEOREM D on arbitrary polynomial readout coefficients.
    edge_a = sorted(H_MIXED)[0][0]
    edge_b = sorted(H_MIXED)[1][1]
    probes = {
        "probe_A": {
            (): constant(2),
            (EPS_U,): variable(edge_a),
            (EPS_T, EPS_E): add(constant(-ONE), HOM_U),
            ALL_EPS: multiply(KAPPA, variable(edge_b)),
        },
        "probe_B": {subset: constant(index + 1)
                    for index, subset
                    in enumerate(tot.subsets(ALL_EPS))},
    }
    for name, g_coefficients in probes.items():
        proper = {}
        for subset, g in g_coefficients.items():
            if subset:
                du_hm = derivative(H_MIXED,
                                   base_variables(directions, subset))
                proper = add(proper, multiply(g, du_hm))
        require(proper, f"{name}: the proper-face functional is zero, "
                        "so the identity test would be vacuous")
        total, defect = readout(g_coefficients, data0["chain"],
                                data0["boundary"], ALL_EPS,
                                DIFFERENTIAL_ORIG)
        require(defect == {"eq": multiply(proper, F_PURE)},
                f"{name}: Theorem D defect functional mismatch")
        response_total, _ = readout(g_coefficients, data0["response"],
                                    data0["boundary"], ALL_EPS,
                                    DIFFERENTIAL_ORIG)
        full = add(multiply(g_coefficients.get((), {}), H_MIXED), proper)
        require(apply_module_map(response_total, ORES) ==
                {"ores": scale(-ONE, multiply(KAPPA,
                                              multiply(full, CAP_Y)))},
                f"{name}: Theorem D ores functional mismatch")

    # certificate 1: the Koszul syzygy readout is a chain map with ores 0.
    base_ut = base_variables(directions, (EPS_U, EPS_T))
    base_ef = base_variables(directions, (EPS_E, EPS_F))
    g_koszul = {(EPS_U, EPS_T): derivative(H_MIXED, base_ef),
                (EPS_E, EPS_F): scale(-ONE, derivative(H_MIXED, base_ut))}
    _, defect = readout(g_koszul, data0["chain"], data0["boundary"],
                        ALL_EPS, DIFFERENTIAL_ORIG)
    require(not defect, "Koszul syzygy readout is not a chain map")
    response_total, _ = readout(g_koszul, data0["response"],
                                data0["boundary"], ALL_EPS,
                                DIFFERENTIAL_ORIG)
    require(not apply_module_map(response_total, ORES),
            "Koszul syzygy readout has nonzero ores")
    # certificate 2: the top readout is not a chain map.
    g_top = {(EPS_E, EPS_F): constant()}
    _, defect_top = readout(g_top, data0["chain"], data0["boundary"],
                            ALL_EPS, DIFFERENTIAL_ORIG)
    require(defect_top ==
            {"eq": multiply(derivative(H_MIXED, base_ef), F_PURE)}
            and defect_top,
            "top readout lost its nonzero eq defect")
    # certificate 3: the bottom readout is the algebra retraction.
    g_bottom = {(): constant()}
    bottom, defect_bottom = readout(g_bottom, data0["chain"],
                                    data0["boundary"], ALL_EPS,
                                    DIFFERENTIAL_ORIG)
    require(not defect_bottom, "bottom readout is not a chain map")
    require(bottom == {"r_0": H_MIXED, "r_m": scale(-ONE, F_PURE),
                       "T": scale(-ONE, H_MIXED)},
            "bottom face is not the physical Koszul cell")
    response_bottom, _ = readout(g_bottom, data0["response"],
                                 data0["boundary"], ALL_EPS,
                                 DIFFERENTIAL_ORIG)
    bottom_ores = apply_module_map(response_bottom, ORES)
    require(bottom_ores ==
            {"ores": scale(-ONE, multiply(KAPPA,
                                          multiply(H_MIXED, CAP_Y)))},
            "bottom readout ores is not -kappa*Y*H_m")
    LEDGER["theorem_d_bottom_ores"] = serialize(bottom_ores["ores"])


# ==========================================================================
# S3  fifteen denominator columns, THEOREM E, leak ledger
# ==========================================================================

def stage3(fifteen, data0):
    h_site = {site: face_hafnian_for(MIXED, site) for site in ODD}
    for site in ODD:
        require(len(h_site[site]) == 3,
                f"h_{site} is not a three-term face hafnian")
    columns = [(site, colour) for site in ODD for colour in (0, 1, 2)]
    require(len(columns) == 15, "denominator column count changed")
    selected = [(site, colour) for site, colour in columns
                if colour == MIXED[site]]
    require(len(selected) == 5, "selected denominator column count changed")

    # 5/3/3/1 ladder for every (v, N).
    ladder_records = []
    for deleted, matching in fifteen:
        internal = internal_variables_for(MIXED, matching)
        counts = []
        for subset in tot.subsets((EPS_E, EPS_F)):
            base = tuple(variable_key for variable_key, epsilon
                         in {internal[0]: EPS_E,
                             internal[1]: EPS_F}.items()
                         if epsilon in subset)
            support = [site for site in ODD
                       if derivative(h_site[site], base)]
            counts.append(len(support))
            if subset == (EPS_E, EPS_F):
                require(support == [deleted],
                        f"top denominator support is not Kronecker at "
                        f"v={deleted}")
        require(counts == [5, 3, 3, 1],
                f"denominator ladder is not 5,3,3,1 at (v={deleted})")
        ladder_records.append([deleted, list(map(list, matching)), counts])
    LEDGER["ladder"] = ladder_records

    # per-column, per-face identities and THEOREM E.
    internal = internal_variables_for(MIXED, fifteen[0][1])
    internal_directions = {internal[0]: EPS_E, internal[1]: EPS_F}
    internal_eps = (EPS_E, EPS_F)
    leak_entries = []
    for site in ODD:
        marked_u, marked_t = endpoint_variables_for(MIXED, site)
        site_directions = {marked_u: eps("su"), marked_t: eps("st"),
                           internal[0]: EPS_E, internal[1]: EPS_F}
        tau = translate(row_for_word(MIXED), site_directions)
        chain = {"r_0": tau, "r_m": scale(-ONE, F_PURE),
                 "T": scale(-ONE, tau)}
        differential = {"r_0": {"eq": F_PURE}, "r_m": {"eq": tau},
                        "T": {"w": scale(-ONE, CAP_Y)},
                        "rho": {"w": constant()}}
        boundary = apply_module_map(chain, differential)
        require(boundary == {"w": multiply(tau, CAP_Y)},
                f"site totalization boundary changed at s={site}")
        external = (eps("su"), eps("st"))
        phi = module_external_face(chain, external)
        phi_boundary = module_external_face(boundary, external)
        tau_h = translate(h_site[site], internal_directions)
        require(phi == {"r_0": tau_h, "T": scale(-ONE, tau_h)},
                f"Phi_s is not tau(h_s)*(r_0-T) at s={site}")
        require(phi_boundary == {"w": multiply(tau_h, CAP_Y)},
                f"Phi_s boundary is not tau(h_s)*Y*w at s={site}")
        require(not apply_module_map(phi, TARGET),
                f"Phi_s retained target at s={site}")
        require(not apply_module_map(phi, ORES),
                f"Phi_s retained ordinary residue at s={site}")
        z_column = module_multiply(
            KAPPA, module_add(phi, {"rho": scale(-ONE,
                                                 multiply(tau_h, CAP_Y))}))
        for subset in tot.subsets(internal_eps):
            piece = module_coefficient(phi, subset, internal_eps)
            piece_boundary = module_coefficient(phi_boundary, subset,
                                                internal_eps)
            image = apply_module_map(piece, DIFFERENTIAL_ORIG)
            defect = {key: add(image.get(key, {}),
                               scale(-ONE, piece_boundary.get(key, {})))
                      for key in set(image) | set(piece_boundary)}
            defect = {key: polynomial
                      for key, polynomial in defect.items() if polynomial}
            base = base_variables(internal_directions, subset)
            du_h = derivative(h_site[site], base)
            predicted = {} if not du_h else {"eq": multiply(du_h, F_PURE)}
            require(defect == predicted,
                    f"column commutator mismatch at s={site}, "
                    f"U={face_label(subset)}")
            if not subset:
                require(defect,
                        f"bottom-face column defect vanished at s={site}; "
                        "the r_m compensator reappeared")
            piece_response = module_coefficient(z_column, subset,
                                                internal_eps)
            ores_value = apply_module_map(piece_response, ORES)
            predicted_ores = ({} if not du_h else
                              {"ores": scale(-ONE,
                                             multiply(KAPPA,
                                                      multiply(du_h,
                                                               CAP_Y)))})
            require(ores_value == predicted_ores,
                    f"column ores mismatch at s={site}, "
                    f"U={face_label(subset)}")
            leak_entries.append([face_label(subset), site, MIXED[site],
                                 serialize(du_h)])

        # THEOREM E functional identity on arbitrary coefficients, and the
        # chain-map <=> ores=0 equivalence, both ways.
        g_probe = {(): constant(), (EPS_E,): variable(sorted(H_MIXED)[0][0]),
                   (EPS_F,): constant(-2), (EPS_E, EPS_F): HOM_U}
        functional = {}
        for subset, g in g_probe.items():
            base = base_variables(internal_directions, subset)
            functional = add(functional,
                             multiply(g, derivative(h_site[site], base)))
        require(functional, f"Theorem E probe functional vanished at "
                            f"s={site}")
        _, defect = readout(g_probe, phi, phi_boundary, internal_eps,
                            DIFFERENTIAL_ORIG)
        require(defect == {"eq": multiply(functional, F_PURE)},
                f"Theorem E defect functional mismatch at s={site}")
        response_total, _ = readout(g_probe, z_column, phi_boundary,
                                    internal_eps, DIFFERENTIAL_ORIG)
        require(apply_module_map(response_total, ORES) ==
                {"ores": scale(-ONE, multiply(KAPPA,
                                              multiply(functional,
                                                       CAP_Y)))},
                f"Theorem E ores functional mismatch at s={site}")
        # zero functional <=> chain map with zero ores (nonzero g).
        base_e = base_variables(internal_directions, (EPS_E,))
        g_zero = {(): derivative(h_site[site], base_e),
                  (EPS_E,): scale(-ONE, h_site[site])}
        zero_functional = add(
            multiply(g_zero[()], h_site[site]),
            multiply(g_zero[(EPS_E,)],
                     derivative(h_site[site], base_e)))
        require(not zero_functional,
                f"Theorem E zero-functional witness failed at s={site}")
        _, defect_zero = readout(g_zero, phi, phi_boundary, internal_eps,
                                 DIFFERENTIAL_ORIG)
        require(not defect_zero,
                f"zero-functional readout is not a chain map at s={site}")
        response_zero, _ = readout(g_zero, z_column, phi_boundary,
                                   internal_eps, DIFFERENTIAL_ORIG)
        require(not apply_module_map(response_zero, ORES),
                f"zero-functional readout has nonzero ores at s={site}")

    # the -kappa*Y readout on the Kronecker column carries exactly the
    # eq-defect (H_0-u)*eq.
    kronecker = fifteen[0][0]
    marked_u, marked_t = endpoint_variables_for(MIXED, kronecker)
    site_directions = {marked_u: eps("su"), marked_t: eps("st"),
                       internal[0]: EPS_E, internal[1]: EPS_F}
    tau = translate(row_for_word(MIXED), site_directions)
    chain = {"r_0": tau, "r_m": scale(-ONE, F_PURE), "T": scale(-ONE, tau)}
    boundary = apply_module_map(chain, {"r_0": {"eq": F_PURE},
                                        "r_m": {"eq": tau},
                                        "T": {"w": scale(-ONE, CAP_Y)},
                                        "rho": {"w": constant()}})
    phi = module_external_face(chain, (eps("su"), eps("st")))
    phi_boundary = module_external_face(boundary, (eps("su"), eps("st")))
    tau_h = translate(h_site[kronecker], internal_directions)
    z_column = module_multiply(
        KAPPA, module_add(phi, {"rho": scale(-ONE,
                                             multiply(tau_h, CAP_Y))}))
    g_top = {(EPS_E, EPS_F): constant()}
    _, defect_top = readout(g_top, phi, phi_boundary, internal_eps,
                            DIFFERENTIAL_ORIG)
    require(defect_top == {"eq": F_PURE},
            "the -kappa*Y readout does not carry the exact eq-defect "
            "(H_0-u)*eq")
    response_top, _ = readout(g_top, z_column, phi_boundary, internal_eps,
                              DIFFERENTIAL_ORIG)
    top_ores = apply_module_map(response_top, ORES)
    require(top_ores == {"ores": scale(-ONE, multiply(KAPPA, CAP_Y))}
            and top_ores["ores"],
            "the Kronecker-column readout lost its -kappa*Y residue")

    # leak ledger: rank and pairwise-disjoint one-edge leaks.
    require(len(leak_entries) == 20,
            "leak ledger does not have twenty face/column pairs")
    monomial_polynomials = []
    for subset in tot.subsets(internal_eps):
        base = base_variables(internal_directions, subset)
        for site in ODD:
            monomial_polynomials.append(derivative(h_site[site], base))
    monomials = sorted({term for polynomial in monomial_polynomials
                        for term in polynomial}, key=str)
    matrix = [[polynomial.get(term, ZERO) for term in monomials]
              for polynomial in monomial_polynomials]
    rank = matrix_rank(matrix)
    require(rank == 12 and len(monomials) == 22,
            f"leak matrix invariants changed: rank {rank} over "
            f"{len(monomials)} monomials")
    for one_edge in ((EPS_E,), (EPS_F,)):
        base = base_variables(internal_directions, one_edge)
        supports = [frozenset(derivative(h_site[site], base))
                    for site in ODD if derivative(h_site[site], base)]
        require(len(supports) == 3 and
                all(not (left & right)
                    for index, left in enumerate(supports)
                    for right in supports[index + 1:]),
                "one-edge leaks are not pairwise disjoint; a signed "
                "cancellation became possible")
    LEDGER["leak_ledger"] = leak_entries
    LEDGER["leak_rank"] = rank
    LEDGER["leak_monomial_count"] = len(monomials)
    return h_site


# ==========================================================================
# S4  the reset-lane lock
# ==========================================================================

def stage4():
    homogeneous_rows = 0
    for word in product((0, 1, 2), repeat=8):
        row = row_for_word(word)
        require(all(len(term) == 4 and all(item[0] == "w" for item in term)
                    for term in row),
                f"hafnian row at word {word} is not edge-degree-4 "
                "homogeneous")
        homogeneous_rows += 1
    require(homogeneous_rows == 6561, "colouring census changed")
    require(evaluate_edges_zero(F_PURE) == scale(-ONE, HOM_U),
            "F_0 at edges=0 is not -u")
    require(evaluate_edges_zero(H_MIXED) == {},
            "H_m does not vanish at edges=0")

    # positive extraction probe: the u-functional sees only the F_0 term.
    edge_a = sorted(H_MIXED)[0][0]
    sample = add(constant(3), HOM_U, variable(edge_a))
    require(u_part(multiply(sample, H_PURE)) == {},
            "u-extraction saw a hafnian row H_0 contribution")
    require(u_part(multiply(sample, H_MIXED)) == {},
            "u-extraction saw a hafnian row H_m contribution")
    product_f0 = multiply(sample, F_PURE)
    require(product_f0.get((U_ITEM,)) == Q(-3),
            "u-extraction lost the -(constant term) functional on F_0")
    extraction = u_part(multiply(KAPPA, F_PURE))
    require(extraction == scale(-ONE, multiply(KAPPA, HOM_U))
            and extraction,
            "the lock extraction -kappa*u vanished; kappa is no longer "
            "forced to zero")

    # discrimination probe: a fabricated module with u in TWO rows is NOT
    # killed by the same extraction, so the probe genuinely depends on the
    # verified uniqueness of u in F_0.
    fabricated_row = add(H_MIXED, HOM_U)          # declared tgt = 0
    fabricated_sum = add(multiply(KAPPA, F_PURE),
                         multiply(KAPPA, fabricated_row))
    require(u_part(fabricated_sum) == {},
            "fabricated two-u module was killed by the extraction; the "
            "lock probe does not discriminate")
    require(evaluate_edges_zero(fabricated_row) == HOM_U,
            "fabricated row does not violate the committed convention "
            "F_alpha|_{edges=0} = -tgt(g_alpha)*u")

    # the committed convention on the two physical rows.
    require(evaluate_edges_zero(F_PURE) == scale(-ONE, HOM_U)
            and evaluate_edges_zero(H_MIXED) == {},
            "committed convention F_alpha|_0 = -tgt(g_alpha)*u failed")
    # cap/residue bookkeeping of the lock: b=0, a=-kappa, A_0=kappa.
    require(apply_module_map({"T": scale(-ONE, KAPPA)},
                             DIFFERENTIAL_ORIG)
            == {"w": multiply(KAPPA, CAP_Y)},
            "cap coefficient a=-kappa does not produce kappa*Y*w")
    require(apply_module_map({"r_0": KAPPA, "T": scale(-ONE, KAPPA)},
                             TARGET) == {},
            "A_0=kappa does not cancel the target of a=-kappa")
    # the localized escape divides by the source equation itself.
    require(() not in H_MIXED and H_MIXED,
            "H_m became a unit; the localized escape would be polynomial")
    # and H_m does not divide H_0-u in the polynomial ring: every monomial
    # of any polynomial multiple of H_m has edge-degree >= 4 (sample
    # multiple computed), while F_0 contains -u at edge-degree 0.
    sample_multiple = multiply(add(constant(), HOM_U, KAPPA), H_MIXED)
    require(all(sum(1 for item in term if item[0] == "w") >= 4
                for term in sample_multiple)
            and any(sum(1 for item in term if item[0] == "w") == 0
                    for term in F_PURE),
            "H_m divides H_0-u: the localized escape "
            "A_m=-kappa*(H_0-u)/H_m would be polynomial")
    LEDGER["lock"] = {
        "rows_checked": homogeneous_rows,
        "edge_degree": 4,
        "u_coefficient_in_F0": str(F_PURE[(U_ITEM,)]),
        "F0_at_edges_zero": serialize(evaluate_edges_zero(F_PURE)),
        "extraction_of_kappa_F0": serialize(extraction),
        "fabricated_two_u_extraction": serialize(u_part(fabricated_sum)),
    }


# ==========================================================================
# S5  prolonged escape and comparison refutation
# ==========================================================================

def stage5(data0):
    ordered = tuple(data0["directions"])
    cycle = tot.indexed_top_koszul_cycle(ordered)
    require(not tot.indexed_hasse_chain_differential(cycle, ordered),
            "prolonged Koszul cycle s_I is not closed")
    require(len(cycle) == 17, "prolonged cycle term count changed")
    require(cycle.get(("r_0", 0)) == constant(),
            "the target-carrying coefficient of s_I is not the unit")
    # kappa*(s_I - T) upstairs: boundary kappa*Y*w, tgt 0, ores 0.
    escape = {key: multiply(KAPPA, coefficient)
              for key, coefficient in cycle.items()}
    escape["T"] = scale(-ONE, KAPPA)
    indexed_part = {key: value for key, value in escape.items()
                    if isinstance(key, tuple)}
    boundary = tot.indexed_hasse_chain_differential(indexed_part, ordered)
    boundary = module_add(boundary,
                          {"w": multiply(escape["T"],
                                         scale(-ONE, CAP_Y))})
    require(boundary == {"w": multiply(KAPPA, CAP_Y)},
            "kappa*(s_I-T) does not have boundary kappa*Y*w upstairs")
    target_value = add(escape[("r_0", 0)], escape["T"])
    require(target_value == {},
            "kappa*(s_I-T) retained target upstairs")

    # --- physical-module bookkeeping on generic symbolic coefficients ---
    # For n = A_0 r_0 + A_m r_m + a T + b rho:
    #   dn = (A_0 F_0 + A_m H_m) e_Eq + (-aY+b) w, tgt(n)=A_0+a, ores(n)=b.
    sym_a0 = variable(("sym", "A0"))
    sym_am = variable(("sym", "Am"))
    sym_a = variable(("sym", "a"))
    sym_b = variable(("sym", "b"))
    generic = {"r_0": sym_a0, "r_m": sym_am, "T": sym_a, "rho": sym_b}
    require(apply_module_map(generic, DIFFERENTIAL_ORIG) ==
            {"eq": add(multiply(sym_a0, F_PURE), multiply(sym_am, H_MIXED)),
             "w": add(scale(-ONE, multiply(sym_a, CAP_Y)), sym_b)},
            "generic physical boundary is not (A0*F0+Am*Hm)*eq+(-a*Y+b)*w")
    require(apply_module_map(generic, TARGET) ==
            {"target": add(sym_a0, sym_a)},
            "generic physical target is not A0+a")
    require(apply_module_map(generic, ORES) == {"ores": sym_b},
            "generic physical ordinary residue is not b")

    # --- eps = evaluation at edges=0 is a ring homomorphism, so the
    # extraction is valid for ARBITRARY polynomial coefficients ---
    probe_left = add(constant(2), variable(sorted(H_MIXED)[0][0]), HOM_U)
    probe_right = add(KAPPA, CAP_Y, variable(sorted(H_MIXED)[1][1]))
    require(evaluate_edges_zero(multiply(probe_left, probe_right)) ==
            multiply(evaluate_edges_zero(probe_left),
                     evaluate_edges_zero(probe_right)),
            "edges=0 evaluation is not multiplicative")
    require(evaluate_edges_zero(add(probe_left, probe_right)) ==
            add(evaluate_edges_zero(probe_left),
                evaluate_edges_zero(probe_right)),
            "edges=0 evaluation is not additive")

    # --- the scalar-only inference is FALSE for polynomial c ---
    # counterexample c = H_m: the bottom Koszul cell kappa*pi_empty(N) is a
    # physical element with (d,tgt,ores) = (c*kappa*Y*w, 0, 0).
    counterexample = {"r_0": multiply(KAPPA, H_MIXED),
                      "r_m": scale(-ONE, multiply(KAPPA, F_PURE)),
                      "T": scale(-ONE, multiply(KAPPA, H_MIXED))}
    require(apply_module_map(counterexample, DIFFERENTIAL_ORIG) ==
            {"w": multiply(multiply(H_MIXED, KAPPA), CAP_Y)},
            "the c=H_m counterexample lost its boundary c*kappa*Y*w")
    require(not apply_module_map(counterexample, TARGET)
            and not apply_module_map(counterexample, ORES),
            "the c=H_m counterexample is not invisible")
    require(H_MIXED and evaluate_edges_zero(multiply(H_MIXED, KAPPA)) == {},
            "the c=H_m counterexample no longer passes the old scalar-only "
            "extraction; the lock now sees polynomial c, which it cannot")
    # the transport constraint kills it: the T-transport forces eps(c)=1,
    # while eps(H_m)=0.
    require(evaluate_edges_zero(H_MIXED) != constant(),
            "the T-transport constraint eps(c)=1 fails to kill the c=H_m "
            "counterexample")

    # --- (i) T-transport, Lambda(w)=c*w: forces eps(c)=1 ---
    # Lambda(T) has ores 0 => b=0; w-component of d Lambda(T) = -c*Y*w
    # gives Y*(a-c)=0 => a=c (domain); eq-component zero gives, under the
    # u-extraction with a GENERIC coefficient, eps(A_0)=0; the edges=0
    # part of tgt(Lambda T)=1 (legitimate: 1, the target values, and
    # kappa are edge-free) then gives eps(c) = 1 - eps(A_0) = 1.
    alpha = variable(("sym", "eps_A0"))
    require(u_part(multiply(alpha, F_PURE)) ==
            scale(-ONE, multiply(alpha, HOM_U))
            and u_part(multiply(alpha, F_PURE)),
            "generic u-extraction lost the -eps(A0)*u functional on F_0")
    require(u_part(multiply(alpha, H_MIXED)) == {},
            "generic u-extraction saw the u-free row H_m")
    require(multiply(CAP_Y, sym_a) != {} and multiply(CAP_Y, KAPPA) != {},
            "Y annihilated a nonzero polynomial; Y*(a-c)=0 no longer "
            "forces a=c")
    forced_by_t_transport = constant()          # eps(c) = 1
    # --- (ii) escape transport, Lambda(w)=c*w: forces eps(c)*kappa=0 ---
    # b=0; a=-c*kappa; tgt gives A_0=c*kappa; eq-extraction gives
    # eps(A_0)=0, i.e. eps(c)*kappa=0.  Substituting the T-forced value:
    require(multiply(forced_by_t_transport, KAPPA) == KAPPA and KAPPA,
            "substituting the T-forced eps(c)=1 into the escape-forced "
            "eps(c)*kappa=0 no longer leaves the contradiction kappa=0")

    # --- (iii) wider normalization Lambda(w) = c*w + q*e_Eq ---
    # rho-transport: ores(Lambda rho)=1 => b=1, and -aY+b=c gives
    # eps(c) = 1 - eps(a)*Y.  The escape transport's eq-line u-extraction
    # gives -eps(c)*kappa*u = kappa*Y*eps(q).  Substituting, the residual
    # must vanish, but its Y-free part is the nonzero monomial -kappa*u:
    # kappa*u = Y*(eps(a)*kappa*u - kappa*eps(q)) is impossible.
    eps_a = variable(("sym", "eps_a"))
    eps_q = variable(("sym", "eps_q"))
    eps_c = add(constant(), scale(-ONE, multiply(eps_a, CAP_Y)))
    lhs = scale(-ONE, multiply(eps_c, multiply(KAPPA, HOM_U)))
    rhs = multiply(KAPPA, multiply(CAP_Y, eps_q))
    residual = add(lhs, scale(-ONE, rhs))
    y_free_residual = {term: coefficient
                       for term, coefficient in residual.items()
                       if not any(item[0] == "cap" for item in term)}
    require(y_free_residual == scale(-ONE, multiply(KAPPA, HOM_U))
            and y_free_residual,
            "wider normalization Lambda(w)=c*w+q*eq escaped: the Y-free "
            "monomial -kappa*u of the extraction identity vanished")
    # discrimination probe: dropping the rho-transport pin (the Y-free
    # part of eps(c) being 1) makes the extraction identity solvable, so
    # the rho-transport is load-bearing.
    unpinned_c = multiply(eps_a, CAP_Y)
    lhs_unpinned = scale(-ONE, multiply(unpinned_c,
                                        multiply(KAPPA, HOM_U)))
    rhs_unpinned = multiply(KAPPA,
                            multiply(CAP_Y,
                                     scale(-ONE, multiply(eps_a, HOM_U))))
    require(add(lhs_unpinned, scale(-ONE, rhs_unpinned)) == {},
            "dropping the rho-transport no longer admits a solution; the "
            "load-bearing constraint has been misattributed")
    LEDGER["prolonged_escape_terms"] = len(cycle)
    LEDGER["comparison_counterexample_boundary"] = serialize(
        apply_module_map(counterexample, DIFFERENTIAL_ORIG)["w"])
    LEDGER["comparison_y_free_residual"] = serialize(y_free_residual)


# ==========================================================================
# S6  parity transport
# ==========================================================================

def stage6(data0):
    tau_hm = data0["tau_hm"]
    chart_differential = {
        "r_0_pq": {"eq": F_PURE}, "r_m_pq": {"eq": tau_hm},
        "r_0_pr": {"eq": F_PURE}, "r_m_pr": {"eq": tau_hm},
        "T": {"w": scale(-ONE, CAP_Y)}, "rho": {"w": constant()},
    }
    chart_ores = {"r_0_pq": {}, "r_m_pq": {}, "r_0_pr": {}, "r_m_pr": {},
                  "T": {}, "rho": {"ores": constant()}}
    n_pq = {"r_0_pq": tau_hm, "r_m_pq": scale(-ONE, F_PURE),
            "T": scale(-ONE, tau_hm)}
    n_pr = {"r_0_pr": tau_hm, "r_m_pr": scale(-ONE, F_PURE),
            "T": scale(-ONE, tau_hm)}
    n_odd = module_add(n_pq, tot.module_scale(-ONE, n_pr))
    n_even = module_add(n_pq, n_pr)
    require("T" not in n_odd and "rho" not in n_odd,
            "chart-odd part has a cap component")
    odd_boundary = apply_module_map(n_odd, chart_differential)
    require(not odd_boundary, "chart-odd part has a nonzero boundary")
    require(not apply_module_map(n_odd, chart_ores),
            "chart-odd part has nonzero ordinary residue")
    even_boundary = apply_module_map(n_even, chart_differential)
    require(even_boundary ==
            {"w": scale(2, multiply(tau_hm, CAP_Y))} and even_boundary,
            "chart-even part lost its nonzero cap boundary 2*tau(H_m)*Y*w")
    require(n_even.get("T") == scale(-2, tau_hm),
            "chart-even cap coefficient is not -2*tau(H_m)")
    bottom_even = module_coefficient(n_even, (), ALL_EPS)
    require(bottom_even.get("T") == scale(-2, H_MIXED),
            "chart-even bottom cap coefficient is not -2*H_m")

    word_parity = {}
    for tag in ("12112", "12212", "02012", "22012"):
        total = sum(int(character) for character in tag)
        word_parity[tag] = [total, "odd" if total % 2 else "even"]
    require(word_parity["12112"][1] == "odd"
            and word_parity["22012"][1] == "odd"
            and word_parity["02012"][1] == "odd"
            and word_parity["12212"][1] == "even",
            "word-parity classification of the reset tags changed")
    pure_odd = tuple(tot.PURE[site] for site in ODD)
    require(sum(pure_odd) % 2 == 0, "Y_0 word parity changed")
    LEDGER["chart_parity"] = {
        "odd_boundary": {key: serialize(value)
                         for key, value in odd_boundary.items()},
        "even_boundary_w": serialize(even_boundary["w"]),
    }
    LEDGER["word_parity"] = word_parity


# ==========================================================================
# S7  indeterminacy: the second direct-free tag
# ==========================================================================

def stage7(fifteen, data0):
    second_row = row_for_word(MIXED2)
    require(len(second_row) == 90, "second-tag row size changed")
    for deleted, matching in fifteen:
        marked = endpoint_variables_for(MIXED2, deleted)
        internal = internal_variables_for(MIXED2, matching)
        top = derivative(second_row, marked + internal)
        require(top == constant(),
                f"second-tag top derivative is not the unit at "
                f"(v={deleted}, N={matching})")
    directions2 = directions_for(MIXED2, fifteen[0][0], fifteen[0][1])
    census = {}
    for subset in tot.subsets(ALL_EPS):
        first = derivative(H_MIXED,
                           base_variables(data0["directions"], subset))
        second = derivative(second_row,
                            base_variables(directions2, subset))
        delta = add(first, scale(-ONE, second))
        if delta:
            census[face_label(subset)] = len(delta)
    require("utef" not in census, "top-face difference is not zero")
    delta_bottom = add(H_MIXED, scale(-ONE, second_row))
    require(delta_bottom and len(delta_bottom) == 180,
            "bottom-face difference H_m - H_m' changed")
    require(evaluate_edges_zero(delta_bottom) == {},
            "H_m - H_m' does not vanish at edges=0")
    LEDGER["second_tag"] = "".join(str(colour) for colour in MIXED2)
    LEDGER["difference_face_census"] = census
    LEDGER["difference_bottom"] = serialize(delta_bottom)


def main():
    stage0()
    fifteen, data0 = stage1()
    stage2(data0)
    stage3(fifteen, data0)
    stage4()
    stage5(data0)
    stage6(data0)
    stage7(fifteen, data0)

    # self-integrity: the imported machinery was not mutated during the run.
    tot_check = load_fresh("verify_h3_full_hasse_koszul_cap_totalization.py",
                           "reset_lock_tot_check")
    require(tot_check.H_MIXED == H_MIXED and tot_check.F_PURE == F_PURE,
            "imported totalization state drifted during the run")

    payload = json.dumps(LEDGER, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_DIGEST,
                f"computed ledger digest changed: {digest}")
    print("h=3 reset-lane ordinary-residue descent lock: PASS")
    print("reconstruction on all 15 (v,N): top r_0-T, (d,tgt,ores)=(Y*w,0,0)")
    print("all 16 faces: [d,pi_U]N=d_U(H_m)*(H_0-u)*eq, "
          "ores(pi_U Z)=-kappa*Y*d_U(H_m)")
    print("THEOREM D: chain-map readout => ores = -kappa*Y*g_empty*H_m")
    print("THEOREM E (20 face/column pairs): defect functional == ores "
          "functional; chain map <=> ores=0")
    print("leak ledger: rank 12 over 22 monomials, one-edge leaks disjoint")
    print("RESET-LANE LOCK: no bounded source chain has (kappa*Y*w,0,0); "
          "u-monomial extraction over all 6561 rows")
    print("comparison refutation: no tgt/ores-preserving chain map onto the "
          "committed module for any Lambda(w)=c*w+q*eq")
    print("  (scalar-only c=0 inference is false: c=H_m counterexample "
          "exhibited; note sec. 6 Option 1 refuted for committed codomain)")
    print("parity: chart-odd object capless and boundaryless; cap target "
          "chart-even; word parity mixes for 12112/22012/02012")
    print("second tag 12212: same top chain; difference top face zero, "
          "bottom face 180 monomials")
    print(f"ledger sha256 {digest}")


if __name__ == "__main__":
    main()
