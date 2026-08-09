#!/usr/bin/env python3
"""Exhaust least-extra exact-ten blocks 4 and 5 (with empty 2 and 3)."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256

import search_n8_sharp_full_fibre_completion as sharp
import search_n8_sparse_triple_completion as sparse


EXPECTED_BLOCK_COUNTS = {2: 0, 3: 0, 4: 136, 5: 1442}
EXPECTED_OUTCOMES = Counter({"odd": 1327, "one-class": 251})
EXPECTED_LEDGER_SHA256 = (
    "9916a56a1c33d90911cbde66abc67a032386cdbf9120ae7059a3d74a5fa96125"
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
        require(optional[:6] == (
            (0, 1, 0, 1), (0, 1, 0, 2), (0, 1, 1, 0),
            (0, 1, 1, 1), (0, 1, 1, 2), (0, 1, 2, 0),
        ), "least optional cells changed")

        block_counts = Counter({block: 0 for block in range(2, 6)})
        outcomes = Counter()
        term_sizes = Counter()
        quotient_profiles = Counter()
        ledger = []
        for block in range(2, 6):
            assumptions = (
                [instance.support[optional[block]]]
                + [-instance.support[cell] for cell in optional[:block]]
            )
            while instance.solver.solve(assumptions=assumptions):
                selected = instance.decode(instance.solver.get_model())
                extra = frozenset(selected - sharp.SEED)
                require(len(extra) == 10, "block support is not exact-ten")
                require(optional[block] in extra
                        and not (set(optional[:block]) & extra),
                        "support escaped its least-extra block")
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
                        print("THIRD_TYPE_BLOCK", block,
                              "EXTRA", sorted(extra), flush=True)
                        raise RuntimeError("genuine multi-class third type")
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

                block_counts[block] += 1
                outcomes[outcome] += 1
                ledger.append(
                    f"{block}:{support_word(extra)}|{witness}\n"
                )
                instance.add_hard_clause(
                    [-instance.support[cell] for cell in sorted(extra)]
                )

        require(dict(block_counts) == EXPECTED_BLOCK_COUNTS,
                "block 2--5 support counts changed")
        require(outcomes == EXPECTED_OUTCOMES,
                "block 4/5 outcomes changed")
        ledger_hash = sha256(
            "".join(sorted(ledger)).encode("ascii")
        ).hexdigest()
        if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
            require(ledger_hash == EXPECTED_LEDGER_SHA256,
                    "block 4/5 signed ledger changed")

        print("least-extra block counts:", dict(sorted(block_counts.items())))
        print("augmented-group outcomes:", dict(sorted(outcomes.items())))
        print("one-class witness term sizes:", dict(sorted(term_sizes.items())))
        print("binomial/HNF profile count:", len(quotient_profiles))
        print("signed certificate ledger sha256:", ledger_hash)
        print("third types: 0")
    finally:
        instance.delete()


if __name__ == "__main__":
    main()
