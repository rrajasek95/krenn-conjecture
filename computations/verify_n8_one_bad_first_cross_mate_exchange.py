#!/usr/bin/env python3
"""Audit the first cancellation mate on the sharp one-bad N=8 boundary.

The pinned sharp-boundary census has two source-oriented representatives.
Each has two private off-diagonal response matchings.  On the four sites
left by either ordered star pair there are exactly two alternative perfect
matchings.  Add the two decorated cells of one alternative matching and
audit the full six-site top tensor.

All eight representative mate charts acquire a coefficient with a unique
mixed top matching.  Thus a direct first mate can cancel the private cross
monomial only by creating a new forbidden top monomial; any completion must
provide a second, coupled cancellation channel.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "computations/verify_n8_one_bad_binary_projection_minimal_counterguards.py"
BASE_HASH = "2b32c6d50ea1dda5a7b412a0fcd6de2373ab483b5b25eba7352684a5499e8f28"
EXPECTED_DIGEST = "41ef349f6519b37919056b4d5eef10f4b177bb95a639b0aedc065d24e0207300"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load_base():
    path = ROOT / BASE
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == BASE_HASH, f"dependency changed: {BASE}: {actual}")
    spec = spec_from_file_location("one_bad_binary_base", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def endpoint_tensor(cells, number, fixed=()):
    """Expand endpoint-coloured cells; edge orientation is increasing."""
    answer = Counter()
    for indices in itertools.combinations(range(len(cells)), number):
        chosen = [cells[index] for index in indices]
        occupied = [site for edge, colours in chosen for site in edge]
        occupied += [site for site, colour in fixed]
        if len(occupied) != 6 or len(set(occupied)) != 6:
            continue
        word = [None] * 6
        for edge, colours in chosen:
            word[edge[0]], word[edge[1]] = colours
        for site, colour in fixed:
            word[site] = colour
        answer[tuple(word)] += 1
    return answer


def decorated_matching(physical_matching, word):
    return tuple((edge, (word[edge[0]], word[edge[1]]))
                 for edge in physical_matching)


def top_decompositions(base, edges, word):
    answer = []
    for triple in itertools.combinations(edges, 3):
        if endpoint_tensor(triple, 3).get(word):
            answer.append(triple)
    return answer


def audit_mates(base):
    charts = []
    signatures = Counter()
    for orbit_index, packet in enumerate(base.SHARP_REPRESENTATIVES):
        a_matching, b_matching, b_holes, c_matching, c_holes = packet
        source = (
            tuple((edge, (base.A, base.A)) for edge in a_matching)
            + tuple((edge, (base.B, base.B)) for edge in b_matching)
            + tuple((edge, (base.C, base.C)) for edge in c_matching)
        )
        require(endpoint_tensor(source, 3)
                == Counter({(base.A,) * 6: 1}),
                "a sharp representative lost its pure top")

        channels = (
            ("bc", base.B, base.C, b_holes[0], c_holes[1]),
            ("cb", base.C, base.B, c_holes[0], b_holes[1]),
        )
        for name, left_colour, right_colour, left_hole, right_hole in channels:
            require(left_hole != right_hole,
                    "a private response became site-zero")
            fixed = ((left_hole, left_colour),
                     (right_hole, right_colour))
            private = endpoint_tensor(source, 2, fixed)
            require(len(private) == 1 and next(iter(private.values())) == 1,
                    "a cross response stopped being a private unit")
            word = next(iter(private))
            residual = tuple(site for site in base.SITES
                             if site not in (left_hole, right_hole))

            physical = tuple(base.perfect_matchings(residual))
            require(len(physical) == 3,
                    "the four-site matching count changed")
            decorated = tuple(decorated_matching(matching, word)
                              for matching in physical)
            old = tuple(matching for matching in decorated
                        if all(cell in source for cell in matching))
            require(len(old) == 1,
                    "the private cross row lost its unique old matching")
            alternatives = tuple(matching for matching in decorated
                                 if frozenset(matching) != frozenset(old[0]))
            require(len(alternatives) == 2,
                    "the private row lost an alternate K4 matching")

            for mate in alternatives:
                require(all(cell not in source for cell in mate),
                        "an alternate response mate reused a sharp cell")
                enlarged = source + mate
                repaired = endpoint_tensor(enlarged, 2, fixed)
                require(repaired[word] == 2,
                        "the added mate did not supply the second cross route")

                top = endpoint_tensor(enlarged, 3)
                pure_excess = top[(base.A,) * 6] - 1
                mixed = {
                    output: coefficient
                    for output, coefficient in top.items()
                    if output != (base.A,) * 6
                }
                require(mixed, "a first mate did not create a mixed top")
                private_mixed = []
                for output, coefficient in mixed.items():
                    decompositions = top_decompositions(base, enlarged, output)
                    if coefficient == 1 and len(decompositions) == 1:
                        private_mixed.append((output, decompositions[0]))
                require(private_mixed,
                        "the mate-created top lost its private coefficient")
                require(all(any(cell in mate for cell in decomposition)
                            for output, decomposition in private_mixed),
                        "a reported top witness does not use the mate")

                signature = (len(mixed), pure_excess)
                signatures[signature] += 1
                charts.append({
                    "sharp_orbit": orbit_index,
                    "channel": name,
                    "holes": [left_hole, right_hole],
                    "old_matching": [list(cell[0]) for cell in old[0]],
                    "mate": [[list(edge), list(colours)]
                             for edge, colours in mate],
                    "mixed_top_words": [list(output) for output in mixed],
                    "private_top_witnesses": [
                        {
                            "word": list(output),
                            "matching": [[list(edge), list(colours)]
                                         for edge, colours in decomposition],
                        }
                        for output, decomposition in private_mixed
                    ],
                    "extra_pure_a_routes": pure_excess,
                })

    require(len(charts) == 8, "the first-mate chart count changed")
    require(signatures == Counter({(2, 0): 4, (1, 1): 4}),
            f"the first-mate signatures changed: {signatures}")
    return {
        "source_orbits": 2,
        "private_channels_per_orbit": 2,
        "alternate_matchings_per_channel": 2,
        "representative_mate_charts": len(charts),
        "labelled_mate_charts": 1440 * 2 * 2,
        "signatures": [
            {
                "mixed_top_words": mixed,
                "extra_pure_a_routes": pure,
                "representative_charts": count,
            }
            for (mixed, pure), count in sorted(signatures.items())
        ],
        "charts": charts,
        "verdict": (
            "every direct first alternate-matching mate creates a private "
            "mixed top coefficient"
        ),
    }


def main():
    base = load_base()
    audit = audit_mates(base)
    ledger = {
        "base": {"path": BASE, "sha256": BASE_HASH},
        "first_cross_mate_exchange": audit,
        "scope": (
            "sharp seven-cell support plus one direct alternate response "
            "matching; simultaneous higher repairs are not excluded"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"first-mate exchange ledger changed: {digest}")

    print("N=8 one-bad first cross-mate exchange: PASS")
    print("representative / labelled mate charts: 8 / 5760")
    print("all mates create a private mixed top coefficient")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
