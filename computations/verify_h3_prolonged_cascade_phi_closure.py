#!/usr/bin/env python3
"""phi-closure of the prolonged cascade in the four-cube's own jet lattice.

Companions:
  * `verify_h3_descent_defect_row_space_invisibility.py` -- rows cannot
    cancel the descent defect (under its hypotheses);
  * `verify_h3_source_valid_tower_first_obstruction.py` -- T1: no
    source-valid tower admits the template; T2: phi bites first at
    order 4; T3: 360 distinct residuals.

This checker supplies the machine-checkable inputs for the next theorem
(the THEOREM is a hand proof in the companion note; the checker verifies
its INPUTS, one symbolic consistency computation, and one end-to-end
example -- it does not and cannot verify the universal quantifier over
towers):

THEOREM (cascade phi-closure; note, hand proof).  Fix one fourth-Hasse
selection (face, matching) with its four marked directions, and extend
the bounded physical complex by the squarefree jet lattice of ANY four
commuting source-valid derivations in those directions.  Then no chain

    n = sum_U a_U r_0[U] + sum_U b_U r_m[U] + alpha*T + beta*rho
        (+ strict chart cycles)

has dn = Yw, tgt(n) = 0, ores(n) = 0.  The prolonged differential is
taken R-LINEAR on coefficients (the committed model's convention,
`module_scale_polynomial`); coefficient-prolonging conventions are
excluded and are exactly where a genuine Spencer lift would differ.

Consequence, stated precisely: every escape through the squarefree
four-direction prolonged lattice of commuting source-valid derivations
is closed, including (via the mixed-chain paragraph of the note) chains
that also carry rows satisfying the row-space theorem's hypotheses.
Still open: the denominator attaching cell (the decoration fork),
multiset and cross-selection lattices (sketched only), and rows with a
phi-surviving edge-degree-0 boundary term.  The count of open escapes
is NOT reduced to one.

Proof shape (note):  ores forces beta = 0; the cap slot then forces
alpha = -1; target (R-linear, the r_0[empty]-coefficient) forces
a_empty = 1.  The e_0[V]-slot equations, after phi, become

  V != empty:  phi(a_V) + sum_{U > V} [phi(a_U) g_{U\\V}
                                        + phi(b_U) h_{U\\V}] = 0,
  V  = empty:  1 + sum_{U != empty} phi(a_U) g_U
                 + sum_U phi(b_U) h_U = 0,

with phi(D_S(B)) = g_S*Bbar, phi(D_S(A)) = h_S*Bbar, Bbar = H_0 - u.
By the T2 filtration h_S = 0 for |S| <= 3, so the V != empty system is
UNITRIANGULAR in the phi(a_V) and forces phi(a_U) = 0 for all
U != empty.  The V = empty equation becomes 1 + sum_{|U|=4}
phi(b_U) h_U = 0.  By the DIVISIBILITY LEMMA below, each order-one pure
part phi(D_i(e)) is a multiple of Bbar, so phi(D_U(A)) in (Bbar^4) and
h_U in (Bbar^3) subseteq (Bbar); hence the equation demands
-1 in (Bbar), impossible: Bbar is nonzero with no constant term, so a
constant multiple of Bbar is zero.  QED.

DIVISIBILITY LEMMA (note, hand proof; inputs verified here).  For any
derivation D with D(A) in I = (A, B): the pure part P_e = phi(D(e)) of
every edge e occurring in A satisfies P_e in (Bbar).  Proof inputs:
  (i)   A is a polynomial in mixed edge variables only (no pure edges,
        no u), so D(A) = sum_e D(e) partial_e A over A's edges;
  (ii)  mixed-degree (count of mixed edge variables) is a ring grading;
        A is mdeg-4 homogeneous and B is mdeg-0 homogeneous, so the
        mdeg-3 component of I is q_3*B and the mdeg-3 component of D(A)
        is sum_e P_e partial_e A;
  (iii) the 360 residuals M\\{e} are pairwise distinct, so matching the
        coefficient of each residual gives P_e = gamma_{M\\e}*Bbar.
The checker verifies (i)-(iii) exhaustively and verifies (iii)'s
extraction SYMBOLICALLY: with formal symbols P_e, the polynomial
sum_e P_e partial_e A has, at each residual monomial, coefficient
exactly one formal P_e -- computed through the actual derivative code,
not stipulated.

Also verified: for the tower D_i = B * d/dz_i, each marked direction
annihilates B (so the derivations commute and are source-valid) and
partial_J(A) = 1 on all fifteen selections, so the template target is
B^4 in I -- an explicit source-valid tower realizing exactly the T1
phenomenon: only I-multiples of the class, never the unit.  (The
template's cycle property for this tower is definitional and is not
re-verified.)

Scope: one selection's squarefree four-direction lattice, commuting
derivations, the fourth-Hasse cap model (dT = -Yw, drho = w,
tgt T = 1, ores rho = 1), chart cycles boundaryless, denominator
attachment EXCLUDED by hypothesis (it is the fork's other branch).
Multiset (higher-order-per-direction) lattices and cross-selection
combinations are not formalized here (the note sketches the same
argument).  Krenn's conjecture remains open.
"""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
QQ = Fraction
EXPECTED_LEDGER_SHA256 = (
    "43a9a4aab4d6be92290058c6b12fcd106841636e575dcd113d55b6d78d9ec3fd"
)


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


