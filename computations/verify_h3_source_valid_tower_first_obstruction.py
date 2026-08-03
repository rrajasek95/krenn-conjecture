#!/usr/bin/env python3
"""First-obstruction ledger for a source-valid fourth Hasse-Schmidt tower.

After `verify_h3_descent_defect_row_space_invisibility.py`, the object
named by the fourth-Hasse audit as the route's missing source datum is a
source-valid fourth Hasse-Schmidt tower.  Conventions, fixed here once:

  * J = {z_1, z_2, z_3, z_4} is the four-direction set of the
    fourth-Hasse audit (its equation (3)); I = (H_m, H_0 - u) is the
    two-generator source ideal of its bounded model, with u a VARIABLE
    (the homogenizing coordinate).  The letters are kept distinct.
  * A tower is a multi-index Hasse-Schmidt family D_S over sub-multisets
    of directions with D_S(xy) = sum over splittings; for the four
    order-one directions of the template, D_J = D_{z_1}D_{z_2}D_{z_3}
    D_{z_4} (disjoint singletons, binomial factors 1).
  * Source-valid means D_S(I) subseteq I for every S.  This is the
    strong ideal-preservation reading of "preserves every EqSystem
    equation"; weaker geometric readings (preserve the radical, or
    I : u^infty) are flagged in the note.
  * "Mixed" edge variable means colour pair != (0,0) -- the
    phi-convention, NOT "two different colours".
  * phi is the pure-colour specialization (mixed edge variables to 0).

Three exact facts, with A = H_m for m8 = 01211222:

  T1 (template impossibility -- corrected from an earlier draft's
     false "circularity" reading).  The template
     s^D = sum_{S subseteq J} D_S(A) r_0[J\\S] - B r_m[J] has target
     (its r_0[empty]-coefficient) D_J(A), BY DEFINITION of the
     template.  Coupling with the cap as n = s^D - lambda*T needs
     tgt(n) = 0, i.e. lambda = D_J(A), and yields boundary
     lambda*Y*w.  For a source-valid tower, A in I forces
     D_J(A) in I.  Now:
       - I contains no nonzero element of weight < 4 under the grading
         wt(edge) = 1, wt(u) = 4 (both generators are weight-4
         homogeneous), so 1 not in I and more generally no nonzero
         rational lies in I.  Hence lambda cannot be a nonzero scalar.
       - If lambda = D_J(A) in I, the boundary lambda*Y*w lies in
         I*Y*w: it vanishes on the source quotient and carries no
         descent information.
     So NO source-valid tower admits an informative four-cube
     template: unconditionally impossible, not "circular".  There is
     also no saturation escape: the checker verifies the witness point
     (all pure edges 1, all mixed edges 0, u = 90), where
     H_m = 0 and H_0 - u = 0 with u = 90 != 0.  Thus V(I) is nonempty
     and meets {u != 0}: neither 1 in I, nor u^k in I, nor 1 in
     radical(I) can hold.  (Emptiness of THIS two-generator variety is
     NOT the open case; the open case is the nine-row system.)
     Consequently the transversality Psi_J(H_m) = 1 of the coordinate
     tower is necessary for an informative template and unattainable
     source-faithfully.

  T2 (phi-filtration).  Every edge variable of every monomial of A is
     mixed in the phi-sense: an edge covering site 0 (m8's only pure
     site) has colour pair (0, m_s) with m_s != 0, and an edge not
     covering site 0 has both endpoints coloured 1 or 2.  Hence for ANY
     tower, phi(D_n(A)) = 0 for n <= 3 automatically, and at order four
     exactly

         phi(D_4(A)) = sum_{M in A} prod_{e in M} phi(D_1(e))
                     = Haf_A(phi o D_1).

     Source-validity therefore first bites at order four, with the
     exact condition Haf_A(phi o D_1) in (H_0 - u).  The proof is the
     two-line multilinear expansion (a total order below four forces
     some factor D_0(e) = e, killed by phi); the symbolic sweep below
     is a CONSISTENCY CHECK of the composition bookkeeping, not an
     independent test of the identity.

  T3 (constant-coefficient rigidity).  The 360 residuals M\\{e} over
     all (M, e) are pairwise distinct, so sum_e c_e partial_e(A) = 0
     with rational c_e, e ranging over the edge variables OCCURRING IN
     A, forces c = 0.

Scope: finite h=3, direct-free, bounded model of the fourth-Hasse
audit.  T1 kills the template within that model's cap coupling; the
general-chain cascade through higher-jet outputs, rows outside the
companion note's hypotheses, and structures beyond the smallest cone
are not excluded here.  No tower is constructed and Krenn's conjecture
remains open.
"""

