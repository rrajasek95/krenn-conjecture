#!/usr/bin/env python3
"""The denominator-marked escape forks on one undetermined datum.

An earlier version of this checker claimed the escape was CLOSED.  That
claim was withdrawn after an independent audit: it rested on an unproved
modelling hypothesis (that the denominator face is chart-neutral), and the
cited four-cube note points the other way.

The literal no-go `verify_h3_literal_full_nine_schur_polar_no_go.py` leaves
one escape: a denominator-marked two-edge cell, generator (18) carrying a
free sign sigma, whose tail contributes -I_5.

What is actually settled here is the arithmetic.  A face built from one
copy of the three-term marked polar h_v is

    w(alpha, beta) = alpha * (h_v)_{pq,direct} + beta * (h_v)_{pr,two-star},

and with the no-go's normalized cochain Lambda_v (+1/6 per pq term, -1/6
per pr term),

    Lambda_v(w(alpha, beta)) = (alpha - beta) / 2.

So the repair value -1 needs alpha - beta = -2, and the outcome depends
ENTIRELY on the chart decoration the denominator face carries:

    chart-neutral (alpha =  beta)  -> 0 for every coefficient   -> CLOSED
    single sector (sigma, 0)       -> sigma/2, so -1 at sigma=-2 -> OPEN
    chart-odd     (alpha = -beta)  -> alpha,   so -1 at alpha=-1 -> OPEN

No restriction |sigma| = 1 is imposed: the no-go's (18) leaves sigma free
and nothing in the repo bounds it, so bounding it would beg the question.

Which decoration is correct is NOT decidable from any artifact in this
repo.  The four-cube checker explicitly declines to give the symbol
cap/ordinary-residue coordinates, and the attaching chain is unconstructed
everywhere.  Positive evidence points toward chart-odd: four-cube section 2
requires the denominator face to cancel the reset commutator on the K_v
side, whose Rees symbol (its equation (9)) is chart-odd.  If the cancelling
face inherits that decoration, sigma = -1 delivers exactly the repair.

The pure-face (Y_0-type) model is separately shown to pair to zero for a
simpler reason -- its monomials are disjoint from h_v -- so that model is
closed regardless of parity.

This is a finite h=3, direct-free statement.  It closes nothing on its own;
it isolates the single datum that decides the escape.  Krenn's conjecture
remains open.
"""

from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
QQ = Fraction
EXPECTED_LEDGER_SHA256 = (
    "b9471153580976ddf8417b8f95b26161f9d46431a70cffab518e368b8e4730a6"
)

