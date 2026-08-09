#!/usr/bin/env python3
"""Exhaust the first two lexicographic exact-ten augmented-group blocks.

For every inclusion-minimal ten-cell repair in a fixed least-extra-cell
block, form the full augmented signed exponent quotient

    (Z^252 + Z/2) / <(d_j, 1)>.

The support is certified either by the sign unit (an odd binomial holonomy)
or by a mixed fibre whose reduced polynomial has one nonzero signed Laurent
class.  The exact HNF quotient and witness provenance enter the frozen ledger.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256

import search_n8_sharp_full_fibre_completion as sharp
import search_n8_sparse_triple_completion as sparse


EXPECTED_SUPPORTS = 2972
EXPECTED_OUTCOMES = Counter({"odd": 2028, "one-class": 944})
EXPECTED_LEDGER_SHA256 = (
    "7bc2097e5c153dea896a8fea37eef725a60f205ad9f7cf0ca40f08f87d1e2826"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def object_digest(value) -> str:
    return sha256(repr(value).encode("ascii")).hexdigest()


def cell_word(cell) -> str:
    return "".join(map(str, cell))


def support_word(extra) -> str:
    return ",".join(cell_word(cell) for cell in sorted(extra))


def main() -> None:
    small_repairs = sharp.direct_frontier("glucose42")
    instance = sharp.TightNoSingletonSearch(26, "glucose42")
    try:
        seed_fibres = sharp.supported_fibres(sharp.SEED, instance.matchings)
        original = tuple(
            (word, terms[0][0])
            for word, terms in sorted(seed_fibres.items())
            if len(set(word)) > 1 and len(terms) == 1
        )
        require(len(original) == 11, "seed singleton obligations changed")
        requirement_families = tuple(
            sharp.minimal_mate_requirements(
                instance, word, trigger, sharp.SEED
            )
            for word, trigger in original
        )
        for word, trigger in original:
            instance.add_singleton_gadget(word, trigger)
        for repair in small_repairs:
            instance.add_hard_clause(
                [-instance.support[cell] for cell in sorted(repair)]
            )

        optional = tuple(cell for cell in instance.cells
                         if cell not in sharp.SEED)
        require(optional[:2] == ((0, 1, 0, 1), (0, 1, 0, 2)),
                "least optional cells changed")

        # Block 0 is an exact empty block.
        require(not instance.solver.solve(
            assumptions=[instance.support[optional[0]]]
        ), "least-extra block 0 acquired a support")

        assumptions = [
            instance.support[optional[1]],
            -instance.support[optional[0]],
        ]
        ledger = []
        outcomes = Counter()
        witness_term_sizes = Counter()
        quotient_profiles = Counter()

        while instance.solver.solve(assumptions=assumptions):
            selected = instance.decode(instance.solver.get_model())
            extra = frozenset(selected - sharp.SEED)
            require(len(extra) == 10, "block support is not exact-ten")
            require(optional[1] in extra and optional[0] not in extra,
                    "support escaped least-extra block 1")
            require(all(
                any(requirement <= extra for requirement in family)
                for family in requirement_families
            ), "block support misses an original mate obligation")
            require(all(
                not all(
                    any(requirement <= extra - {cell}
                        for requirement in family)
                    for family in requirement_families
                )
                for cell in extra
            ), "block support is not an inclusion-minimal direct repair")

            fibres = sharp.supported_fibres(selected, instance.matchings)
            _mixed, rows = sparse.binomial_system(instance, fibres)
            consistent, lattice = sparse.toric.signed_quotient_lattice(
                rows, len(instance.cells)
            )
            lattice_hash = object_digest(lattice)
            quotient_profiles[len(rows), len(lattice[0])] += 1

            if not consistent:
                # Exact replay of the augmented-group sign unit.
                sign_remainder = sparse.toric.quotient_key(
                    (0,) * len(instance.cells) + (1,), lattice
                )
                require(not any(sign_remainder),
                        "odd support did not kill the sign generator")
                outcome = "odd"
                witness = f"O:{lattice_hash}"
            else:
                one_class = []
                for word, terms in sorted(fibres.items()):
                    if len(set(word)) == 1:
                        continue
                    remainder = sparse.reduced_polynomial(
                        instance, terms, lattice
                    )
                    if len(remainder) == 1:
                        (signed_class, coefficient), = remainder.items()
                        require(coefficient != 0,
                                "one-class coefficient vanished")
                        one_class.append(
                            (len(terms), word, coefficient, signed_class)
                        )
                if not one_class:
                    print("THIRD_TYPE_EXTRA", sorted(extra), flush=True)
                    raise RuntimeError(
                        "genuine multi-class third type entered block 1"
                    )
                # Prefer the most informative (largest) fibre, then the
                # lexicographically first word.  Singleton witnesses remain
                # admissible and are explicitly counted.
                term_count, word, coefficient, signed_class = min(
                    one_class, key=lambda item: (-item[0], item[1])
                )
                replay = sparse.reduced_polynomial(
                    instance, fibres[word], lattice
                )
                require(replay == {signed_class: coefficient},
                        "one-class witness did not replay")
                outcome = "one-class"
                witness_term_sizes[term_count] += 1
                witness = (
                    f"M:{lattice_hash}:{''.join(map(str, word))}:"
                    f"{term_count}:{coefficient}:"
                    f"{object_digest(signed_class)}"
                )

            outcomes[outcome] += 1
            ledger.append(f"{support_word(extra)}|{witness}\n")
            # Because every admissible support has ten extras, this clause
            # excludes exactly the current support inside the cap.
            instance.add_hard_clause(
                [-instance.support[cell] for cell in sorted(extra)]
            )

        require(len(ledger) == EXPECTED_SUPPORTS,
                "block-1 support count changed")
        require(outcomes == EXPECTED_OUTCOMES,
                "block-1 augmented-group outcomes changed")
        digest = sha256("".join(sorted(ledger)).encode("ascii")).hexdigest()
        if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
            require(digest == EXPECTED_LEDGER_SHA256,
                    "block-1 signed certificate ledger changed")

        print("least-extra blocks 0/1: 0 /", len(ledger))
        print("augmented-group outcomes:", dict(sorted(outcomes.items())))
        print("one-class witness term sizes:",
              dict(sorted(witness_term_sizes.items())))
        print("binomial/HNF profile count:", len(quotient_profiles))
        print("signed certificate ledger sha256:", digest)
        print("third types: 0")
    finally:
        instance.delete()


if __name__ == "__main__":
    main()
