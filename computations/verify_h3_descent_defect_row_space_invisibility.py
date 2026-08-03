#!/usr/bin/env python3
"""The four-cube descent defect needs a phi-surviving edge-degree-zero term.

The fourth-Hasse cone audit
(`verify_h3_full_hasse_cone_d4_descent_obstruction.py`) proves that the
formal chain n_I = s_I - T has boundary Yw with zero target and cap
residue, but that its diagonal projection to the physical complex has the
exact chain-map defect

    (H_0 - u) e_0,

and that no target-zero repair exists in the two-row span: b*H_m = H_0 - u
has no polynomial solution (its equation (26)).

This checker extends that obstruction to every row family satisfying two
checkable hypotheses.  Let phi be the pure-colour specialization: the
ring homomorphism sending every edge variable with colour pair other than
(0,0) to zero, and fixing pure edges and the homogenizing u.

THEOREM.  Let {rho_i} be any family of TARGET-ZERO physical rows whose
e_0-boundary coefficients beta_i satisfy: every monomial of phi(beta_i)
has edge-degree >= 1.  Then no chain x = a r_0 + sum b_i rho_i with
target zero has e_0-boundary (H_0 - u) e_0.

Proof.  In the fourth-Hasse model the target is R-linear -- the
polynomial coefficient of r_0 (`target_of_hasse_chain`, which returns
chain.get(("r0", 0))) -- so target zero forces a = 0 identically.  Then
phi(e_0-boundary of x) = sum phi(b_i) phi(beta_i), every monomial of
which has edge-degree >= 1, while phi(H_0 - u) = H_0 - u contains the
standalone monomial -u of edge-degree 0.  QED.

The two hypotheses are verified against the literal geometry:

  A.  (phi-null rows.)  For every one of the 6560 mixed words c, every
      one of the 90 monomials of the direct-free hafnian H_c contains a
      mixed-colour edge, so phi(H_c) = 0 -- these rows satisfy the
      hypothesis vacuously.  This includes the all-1 and all-2 pure-word
      rows, whose edges carry colours (1,1)/(2,2); like every reset row
      in this model they carry target zero, so they fall under the
      theorem.  (The sweep re-derives what is definitionally true of the
      constructed hafnians; the content of this checker is the theorem's
      two-line argument plus fact B and the denominator computation
      below, not the sweep.)

  B.  (The defect's edge-degree-zero term.)  Every monomial of H_0 has
      edge-degree 4, phi fixes it (all edges pure), and the fourth-Hasse
      B_PURE = H_0 - u is fixed by that module's own kill_mixed_variables
      and contains the edge-degree-0 monomial -u.  So the defect is not
      reachable from edge-degree->=1 material.

  C.  (The phi-surviving generators of the cited cone.)  The complete
      denominator presentation delta(d_{s,a}) = sum_{c: c_s = a}
      Haf(q_c|_{D\\{s}}) e_c has, for a = 0, an e_0-component equal to
      the PURE face hafnian Haf(q_0|_{D\\{s}}) -- three monomials, all
      pure, all of edge-degree exactly 2.  These columns are NOT phi-null
      -- an earlier draft of this checker wrongly claimed no such row
      existed -- but they satisfy the edge-degree hypothesis, so the
      theorem covers them: no combination of denominator a=0 columns
      (with any polynomial coefficients) reaches the -u term.

Consequence: the defect is reachable only by a row whose e_0-coefficient
has a phi-surviving edge-degree-0 term -- a q-zero unit.  Producing that
unit source-faithfully is exactly the Spencer-generator problem the
fourth-Hasse audit isolates, so the missing object is of Spencer type,
not any row family satisfying the hypotheses.

Scope: finite h=3, direct-free, bounded model of the fourth-Hasse audit,
with that model's R-linear target convention.  A row violating either
hypothesis (nonzero target, or a phi-surviving edge-degree-0 boundary
term) is not excluded -- constructing the latter source-faithfully IS the
open problem.  Whether the denominator columns carry target zero is not
decided by any artifact; the edge-degree argument covers them either way
for the e_0 slot.  This constructs no Spencer lift and does not prove
Krenn's conjecture, which remains open.
"""

