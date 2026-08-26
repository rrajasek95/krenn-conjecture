#!/usr/bin/env python3
r"""REPAIR PROBE (item 2a): DERIVE the ridge terminal (eta_z, sigma) packet.

UNAUDITED.  Pinned to krenn-conjecture HEAD 7d57c552a3ef57d3a95c3bc933af547ad55e087d.

The committed checker
``computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py``
*stipulates* the two terminal contractions

    eta_z(-Omega_v) = 1 + delta_(vz) * u_z / t,      sigma(-Omega_v) = -q_pq^22

as strings, and then "derives" the ridge -Omega_v = -a+t+b-u by solving a 4x4
system whose right-hand side is those very values.  That is a backwards solve:
nothing in the repo ever applies a physically defined derivation to a
physically defined Omega_v and *computes* the two answers.

This script does exactly that, forward and exactly:

  (1) Omega_v is rebuilt from the literal colour-bar prism boundary (two pq
      colour-square paths and one xv interval), independently of any eta/sigma
      datum, and cross-checked against the committed module
      verify_h3_rootless_five_ridge_response_bianchi_cokernel.py.

  (2) eta_z and sigma are rebuilt as colour-diagonal GHZ-stabilizer tangents:

        eta_z = X_mu / t,   mu = {(p,0): +1, (z,0): -1}          (z = 1..5)
        sigma = X_lambda,   lambda = {(p,2): +1, (x,2): -1}

      Both weight fields are re-verified to be literal infinitesimal
      stabilizers of all three GHZ targets (every colour sum vanishes).  The
      action on a decorated coordinate is the logarithmic-derivative rule
      already committed in
      verify_h3_rootless_clean_c5_separator_endpoint_kernel_boundary.py:

        X_mu(q_(s,s')^(c,c')) = (mu(s,c) + mu(s',c')) * q_(s,s')^(c,c').

  (3) eta_z(-Omega_v) and sigma(-Omega_v) are computed in the exact Laurent
      ring Q[q^{+-1}] and compared to the stipulated constants and to the
      committed TERMINAL_ROWS packet of
      verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py.

The ledger hashes the *computed Laurent polynomials*, not booleans.
Mutation controls at the bottom must all FAIL.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import importlib.util
import json
from pathlib import Path
import sys


REPO = Path(__file__).resolve().parents[2]
PINNED_HEAD = "7d57c552a3ef57d3a95c3bc933af547ad55e087d"

# Content pins on every committed file whose *definitions* are reused here.
PINS = {
    "computations/verify_h3_rootless_clean_c5_separator_endpoint_kernel_boundary.py":
        "a98c6e0e90127e81e869c68342f3999abbbd8898d2b2eeafbeccbad06575a324",
    "computations/verify_h3_rootless_five_ridge_response_bianchi_cokernel.py":
        "14f177a31544659cbeeeeb72f0e1db95185d715dd11a95e7ff4a9a3bc83b510c",
    "computations/verify_h3_rootless_clean_c5_formal_F_full_jacobian_boundary.py":
        "1c17b29f1179416d57acbb2daada0d1f34ee5a69e5f3a68bd6827da0858363e3",
    "computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py":
        "aea73ce5ff6ce183245d209393ed60192066d38eab7d4d203caa0c82cc5b16d6",
    "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py":
        "b890195a8fc0c4e90c9c9c0c03c41a95690228c81026f4c2ea1fa95908564e38",
    "computations/verify_h3_rootless_eta_character_source_interface.py":
        "2357e1a4e1c22c4496d99be12b8bf49deea3838337743ea849da29757508517c",
}

SITES = tuple(range(8))
COLOURS = (0, 1, 2)
X, P, QSITE = 0, 6, 7
ODD = (1, 2, 3, 4, 5)
# MIXED middle colour of each odd face; identical to MIDDLE/MIXED in the repo.
MIDDLE = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(
        name, REPO / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


# ---------------------------------------------------------------- coordinates

def coord(left, right, left_colour, right_colour):
    """A decorated q coordinate, normalized so the site pair is increasing."""
    if left < right:
        return (left, right, left_colour, right_colour)
    return (right, left, right_colour, left_colour)


T = coord(P, QSITE, 0, 0)                       # t   = q_pq^00
A = coord(P, QSITE, 2, 2)                       # a   = q_pq^22
U = {v: coord(X, v, 0, 0) for v in ODD}         # u_v = q_xv^00
B = {v: coord(X, v, 0, MIDDLE[v]) for v in ODD}  # b_v = q_xv^(0,m_v)


def name(c):
    return "q_(%d,%d)^(%d,%d)" % c


# ------------------------------------------------- exact Laurent polynomials
# A monomial is a frozen sorted tuple of (coordinate, exponent) with nonzero
# exponents; a polynomial is {monomial: Fraction}.

def monomial(*pairs):
    exponents = {}
    for c, e in pairs:
        exponents[c] = exponents.get(c, 0) + e
    return tuple(sorted((c, e) for c, e in exponents.items() if e))


ONE_MONOMIAL = monomial()


def poly(*terms):
    answer = {}
    for coefficient, mono in terms:
        answer[mono] = answer.get(mono, Q(0)) + Q(coefficient)
    return {m: c for m, c in answer.items() if c}


def padd(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for mono, coefficient in polynomial.items():
            answer[mono] = answer.get(mono, Q(0)) + coefficient
    return {m: c for m, c in answer.items() if c}


def pscale(value, polynomial):
    value = Q(value)
    if not value:
        return {}
    return {m: value * c for m, c in polynomial.items()}


def pmul_monomial(polynomial, mono):
    answer = {}
    for other, coefficient in polynomial.items():
        product = monomial(*(list(other) + list(mono)))
        answer[product] = answer.get(product, Q(0)) + coefficient
    return {m: c for m, c in answer.items() if c}


def render(polynomial):
    """Canonical printable/hashable form of a Laurent polynomial."""
    parts = []
    for mono, coefficient in sorted(polynomial.items()):
        factors = "*".join(
            name(c) if e == 1 else "%s^%d" % (name(c), e) for c, e in mono)
        parts.append([str(coefficient), factors or "1"])
    return parts


# --------------------------------------------------------- stabilizer fields

def check_ghz_stabilizer(weights):
    """A colour-diagonal weight field is an infinitesimal GHZ stabilizer iff
    every colour's site weights sum to zero (all three GHZ targets fixed)."""
    sums = {}
    for colour in COLOURS:
        sums[colour] = sum(weights.get((site, colour), 0) for site in SITES)
    require(all(value == 0 for value in sums.values()),
            ("not a GHZ stabilizer", weights, sums))
    return sums