PQ_SECTOR = ("pq", "direct")
PR_SECTOR = ("pr", "two_star")


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load(
    "h3_decoration_fork_base",
    "verify_h3_direct_free_literal_four_face_full_nine_no_go.py",
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add_value(vector, key, value):
    updated = vector.get(key, QQ(0)) + QQ(value)
    if updated:
        vector[key] = updated
    else:
        vector.pop(key, None)


def add_vectors(*vectors):
    answer = {}
    for vector in vectors:
        for key, value in vector.items():
            add_value(answer, key, value)
    return answer


def scale(vector, scalar):
    scalar = QQ(scalar)
    if not scalar:
        return {}
    return {key: value * scalar for key, value in vector.items()}


def pairing(vector, cochain):
    return sum(
        (QQ(value) * cochain.get(key, QQ(0)) for key, value in vector.items()),
        QQ(0),
    )


def tagged(sector, polynomial):
    return {(sector, monomial): QQ(value)
            for monomial, value in polynomial.items() if value}


def build_polars():
    """The literal three-term marked polars h_v, from the eight-site rows."""
    polar = {}
    for deleted_site in BASE.ODD:
        word = [0] * 8
        for site in BASE.ODD:
            if site != deleted_site:
                word[site] = BASE.MIXED_ODD[site - 1]
        word = tuple(word)
        require("".join(map(str, word))
                == BASE.EXPECTED_GLOBAL_ROWS[deleted_site],
                "one labelled global polar row changed")

        global_boundary = {
            monomial: QQ(1)
            for monomial in BASE.full_nine_polynomial(word)
        }
        require(len(global_boundary) == 90,
                "a direct-free global row lost its 90 matchings")

        marked_edges = (
            BASE.edge(BASE.X, deleted_site, 0, 0),
            BASE.edge(BASE.P, BASE.Q_SITE, 0, 0),
        )
        marked = BASE.sparse_derivative(tuple(global_boundary), marked_edges)
        require(len(marked) == 3 and set(marked.values()) == {1},
                "one marked polar stopped being a three-term hafnian")
        require(dict(marked) == {
            monomial: QQ(1)
            for monomial in BASE.face_hafnian(
                deleted_site, BASE.face_word(deleted_site))
        }, "the marked polar stopped equalling the face hafnian h_v")

        # The two chart sectors carry this same polar, as the no-go proves.
        pq_direct, pq_stars = BASE.chart_partition(
            word, (BASE.P, BASE.Q_SITE))
        pr_direct, pr_stars = BASE.chart_partition(word, (BASE.P, BASE.R))
        require(BASE.sparse_derivative(pq_direct, marked_edges) == marked
                and not BASE.sparse_derivative(pq_stars, marked_edges),
                "pq marked tail left its direct sector")
        require(not BASE.sparse_derivative(pr_direct, marked_edges)
                and BASE.sparse_derivative(pr_stars, marked_edges) == marked,
                "pr marked tail left its two-star sector")
        polar[deleted_site] = dict(marked)
    return polar


def audit():
    polar = build_polars()

    cochains = {}
    for deleted_site in BASE.ODD:
        cochain = {}
        for monomial in polar[deleted_site]:
            cochain[(PQ_SECTOR, monomial)] = QQ(1, 6)
            cochain[(PR_SECTOR, monomial)] = QQ(-1, 6)
        cochains[deleted_site] = cochain

    squares = {
        deleted_site: add_vectors(
            tagged(PQ_SECTOR, polar[deleted_site]),
            scale(tagged(PR_SECTOR, polar[deleted_site]), -1),
        )
        for deleted_site in BASE.ODD
    }

    # 1. Disjointness of the five face supports.  Without it, faces at other
    #    deletion sites could interfere and the five conditions would not be
    #    independent.
    for left in BASE.ODD:
        for right in BASE.ODD:
            shared = set(polar[left]) & set(polar[right])
            if left == right:
                require(len(shared) == 3,
                        "a face lost its own three monomials")
            else:
                require(not shared,
                        "two distinct deletion faces share a monomial")

    # 2. The exact embedding formula Lambda_v(w(alpha,beta)) = (alpha-beta)/2,
    #    verified over an integer grid, for every deletion face.
    grid = range(-3, 4)
    formula_checks = 0
    for deleted_site in BASE.ODD:
        for alpha, beta in product(grid, repeat=2):
            face = add_vectors(
                scale(tagged(PQ_SECTOR, polar[deleted_site]), alpha),
                scale(tagged(PR_SECTOR, polar[deleted_site]), beta),
            )
            value = pairing(face, cochains[deleted_site])
            require(value == QQ(alpha - beta, 2),
                    "the single-copy embedding formula failed")
            for other in BASE.ODD:
                if other != deleted_site:
                    require(pairing(face, cochains[other]) == 0,
                            "a face paired against a foreign deletion site")
            formula_checks += 1
    require(formula_checks == 5 * len(grid) ** 2 == 245,
            "the embedding grid changed size")

    # 3. Chart-neutral faces pair to zero for EVERY coefficient.  This is the
    #    denominator column's case: its symbol h_v*Y_0 carries no chart label.
    for deleted_site in BASE.ODD:
        for sigma in grid:
            neutral = add_vectors(
                scale(tagged(PQ_SECTOR, polar[deleted_site]), sigma),
                scale(tagged(PR_SECTOR, polar[deleted_site]), sigma),
            )
            require(pairing(neutral, cochains[deleted_site]) == 0,
                    "a chart-neutral denominator face paired nontrivially")

    # 4. The fork.  Enumerate every chart decoration the denominator face
    #    could carry, over ALL integer coefficients -- not just +/-1.  The
    #    no-go's escape generator (18) leaves sigma free, and nothing in the
    #    repo restricts |sigma| = 1, so restricting it would beg the
    #    question.  By (2) the pairing is (alpha - beta)/2, so:
    #
    #      chart-neutral  (alpha =  beta) -> 0        for every sigma
    #      single-sector  (sigma, 0)      -> sigma/2  -> -1 at sigma = -2
    #      chart-odd      (alpha = -beta) -> alpha    -> -1 at alpha = -1
    #
    #    So the escape is CLOSED only under the chart-neutral decoration,
    #    and is OPEN under the other two.  It is a fork, not a no-go.
    decorations = {}
    for deleted_site in BASE.ODD:
        cochain = cochains[deleted_site]
        for sigma in range(-4, 5):
            neutral = add_vectors(
                scale(tagged(PQ_SECTOR, polar[deleted_site]), sigma),
                scale(tagged(PR_SECTOR, polar[deleted_site]), sigma),
            )
            single = scale(tagged(PQ_SECTOR, polar[deleted_site]), sigma)
            odd = add_vectors(
                scale(tagged(PQ_SECTOR, polar[deleted_site]), sigma),
                scale(tagged(PR_SECTOR, polar[deleted_site]), -sigma),
            )
            require(pairing(neutral, cochain) == 0,
                    "a chart-neutral face stopped pairing to zero")
            require(pairing(single, cochain) == QQ(sigma, 2),
                    "the single-sector value left sigma/2")
            require(pairing(odd, cochain) == sigma,
                    "the chart-odd value left sigma")
            for name, value in (("neutral", pairing(neutral, cochain)),
                                ("single", pairing(single, cochain)),
                                ("odd", pairing(odd, cochain))):
                if value == -1:
                    decorations.setdefault(name, set()).add(sigma)
    require("neutral" not in decorations,
            "a chart-neutral face reached -1")
    require(decorations["single"] == {-2},
            "the single-sector face reaches -1 at an unexpected coefficient")
    require(decorations["odd"] == {-1},
            "the chart-odd face reaches -1 at an unexpected coefficient")

    # 5. The pure-face (Y_0-type) model pairs to zero for a second, simpler
    #    reason: its monomials are disjoint from h_v.  So that model also
    #    cannot reach -1, independently of parity.
    for deleted_site in BASE.ODD:
        pure_face = {
            monomial: QQ(1)
            for monomial in BASE.face_hafnian(deleted_site, (0,) * 4)
        }
        require(not (set(pure_face) & set(polar[deleted_site])),
                "the pure face stopped being disjoint from h_v")
        for sigma in range(-4, 5):
            for placement in (
                add_vectors(scale(tagged(PQ_SECTOR, pure_face), sigma),
                            scale(tagged(PR_SECTOR, pure_face), sigma)),
                scale(tagged(PQ_SECTOR, pure_face), sigma),
                add_vectors(scale(tagged(PQ_SECTOR, pure_face), sigma),
                            scale(tagged(PR_SECTOR, pure_face), -sigma)),
            ):
                require(pairing(placement, cochains[deleted_site]) == 0,
                        "a pure-face model paired nontrivially")

    # 6. Cross-face independence: a face at one deletion site contributes
    #    nothing at any other, so the five conditions cannot be traded off.
    for left in BASE.ODD:
        for right in BASE.ODD:
            if left == right:
                continue
            face = tagged(PQ_SECTOR, polar[left])
            require(pairing(face, cochains[right]) == 0,
                    "a face paired against a foreign deletion site")

    ledger = {
        "deletion_faces": len(BASE.ODD),
        "coefficient_range_swept": [-4, 4],
        "no_unit_coefficient_assumption": True,
        "pure_face_model_closed_by_disjoint_support": True,
        "cross_face_interference": False,
        "face_supports_disjoint": True,
        "embedding_formula": "Lambda_v(alpha*pq + beta*pr) = (alpha-beta)/2",
        "embedding_grid_checks": formula_checks,
        "chart_neutral_pairing": 0,
        "decorations_reaching_minus_one": {
            name: sorted(values) for name, values in decorations.items()
        },
        "denominator_face_can_reach_minus_one": "depends on its chart decoration: no if chart-neutral, yes if single-sector (sigma=-2) or chart-odd (sigma=-1)",
        "escape_closed": False,
        "conclusion": (
            "the escape is a fork, not a no-go.  Lambda_v of a single-copy "
            "face is (alpha-beta)/2, so the repair value -1 is unreachable "
            "under a chart-neutral decoration but reachable under a "
            "single-sector one (sigma=-2) or a chart-odd one (sigma=-1).  "
            "Which decoration the denominator face carries is not decidable "
            "from any artifact in this repo, and the four-cube note's "
            "cancellation requirement points toward chart-odd"
        ),
        "scope": (
            "finite h=3 direct-free statement; isolates the datum that "
            "decides the escape rather than closing it, constructs no "
            "replacement comparison, and leaves Krenn's conjecture open"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "h3 denominator decoration-fork ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h=3 denominator-marked escape: FORK (exact arithmetic)")
    print("embedding formula:                ", ledger["embedding_formula"])
    print("grid checks:                      ",
          ledger["embedding_grid_checks"])
    print("decorations reaching -1:          ",
          ledger["decorations_reaching_minus_one"],
          "(chart-neutral: never)")
    print("escape closed:                    ", ledger["escape_closed"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