from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_LEDGER_SHA256 = (
    "10c3511560ee5c9b1693b08bd680dae3d333385bd0d458063a0d358a247d5022"
)

M8 = (0, 1, 2, 1, 1, 2, 2, 2)


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load(
    "h3_row_space_base",
    "verify_h3_direct_free_literal_four_face_full_nine_no_go.py",
)
HASSE = load(
    "h3_row_space_hasse",
    "verify_h3_full_hasse_cone_d4_descent_obstruction.py",
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def is_mixed(edge_variable):
    _left, _right, left_colour, right_colour = edge_variable
    return (left_colour, right_colour) != (0, 0)


def phi_kills_monomial(monomial):
    """The pure specialization kills a monomial iff it has a mixed edge."""
    return any(is_mixed(edge_variable) for edge_variable in monomial)


def canonical(monomial):
    """Encoding-independent form of a labelled matching monomial."""
    return tuple(sorted(tuple(edge_variable)
                        for edge_variable in monomial))


def hasse_canonical(term):
    """Strip the fourth-Hasse 'a' tag: ('a',l,r,lc,rc) -> (l,r,lc,rc)."""
    return tuple(sorted(tuple(item[1:]) for item in term))


def content_hash(monomial_sets):
    hasher = sha256()
    for monomial_set in monomial_sets:
        for monomial in sorted(monomial_set):
            hasher.update(repr(monomial).encode("ascii"))
        hasher.update(b"|")
    return hasher.hexdigest()


def audit():
    pure_word = (0,) * 8
    words_scanned = 0
    mixed_rows_all_die = True
    pure_row_all_pure = True
    monomials_scanned = 0

    for word in product(BASE.COLORS, repeat=8):
        words_scanned += 1
        row = BASE.full_nine_polynomial(word)
        for monomial in row:
            monomials_scanned += 1
            if word == pure_word:
                if phi_kills_monomial(monomial):
                    pure_row_all_pure = False
            else:
                if not phi_kills_monomial(monomial):
                    mixed_rows_all_die = False
    require(words_scanned == 3 ** 8 == 6561,
            "the global word sweep changed size")
    require(monomials_scanned == 6561 * 90,
            "the monomial sweep changed size")
    require(mixed_rows_all_die,
            "a mixed-row monomial survived the pure specialization")
    require(pure_row_all_pure,
            "a pure-row monomial acquired a mixed edge")

    # --- B: the defect's edge-degree structure. -------------------------
    pure_row = BASE.full_nine_polynomial(pure_word)
    pure_degrees = {len(monomial) for monomial in pure_row}
    require(pure_degrees == {4},
            "the pure row left edge-degree four")
    # The fourth-Hasse module's own defect B_PURE = H_0 - u: fixed by its
    # own kill_mixed_variables, and containing the -u monomial.
    b_pure_fixed = HASSE.kill_mixed_variables(HASSE.B_PURE) == HASSE.B_PURE
    require(b_pure_fixed and HASSE.B_PURE,
            "the fourth-Hasse defect is not phi-fixed and nonzero")
    u_term = HASSE.HOMOGENIZING_U
    u_coefficient = HASSE.B_PURE.get((u_term,), 0)
    require(u_coefficient == -1,
            "the defect lost its -u monomial")
    defect_edge_degrees = set()
    for term in HASSE.B_PURE:
        edge_items = [item for item in term if item[0] == "a"]
        defect_edge_degrees.add(len(edge_items))
    require(defect_edge_degrees == {0, 4},
            "the defect's edge-degree support changed")

    # --- Cross-model anchor: the two independent hafnian constructions
    #     agree as monomial sets, for both the mixed and the pure word.
    require(tuple(HASSE.MIXED8) == M8,
            "the fourth-Hasse mixed word changed")
    h_m8 = BASE.full_nine_polynomial(M8)
    require({hasse_canonical(term) for term in HASSE.H_MIXED}
            == {canonical(monomial) for monomial in h_m8},
            "the two independent hafnian constructions disagree at m8")
    require({hasse_canonical(term) for term in HASSE.H_PURE}
            == {canonical(monomial) for monomial in pure_row},
            "the two independent hafnian constructions disagree at 0")

    # --- C: the phi-surviving denominator a=0 columns. ------------------
    # e_0-component of delta(d_{s,0}) is the pure face hafnian on D\{s}:
    # three monomials, all pure, all of edge-degree exactly two.  These
    # violate phi-nullity but satisfy the edge-degree hypothesis.
    denominator_faces = []
    for site in BASE.ODD:
        face = BASE.face_hafnian(site, (0,) * 4)
        require(len(face) == 3,
                "a pure face hafnian lost its three monomials")
        for monomial in face:
            require(not phi_kills_monomial(monomial),
                    "a denominator a=0 monomial stopped being pure")
            require(len(monomial) == 2,
                    "a denominator a=0 monomial left edge-degree two")
        denominator_faces.append({canonical(m) for m in face})

    # The theorem's hypothesis check, in one place: every phi-surviving
    # monomial available from the covered generators has edge-degree >= 1
    # (mixed rows contribute none; denominator faces contribute degree 2),
    # while the defect has the edge-degree-0 monomial -u.
    minimum_surviving_degree = min(
        len(monomial)
        for face in denominator_faces
        for monomial in face
    )
    require(minimum_surviving_degree == 2 >= 1,
            "a covered generator produced an edge-degree-0 monomial")

    ledger = {
        "words_scanned": words_scanned,
        "monomials_scanned": monomials_scanned,
        "phi": "set every edge variable with colour pair != (0,0) to zero",
        "mixed_rows_die_under_phi": mixed_rows_all_die,
        "pure_row_fixed_by_phi": pure_row_all_pure,
        "defect_phi_fixed_and_nonzero": bool(b_pure_fixed and HASSE.B_PURE),
        "defect_u_coefficient": int(u_coefficient),
        "defect_edge_degrees": sorted(defect_edge_degrees),
        "denominator_a0_columns": len(denominator_faces),
        "denominator_a0_edge_degree": minimum_surviving_degree,
        "content_sha256": content_hash(
            [
                [canonical(m) for m in pure_row],
                [canonical(m) for m in h_m8],
                [hasse_canonical(t) for t in HASSE.H_MIXED],
                [hasse_canonical(t) for t in HASSE.H_PURE],
            ]
            + [sorted(face) for face in denominator_faces]
        ),
        "theorem": (
            "no target-zero chain over rows whose phi-image e_0 "
            "coefficients have every monomial of edge-degree >= 1 reaches "
            "the defect (H_0 - u) e_0, because target zero kills the r_0 "
            "coefficient (R-linear target) and the defect's -u monomial "
            "has edge-degree 0"
        ),
        "scope": (
            "finite h=3 direct-free bounded model with the fourth-Hasse "
            "R-linear target convention; covers phi-null rows (all 6560 "
            "mixed reset rows) and the phi-surviving denominator a=0 "
            "columns; does not exclude a row with a phi-surviving "
            "edge-degree-0 boundary term, whose source-faithful "
            "construction is the open Spencer problem; Krenn's "
            "conjecture remains open"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "h3 descent-defect row-space ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h=3 descent-defect row-space theorem: PASS (exact)")
    print("words / monomials swept:            %d %d"
          % (ledger["words_scanned"], ledger["monomials_scanned"]))
    print("mixed rows die under phi:          ",
          ledger["mixed_rows_die_under_phi"])
    print("defect phi-fixed, -u coefficient:  ",
          ledger["defect_phi_fixed_and_nonzero"],
          ledger["defect_u_coefficient"])
    print("defect edge-degrees:               ",
          ledger["defect_edge_degrees"])
    print("denominator a=0 columns (deg 2):    %d"
          % ledger["denominator_a0_columns"])
    print("content sha256:", ledger["content_sha256"][:32], "...")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