def weight_of(weights, c):
    """Logarithmic weight w_e with X_mu(q_e) = w_e * q_e."""
    left, right, left_colour, right_colour = c
    return (weights.get((left, left_colour), 0)
            + weights.get((right, right_colour), 0))


def derivation(weights, polynomial):
    """X_mu applied to a Laurent polynomial (a derivation, so monomialwise)."""
    answer = {}
    for mono, coefficient in polynomial.items():
        factor = sum(exponent * weight_of(weights, c) for c, exponent in mono)
        if factor:
            answer[mono] = answer.get(mono, Q(0)) + factor * coefficient
    return {m: c for m, c in answer.items() if c}


def eta_weights(z):
    require(z in ODD, ("auxiliary must be an odd site", z))
    return {(P, 0): 1, (z, 0): -1}


SIGMA_WEIGHTS = {(P, 2): 1, (X, 2): -1}


def eta(z, polynomial):
    """eta_z = X_mu / t, the normalization with eta_z(t) = 1."""
    return pmul_monomial(derivation(eta_weights(z), polynomial),
                         monomial((T, -1)))


def sigma(polynomial):
    """sigma = X_lambda, unnormalized (this is the repo's convention: it must
    read -q_pq^22 rather than -q_pq^22/t)."""
    return derivation(SIGMA_WEIGHTS, polynomial)