HASSE = load(
    "h3_cascade_hasse",
    "verify_h3_full_hasse_cone_d4_descent_obstruction.py",
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def is_mixed_item(item):
    if item == HASSE.HOMOGENIZING_U:
        return False
    require(len(item) == 5 and item[0] == "a",
            "an unexpected symbol reached the mixedness test")
    return (item[3], item[4]) != (0, 0)


def mdeg(term):
    return sum(1 for item in term if item != HASSE.HOMOGENIZING_U
               and is_mixed_item(item))


def popcount(mask):
    return bin(mask).count("1")


def content_hash(monomial_sets):
    hasher = sha256()
    for monomial_set in monomial_sets:
        for monomial in sorted(monomial_set):
            hasher.update(repr(monomial).encode("ascii"))
        hasher.update(b"|")
    return hasher.hexdigest()


def audit():
    A = HASSE.H_MIXED
    B = HASSE.B_PURE
    require(tuple(HASSE.MIXED8) == (0, 1, 2, 1, 1, 2, 2, 2),
            "the fourth-Hasse mixed word changed")
    require(HASSE.FORBIDDEN == frozenset((HASSE.P, HASSE.RCHART)),
            "the fourth-Hasse direct-free pair changed")
    require(len(A) == 90, "H_m lost its 90 monomials")

    # ---- Lemma input (i): A uses mixed edges only. ----------------------
    a_edges = set()
    for term in A:
        for item in term:
            require(item != HASSE.HOMOGENIZING_U,
                    "H_m acquired the homogenizing variable")
            require(is_mixed_item(item),
                    "H_m acquired a pure edge variable")
            a_edges.add(item)
    require(len(a_edges) == 27, "the m8 edge-variable support changed")

    # ---- Lemma input (ii): the mixed-degree grading. --------------------
    require({mdeg(term) for term in A} == {4},
            "H_m stopped being mdeg-4 homogeneous")
    require({mdeg(term) for term in B} == {0},
            "H_0 - u stopped being mdeg-0 homogeneous")

    # Bbar = phi(B) = B itself (B is mdeg-0); nonzero, no constant term.
    require(HASSE.kill_mixed_variables(B) == B,
            "the defect stopped being phi-fixed")
    require(B and () not in B,
            "H_0 - u acquired a constant term or vanished")

    # ---- Lemma input (iii): 360 pairwise distinct residuals. ------------
    residuals = {}
    for term in A:
        for item in term:
            rest = tuple(sorted(other for other in term if other != item))
            require(rest not in residuals,
                    "two (monomial, edge) pairs share a residual")
            residuals[rest] = (term, item)
    require(len(residuals) == 360, "the residual count changed")

    # ---- Lemma extraction, symbolically. --------------------------------
    # sum_e P_e * partial_e(A) with formal coefficient symbols P_e,
    # computed through the actual derivative code.  At each residual the
    # coefficient must be exactly one formal symbol.
    symbolic = {}
    for edge in sorted(a_edges):
        partial = HASSE.derivative(A, edge)
        for residual_term, coefficient in partial.items():
            key = tuple(sorted(residual_term))
            symbolic.setdefault(key, []).append((edge, coefficient))
    require(set(symbolic) == set(residuals),
            "the symbolic extraction support is not the residual set")
    for key, contributions in symbolic.items():
        require(len(contributions) == 1,
                "a residual received two formal contributions")
        edge, coefficient = contributions[0]
        require(coefficient == 1,
                "a residual coefficient is not the bare formal symbol")
        require(residuals[key][1] == edge,
                "the symbolic extraction disagrees with the residual map")

    # ---- The unitriangular phi-cascade, verified falsifiably. -----------
    # Jet lattice: 16 masks over four directions.  Equations for
    # V != 0:  phi(a_V) + sum_{U > V} phi(a_U) g_{U\V} = 0
    # (the b-terms are absent because h_S = 0 for |S| <= 3, and
    # |U \ V| <= 3 whenever V != 0).  An earlier draft "verified" this
    # by running the homogeneous back-substitution, which returns zero
    # for every input (tautological; caught by audit).  Instead: build
    # the 15x15 system matrix, verify its unitriangularity from the
    # construction, solve a PLANTED inhomogeneous system two independent
    # ways (poset back-substitution vs dense Gaussian elimination), and
    # require agreement; uniqueness then gives the homogeneous-zero
    # conclusion used in the proof.
    unknown_masks = tuple(sorted(range(1, 16), key=popcount))
    index_of = {mask: index for index, mask in enumerate(unknown_masks)}
    cascade_trials_run = 0
    for trial in (1, 2):
        g = {mask: QQ(3 * popcount(mask) + trial, popcount(mask) + 2)
             for mask in range(1, 16)}
        matrix = []
        for v_mask in unknown_masks:
            row_vector = [QQ(0)] * 15
            for u_mask in unknown_masks:
                if u_mask == v_mask:
                    row_vector[index_of[u_mask]] = QQ(1)
                elif (u_mask & v_mask) == v_mask:
                    row_vector[index_of[u_mask]] = g[u_mask ^ v_mask]
            matrix.append(row_vector)
        for row_position, v_mask in enumerate(unknown_masks):
            require(matrix[row_position][index_of[v_mask]] == 1,
                    "the cascade matrix lost its unit diagonal")
            for column_position, u_mask in enumerate(unknown_masks):
                if (u_mask & v_mask) != v_mask:
                    require(matrix[row_position][column_position] == 0,
                            "the cascade matrix left the mask poset")
        planted = [QQ(2 * position - 7, position + 3)
                   for position in range(15)]
        # Solver 1: poset back-substitution, top-down as in the proof.
        solution_poset = {}
        for v_mask in sorted(unknown_masks, key=popcount, reverse=True):
            total = planted[index_of[v_mask]]
            for u_mask in unknown_masks:
                if u_mask != v_mask and (u_mask & v_mask) == v_mask:
                    total -= solution_poset[u_mask] * g[u_mask ^ v_mask]
            solution_poset[v_mask] = total
        # Solver 2: dense Gaussian elimination, written independently.
        work = [row_vector[:] + [planted[position]]
                for position, row_vector in enumerate(matrix)]
        for column in range(15):
            pivot = next(row for row in range(column, 15)
                         if work[row][column])
            work[column], work[pivot] = work[pivot], work[column]
            scale_value = work[column][column]
            work[column] = [entry / scale_value for entry in work[column]]
            for row in range(15):
                if row != column and work[row][column]:
                    factor = work[row][column]
                    work[row] = [entry - factor * lead for entry, lead
                                 in zip(work[row], work[column])]
        for position, v_mask in enumerate(unknown_masks):
            require(work[position][15] == solution_poset[v_mask],
                    "the two cascade solvers disagree")
        # Verify the poset solution satisfies every equation directly.
        for row_position, v_mask in enumerate(unknown_masks):
            value = sum(
                (matrix[row_position][index_of[u_mask]]
                 * solution_poset[u_mask] for u_mask in unknown_masks),
                QQ(0),
            )
            require(value == planted[row_position],
                    "the cascade solution fails an equation")
        cascade_trials_run += 1

    # With phi(a_U) = 0 for U != 0 and a_0 = 1, the V = 0 equation is
    # 1 + sum_{|U|=4} phi(b_U) h_U = 0 with each h_U in (Bbar); a
    # solution would put the constant -1 in (Bbar).  A constant multiple
    # of Bbar: c = q*Bbar with Bbar lacking a constant term forces the
    # constant term of the product to be 0, so c = 0.  Recorded as the
    # note's argument; the checker verified its input (no constant term)
    # above.

    # ---- Example tower D_i = B * d/dz_i: the two facts that matter. -----
    # (a) each marked direction annihilates B (so the D_i are commuting
    #     and D_i(B) = 0, making the tower source-valid:
    #     D_i(A) = B * partial_i(A) in I); and
    # (b) partial_J(A) = 1 on every selection, so the template target is
    #     D_J(A) = B^4 * 1 = B^4 in I -- exactly the T1 phenomenon.
    # The cycle property of the template for this tower is definitional
    # (d r_0[U] = B e[U] and d r_m[U]'s terms cancel it pairwise), so it
    # is NOT re-verified here; an earlier draft "verified" it by adding
    # and subtracting the same product, which was vacuous and slow.
    example_records = 0
    for deleted in HASSE.ODD:
        for matching in HASSE.matchings(HASSE.face(deleted)):
            directions, _internal, _external = HASSE.selected_directions(
                deleted, matching)
            require(len(directions) == 4,
                    "a selection lost its four directions")
            for direction in directions:
                require(HASSE.derivative(B, direction) == {},
                        "a marked direction stopped annihilating B")
            top = HASSE.derivatives(A, directions)
            require(top == HASSE.constant(),
                    "partial_J(A) stopped being one on a selection")
            example_records += 1
    require(example_records == 15,
            "the example sweep changed size")

    a_mdegs = sorted({mdeg(term) for term in A})
    b_mdegs = sorted({mdeg(term) for term in B})
    ledger = {
        "geometry_sha256": content_hash([
            [tuple(sorted(term)) for term in A],
            [tuple(sorted(term)) for term in B],
        ]),
        "mixed_word": "".join(map(str, HASSE.MIXED8)),
        "a_edge_support": len(a_edges),
        "a_mdegs": a_mdegs,
        "b_mdegs": b_mdegs,
        "defect_has_constant_term": () in B,
        "distinct_residuals": len(residuals),
        "symbolic_extraction_checked_residuals": len(symbolic),
        "cascade_trials": cascade_trials_run,
        "cascade_solvers_agree": True,
        "example_tower": "D_i = B * d/dz_i",
        "example_selections": example_records,
        "example_target": "B^4 (definitional from partial_J(A) = 1)",
        "theorem_status": (
            "hand proof in the note; this checker verifies its inputs "
            "(mixedness, gradings, residual distinctness, no constant "
            "term), the symbolic residual extraction, the unitriangular "
            "cascade solve, and the end-to-end example tower.  The "
            "universal quantifier over towers is NOT machine-verified"
        ),
        "consequence": (
            "every escape through the squarefree four-direction "
            "prolonged lattice of commuting source-valid derivations is "
            "closed, including mixed chains carrying rows under the "
            "row-space hypotheses; still open: the denominator attaching "
            "cell (the fork), multiset and cross-selection lattices, and "
            "rows with a phi-surviving edge-degree-0 boundary term"
        ),
        "scope": (
            "one selection's squarefree four-direction lattice, "
            "commuting source-valid derivations, fourth-Hasse cap model, "
            "denominator attachment excluded by hypothesis; multiset "
            "lattices and cross-selection combinations not formalized; "
            "Krenn's conjecture remains open"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "h3 prolonged-cascade phi-closure ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h=3 prolonged-cascade phi-closure inputs: PASS (exact)")
    print("lemma inputs: edges/mdegA/mdegB/const:  %d %s %s %s"
          % (ledger["a_edge_support"], ledger["a_mdegs"], ledger["b_mdegs"],
             ledger["defect_has_constant_term"]))
    print("residuals / symbolic extraction:         %d %d"
          % (ledger["distinct_residuals"],
             ledger["symbolic_extraction_checked_residuals"]))
    print("cascade: planted solves agree (trials): ",
          ledger["cascade_trials"])
    print("geometry sha256:", ledger["geometry_sha256"][:32], "...")
    print("example tower %s: target %s"
          % (ledger["example_tower"], ledger["example_target"]))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