from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
QQ = Fraction
EXPECTED_LEDGER_SHA256 = (
    "085191a1e2be1ed842fe80c71b38083e630c755fb0221e67b14a7c023845dbb5"
)

M8 = (0, 1, 2, 1, 1, 2, 2, 2)


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load(
    "h3_tower_base",
    "verify_h3_direct_free_literal_four_face_full_nine_no_go.py",
)
HASSE = load(
    "h3_tower_hasse",
    "verify_h3_full_hasse_cone_d4_descent_obstruction.py",
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def is_mixed(edge_variable):
    """phi-convention: colour pair != (0,0)."""
    _left, _right, left_colour, right_colour = edge_variable
    return (left_colour, right_colour) != (0, 0)


def compositions(total, parts):
    """All tuples of `parts` nonnegative integers summing to `total`."""
    if parts == 1:
        yield (total,)
        return
    for head in range(total + 1):
        for tail in compositions(total - head, parts - 1):
            yield (head,) + tail


def evaluate_hasse_polynomial(polynomial, pure_value, mixed_value, u_value):
    """Evaluate a fourth-Hasse polynomial at a diagonal edge point."""
    total = QQ(0)
    for term, coefficient in polynomial.items():
        value = QQ(coefficient)
        for item in term:
            if item == HASSE.HOMOGENIZING_U:
                value *= u_value
            else:
                require(len(item) == 5 and item[0] == "a",
                        "an unexpected symbol reached the evaluator")
                _a, _l, _r, lc, rc = item
                value *= pure_value if (lc, rc) == (0, 0) else mixed_value
        total += value
    return total


def audit():
    row = BASE.full_nine_polynomial(M8)
    require(len(row) == 90, "the m8 row lost its 90 matchings")

    # --- T2 mixedness, with both cases of the argument. ------------------
    for monomial in row:
        edges = tuple(sorted(monomial))
        require(len(set(edges)) == 4,
                "an m8 monomial is not squarefree in four edges")
        for left, right, left_colour, right_colour in edges:
            require((left_colour, right_colour) != (0, 0),
                    "an m8-row edge variable is phi-pure")
            if 0 in (left, right):
                site_colour = right_colour if left == 0 else left_colour
                require(site_colour != 0,
                        "an edge covering site 0 lost its mixed endpoint")
            else:
                require(left_colour != 0 and right_colour != 0,
                        "an off-site-0 edge acquired a zero colour")

    # --- T2 filtration counts (a corollary of mixedness, recorded). ------
    surviving_by_size = {1: 0, 2: 0, 3: 0, 4: 0}
    for monomial in row:
        for size in (1, 2, 3, 4):
            for chosen in combinations(monomial, size):
                rest = [edge_variable for edge_variable in monomial
                        if edge_variable not in chosen]
                if all(not is_mixed(edge_variable)
                       for edge_variable in rest):
                    surviving_by_size[size] += 1
    require(surviving_by_size == {1: 0, 2: 0, 3: 0, 4: 90},
            "the phi-filtration of the m8 row changed")

    # --- T2 composition bookkeeping (consistency check, so labelled). ----
    hafnian_terms = set()
    expansion_terms = set()
    distributions_scanned = 0
    for monomial in row:
        edges = tuple(sorted(monomial))
        hafnian_terms.add(tuple(("d", edge) for edge in edges))
        for distribution in compositions(4, 4):
            distributions_scanned += 1
            factors = []
            dead = False
            for order, edge in zip(distribution, edges):
                if order == 0:
                    dead = True     # D_0(e) = e, and phi(e) = 0 (mixed)
                    break
                factors.append(("d", edge) if order == 1
                               else ("D", order, edge))
            if not dead:
                expansion_terms.add(tuple(factors))
    require(distributions_scanned == 90 * 35,
            "the Hasse distribution sweep changed size")
    require(expansion_terms == hafnian_terms,
            "phi(D_4(A)) bookkeeping left the A-hafnian of order-one parts")
    for total in (1, 2, 3):
        for distribution in compositions(total, 4):
            require(0 in distribution,
                    "a low-order Hasse distribution avoided order zero")

    # --- T1 inputs. -------------------------------------------------------
    # (i) Weight-4 homogeneity of both generators: wt(edge)=1, wt(u)=4.
    def weight(term):
        return sum(4 if item == HASSE.HOMOGENIZING_U else 1
                   for item in term)
    require({weight(term) for term in HASSE.H_MIXED} == {4},
            "H_m stopped being weight-4 homogeneous")
    require({weight(term) for term in HASSE.B_PURE} == {4},
            "H_0 - u stopped being weight-4 homogeneous")

    # (ii) The witness point: V(I) is nonempty and meets {u != 0}.
    #      All pure edges 1, all mixed edges 0, u = 90.
    h_m_value = evaluate_hasse_polynomial(HASSE.H_MIXED, QQ(1), QQ(0),
                                          QQ(90))
    b_value = evaluate_hasse_polynomial(HASSE.B_PURE, QQ(1), QQ(0), QQ(90))
    h_0_value = evaluate_hasse_polynomial(HASSE.H_PURE, QQ(1), QQ(0),
                                          QQ(90))
    require(h_m_value == 0, "the witness point left V(H_m)")
    require(b_value == 0, "the witness point left V(H_0 - u)")
    require(h_0_value == 90, "the pure hafnian changed value at the witness")

    # (iii) The coordinate transversality partial_J(A) = 1, computed here
    #       from the BASE encoding, independently of the fourth-Hasse
    #       constructor: deleting the four edges of any monomial M of A
    #       from the row leaves exactly the constant 1 (M itself), i.e.
    #       M appears once and no other monomial contains all four edges.
    anchors = 0
    for monomial in row:
        containing = [other for other in row
                      if set(monomial) <= set(other)]
        require(containing == [monomial],
                "a four-edge set lies in more than one m8 monomial")
        anchors += 1
    require(anchors == 90,
            "the coordinate transversality sweep changed size")

    # --- T3: the 360 residuals are pairwise distinct. --------------------
    residuals = {}
    for monomial in row:
        for edge_variable in monomial:
            rest = tuple(sorted(
                other for other in monomial if other != edge_variable))
            require(rest not in residuals,
                    "two (monomial, edge) pairs share a residual")
            residuals[rest] = (monomial, edge_variable)
    require(len(residuals) == 360,
            "the residual count changed")

    ledger = {
        "word": "".join(map(str, M8)),
        "row_monomials": len(row),
        "mixed_convention": "colour pair != (0,0)",
        "all_edges_phi_mixed": True,
        "phi_filtration_surviving": {
            str(size): count for size, count in surviving_by_size.items()
        },
        "hasse_distributions_scanned": distributions_scanned,
        "generators_weight4_homogeneous": True,
        "witness_point": {
            "pure_edges": 1, "mixed_edges": 0, "u": 90,
            "H_m": 0, "H_0_minus_u": 0, "H_0": 90,
        },
        "one_not_in_I": (
            "both generators weight-4 homogeneous, so I has no nonzero "
            "element of weight below 4; and V(I) meets {u != 0} at the "
            "witness, so no saturation escape"
        ),
        "coordinate_transversality_checks": anchors,
        "distinct_residuals": len(residuals),
        "T1": (
            "the template's target is D_J(A) by definition; source-"
            "validity gives D_J(A) in I; no nonzero rational lies in I, "
            "and a coupling scalar lambda = D_J(A) in I makes the "
            "boundary lambda*Y*w vanish on the source quotient.  No "
            "source-valid tower admits an informative template: "
            "unconditional impossibility, not circularity"
        ),
        "T2": (
            "phi(D_n(A)) = 0 automatically for n <= 3; "
            "phi(D_4(A)) = Haf_A(phi o D_1) by the displayed expansion "
            "(the symbolic sweep is a consistency check); source-"
            "validity first bites at order four via "
            "Haf_A(phi o D_1) in (H_0 - u)"
        ),
        "T3": (
            "constant-coefficient syzygies of the order-one faces, over "
            "the edge variables occurring in A, are zero: the 360 "
            "residuals are pairwise distinct"
        ),
        "scope": (
            "finite h=3 direct-free bounded model; kills the template "
            "within the smallest cone's cap coupling; the higher-jet "
            "cascade, rows outside the companion hypotheses, and larger "
            "structures are not excluded; no tower constructed; Krenn's "
            "conjecture remains open"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "h3 source-valid tower first-obstruction ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h=3 source-valid tower first obstructions: PASS (exact)")
    print("phi-filtration (|S|=1,2,3,4):        ",
          [ledger["phi_filtration_surviving"][k] for k in "1234"])
    print("generators weight-4 homogeneous:     ",
          ledger["generators_weight4_homogeneous"])
    print("witness point on V(I) with u=90:     ",
          ledger["witness_point"])
    print("coordinate transversality checks:    ",
          ledger["coordinate_transversality_checks"])
    print("constant syzygy rigidity (residuals):",
          ledger["distinct_residuals"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