# ------------------------------------------------------ the ridge Omega_v

def edge_boundary(left, right):
    """Oriented interval from left to right, as in the committed module."""
    return poly((1, monomial((right, 1))), (-1, monomial((left, 1))))


def build_omega(v):
    """Rebuild Omega_v from the literal colour-bar prism, exactly as
    verify_h3_rootless_five_ridge_response_bianchi_cokernel.endpoint_ridge_paths
    does, but with no reference to any eta/sigma value."""
    t22 = coord(P, QSITE, 2, 2)
    t02 = coord(P, QSITE, 0, 2)
    t20 = coord(P, QSITE, 2, 0)
    t00 = coord(P, QSITE, 0, 0)
    first_p = padd(edge_boundary(t22, t02), edge_boundary(t02, t00))
    first_q = padd(edge_boundary(t22, t20), edge_boundary(t20, t00))
    require(first_p == first_q, ("pq colour-square paths disagree", v))
    require(first_p == poly((1, monomial((t00, 1))), (-1, monomial((t22, 1)))),
            "pq square boundary changed")
    xv = edge_boundary(B[v], U[v])
    correction = padd(first_p, pscale(-1, xv))
    omega = poly((1, monomial((A, 1))), (-1, monomial((T, 1))),
                 (-1, monomial((B[v], 1))), (1, monomial((U[v], 1))))
    require(correction == pscale(-1, omega),
            ("endpoint prism stopped repairing Omega", v))
    return omega


def cross_check_omega_against_repo(omegas):
    module = load(
        "computations/verify_h3_rootless_five_ridge_response_bianchi_cokernel.py",
        "repair23_bianchi")
    records = module.endpoint_ridge_paths()
    translate = {
        "pq:22": A, "pq:00": T,
        **{f"x{v}:0{MIDDLE[v]}": B[v] for v in ODD},
        **{f"x{v}:00": U[v] for v in ODD},
    }
    for record in records:
        v = record["v"]
        rebuilt = poly(*((coefficient, monomial((translate[basis], 1)))
                         for basis, coefficient in record["omega"].items()))
        require(rebuilt == omegas[v],
                ("committed Omega_v disagrees with the rebuild", v))
    return [record["v"] for record in records]


# ------------------------------------------------------------- the derivation

def stipulated_eta(v, z):
    """1 + delta_(vz) * u_z / t, as an exact Laurent polynomial."""
    terms = [(1, ONE_MONOMIAL)]
    if v == z:
        terms.append((1, monomial((U[z], 1), (T, -1))))
    return poly(*terms)


STIPULATED_SIGMA = poly((-1, monomial((A, 1))))


def derive_terminal_table(omegas):
    table = {}
    for v in ODD:
        minus_omega = pscale(-1, omegas[v])
        for z in ODD:
            table[(v, z)] = eta(z, minus_omega)
        table[(v, "sigma")] = sigma(minus_omega)
    return table


def compare_with_stipulation(table):
    mismatches = []
    for v in ODD:
        for z in ODD:
            if table[(v, z)] != stipulated_eta(v, z):
                mismatches.append(("eta", v, z, render(table[(v, z)]),
                                   render(stipulated_eta(v, z))))
        if table[(v, "sigma")] != STIPULATED_SIGMA:
            mismatches.append(("sigma", v, render(table[(v, "sigma")]),
                               render(STIPULATED_SIGMA)))
    return mismatches


# ------------------------------- the committed 7-row terminal packet (v = 1)

