#!/usr/bin/env python3
"""Independent exact setup/referee for the orbit-0 T^2 pivot.

This script does not consume a Rust target-square interface.  It rebuilds the
orbit-0 action, the K-degree-eight residual of the cutoff-eight identity, its
labelled coefficient normalization, exact sample double-orbit products, and
literal degree-24 source incidence.  It also records why the cutoff-nine dual
cannot simply be tensored through polynomial multiplication.

Rows are sorted byte multisets of cell identifiers, so repeated variables are
retained.  Quotient coordinates use *orbit mass*, not the coefficient of one
labelled monomial.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "audit_dangerous_charts.py"
BASE_SPEC = importlib.util.spec_from_file_location("dangerous_base_t2", BASE_PATH)
BASE = importlib.util.module_from_spec(BASE_SPEC)
BASE_SPEC.loader.exec_module(BASE)

CERTIFICATE = HERE / "results_orbit0_cutoff8_sparse_full_certificate.json"
DUAL_AUDIT = HERE / "results_orbit0_cutoff9_exact_dual_audit.json"
RUST = HERE.parent / "unaudited-codex-anchor-k-rust-2026-08-20"
CUTOFF9_INTERFACE = RUST / "results_orbit0_cutoff9_direct.jsonl"
OUT = HERE / "results_orbit0_t2_pivot_setup.json"

M0 = ((0, 1), (2, 3), (4, 5), (6, 7))
ANCHORS = frozenset(BASE.CELL_ID[(u, v, c, c)]
                    for c in BASE.COLORS for u, v in M0)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def transform_cell(cell, sites, colours):
    u, v, a, b = cell
    pu, pv = sites[u], sites[v]
    pa, pb = colours[a], colours[b]
    if pu < pv:
        return pu, pv, pa, pb
    return pv, pu, pb, pa


def build_actions():
    """Build C2 wr S4 times S3 directly, without the cutoff exporter."""
    actions = []
    for block_permutation in permutations(range(4)):
        for flips in product(range(2), repeat=4):
            sites = [None] * 8
            for source_block, target_block in enumerate(block_permutation):
                target_left = 2 * target_block
                flip = flips[source_block]
                sites[2 * source_block] = target_left + flip
                sites[2 * source_block + 1] = target_left + 1 - flip
            for colours in permutations(BASE.COLORS):
                actions.append((tuple(sites), tuple(colours)))
    require(len(actions) == len(set(actions)) == 2304,
            "orbit-0 action did not have order 2304")
    return tuple(actions)


ACTIONS = build_actions()
TRANSFORMS = tuple(bytes(BASE.CELL_ID[transform_cell(cell, sites, colours)]
                         for cell in BASE.CELLS)
                   for sites, colours in ACTIONS)


def move_row(row, transform):
    return bytes(sorted(transform[cell] for cell in row))


@lru_cache(maxsize=None)
def row_orbit(row):
    return tuple(sorted({move_row(row, transform) for transform in TRANSFORMS}))


@lru_cache(maxsize=None)
def canonical_row(row):
    return min(move_row(row, transform) for transform in TRANSFORMS)


def row_k_degree(row):
    return sum(cell not in ANCHORS for cell in row)


def add_scaled(left, right, scale):
    for key, value in right.items():
        updated = left.get(key, 0) + scale * value
        if updated:
            left[key] = updated
        else:
            left.pop(key, None)


def target_degree_eight_actual():
    groups = []
    for colour in BASE.COLORS:
        by_degree = defaultdict(list)
        for row in BASE.word_terms((colour,) * BASE.N):
            by_degree[row_k_degree(row)].append(row)
        groups.append(by_degree)
    target = Counter()
    for degrees in product(range(9), repeat=3):
        if sum(degrees) != 8:
            continue
        for terms in product(*(groups[c].get(degrees[c], ())
                               for c in BASE.COLORS)):
            target[bytes(sorted(b"".join(terms)))] += 1
    return target


def quotient_mass(polynomial):
    """Map an invariant labelled polynomial to total-mass orbit coordinates."""
    answer = Counter()
    for row, coefficient in polynomial.items():
        answer[canonical_row(row)] += coefficient
    return answer


def rebuild_r8():
    certificate = json.loads(CERTIFICATE.read_text())
    actual_target = target_degree_eight_actual()
    residual = Counter({row: Fraction(value)
                        for row, value in quotient_mass(actual_target).items()})
    for term in certificate["terms"]:
        coefficient = Fraction(*term["coefficient"])
        word = tuple(map(int, term["word"]))
        multiplier = bytes(term["multiplier_cell_ids"])
        column = Counter()
        for matching_term in BASE.word_terms(word):
            row = bytes(sorted(multiplier + matching_term))
            if row_k_degree(row) == 8:
                column[canonical_row(row)] += 1
        add_scaled(residual, column, -coefficient)
    residual += Counter()
    require(len(residual) == 301 and all(row_k_degree(row) == 8
                                         for row in residual),
            "rebuilt R8 support changed")
    return residual, actual_target


def labelled_normalization(residual):
    orbit_sizes = {}
    labelled_coefficients = Counter()
    labelled_support = 0
    for row, mass in residual.items():
        size = len(row_orbit(row))
        coefficient = mass / size
        orbit_sizes[row] = size
        labelled_coefficients[coefficient] += size
        labelled_support += size
    require(labelled_support == 453600,
            "R8 labelled support changed")
    return orbit_sizes, labelled_coefficients


def pair_product_quotient(left, right, left_mass, right_mass, symmetric):
    """Exact quotient product for one unordered pair of residual orbits.

    Fix ``left`` and enumerate the labelled orbit of ``right``.  Stabilizer
    transitivity supplies the missing factor |Orb(left)|.  Since the stored
    inputs are orbit masses, that factor cancels the labelled normalization
    of the left coefficient, leaving m_left*m_right/|Orb(right)|.
    """
    right_orbit = row_orbit(right)
    fixed_products = Counter(bytes(sorted(left + moved))
                             for moved in right_orbit)
    factor = Fraction(left_mass * right_mass, len(right_orbit))
    if symmetric:
        factor *= 2
    answer = Counter()
    unclassified = set(fixed_products)
    double_orbits = 0
    while unclassified:
        raw = min(unclassified)
        orbit = row_orbit(raw)
        representative = orbit[0]
        multiplicity = sum(fixed_products.get(item, 0) for item in orbit)
        require(multiplicity, "empty double-orbit intersection")
        answer[representative] += factor * multiplicity
        unclassified.difference_update(orbit)
        double_orbits += 1
    expected_mass = left_mass * right_mass * (2 if symmetric else 1)
    require(sum(answer.values()) == expected_mass,
            "pair-product quotient lost orbit mass")
    require(all(len(row) == 24 and row_k_degree(row) == 16 for row in answer),
            "pair-product escaped total degree 24 or K degree 16")
    return answer, double_orbits


@lru_cache(maxsize=None)
def degree24_column_rows(column):
    word, multiplier = column
    require(len(word) == 8 and len(multiplier) == 20,
            "degree-24 source has wrong bidegree")
    return tuple(bytes(sorted(multiplier + term))
                 for term in BASE.word_terms(word))


def incident_degree24_columns(row):
    """Enumerate every literal H_word*x^u column containing ``row``.

    Choosing four occurrences from the 24-byte multiset retains multiplicity.
    The chosen cells must be a perfect matching of the eight sites.  Duplicate
    position choices are deduplicated only after the exact word and residual
    20-cell multiplier have been recovered.
    """
    require(len(row) == 24, "incident source expects a degree-24 monomial")
    decoded = tuple(BASE.CELLS[cell] for cell in row)
    columns = set()
    for selected in combinations(range(24), 4):
        word = [None] * 8
        covered = []
        consistent = True
        for index in selected:
            u, v, a, b = decoded[index]
            if word[u] not in (None, a) or word[v] not in (None, b):
                consistent = False
                break
            word[u], word[v] = a, b
            covered.extend((u, v))
        if not consistent or len(set(covered)) != 8 or None in word:
            continue
        word = tuple(word)
        if len(set(word)) == 1:
            continue
        selected_set = frozenset(selected)
        multiplier = bytes(row[index] for index in range(24)
                           if index not in selected_set)
        columns.add((word, multiplier))
    columns = tuple(sorted(columns, key=repr))
    for column in columns:
        outputs = degree24_column_rows(column)
        require(outputs.count(row) == 1,
                "incident column does not contain the row exactly once")
    return columns


def source_control(row):
    columns = incident_degree24_columns(row)
    minimum_histogram = Counter()
    degree16_term_histogram = Counter()
    word_profile_histogram = Counter()
    for word, multiplier in columns:
        outputs = degree24_column_rows((word, multiplier))
        degrees = tuple(row_k_degree(output) for output in outputs)
        minimum_histogram[min(degrees)] += 1
        degree16_term_histogram[degrees.count(16)] += 1
        word_profile_histogram[tuple(sorted(Counter(word).values(), reverse=True))] += 1
    return {
        "row": row.hex(),
        "incident_columns": len(columns),
        "minimum_K_degree_histogram": {
            str(key): value for key, value in sorted(minimum_histogram.items())
        },
        "K16_terms_per_column_histogram": {
            str(key): value for key, value in sorted(degree16_term_histogram.items())
        },
        "word_profile_histogram": {
            "".join(map(str, key)): value
            for key, value in sorted(word_profile_histogram.items())
        },
        "first_columns": [
            {
                "word": "".join(map(str, word)),
                "multiplier": multiplier.hex(),
                "minimum_K_degree": min(row_k_degree(output)
                                        for output in degree24_column_rows((word, multiplier))),
                "K16_outputs": sum(row_k_degree(output) == 16
                                   for output in degree24_column_rows((word, multiplier))),
            }
            for word, multiplier in columns[:8]
        ],
    }


def dual_multiplication_collisions():
    dual_data = json.loads(DUAL_AUDIT.read_text())
    with CUTOFF9_INTERFACE.open() as handle:
        header = json.loads(next(handle))
    rows = tuple(bytes.fromhex(value) for value in header["rows_hex"])
    support = [(rows[index], Fraction(numerator, denominator), index)
               for index, numerator, denominator in dual_data["dual"]]
    products = {}
    collisions = []
    for left_number, (left, left_value, left_index) in enumerate(support):
        for right, right_value, right_index in support[left_number:]:
            monomial = bytes(sorted(left + right))
            value = left_value * right_value
            record = (value, left_index, right_index)
            if monomial in products and products[monomial][0] != value:
                collisions.append({
                    "monomial": monomial.hex(),
                    "first": [products[monomial][1], products[monomial][2],
                              products[monomial][0].numerator,
                              products[monomial][0].denominator],
                    "second": [left_index, right_index,
                               value.numerator, value.denominator],
                    "K_degree": row_k_degree(monomial),
                })
            else:
                products[monomial] = record
    require(len(products) == 699 and len(collisions) == 4,
            "cutoff-nine dual multiplication collision census changed")
    return collisions


def fraction_histogram(values):
    histogram = Counter(values)
    return {str(value): count for value, count in sorted(histogram.items())}


def main():
    residual, actual_target = rebuild_r8()
    orbit_sizes, labelled_coefficients = labelled_normalization(residual)
    entries = tuple(sorted(residual.items()))

    smallest = min(range(len(entries)), key=lambda i: (orbit_sizes[entries[i][0]], i))
    largest = max(range(len(entries)), key=lambda i: (orbit_sizes[entries[i][0]], -i))
    sample_indices = ((smallest, smallest), (smallest, largest), (0, 1))
    pair_controls = []
    sample_source_row = None
    for left_index, right_index in sample_indices:
        left, left_mass = entries[left_index]
        right, right_mass = entries[right_index]
        quotient, double_orbits = pair_product_quotient(
            left, right, left_mass, right_mass, left_index != right_index
        )
        if sample_source_row is None:
            sample_source_row = min(quotient)
        pair_controls.append({
            "indices": [left_index, right_index],
            "left_orbit_size": orbit_sizes[left],
            "right_orbit_size": orbit_sizes[right],
            "left_mass": [left_mass.numerator, left_mass.denominator],
            "right_mass": [right_mass.numerator, right_mass.denominator],
            "product_row_orbits": len(quotient),
            "double_orbit_intersections": double_orbits,
            "quotient_mass": [sum(quotient.values()).numerator,
                              sum(quotient.values()).denominator],
            "coefficient_denominators": sorted({value.denominator
                                                for value in quotient.values()}),
            "logical_sha256": sha256(json.dumps(
                [[row.hex(), value.numerator, value.denominator]
                 for row, value in sorted(quotient.items())],
                separators=(",", ":")).encode("ascii")).hexdigest(),
        })

    source = source_control(sample_source_row)
    collisions = dual_multiplication_collisions()
    total_mass = sum(residual.values())
    result = {
        "status": "UNAUDITED independent exact orbit-0 T^2 pivot setup",
        "stabilizer_order": len(ACTIONS),
        "anchor_ids": bytes(sorted(ANCHORS)).hex(),
        "cutoff8_certificate_sha256": sha256(CERTIFICATE.read_bytes()).hexdigest(),
        "cutoff9_dual_audit_sha256": sha256(DUAL_AUDIT.read_bytes()).hexdigest(),
        "R8": {
            "quotient_orbits": len(residual),
            "labelled_support": sum(orbit_sizes.values()),
            "orbit_size_histogram": {
                str(size): count for size, count in
                sorted(Counter(orbit_sizes.values()).items())
            },
            "orbit_mass_histogram": fraction_histogram(residual.values()),
            "labelled_coefficient_histogram": fraction_histogram(
                coefficient for coefficient, count in labelled_coefficients.items()
                for _ in range(count)
            ),
            "quotient_total_mass": [total_mass.numerator, total_mass.denominator],
            "degree8_pure_target_labelled_rows": len(actual_target),
            "degree8_pure_target_total_mass": sum(actual_target.values()),
        },
        "R8_square": {
            "total_degree": 24,
            "K_degree": 16,
            "expected_total_orbit_mass": [(total_mass * total_mass).numerator,
                                          (total_mass * total_mass).denominator],
            "pair_product_controls": pair_controls,
            "normalization_formula": (
                "For i<=j with quotient masses m_i,m_j and labelled orbit "
                "O_j, fix r_i and count n_k=#{y in O_j: can(r_i*y)=k}. "
                "The square quotient contribution is m_i*m_j*n_k/|O_j| "
                "for i=j and twice that for i<j."
            ),
        },
        "degree24_source_control": source,
        "degree24_source_formula": (
            "For each nonconstant word w and degree-20 multiplier multiset U, "
            "C(w,U)=sum_{P in PM8} x^(U+term(w,P)). Its K16 component keeps "
            "exactly the outputs with sixteen non-anchor occurrences. Every "
            "column incident to a degree-24 row is recovered by selecting four "
            "occurrences covering the eight sites and subtracting that term "
            "as a multiset; repeated position choices are deduplicated only "
            "after (w,U) is formed."
        ),
        "filtered_algebra_lemma": (
            "Write the exact cutoff-eight residual as R=T-S=R8+R>=9 with "
            "S in I_mix, R8 in K^8, and R>=9 in K^9. Then T^2-R^2="
            "S(T+R) lies in I_mix, while R^2-R8^2=2*R8*R>=9+(R>=9)^2 "
            "lies in K^17. Hence [T^2] in gr_K^16(R/I_mix) is [R8^2]."
        ),
        "associated_graded_scope_guard": (
            "Direct columns whose individual minimum K-degree is sixteen give "
            "a sufficient positive test only. A negative result is not global: "
            "gr_K^16(I_mix)_24 also contains degree-sixteen tails of linear "
            "combinations of lower-minimum columns whose degrees below sixteen "
            "cancel. A sound negative test must close all rows of K-degree<17 "
            "and their incident degree-24 columns, or equivalently add the full "
            "lower-kernel transfer into degree sixteen."
        ),
        "cutoff9_dual_square": {
            "support_product_monomials": 699,
            "unequal_fibre_collisions": collisions,
            "conclusion": (
                "lambda tensor lambda does not descend through polynomial "
                "multiplication, so the 37-term cutoff-nine dual gives no "
                "immediate degree-24 functional or lower bound on R8^2."
            ),
        },
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("orbit0 T^2 pivot setup referee: PASS")
    print("R8 quotient/labelled support:", len(residual), sum(orbit_sizes.values()))
    print("R8 total mass / square mass:", total_mass, total_mass * total_mass)
    print("pair controls:", [(item["indices"], item["product_row_orbits"])
                             for item in pair_controls])
    print("source incident columns:", source["incident_columns"])
    print("dual multiplication collisions:", len(collisions))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
