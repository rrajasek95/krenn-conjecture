#!/usr/bin/env python3
"""Exact exhaustion of weighted same-colour three-term polarized supports.

The exhaustive combinatorics and sound Gram-closure rules live in the
companion exploration module.  This locked verifier replays all normalized
flagged supports, asserts the exact counts, and hashes the complete ordered
certificate ledger.
"""

from __future__ import annotations

import hashlib

import explore_polarized_three_term_pair_cap_gram_patterns as explore


EXPECTED_EXACT = 9888
EXPECTED_SEVEN_ENTRY = 7968
EXPECTED_CLOSURE_ONLY = 1920
EXPECTED_SHA256 = "5f42b78f2f972ed25a96f6ea01a25dcaf2b1c108174ba0fe2d0804132dddb639"


def main():
    base = (((0, 1), (2, 3), (4, 5), (6, 7)), (0, 1))
    digest = hashlib.sha256()
    exact_count = 0
    seven_entry_count = 0
    closure_only_count = 0

    assert len(explore.MATCHINGS8) == 105
    assert len(explore.FLAGGED) == 420
    assert len(explore.FLAGGED) ** 2 == 176400

    for flagged1 in explore.FLAGGED:
        for flagged2 in explore.FLAGGED:
            flagged = (base, flagged1, flagged2)
            q_by_edge, q_cells = explore.q_table(flagged)
            if not explore.exact_polarized(flagged, q_by_edge):
                continue
            exact_count += 1
            word_map, q_four = explore.word_data(q_cells)

            # Every exact support has one literal ps contributor to each
            # pure word and no pure q^[4] contribution.
            for colour, (_, distinguished) in enumerate(flagged):
                expected = ((distinguished[0], colour),
                            (distinguished[1], colour))
                assert word_map[(colour,) * 8] == [expected]
                assert q_four[(colour,) * 8] == 0

            seven_entry = explore.gram_pattern(flagged, word_map, q_four)
            closure = explore.six_mode_zero_contradiction(
                flagged, word_map, q_four
            )
            assert seven_entry or closure
            if seven_entry:
                seven_entry_count += 1
            else:
                assert closure
                closure_only_count += 1
            digest.update(repr((flagged1, flagged2, int(seven_entry))).encode())
            digest.update(b"\n")

    assert exact_count == EXPECTED_EXACT
    assert seven_entry_count == EXPECTED_SEVEN_ENTRY
    assert closure_only_count == EXPECTED_CLOSURE_ONLY
    assert digest.hexdigest() == EXPECTED_SHA256

    print("eight-site three-term pair-cap exhaustion: PASS")
    print("105 matchings, 420 flagged matchings, 176400 normalized pairs: PASS")
    print("9888 combinatorially three-term same-colour supports: PASS")
    print("singleton coefficients are nonzero monomials for all nonzero weights: PASS")
    print("7968 seven-entry + 1920 closure-only Gram contradictions: PASS")
    print(f"certificate-ledger SHA-256: {digest.hexdigest()}")
    print("all 9888 fixed-support pair-cap preimages excluded: PASS")


if __name__ == "__main__":
    main()
