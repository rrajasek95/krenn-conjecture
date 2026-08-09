#!/usr/bin/env python3
"""Exact structural audit and frozen CNF frontier for N=8 D1 at m=10.

This does not claim the m=10 frontier is empty.  It proves completeness of
the 3/4-anchor normal forms through one-colour size seven, counts the exact
anchor-state quotient, applies every currently available repair certificate
symbolically, and freezes a small exact CNF for the first 3+3+4 support-base
family.  A checked UNSAT proof for that CNF remains future work.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import itertools
import math
import os
import sys
from collections import Counter
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_M9_SHA256 = (
    "2ce3219230392c7c162cf55b1e7c94c583e90b35f06eea892c7576a9ec060ae8"
)
M9_PATH = os.path.join(HERE, "verify_n8_d1_m9_support_shadow_closure.py")
with open(M9_PATH, "rb") as handle:
    M9_SHA256 = hashlib.sha256(handle.read()).hexdigest()
require(M9_SHA256 == PINNED_M9_SHA256,
        "the committed m=9 support-shadow source changed")
M9 = importlib.import_module("verify_n8_d1_m9_support_shadow_closure")
M8 = M9.M8
N = M9.N
V = M9.V
D = M9.D

EXPECTED_DIMACS_SHA256 = (
    "f0a751847300019fb4a72c5b492340b476babd2c050ec0261bca5ffc049abdda"
)
EXPECTED_LEDGER_SHA256 = (
    "24100862cdf91cc587626d0c7b26e8b7490cf6709bcffd2c87551b8f125aa65e"
)


CORE_FIBRES = (
    ((0,1,2,3,4,5,6,7),(0,0,0,0,0,0,0,0),True),
    ((0,1,2,3,4,5,6,7),(0,0,1,1,0,0,1,1),False),
    ((0,1,2,3,4,5,6,7),(0,1,0,0,0,1,0,0),False),
    ((0,1,2,3,4,5,6,7),(0,1,1,1,0,1,1,1),False),
    ((0,1,2,3,4,5,6,7),(1,0,0,0,1,0,0,0),False),
    ((0,1,2,3,4,5,6,7),(1,0,1,1,0,0,1,1),False),
    ((0,1,2,3,4,5,6,7),(1,0,1,1,1,0,1,1),False),
    ((0,1,2,3,4,5,6,7),(1,1,1,1,1,0,0,0),False),
    ((0,1,2,3,4,5,6,7),(1,1,1,1,1,1,0,0),False),
    ((0,2,4,5,6,7),(0,1,0,0,1,1),False),
    ((0,2,4,5,6,7),(1,1,1,1,1,1),False),
    ((1,3,4,5,6,7),(1,1,0,1,1,1),False),
    ((1,3,4,5,6,7),(1,1,1,1,0,0),False),
    ((4,5,6,7),(0,0,1,1),False),
    ((4,5,6,7),(0,1,1,1),False),
    ((4,5,6,7),(1,0,1,1),False),
)


def monochrome_normal_forms_through_seven(colour, off_sigma):
    monochrome = sorted(entry for entry in off_sigma
                        if entry[2:] == (colour, colour))
    full_traces = {
        frozenset(V.cell(u, v, colour, colour) for u, v in matching
                  if V.cell(u, v, colour, colour) in off_sigma)
        for matching in V.MATCHINGS[V.SITES]
    }
    residue_matchings = {
        frozenset(V.cell(u, v, colour, colour) for u, v in matching)
        for matching in V.MATCHINGS[V.RESIDUE]
    }
    valid, minimal = {}, {}
    for size in range(2, 8):
        supports = set()
        for chosen in itertools.combinations(monochrome, size):
            support = frozenset(chosen)
            if not any(trace <= support for trace in full_traces):
                continue
            if sum(matching <= support
                   for matching in residue_matchings) == 1:
                continue
            supports.add(support)
        valid[size] = supports
        minimal[size] = {
            support for support in supports
            if not any(smaller <= support
                       for earlier in range(2, size)
                       for smaller in minimal[earlier])
        }
    require({size: len(rows) for size, rows in valid.items()}
            == {2: 0, 3: 72, 4: 1179, 5: 8382, 6: 34657,
                7: 95272},
            "the one-colour census through size seven changed")
    require({size: len(rows) for size, rows in minimal.items()}
            == {2: 0, 3: 72, 4: 27, 5: 0, 6: 0, 7: 0},
            "a new one-colour minimal normal form appeared")
    require(minimal[3] == {state[0] for state in N.triple_states(colour)}
            and minimal[4] == {
                state[0] for state in N.special_four_supports(colour)[0]
            }, "the constructive normal forms are incomplete")
    return {
        "valid_by_size": {size: len(rows)
                          for size, rows in sorted(valid.items())},
        "minimal_by_size": {size: len(rows)
                            for size, rows in sorted(minimal.items())},
    }


def repair_witness(state, additions, admissible, sigma, off_sigma,
                   off_cells, cell_index):
    certificates = M8.repair_certificates(
        state, additions, admissible, sigma, off_sigma
    )
    requirements = []
    for _word_key, repairs in certificates:
        requirements.append(tuple(sorted({
            M9.mask_for(repair, cell_index) for repair in repairs
        })))
    free_mask = M9.mask_for(off_sigma - set(state[0]), cell_index)
    visited = set()

    def search(chosen):
        if chosen in visited:
            return None
        visited.add(chosen)
        if chosen.bit_count() > additions:
            return None
        unsatisfied = [
            repairs for repairs in requirements
            if not any(chosen & repair == repair for repair in repairs)
        ]
        if not unsatisfied:
            witness = chosen
            for index in range(len(off_cells)):
                if witness.bit_count() == additions:
                    break
                bit = 1 << index
                if free_mask & bit and not witness & bit:
                    witness |= bit
            return witness if witness.bit_count() == additions else None
        options = []
        for repairs in unsatisfied:
            extensions = sorted({
                chosen | repair for repair in repairs
                if (chosen | repair).bit_count() <= additions
            })
            options.append((
                len(extensions),
                sum(extension.bit_count() - chosen.bit_count()
                    for extension in extensions),
                extensions,
            ))
        for extension in min(options)[2]:
            witness = search(extension)
            if witness is not None:
                return witness
        return None

    witness = search(0)
    return witness, len(certificates), len(visited)


def support_pair_orbits(first, second, group):
    pairs = {(left, right) for left in first for right in second}
    representatives = []
    while pairs:
        seed = min(pairs, key=lambda row: (tuple(sorted(row[0])),
                                           tuple(sorted(row[1]))))
        orbit = {
            (M8.map_set(seed[0], mapping), M8.map_set(seed[1], mapping))
            for mapping in group
        }
        pairs -= orbit
        representatives.append(seed)
    return representatives


def add_exact(cnf, variables, target):
    previous = {0: True}
    for index, variable in enumerate(variables, 1):
        current = {0: True}
        for level in range(1, min(index, target + 1) + 1):
            old_same = previous.get(level, False)
            old_lower = previous.get(level - 1, False)
            output = cnf.var(("COUNT", index, level))
            current[level] = output
            if old_same is False and old_lower is True:
                cnf.add(-output, variable)
                cnf.add(-variable, output)
            elif old_same is False:
                cnf.add(-output, old_lower)
                cnf.add(-output, variable)
                cnf.add(-old_lower, -variable, output)
            elif old_lower is True:
                cnf.add(-old_same, output)
                cnf.add(-variable, output)
                cnf.add(-output, old_same, variable)
            else:
                cnf.add(-output, old_same, old_lower)
                cnf.add(-output, old_same, variable)
                cnf.add(-old_same, output)
                cnf.add(-old_lower, -variable, output)
        previous = current
    cnf.add(previous[target])
    cnf.add(-previous[target + 1])


def build_frontier_cnf(base, admissible, sigma, off_sigma):
    base = set(base)
    require(len(base) == 6 and base <= off_sigma,
            "the frozen frontier base changed")
    cnf = M8.CNF()
    free = sorted(off_sigma - base)
    sigma_ids = {entry: cnf.var(("SIGMA", entry))
                 for entry in sorted(sigma)}
    off_ids = {entry: cnf.var(("EXTRA", entry)) for entry in free}
    add_exact(cnf, [off_ids[entry] for entry in free], 4)
    mandatory = set(V.BASE_UNITS) | {
        V.cell(0, 2, 2, 2), V.cell(1, 3, 2, 2),
    }
    for entry in sorted(mandatory):
        cnf.add(sigma_ids[entry])

    def matching_term(domain, values, word, matching):
        factors = []
        for u, v in matching:
            entry = V.cell(u, v, word[u], word[v])
            if entry not in admissible:
                return False
            if entry in base:
                continue
            factors.append(sigma_ids[entry] if entry in sigma
                           else off_ids[entry])
        return cnf.and_var(
            factors, ("TERM", tuple(domain), tuple(values), tuple(matching))
        )

    for domain, values, pure in CORE_FIBRES:
        require(tuple(domain) in V.MATCHINGS and len(values) == len(domain),
                "a frozen core fibre is malformed")
        expected_pure = (len(set(values)) == 1
                         if tuple(domain) == V.SITES else set(values) == {2})
        require(pure == expected_pure,
                "a frozen core fibre has the wrong target class")
        word = dict(zip(domain, values))
        terms, constants = [], 0
        for matching in V.MATCHINGS[tuple(domain)]:
            term = matching_term(domain, values, word, matching)
            if term is True:
                constants += 1
            elif term is not False:
                terms.append(term)
        if pure:
            if constants == 0:
                cnf.add(*terms)
            continue
        if constants >= 2:
            continue
        if constants == 1:
            cnf.add(*terms)
            continue
        if len(terms) == 1:
            cnf.add(-terms[0])
            continue
        if not terms:
            continue
        fibre_key = tuple(domain), tuple(values), pure
        prefix, current = [None] * len(terms), None
        for index, term in enumerate(terms):
            prefix[index] = current
            current = cnf.or_var(current, term,
                                 ("PRE", fibre_key, index))
        suffix, current = [None] * len(terms), None
        for index in range(len(terms) - 1, -1, -1):
            suffix[index] = current
            current = cnf.or_var(current, terms[index],
                                 ("SUF", fibre_key, index))
        for index, term in enumerate(terms):
            clause = [-term]
            if prefix[index] is not None:
                clause.append(prefix[index])
            if suffix[index] is not None:
                clause.append(suffix[index])
            cnf.add(*clause)
    return cnf


def dimacs_bytes(cnf):
    text = "p cnf %d %d\n" % (cnf.variable_count, len(cnf.clauses))
    text += "".join(" ".join(map(str, clause)) + " 0\n"
                    for clause in cnf.clauses)
    return text.encode("ascii")


def audit():
    started = monotonic()
    admissible, sigma, off_sigma, _kinds = V.reconstruct_support_domains()
    off_cells = sorted(off_sigma)
    cell_index = {entry: index for index, entry in enumerate(off_cells)}
    group = V.d1_group()
    normal_forms = {
        "b": monochrome_normal_forms_through_seven(0, off_sigma),
        "c": monochrome_normal_forms_through_seven(1, off_sigma),
    }
    triples = [N.triple_states(colour) for colour in (0, 1)]
    special = [N.special_four_supports(colour)[0] for colour in (0, 1)]
    families = (
        ("3+3+4", triples[0], triples[1], 4, 5184, 132,
         1159407480, 132, 0, 1, 876, 56),
        ("3+4+3", triples[0], special[1], 3, 2376, 64,
         18430720, 58, 6, 4, 875, 278),
        ("4+3+3", special[0], triples[1], 3, 2376, 64,
         18430720, 58, 6, 4, 954, 301),
        ("4+4+2", special[0], special[1], 2, 1089, 52,
         371280, 23, 29, 4, 546, 49),
    )
    family_rows = {}
    all_witnesses = []
    for (name, first, second, additions, expected_labelled,
         expected_orbits, expected_raw, expected_sat, expected_unsat,
         expected_zero, expected_nodes, expected_max_nodes) in families:
        labelled, representatives = M8.state_pair_orbits(first, second, group)
        require((labelled, len(representatives))
                == (expected_labelled, expected_orbits),
                "the %s anchor quotient changed" % name)
        raw = sum(math.comb(len(off_sigma) - len(state[0]), additions)
                  for state in representatives)
        sat, zero = 0, 0
        node_counts = []
        certificate_histogram = Counter()
        witnesses = []
        for index, state in enumerate(representatives):
            witness, certificate_count, nodes = repair_witness(
                state, additions, admissible, sigma, off_sigma,
                off_cells, cell_index
            )
            certificate_histogram[certificate_count] += 1
            zero += certificate_count == 0
            node_counts.append(nodes)
            if witness is not None:
                sat += 1
                row = {"family": name, "branch": index,
                       "extra_mask": hex(witness)}
                witnesses.append(row)
                all_witnesses.append(row)
        require((raw, sat, len(representatives) - sat, zero,
                 sum(node_counts), max(node_counts))
                == (expected_raw, expected_sat, expected_unsat,
                    expected_zero, expected_nodes, expected_max_nodes),
                "the %s repair-DNF audit changed" % name)
        family_rows[name] = {
            "labelled_anchor_states": labelled,
            "anchor_state_orbits": len(representatives),
            "raw_addition_choices": raw,
            "repair_DNF_sat_branches": sat,
            "repair_DNF_unsat_branches": len(representatives) - sat,
            "zero_initial_certificate_branches": zero,
            "certificate_count_histogram": dict(
                sorted(certificate_histogram.items())
            ),
            "memo_states": sum(node_counts),
            "max_memo_states": max(node_counts),
            "witness_sha256": D.content_hash(witnesses),
        }
    require(sum(row["raw_addition_choices"]
                for row in family_rows.values()) == 1196640200
            and sum(row["repair_DNF_sat_branches"]
                    for row in family_rows.values()) == 271
            and sum(row["repair_DNF_unsat_branches"]
                    for row in family_rows.values()) == 41,
            "the aggregate m=10 scalability census changed")

    triple_supports = [{state[0] for state in triples[colour]}
                       for colour in (0, 1)]
    support_representatives = support_pair_orbits(
        triple_supports[0], triple_supports[1], group
    )
    require(len(support_representatives) == 132,
            "the 3+3 base-support quotient changed")
    frontier_base = support_representatives[0][0] | support_representatives[0][1]
    expected_base = {
        (0,4,0,0), (0,4,1,1), (1,5,0,0),
        (1,5,1,1), (6,7,0,0), (6,7,1,1),
    }
    require(frontier_base == expected_base,
            "the canonical frontier base changed")
    cnf = build_frontier_cnf(frontier_base, admissible, sigma, off_sigma)
    encoded = dimacs_bytes(cnf)
    dimacs_digest = hashlib.sha256(encoded).hexdigest()
    require((cnf.variable_count, len(cnf.clauses), dimacs_digest)
            == (3539, 12897, EXPECTED_DIMACS_SHA256),
            "the frozen m=10 frontier CNF changed")
    ledger = {
        "pinned_m9_sha256": M9_SHA256,
        "normal_forms": normal_forms,
        "families": family_rows,
        "raw_addition_choices": 1196640200,
        "repair_DNF": {
            "closed_anchor_branches": 41,
            "surviving_symbolic_branches": 271,
            "zero_initial_certificate_branches": 13,
            "memo_states": sum(row["memo_states"]
                               for row in family_rows.values()),
            "witness_sha256": D.content_hash(all_witnesses),
        },
        "frontier": {
            "family": "lex-first 3+3 base support plus exactly four extras",
            "base": [list(entry) for entry in sorted(frontier_base)],
            "core_fibres": [[list(domain), list(values), pure]
                            for domain, values, pure in CORE_FIBRES],
            "variables": cnf.variable_count,
            "clauses": len(cnf.clauses),
            "dimacs_sha256": dimacs_digest,
            "proof_status": ("native UNSAT observed; a checked deletion-free "
                             "RUP/LRAT artifact is not yet committed"),
        },
        "status": ("m=10 remains open in 271 symbolic anchor branches; "
                   "the first exact 3+3+4 CNF frontier is frozen"),
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the m=10 frontier ledger changed")
    return ledger, digest, encoded, monotonic() - started


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-dimacs", metavar="PATH")
    args = parser.parse_args()
    ledger, digest, encoded, seconds = audit()
    if args.emit_dimacs:
        with open(args.emit_dimacs, "wb") as handle:
            handle.write(encoded)
        print("wrote:", args.emit_dimacs)
    print("n8 D1 m=10 structural frontier: PASS (exact audit)")
    print("raw additions:", ledger["raw_addition_choices"])
    print("repair-DNF: 41 branches closed; 271 symbolic survivors")
    print("frontier CNF: 3539 variables; 12897 clauses")
    print("DIMACS sha256:", ledger["frontier"]["dimacs_sha256"])
    print("ledger sha256:", digest)
    print("status: m=10 OPEN (checked proof frontier)")
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