def derived_terminal_vector(table, literal):
    """Read the committed TERMINAL_ROWS off the derived Laurent values.

    TERMINAL_ROWS = (eta1_constant..eta5_constant, eta1_U1, sigma_qpq22).
    The row `etaZ_constant` is the coefficient of the empty monomial in
    eta_z(-Omega_1); `eta1_U1` is the coefficient of u_1/t in eta_1(-Omega_1);
    `sigma_qpq22` is the coefficient of q_pq^22 in sigma(-Omega_1).
    """
    entries = {}
    for z in ODD:
        value = table[(1, z)]
        entries[f"eta{z}_constant"] = value.get(ONE_MONOMIAL, Q(0))
    entries["eta1_U1"] = table[(1, 1)].get(monomial((U[1], 1), (T, -1)), Q(0))
    entries["sigma_qpq22"] = table[(1, "sigma")].get(monomial((A, 1)), Q(0))

    # Nothing else may be present in the derived values on the v = 1 face:
    # the terminal readout must be exhaustive, not a projection that discards
    # unmodelled monomials.
    leftovers = []
    for z in ODD:
        allowed = {ONE_MONOMIAL, monomial((U[1], 1), (T, -1))}
        for mono in table[(1, z)]:
            if mono not in allowed:
                leftovers.append(("eta", z, render({mono: table[(1, z)][mono]})))
    for mono in table[(1, "sigma")]:
        if mono != monomial((A, 1)):
            leftovers.append(("sigma", render({mono: table[(1, "sigma")][mono]})))
    require(not leftovers, ("derived terminal has unmodelled monomials",
                            leftovers))

    vector = literal.vector(**{row: entries[row] for row in literal.TERMINAL_ROWS})
    return entries, vector


# ------------------------------------ invariance of the old source inventory

def companion_matchings():
    """The fifteen labelled all-derivation companions q_(v,N)."""
    answer = []
    for v in ODD:
        face = tuple(site for site in ODD if site != v)
        first = face[0]
        for partner in face[1:]:
            rest = tuple(site for site in face if site not in (first, partner))
            matching = (coord(first, partner, MIDDLE[first], MIDDLE[partner]),
                        coord(rest[0], rest[1], MIDDLE[rest[0]],
                              MIDDLE[rest[1]]))
            answer.append((v, matching))
    require(len(answer) == 15, "companion census changed")
    return answer


CLEAN_C5 = tuple(coord(left, right, MIDDLE[left], MIDDLE[right])
                 for left, right in ((1, 2), (2, 3), (3, 4), (4, 5), (1, 5)))


def old_inventory_invariance():
    """Every clean-C5 cell and every companion monomial is killed by all five
    eta_z and by sigma.  This is what makes the terminal rows of -O_alpha zero,
    i.e. what makes K the *only* carrier of the terminal packet."""
    records = {"clean_c5": {}, "companions": {}}
    for c in CLEAN_C5:
        weights = {"sigma": weight_of(SIGMA_WEIGHTS, c)}
        for z in ODD:
            weights[f"eta{z}"] = weight_of(eta_weights(z), c)
        require(set(weights.values()) == {0},
                ("a clean-C5 cell moved", name(c), weights))
        records["clean_c5"][name(c)] = weights
    for v, matching in companion_matchings():
        for c in matching:
            weights = {"sigma": weight_of(SIGMA_WEIGHTS, c)}
            for z in ODD:
                weights[f"eta{z}"] = weight_of(eta_weights(z), c)
            require(set(weights.values()) == {0},
                    ("a companion cell moved", v, name(c), weights))
        records["companions"][f"v{v}:" + "|".join(name(c) for c in matching)] = 0
    return records


def compensation_identity(omegas):
    """Cross-check against verify_h3_rootless_eta_cyclic_compensation_boundary
    and verify_h3_residual_q_eta_one_cell_fiber_product_gate: Omega_v + c_v
    with c_v = t - u_v is eta-invariant and sigma-moves by +q_pq^22."""
    records = []
    for v in ODD:
        c_v = poly((1, monomial((T, 1))), (-1, monomial((U[v], 1))))
        total = padd(omegas[v], c_v)
        require(total == poly((1, monomial((A, 1))),
                              (-1, monomial((B[v], 1)))),
                ("Omega_v + c_v changed", v))
        for z in ODD:
            require(eta(z, total) == {},
                    ("Omega_v + c_v is not eta-invariant", v, z))
            require(eta(z, c_v) == stipulated_eta(v, z) if v == z
                    else eta(z, c_v) == poly((1, ONE_MONOMIAL)),
                    ("eta_z(c_v) changed", v, z))
        require(sigma(total) == poly((1, monomial((A, 1)))),
                ("sigma(Omega_v + c_v) changed", v))
        require(sigma(c_v) == {}, ("c_v acquired a sigma response", v))
        records.append({"v": v, "eta_z(Omega_v+c_v)": 0,
                        "sigma(Omega_v+c_v)": "+q_pq^22"})
    return records


