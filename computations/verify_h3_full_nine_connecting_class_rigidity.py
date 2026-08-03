#!/usr/bin/env python3
"""Every literal chart-odd tail is a kernel-vector tail, and the connecting map is I_5.

The literal no-go `verify_h3_literal_full_nine_schur_polar_no_go.py` shows
the five marked polar cochains have source-relative connecting matrix I_5.
Two escapes have been discussed: denominator-marked cells, and more general
added comparison cells.

This checker proves what the literal chart-labelled source rows can and
cannot supply, over the WHOLE literal complex rather than a chosen family.
It does NOT decide whether supplying the tail of -k_v constitutes a
repair; that depends on the unconstructed comparison complex.

Structural facts, each verified here from the eight-site geometry:

  A.  For every global word w (checked once per word, being independent of
      the marking), the pq-chart and pr-chart source rows have the SAME
      90-term direct-free boundary.  Hence
          k_w = r_w^{pq} - r_w^{pr}
      lies in ker A' for every one of the 3^8 words.

  B.  For every marking (a_xv^00, a_pq^00) and every word w, the pq-chart
      marked tail and the pr-chart marked tail are the SAME polynomial
      X_{v,w}, differently tagged.  The reason is exact and one-sided:
      differentiating by a_pq^00 forces the pq edge, so all pq-chart marked
      material is pq-direct; and the direct-free hypothesis A_pr = 0 makes
      the pr-direct piece empty, so all pr-chart marked material is
      pr-two-star.

  C.  Consequently the chart-odd part of ANY combination of literal
      chart-labelled columns is again of the form T'(kappa) for a kernel
      element kappa.  Chart-odd tails are exactly the kernel-vector tails:
          {chart-odd tails} = T'(ker A').

  D.  Sweeping all 6561 words, exactly ONE literal tail per deletion site
      meets the corresponding polar cochain -- the selected polar row --
      with value exactly 1.  So the connecting map over the whole literal
      chart-labelled source complex is I_5.

The scope of the conclusion is exactly this: every chart-odd tail available
from the literal chart-labelled source rows is a kernel-vector tail, and
-I_5 is reachable among them only as the tail of -k_v.  Whether that
counts as a repair or merely restates the kernel vector is a question about
the unconstructed comparison complex, and is NOT decided here.

This is a finite h=3, direct-free statement.  It does not exclude an
operation whose tail is NOT a literal chart-labelled source tail -- in
particular it does not exclude the Hasse/Spencer totalization or any
denominator/cap material that the no-go leaves open.  It constructs no
replacement comparison and does not prove Krenn's conjecture, which
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
    "b2e0a4d4bbbfd07fbc354df7f3b5a1ac776929bd06ed4ffc0458ea894a637c4c"
)

PQ_SECTOR = ("pq", "direct")
PR_SECTOR = ("pr", "two_star")


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load(
    "h3_rigidity_base",
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


def iota(vector):
    answer = {}
    for (sector, monomial), value in vector.items():
        if sector == PQ_SECTOR:
            flipped = PR_SECTOR
        elif sector == PR_SECTOR:
            flipped = PQ_SECTOR
        else:
            raise RuntimeError("an unexpected chart sector reached iota")
        add_value(answer, (flipped, monomial), value)
    return answer


def odd_part(vector):
    return scale(add_vectors(vector, scale(iota(vector), -1)), QQ(1, 2))


def marked_edges_for(deleted_site):
    return (
        BASE.edge(BASE.X, deleted_site, 0, 0),
        BASE.edge(BASE.P, BASE.Q_SITE, 0, 0),
    )


def audit():
    # ---- A and B, swept over every global word and every marking. --------
    words_scanned = 0
    nonzero_tails = 0
    marked_support_words = {site: [] for site in BASE.ODD}
    polar = {}

    for word in product(BASE.COLORS, repeat=8):
        words_scanned += 1
        row = BASE.full_nine_polynomial(word)
        require(len(row) == 90, "a direct-free row lost its 90 matchings")

        pq_direct, pq_stars = BASE.chart_partition(
            word, (BASE.P, BASE.Q_SITE))
        pr_direct, pr_stars = BASE.chart_partition(word, (BASE.P, BASE.R))

        # A: the two charts partition the SAME global row.
        require(set(pq_direct) | set(pq_stars) == set(row),
                "the pq chart lost a global matching")
        require(set(pr_direct) | set(pr_stars) == set(row),
                "the pr chart lost a global matching")
        # The direct-free hypothesis: the pr chart has no direct piece.
        require(len(pr_direct) == 0 and len(pr_stars) == 90,
                "the direct-free pr chart split changed")
        require(len(pq_direct) == 15 and len(pq_stars) == 75,
                "the pq chart split changed")

        for deleted_site in BASE.ODD:
            marks = marked_edges_for(deleted_site)
            pq_direct_tail = BASE.sparse_derivative(pq_direct, marks)
            pq_star_tail = BASE.sparse_derivative(pq_stars, marks)
            pr_direct_tail = BASE.sparse_derivative(pr_direct, marks)
            pr_star_tail = BASE.sparse_derivative(pr_stars, marks)

            # B: all pq marked material is direct; all pr marked material is
            # two-star; and the two chart tails are the same polynomial.
            require(not pq_star_tail,
                    "a pq marked tail escaped its direct sector")
            require(not pr_direct_tail,
                    "a pr marked tail entered the empty direct sector")
            require(pq_direct_tail == pr_star_tail,
                    "the two chart marked tails stopped being equal")

            if pq_direct_tail:
                nonzero_tails += 1
                marked_support_words[deleted_site].append(word)

    require(words_scanned == 3 ** 8 == 6561,
            "the global word sweep changed size")
    # The marking needs colour zero at x, v, p, q, leaving the other four
    # odd sites free: 3^4 = 81 words per deletion site.
    for deleted_site in BASE.ODD:
        require(len(marked_support_words[deleted_site]) == 81,
                "the marked-support word count changed")
    require(nonzero_tails == 5 * 81 == 405,
            "the total nonzero marked-tail count changed")

    # ---- The five selected polar rows, and their cochains. ---------------
    for deleted_site in BASE.ODD:
        word = [0] * 8
        for site in BASE.ODD:
            if site != deleted_site:
                word[site] = BASE.MIXED_ODD[site - 1]
        word = tuple(word)
        require("".join(map(str, word))
                == BASE.EXPECTED_GLOBAL_ROWS[deleted_site],
                "one labelled global polar row changed")
        require(word in marked_support_words[deleted_site],
                "a selected polar row left the marked support")
        marks = marked_edges_for(deleted_site)
        marked = BASE.sparse_derivative(
            tuple(BASE.full_nine_polynomial(word)), marks)
        require(len(marked) == 3 and set(marked.values()) == {1},
                "one marked polar stopped being a three-term hafnian")
        polar[deleted_site] = dict(marked)

    cochains = {
        deleted_site: {
            **{(PQ_SECTOR, monomial): QQ(1, 6)
               for monomial in polar[deleted_site]},
            **{(PR_SECTOR, monomial): QQ(-1, 6)
               for monomial in polar[deleted_site]},
        }
        for deleted_site in BASE.ODD
    }

    # ---- C: every chart-odd tail is a kernel-vector tail. ----------------
    # Build the whole chart-labelled column family in the marked support of
    # each deletion site, and check that the chart-odd part of an arbitrary
    # combination is the tail of the corresponding kernel combination.
    rigidity_checks = 0
    for deleted_site in BASE.ODD:
        marks = marked_edges_for(deleted_site)
        support_words = marked_support_words[deleted_site]

        # Build the two chart tails INDEPENDENTLY, each from its own chart
        # partition.  Tagging one shared polynomial into both sectors would
        # make the identity below hold for any polynomial whatsoever; going
        # through chart_partition twice is what makes it depend on Fact B.
        tails = []
        for word in support_words:
            pq_direct, _pq_stars = BASE.chart_partition(
                word, (BASE.P, BASE.Q_SITE))
            _pr_direct, pr_stars = BASE.chart_partition(
                word, (BASE.P, BASE.R))
            pq_common = BASE.sparse_derivative(pq_direct, marks)
            pr_common = BASE.sparse_derivative(pr_stars, marks)
            require(pq_common and pr_common,
                    "a marked-support word lost one of its chart tails")
            tails.append((
                tagged(PQ_SECTOR, pq_common),   # column r_w^{pq}
                tagged(PR_SECTOR, pr_common),   # column r_w^{pr}
                pq_common,
                pr_common,
            ))

        # Deterministic exact rational coefficients, one pair per column.
        for trial in range(3):
            combination = {}
            kernel_tail = {}
            for index, (pq_tail, pr_tail, pq_common, pr_common) in enumerate(
                    tails):
                left = QQ(index + 1 + trial, 2 * trial + 3)
                right = QQ(index - 2 * trial, 5 + trial)
                combination = add_vectors(
                    combination,
                    scale(pq_tail, left),
                    scale(pr_tail, right),
                )
                # The kernel element k_w enters with coefficient
                # (left - right)/2, and its tail is the chart-odd square.
                # Note the square is built from the pq tail on both sides:
                # that is only legitimate BECAUSE Fact B says the two chart
                # tails are equal, so this identity has real content.
                kernel_tail = add_vectors(
                    kernel_tail,
                    scale(add_vectors(
                        tagged(PQ_SECTOR, pq_common),
                        scale(tagged(PR_SECTOR, pq_common), -1),
                    ), QQ(left - right, 2)),
                )
            require(odd_part(combination) == kernel_tail,
                    "a chart-odd part is not a kernel-vector tail")
            require(iota(kernel_tail) == scale(kernel_tail, -1),
                    "a kernel-vector tail stopped being chart-odd")
            # And the cochain sees only that kernel-vector tail.
            for site in BASE.ODD:
                require(pairing(combination, cochains[site])
                        == pairing(kernel_tail, cochains[site]),
                        "the cochain saw more than the kernel-vector tail")
            rigidity_checks += 1
    require(rigidity_checks == 15,
            "the rigidity trial count changed")

    # ---- ker A' really is spanned by the k_w: the rows are independent. --
    # A labelled matching monomial records the colour of every site, since
    # each site lies in exactly one edge.  So a monomial determines its
    # word, the 6561 row supports are pairwise disjoint, and the rows are
    # linearly independent.  This is the inclusion that upgrades
    # {chart-odd literal tails} subset T'(ker A') to an equality.
    seen_monomial_words = {}
    for word in product(BASE.COLORS, repeat=8):
        for monomial in BASE.full_nine_polynomial(word):
            recovered = [None] * 8
            for left, right, left_color, right_color in monomial:
                recovered[left] = left_color
                recovered[right] = right_color
            require(tuple(recovered) == word,
                    "a labelled monomial failed to determine its word")
            previous = seen_monomial_words.get(monomial)
            require(previous is None or previous == word,
                    "two distinct words share a labelled monomial")
            seen_monomial_words[monomial] = word
    require(len(seen_monomial_words) == 6561 * 90,
            "the row supports stopped being pairwise disjoint")

    # ---- The connecting map over the WHOLE literal source complex. -------
    # The companion chart-parity note was refuted by a chart-odd witness
    # supported on a SINGLE monomial of h_v.  No literal source tail is
    # like that: a marked derivative of a hafnian is always a full
    # three-term face hafnian.  Sweeping every word makes this exact, and
    # is what section 3 of the note needs over all of ker A'.
    nonzero_connecting = {site: [] for site in BASE.ODD}
    for deleted_site in BASE.ODD:
        marks = marked_edges_for(deleted_site)
        for word in product(BASE.COLORS, repeat=8):
            pq_direct, _stars = BASE.chart_partition(
                word, (BASE.P, BASE.Q_SITE))
            tail = BASE.sparse_derivative(pq_direct, marks)
            if not tail:
                continue
            mass = sum(
                (QQ(tail.get(monomial, 0))
                 for monomial in polar[deleted_site]),
                QQ(0),
            )
            if mass:
                nonzero_connecting[deleted_site].append(
                    ("".join(map(str, word)), mass / 3))
    for deleted_site in BASE.ODD:
        entries = nonzero_connecting[deleted_site]
        require(len(entries) == 1,
                "more than one literal source tail met a polar cochain")
        selected_word, value = entries[0]
        require(selected_word == BASE.EXPECTED_GLOBAL_ROWS[deleted_site],
                "the sole contributing word is not the selected polar row")
        require(value == 1,
                "the sole contributing literal tail stopped pairing to 1")

    # ---- The connecting map is the identity on the selected squares. -----
    squares = {
        deleted_site: add_vectors(
            tagged(PQ_SECTOR, polar[deleted_site]),
            scale(tagged(PR_SECTOR, polar[deleted_site]), -1),
        )
        for deleted_site in BASE.ODD
    }
    identity5 = tuple(
        tuple(QQ(1) if row == column else QQ(0) for column in range(5))
        for row in range(5)
    )
    connecting = tuple(
        tuple(pairing(squares[column], cochains[row])
              for column in BASE.ODD)
        for row in BASE.ODD
    )
    require(connecting == identity5,
            "the connecting matrix on the selected squares is not I_5")

    ledger = {
        "global_words_scanned": words_scanned,
        "charts_partition_same_row": True,
        "pr_direct_piece_empty": True,
        "chart_marked_tails_equal": True,
        "nonzero_marked_tails": nonzero_tails,
        "marked_support_words_per_site": 81,
        "rigidity_trials": rigidity_checks,
        "chart_odd_equals_kernel_tail": True,
        "row_supports_pairwise_disjoint": True,
        "distinct_labelled_monomials": len(seen_monomial_words),
        "literal_tails_meeting_each_cochain": 1,
        "sole_contributing_word_is_selected_row": True,
        "connecting_matrix": [
            [[value.numerator, value.denominator] for value in row]
            for row in connecting
        ],
        "conclusion": (
            "over all 6561 global words the two charts partition the same "
            "row and carry the same marked tail; the row supports are "
            "pairwise disjoint so ker A' is spanned by the k_w; every "
            "chart-odd literal tail is therefore T'(kappa) for a kernel "
            "element kappa; and exactly one literal tail per site meets "
            "each polar cochain, with value 1, so the connecting map over "
            "the whole literal complex is I_5.  Among literal tails -I_5 "
            "is reachable only as the tail of -k_v"
        ),
        "scope": (
            "finite h=3 direct-free statement; does not exclude a tail that "
            "is not a literal chart-labelled source tail, constructs no "
            "replacement comparison, and leaves Krenn's conjecture open"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "h3 full-nine connecting-class rigidity ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h=3 full-nine connecting-class rigidity: PASS (exact)")
    print("global words scanned:              ",
          ledger["global_words_scanned"])
    print("two charts partition the same row: ",
          ledger["charts_partition_same_row"])
    print("two chart marked tails equal:      ",
          ledger["chart_marked_tails_equal"])
    print("nonzero marked tails:              ",
          ledger["nonzero_marked_tails"])
    print("chart-odd tail = kernel-vector tail:",
          ledger["chart_odd_equals_kernel_tail"])
    print("connecting matrix:                  I_5")
    print("literal tails meeting each cochain: ",
          ledger["literal_tails_meeting_each_cochain"],
          "(the selected polar row, value 1)")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
