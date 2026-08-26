#!/usr/bin/env python3
"""Exact/local-linear audit of the missing 440/2110 zero-tail orbit.

The computation stays in the normalized anchor-pair block variables.  It
derives the literal canonical polynomial, tests its degree-four Macaulay
containment in the two-colour master packet at two primes, exports all 144
source labels in its B4 x S3 orbit, and tests what the extended full-440
packet does to the four non-pairconstant 422 signatures.

No Groebner basis is used.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORE_PATH = (ROOT / "computations/unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
             "audit_polarized_superpair_core_identity.py")
ROUTING = HERE / "results_x5_zero_tail_routing.json"
EXTENSION = HERE / "extension_440_2110_source_labels.json"
OUT = HERE / "results_440_2110_extension.json"
PRIMES = (1009, 1013)


def load_core():
    spec = importlib.util.spec_from_file_location("x5_440_core", CORE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CORE = load_core()


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode("ascii")).hexdigest()


def clean(poly):
    return Counter({monomial: coefficient for monomial, coefficient
                    in poly.items() if coefficient})


def add(*polys):
    answer = Counter()
    for poly in polys:
        answer.update(poly)
    return clean(answer)


def multiply(*polys):
    answer = Counter({(): 1})
    for poly in polys:
        updated = Counter()
        for left, a in answer.items():
            for right, b in poly.items():
                updated[tuple(sorted(left+right))] += a*b
        answer = clean(updated)
    return answer


def monomial(indices):
    return Counter({tuple(indices): 1})


def shift(poly, offset):
    return Counter({tuple(variable+offset for variable in monomial): coefficient
                    for monomial, coefficient in poly.items()})


def derivative(poly, variable):
    answer = Counter()
    for monomial, coefficient in poly.items():
        multiplicity = monomial.count(variable)
        if multiplicity:
            reduced = list(monomial)
            reduced.remove(variable)
            answer[tuple(reduced)] += coefficient*multiplicity
    return clean(answer)


def edge(site_left, site_right):
    super_left, clone_left = divmod(site_left, 2)
    super_right, clone_right = divmod(site_right, 2)
    if super_left == super_right:
        return Counter({(): 1})
    return CORE.entry(super_left, super_right, clone_left, clone_right)


def hafnian_even_subset(sites):
    sites = tuple(sites)
    if not sites:
        return Counter({(): 1})
    if len(sites) == 2:
        return edge(*sites)
    require(len(sites) == 4, f"unsupported local Hafnian size {len(sites)}")
    a, b, c, d = sites
    return add(multiply(edge(a, b), edge(c, d)),
               multiply(edge(a, c), edge(b, d)),
               multiply(edge(a, d), edge(b, c)))


def word_poly(label, colours=3):
    word = tuple(map(int, label))
    answer = Counter({(): 1})
    for colour in range(colours):
        sites = [index for index, value in enumerate(word) if value == colour]
        answer = multiply(answer, shift(hafnian_even_subset(sites), 24*colour))
    return answer


def variable_name(index):
    colour, raw = divmod(index, 24)
    super_edge, position = divmod(raw, 4)
    i, j = CORE.SUPER_EDGES[super_edge]
    clone_i, clone_j = divmod(position, 2)
    return f"x{colour}_{i}{clone_i}_{j}{clone_j}"


def serialize(poly, modulus=None):
    records = []
    for monomial, coefficient in sorted(poly.items()):
        value = coefficient if modulus is None else coefficient % modulus
        if value:
            records.append({"variables": [variable_name(index) for index in monomial],
                            "coefficient": value})
    return records


def poly_sha(poly, modulus=None):
    return logical_sha(serialize(poly, modulus))


def pivot(row):
    return max(row, key=lambda monomial: (len(monomial), monomial))


def macaulay_remainders(rows, targets, prime):
    """Sparse row-span reduction; rows are already degree-cutoff multiples."""
    basis = {}
    for row in rows:
        work = {monomial: coefficient % prime
                for monomial, coefficient in row.items()
                if coefficient % prime}
        while work:
            lead = pivot(work)
            if lead not in basis:
                inverse = pow(work[lead], -1, prime)
                basis[lead] = {monomial: coefficient*inverse % prime
                               for monomial, coefficient in work.items()}
                break
            factor = work[lead]
            for monomial, coefficient in basis[lead].items():
                value = (work.get(monomial, 0)-factor*coefficient) % prime
                if value:
                    work[monomial] = value
                else:
                    work.pop(monomial, None)
    results = {}
    for label, target in targets.items():
        work = {monomial: coefficient % prime
                for monomial, coefficient in target.items()
                if coefficient % prime}
        while work:
            lead = pivot(work)
            if lead not in basis:
                break
            factor = work[lead]
            for monomial, coefficient in basis[lead].items():
                value = (work.get(monomial, 0)-factor*coefficient) % prime
                if value:
                    work[monomial] = value
                else:
                    work.pop(monomial, None)
        remainder = Counter(work)
        results[label] = {
            "zero": not remainder,
            "terms": len(remainder),
            "sha256": poly_sha(remainder, prime),
            "leading_monomial": ([variable_name(index) for index in pivot(remainder)]
                                 if remainder else None),
        }
    return {"prime": prime, "row_rank": len(basis), "targets": results}


PURE_H = CORE.pure_hafnian()
COFACTORS = tuple(derivative(PURE_H, index) for index in range(24))


def base_macaulay_rows(colours, variable_count, cutoff=4):
    require(cutoff == 4, "only the audited degree-four cutoff is supported")
    e_rows = []
    t_rows = []
    for colour in range(colours):
        for super_edge in CORE.SUPER_EDGES:
            e_rows.append(shift(CORE.e_pair(*super_edge), 24*colour))
        for triple in combinations(range(4), 3):
            t_rows.append(shift(CORE.t_triple(*triple), 24*colour))
    degree_two_monomials = ([()] + [(index,) for index in range(variable_count)]
                            + list(combinations_with_replacement(
                                range(variable_count), 2)))
    degree_one_monomials = [()] + [(index,) for index in range(variable_count)]
    rows = [multiply(row, monomial(multiplier))
            for row in e_rows for multiplier in degree_two_monomials]
    rows.extend(multiply(row, monomial(multiplier))
                for row in t_rows for multiplier in degree_one_monomials)
    return rows


def cross_620_rows(colour_left, colour_right):
    rows = []
    for raw_index in range(24):
        x_left = shift(monomial((raw_index,)), 24*colour_left)
        x_right = shift(monomial((raw_index,)), 24*colour_right)
        c_left = shift(COFACTORS[raw_index], 24*colour_left)
        c_right = shift(COFACTORS[raw_index], 24*colour_right)
        rows.extend((multiply(x_left, c_right), multiply(c_left, x_right)))
    return rows


def selected_440_rows(colour_left, colour_right):
    rows = []
    for orientation in range(16):
        bits = tuple((orientation >> (3-site)) & 1 for site in range(4))
        complement = tuple(1-bit for bit in bits)
        rows.append(multiply(shift(CORE.q_orientation(bits), 24*colour_left),
                             shift(CORE.q_orientation(complement),
                                   24*colour_right)))
    return rows


def full_440_rows(colour_left, colour_right):
    rows = []
    for sites in combinations(range(8), 4):
        complement = tuple(index for index in range(8) if index not in sites)
        rows.append(multiply(shift(hafnian_even_subset(sites), 24*colour_left),
                             shift(hafnian_even_subset(complement),
                                   24*colour_right)))
    require(len(rows) == 70, "full two-colour 440 count changed")
    return rows


def formula(label):
    word = tuple(map(int, label))
    factors = []
    for colour in range(3):
        sites = tuple(index for index, value in enumerate(word) if value == colour)
        if not sites:
            continue
        if len(sites) == 4:
            factors.append(f"Q_{colour}[{''.join(map(str, sites))}]")
        elif len(sites) == 2:
            factors.append(f"X_{colour}[{sites[0]}{sites[1]}]")
        else:
            raise RuntimeError("extension formula received a non-440/422 label")
    return "*".join(factors)


def main():
    require(CORE_PATH.is_file() and ROUTING.is_file(), "upstream source missing")
    routing = json.loads(ROUTING.read_text())
    require(routing["logical_sha256"] ==
            "85a18c7f6c02678fe9806ca8ab9654643c5f6b0637867d4f2b71d181e3b21171",
            "zero-tail routing audit changed")
    orbit = next(row for row in routing["routing_table"]
                 if row["orbit"] == "440_one_loop_each_two_cross_edges")
    labels = orbit["literal_source_labels"]
    require(len(labels) == 144 and labels[0] == "00010111",
            "440/2110 source orbit changed")

    canonical = word_poly("00010111", colours=2)
    require(len(canonical) == 9, "canonical 440/2110 polynomial term count changed")
    # Direct literal derivation:
    # Q0[0124]=(x24+x02*x14+x04*x12), and analogously on the complement.
    q_left = hafnian_even_subset((0, 1, 2, 4))
    q_right = shift(hafnian_even_subset((3, 5, 6, 7)), 24)
    require(canonical == multiply(q_left, q_right),
            "canonical literal factorization changed")

    pair_rows = base_macaulay_rows(2, 48)
    pair_rows.extend(cross_620_rows(0, 1))
    pair_rows.extend(selected_440_rows(0, 1))
    require(len(pair_rows) == 15156, "two-colour degree-four row count changed")
    pair_tests = [macaulay_remainders(pair_rows, {"00010111": canonical}, prime)
                  for prime in PRIMES]
    require(all(not test["targets"]["00010111"]["zero"]
                and test["targets"]["00010111"]["terms"] == 9
                for test in pair_tests),
            "canonical row entered the degree-four master span")

    extension_records = []
    for label in labels:
        polynomial = word_poly(label, colours=3)
        require(len(polynomial) == 9, f"440 extension row {label} changed")
        extension_records.append({"source_label": label,
                                  "factor_formula": formula(label),
                                  "terms": len(polynomial),
                                  "polynomial_sha256": poly_sha(polynomial)})
    extension_payload = {
        "status": "exact source-label export of the missing 440/2110 orbit",
        "canonical_word": "00010111",
        "B4_times_S3_orbit_size": len(extension_records),
        "rows": extension_records,
        "scope": (
            "Each row is the exact tail-zero factor Q_c[S]Q_d[V\\S] in "
            "the normalized anchor pairing. This extends the selected "
            "270-row packet; it is not claimed redundant or ideal-minimal."),
    }
    extension_payload["logical_sha256"] = logical_sha(extension_payload)
    EXTENSION.write_text(json.dumps(extension_payload, indent=2,
                                    sort_keys=True)+"\n")

    # Add the entire 440 packet for all three colour pairs and ask which of
    # the four previously missing 422 representatives enters the same exact
    # degree-four span.
    triple_rows = base_macaulay_rows(3, 72)
    for left, right in combinations(range(3), 2):
        triple_rows.extend(cross_620_rows(left, right))
        triple_rows.extend(full_440_rows(left, right))
    require(len(triple_rows) == 49848, "three-colour extended row count changed")
    target_labels = ("01010202", "00010212", "00001212", "00010122")
    targets = {label: word_poly(label, colours=3) for label in target_labels}
    require(all(len(target) == 3 for target in targets.values()),
            "422 representative term count changed")

    # One 422 signature is already exactly an e-row multiple: the majority
    # four-set is two complete anchor pairs.
    e_01_colour0 = CORE.e_pair(0, 1)
    routed_422_multiplier = multiply(shift(edge(4, 6), 24),
                                     shift(edge(5, 7), 48))
    require(targets["00001212"] ==
            multiply(e_01_colour0, routed_422_multiplier),
            "exact e-multiple routing for 00001212 changed")

    triple_tests = [macaulay_remainders(triple_rows, targets, prime)
                    for prime in PRIMES]
    for test in triple_tests:
        require(test["targets"]["00001212"]["zero"],
                "e-multiple 422 row failed modular reduction")
        require(all(not test["targets"][label]["zero"]
                    and test["targets"][label]["terms"] == 3
                    for label in ("01010202", "00010212", "00010122")),
                "a remaining 422 row unexpectedly entered degree-four span")

    result = {
        "status": "PASS exact/local-linear 440/2110 extension audit",
        "normalization": (
            "four internal anchor edges per colour equal one; e_ij=1+perm(M_ij), "
            "t_ijk are the literal normalized pairconstant base equations"),
        "canonical_440_2110": {
            "source_label": "00010111",
            "factor_formula": "Q_0[0124]*Q_1[3567]",
            "left_factor_terms": serialize(q_left),
            "right_factor_terms": serialize(q_right),
            "expanded_terms": serialize(canonical),
            "expanded_sha256": poly_sha(canonical),
        },
        "degree4_master_containment_test": {
            "two_colour_variables": 48,
            "rows": len(pair_rows),
            "generators": (
                "e multiples through degree 2, t multiples through degree 1, "
                "48 directed cross-anchor X*C rows, and 16 fully-split Q*Q rows"),
            "prime_results": pair_tests,
            "verdict": (
                "NONMEMBER of the degree-at-most-four Macaulay span at both "
                "primes. This rules out a degree-four sparse identity; it is "
                "not an unrestricted ideal/radical noncontainment theorem."),
        },
        "extension_440_2110": {
            "path": EXTENSION.name,
            "sha256": file_sha(EXTENSION),
            "logical_sha256": extension_payload["logical_sha256"],
            "source_rows": len(extension_records),
            "minimal_by_signature": True,
        },
        "extended_full440_to_422": {
            "three_colour_variables": 72,
            "rows": len(triple_rows),
            "prime_results": triple_tests,
            "exact_routing": {
                "00001212": (
                    "Q_0[0123]*X_1[46]*X_2[57]="
                    "e^0_01*X_1[46]*X_2[57], hence zero already on e=0"),
            },
            "unrouted_degree4_representatives": [
                "01010202", "00010212", "00010122"],
            "verdict": (
                "The new 440/2110 orbit does not place the other three 422 "
                "signature representatives in the degree-four span. One of "
                "the four prior 422 gaps is exactly redundant by e=0."),
        },
        "next_exact_target": (
            "Treat 00010122 first: its minor-colour anchor factor is one, so "
            "the row is the smallest remaining three-term R_0[0124]*X_1[35] "
            "signature. Search an X*C/cofactor identity before expanding the "
            "genuinely tricolour 01010202 and 00010212 types."),
        "source_hashes": {
            str(CORE_PATH.relative_to(ROOT)): file_sha(CORE_PATH),
            str(ROUTING.relative_to(ROOT)): file_sha(ROUTING),
        },
        "scope": (
            "Exact literal polynomial/export and exact e-multiple identity; "
            "the two-prime Macaulay statements are bounded modular linear "
            "algebra only. No GB and no 252-variable computation is used."),
        "mutation_guards": {
            "delete_middle_440_signature": True,
            "replace_00010111_by_fully_split_01010101": True,
            "declare_bounded_nonmembership_unrestricted": True,
            "miss_exact_e_factor_in_00001212": True,
        },
    }
    result["logical_sha256"] = logical_sha(result)
    text = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if "--write-results" in sys.argv:
        OUT.write_text(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