# ------------------------------------------------------------------ controls

def mutation_controls(omegas):
    """Each mutation must break the derived terminal packet.  A control that
    passes would prove the derivation is insensitive to that datum."""
    results = []

    def broken(label, fn):
        try:
            fn()
        except RuntimeError as error:
            results.append({"mutation": label, "detected": True,
                            "error": str(error)[:120]})
            return
        results.append({"mutation": label, "detected": False})

    def flip_eta_sign():
        weights = {(P, 0): -1, (1, 0): 1}
        check_ghz_stabilizer(weights)
        value = pmul_monomial(derivation(weights, pscale(-1, omegas[1])),
                              monomial((T, -1)))
        require(value == stipulated_eta(1, 1), "M1 detected")

    def drop_t_normalization():
        value = derivation(eta_weights(1), pscale(-1, omegas[1]))
        require(value == stipulated_eta(1, 1), "M2 detected")

    def wrong_sigma_colour():
        weights = {(P, 0): 1, (X, 0): -1}
        check_ghz_stabilizer(weights)
        value = derivation(weights, pscale(-1, omegas[1]))
        require(value == STIPULATED_SIGMA, "M3 detected")

    def perturb_ridge():
        mutated = padd(omegas[1], poly((1, monomial((U[1], 1)))))
        require(eta(1, pscale(-1, mutated)) == stipulated_eta(1, 1),
                "M4 detected")

    def swap_middle_colour():
        bad = coord(X, 1, 0, 0)  # replace b_1 by u_1: kills the b/u distinction
        mutated = poly((1, monomial((A, 1))), (-1, monomial((T, 1))),
                       (-1, monomial((bad, 1))), (1, monomial((U[1], 1))))
        require(eta(1, pscale(-1, mutated)) == stipulated_eta(1, 1)
                and sigma(pscale(-1, mutated)) == STIPULATED_SIGMA,
                "M5 detected")

    def non_stabilizer_field():
        weights = {(P, 0): 1}
        check_ghz_stabilizer(weights)
        results.append({"mutation": "M6", "detected": False})

    broken("M1 eta weight signs flipped", flip_eta_sign)
    broken("M2 eta not normalized by t", drop_t_normalization)
    broken("M3 sigma placed on colour 0", wrong_sigma_colour)
    broken("M4 ridge perturbed by +u_1", perturb_ridge)
    broken("M5 mixed endpoint cell b_1 collapsed to u_1", swap_middle_colour)
    broken("M6 non-GHZ weight field rejected", non_stabilizer_field)
    return results


# ---------------------------------------------------------------------- main

