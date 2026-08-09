#!/usr/bin/env python3
"""Exhaust least-extra exact-ten block 6 with the integral signed HNF.

This is an additive continuation of blocks 0--5.  No rational row-echelon
quotient is used: every binomial character and every residual fibre is
reduced by the row Hermite normal form of

    <(exponent_difference, 1), (0, 2)> in Z^253.

The complete HNF and a replayed terminal fibre enter the frozen ledger.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256

import search_n8_sharp_full_fibre_completion as sharp
import search_n8_sparse_triple_completion as sparse


BLOCK = 6
EXPECTED_BLOCK_CELL = (0, 1, 2, 1)
EXPECTED_BLOCK_COUNT = 712
EXPECTED_OUTCOMES = Counter({"odd": 667, "one-class": 45})
EXPECTED_LEDGER_SHA256 = (
    "a8df813c3eeb425d6ea0e48844b9a4ecccd926f11a3c54c5a15a236dc1fbf9fa"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(value) -> str:
    return sha256(repr(value).encode("ascii")).hexdigest()


def support_word(extra) -> str:
    return ",".join("".join(map(str, cell)) for cell in sorted(extra))


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
        families = tuple(
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
        require(optional[BLOCK] == EXPECTED_BLOCK_CELL,
                f"least optional block-{BLOCK} cell changed")
        assumptions = (
            [instance.support[optional[BLOCK]]]
            + [-instance.support[cell] for cell in optional[:BLOCK]]
        )

        block_count = 0
        outcomes = Counter()
        term_sizes = Counter()
        quotient_profiles = Counter()
        ledger = []
        while instance.solver.solve(assumptions=assumptions):
            selected = instance.decode(instance.solver.get_model())
            extra = frozenset(selected - sharp.SEED)
            require(len(extra) == 10, "block support is not exact-ten")
            require(optional[BLOCK] in extra
                    and not (set(optional[:BLOCK]) & extra),
                    f"support escaped least-extra block {BLOCK}")
            require(all(
                any(requirement <= extra for requirement in family)
                for family in families
            ), "support misses an original mate obligation")
            require(all(
                not all(
                    any(requirement <= extra - {cell}
                        for requirement in family)
                    for family in families
                )
                for cell in extra
            ), "support is not inclusion-minimal")

            fibres = sharp.supported_fibres(selected, instance.matchings)
            _mixed, rows = sparse.binomial_system(instance, fibres)
            consistent, lattice = sparse.toric.signed_quotient_lattice(
                rows, len(instance.cells)
            )
            lattice_hash = digest(lattice)
            quotient_profiles[len(rows), len(lattice[0])] += 1
            if not consistent:
                sign_remainder = sparse.toric.quotient_key(
                    (0,) * len(instance.cells) + (1,), lattice
                )
                require(not any(sign_remainder),
                        "odd support retained its sign generator")
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
                        one_class.append(
                            (len(terms), word, coefficient, signed_class)
                        )
                if not one_class:
                    print("THIRD_TYPE_BLOCK", BLOCK,
                          "EXTRA", sorted(extra), flush=True)
                    raise RuntimeError(
                    f"block {BLOCK} integral signed HNF leaves a "
                    "multi-class third type"
                    )
                term_count, word, coefficient, signed_class = min(
                    one_class, key=lambda item: (-item[0], item[1])
                )
                require(coefficient != 0, "one-class coefficient vanished")
                require(sparse.reduced_polynomial(
                    instance, fibres[word], lattice
                ) == {signed_class: coefficient},
                    "one-class witness did not replay")
                outcome = "one-class"
                term_sizes[term_count] += 1
                witness = (
                    f"M:{lattice_hash}:{''.join(map(str, word))}:"
                    f"{term_count}:{coefficient}:{digest(signed_class)}"
                )

            block_count += 1
            outcomes[outcome] += 1
            ledger.append(f"{support_word(extra)}|{witness}\n")
            instance.add_hard_clause(
                [-instance.support[cell] for cell in sorted(extra)]
            )

        ledger_hash = sha256(
            "".join(sorted(ledger)).encode("ascii")
        ).hexdigest()
        if EXPECTED_BLOCK_COUNT is not None:
            require(block_count == EXPECTED_BLOCK_COUNT,
                    f"block-{BLOCK} support count changed")
        if EXPECTED_OUTCOMES is not None:
            require(outcomes == EXPECTED_OUTCOMES,
                    f"block-{BLOCK} signed-HNF outcomes changed")
        if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
            require(ledger_hash == EXPECTED_LEDGER_SHA256,
                    f"block-{BLOCK} signed ledger changed")

        print(f"least-extra block {BLOCK} count:", block_count)
        print("integral augmented-HNF outcomes:", dict(sorted(outcomes.items())))
        print("one-class witness term sizes:", dict(sorted(term_sizes.items())))
        print("binomial/HNF profile count:", len(quotient_profiles))
        print("signed certificate ledger sha256:", ledger_hash)
        print("third types: 0")
    finally:
        instance.delete()


if __name__ == "__main__":
    main()