def audit():
    pin_report = {}
    for relative, expected in PINS.items():
        actual = sha256((REPO / relative).read_bytes()).hexdigest()
        pin_report[relative] = actual
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual))

    eta_stabilizer_check = {str(z): check_ghz_stabilizer(eta_weights(z))
                            for z in ODD}
    sigma_stabilizer_check = check_ghz_stabilizer(SIGMA_WEIGHTS)

    omegas = {v: build_omega(v) for v in ODD}
    checked = cross_check_omega_against_repo(omegas)
    require(checked == list(ODD), "committed Omega_v census changed")

    table = derive_terminal_table(omegas)
    mismatches = compare_with_stipulation(table)

    literal = load(
        "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py",
        "repair23_literal")
    entries, vector = derived_terminal_vector(table, literal)

    committed_packet = {
        **{f"eta{face}_constant": Q(1) for face in range(1, 6)},
        "eta1_U1": Q(1),
        "sigma_qpq22": Q(-1),
    }
    packet_match = all(entries[row] == committed_packet[row]
                       for row in literal.TERMINAL_ROWS)

    ridge = load(
        "computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py",
        "repair23_ridge")
    ridge_ledger = ridge.audit()
    stipulated_strings = (
        ridge_ledger["terminal_ridge_uniqueness"]["eta_contraction"],
        ridge_ledger["terminal_ridge_uniqueness"]["sigma_contraction"],
        ridge_ledger["terminal_ridge_uniqueness"]["unique_ridge"],
    )

    return {
        "pinned_head": PINNED_HEAD,
        "pins": pin_report,
        "eta_field": "eta_z = X_mu/t,  mu = {(p,0):+1, (z,0):-1}",
        "sigma_field": "sigma = X_lambda,  lambda = {(p,2):+1, (x,2):-1}",
        "eta_ghz_colour_sums": eta_stabilizer_check,
        "sigma_ghz_colour_sums": sigma_stabilizer_check,
        "omega_rebuilt_from": (
            "two pq colour-square bar paths minus one xv interval; agrees "
            "with verify_h3_rootless_five_ridge_response_bianchi_cokernel"),
        "omega": {str(v): render(omegas[v]) for v in ODD},
        "derived_eta_table": {
            "%d,%d" % (v, z): render(table[(v, z)])
            for v in ODD for z in ODD},
        "derived_sigma": {str(v): render(table[(v, "sigma")]) for v in ODD},
        "stipulated_eta_table": {
            "%d,%d" % (v, z): render(stipulated_eta(v, z))
            for v in ODD for z in ODD},
        "stipulated_sigma": render(STIPULATED_SIGMA),
        "mismatches": mismatches,
        "derived_terminal_rows": {row: str(entries[row])
                                  for row in literal.TERMINAL_ROWS},
        "committed_terminal_rows": {row: str(committed_packet[row])
                                    for row in literal.TERMINAL_ROWS},
        "derived_terminal_vector": [str(value) for value in vector],
        "derived_equals_committed_terminal_packet": packet_match,
        "ridge_checker_strings": list(stipulated_strings),
        "old_inventory_killed_by_eta_and_sigma": old_inventory_invariance(),
        "compensation_identity": compensation_identity(omegas),
        "mutation_controls": mutation_controls(omegas),
        "verdict": ("DERIVED" if not mismatches and packet_match
                    else "CONTRADICTED"),
    }


def main():
    ledger = {
        "probe": "repair item 2a: forward derivation of the ridge terminal packet",
        "status": "UNAUDITED REPAIR PROBE",
        "audit": audit(),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    result = ledger["audit"]
    require(all(record["detected"] for record in result["mutation_controls"]),
            ("a mutation control was not detected",
             result["mutation_controls"]))
    print("repair23 ridge terminal derivation:", result["verdict"])
    print("eta_z(-Omega_v) derived   :", result["derived_eta_table"]["1,1"])
    print("eta_z(-Omega_v) stipulated:", result["stipulated_eta_table"]["1,1"])
    print("sigma(-Omega_v) derived   :", result["derived_sigma"]["1"])
    print("sigma(-Omega_v) stipulated:", result["stipulated_sigma"])
    print("terminal packet rows      :", result["derived_terminal_rows"])
    print("matches committed packet  :",
          result["derived_equals_committed_terminal_packet"])
    print("mutation controls detected:",
          sum(record["detected"] for record in result["mutation_controls"]),
          "/", len(result["mutation_controls"]))
    print("ledger_sha256=" + digest)
    Path(__file__).with_name("ledger_derive_ridge_terminal.json").write_text(
        json.dumps(ledger, sort_keys=True, indent=1) + "\n")
    return 0 if result["verdict"] == "DERIVED" else 1


if __name__ == "__main__":
    sys.exit(main())
