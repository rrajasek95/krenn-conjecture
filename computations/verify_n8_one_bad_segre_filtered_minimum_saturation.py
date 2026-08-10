#!/usr/bin/env python3
"""Close the exact six-positive-cell filtered frontier over Q.

For each of the twenty minimum positive-q supports certified by the filtered
support checker, retain every grade-zero face/diagonal coordinate and every
endpoint-star coordinate as an arbitrary variable and set the other positive-q
coordinates to zero.  A 19-row exact Singular ``liftstd`` identity proves that
the ordinary top/diagonal-response ideal is the unit ideal on every envelope.
In particular, no localization or nonvanishing assumption is used.
"""

from __future__ import annotations

from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import argparse
import itertools
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
FRONTIER = ROOT / (
    "computations/verify_n8_one_bad_segre_off01_filtered_response_frontier.py"
)
ANCHOR = ROOT / "computations/verify_n8_one_bad_segre_cube_anchor_initial_cover.py"
FRONTIER_SHA256 = "6c147b1e7fad988baaa6109bffd6d7c649b20a0862656c671e4a847197a1c682"
ANCHOR_SHA256 = "a0a2f5600029f6c79ce931171b53fff772f2fef7e0c0bb4b971ba56c0fd44ef0"
EXPECTED_SUPPORTS_SHA256 = (
    "34511470fe2bde5aaa0a34228500608f927565ef8f94e1e61709ac06136fb240"
)
EXPECTED_LEDGER_SHA256 = (
    "3f7fca2742f9e16c11fa67568fd8a35bc8499add9696ac1856d2f39915be4d8a"
)

COCHARACTER = (
    (0, 0, 0),
    (0, 1, 1),
    (0, 1, 0),
    (0, 0, 1),
    (0, 1, 0),
    (0, 0, 1),
)

SUPPORTS = tuple(
    tuple(line.split()) for line in """
02:01 12:01 14:22 23:11 24:12 25:11
03:02 13:02 15:11 23:22 34:22 35:21
04:01 12:22 14:01 24:21 34:11 45:11
05:02 13:11 15:02 25:22 35:12 45:22
12:01 14:22 23:10 23:11 24:12 25:11
12:01 14:22 23:10 23:11 25:10 25:11
12:01 14:22 23:11 24:10 24:12 25:11
12:01 14:22 23:11 24:12 25:10 25:11
12:22 14:01 24:01 24:21 34:11 45:11
12:22 14:01 24:21 34:01 34:11 45:11
12:22 14:01 24:21 34:11 45:10 45:11
12:22 14:01 34:01 34:11 45:10 45:11
13:02 15:11 23:02 23:22 34:20 34:22
13:02 15:11 23:02 23:22 34:22 35:21
13:02 15:11 23:22 34:20 34:22 35:21
13:02 15:11 23:22 34:22 35:20 35:21
13:11 15:02 25:02 25:22 35:12 45:22
13:11 15:02 25:02 25:22 45:02 45:22
13:11 15:02 25:22 35:02 35:12 45:22
13:11 15:02 25:22 35:12 45:02 45:22
""".strip().splitlines()
)

FIRST_CORE_LABELS = (
    "top:000000", "top:000001", "top:000100", "top:000101",
    "top:001001", "top:001100",
    "p1s1:010011", "p1s1:010110", "p1s1:010111",
    "p1s1:011011", "p1s1:011110", "p1s1:011111",
    "p1s1:110010", "p1s1:110011", "p1s1:110110",
    "p1s1:110111", "p1s1:111011", "p1s1:111110",
    "p1s1:111111",
)

FAMILY_TRANSFORMS = (
    ((0, 1, 2, 3, 4, 5), (0, 1, 2)),
    ((0, 1, 3, 2, 5, 4), (0, 2, 1)),
    ((0, 1, 4, 3, 2, 5), (0, 1, 2)),
    ((0, 1, 5, 2, 3, 4), (0, 2, 1)),
)

FAMILY_FOR_SUPPORT = (
    0, 1, 2, 3, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, 3, 3, 3, 3,
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_dependencies():
    frontier_hash = sha256(FRONTIER.read_bytes()).hexdigest()
    require(frontier_hash == FRONTIER_SHA256,
            f"frontier dependency changed: {frontier_hash}")
    anchor_hash = sha256(ANCHOR.read_bytes()).hexdigest()
    require(anchor_hash == ANCHOR_SHA256,
            f"anchor dependency changed: {anchor_hash}")
    spec = spec_from_file_location("filtered_anchor", ANCHOR)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, frontier_hash, anchor_hash


def add_term(polynomial, monomial, coefficient=1):
    polynomial[tuple(sorted(monomial))] += Fraction(coefficient)


def expression(polynomial):
    terms = []
    for monomial, coefficient in sorted(polynomial.items()):
        if not coefficient:
            continue
        product = "*".join(monomial) if monomial else "1"
        terms.append(
            f"({coefficient.numerator}/{coefficient.denominator})*{product}"
        )
    return "+".join(terms) or "0"


def source_context(anchor):
    four = anchor.load_dependency()
    one = four.load_dependency()
    first = one.load_dependency()
    diagonal = first.load_dependency()
    pure = diagonal.load_dependency()
    source = pure.load_dependency()
    support_h, weights_h = pure.build_top_null_H(source)
    face_labels = tuple(sorted(anchor.LARGE_ZERO_CLASS))
    grade_zero_diagonal_labels = tuple(sorted(
        anchor.cell_label((edge, (colour, colour)))
        for edge in anchor.EDGES for colour in anchor.COLOURS
        if (edge, (colour, colour)) not in support_h
        and anchor.weight(
            (edge, (colour, colour)), COCHARACTER
        ) == 0
    ))
    require(len(face_labels) == 24, "the filtered face changed")
    require(len(grade_zero_diagonal_labels) == 21,
            "the grade-zero diagonal universe changed")
    return anchor, support_h, weights_h, face_labels, grade_zero_diagonal_labels


def build_generators(anchor, support_h, weights_h, face_labels,
                     grade_zero_diagonal_labels, support):
    optional_labels = set(face_labels) | set(grade_zero_diagonal_labels) | set(support)
    optional_cells = {anchor.parse_cell(label) for label in optional_labels}
    q_variables = {
        cell: f"x{cell[0][0]}{cell[0][1]}_{cell[1][0]}{cell[1][1]}"
        for cell in sorted(optional_cells)
    }
    q = {cell: (None, Fraction(value)) for cell, value in weights_h.items()}
    q.update({cell: (name, Fraction(1))
              for cell, name in q_variables.items()})
    star_names = tuple(
        f"{star}_{site}" for star in ("p1", "p2", "s1", "s2")
        for site in anchor.SITES
    )
    variables = tuple(q_variables.values()) + star_names

    generators = []
    labels = []
    for word in itertools.product(anchor.COLOURS, repeat=6):
        polynomial = Counter()
        for matching in anchor.MATCHINGS:
            monomial, coefficient = [], Fraction(1)
            for edge in matching:
                cell = (edge, (word[edge[0]], word[edge[1]]))
                if cell not in q:
                    break
                variable, value = q[cell]
                coefficient *= value
                if variable:
                    monomial.append(variable)
            else:
                add_term(polynomial, monomial, coefficient)
        if word == (0,) * 6:
            add_term(polynomial, (), -1)
        polynomial = Counter({m: c for m, c in polynomial.items() if c})
        if polynomial:
            generators.append(polynomial)
            labels.append("top:" + "".join(map(str, word)))

    response_data = (
        ("p1", "s1", 1, 1, (1,) * 6),
        ("p1", "s2", 1, 2, None),
        ("p2", "s1", 2, 1, None),
        ("p2", "s2", 2, 2, (2,) * 6),
    )
    for p_star, s_star, p_colour, s_colour, target in response_data:
        for word in itertools.product(anchor.COLOURS, repeat=6):
            polynomial = Counter()
            for p_site in anchor.SITES:
                if word[p_site] != p_colour:
                    continue
                for s_site in anchor.SITES:
                    if s_site == p_site or word[s_site] != s_colour:
                        continue
                    residual = tuple(site for site in anchor.SITES
                                     if site not in (p_site, s_site))
                    for matching in anchor.perfect_matchings(residual):
                        monomial = [f"{p_star}_{p_site}", f"{s_star}_{s_site}"]
                        coefficient = Fraction(1)
                        for edge in matching:
                            cell = (edge, (word[edge[0]], word[edge[1]]))
                            if cell not in q:
                                break
                            variable, value = q[cell]
                            coefficient *= value
                            if variable:
                                monomial.append(variable)
                        else:
                            add_term(polynomial, monomial, coefficient)
            if target is not None and word == target:
                add_term(polynomial, (), -1)
            polynomial = Counter({m: c for m, c in polynomial.items() if c})
            if polynomial:
                generators.append(polynomial)
                labels.append(f"{p_star}{s_star}:" + "".join(map(str, word)))

    return variables, labels, generators


def singular_lift_program(variables, generators):
    code = f"ring r=0,({','.join(variables)}),dp; option(redSB);\n"
    code += "ideal I=" + ",".join(expression(g) for g in generators) + ";\n"
    code += "matrix L; ideal G=liftstd(I,L);\n"
    code += (
        'if(size(G)!=1 || G[1]!=1){print("UNIT_SHAPE_FAILED");exit(1);}\n'
        'if(nrows(L)!=size(I) || ncols(L)!=1)'
        '{print("LIFT_SHAPE_FAILED");exit(1);}\n'
        'if(matrix(I)*L-matrix(G)!=0){print("SOURCE_LIFT_FAILED");exit(1);}\n'
        'int i;int nz=0;print("BEGIN_LIFT");\n'
        'for(i=1;i<=nrows(L);i++){if(L[i,1]!=0){'
        'nz=nz+1;print("INDEX");print(i);print("VALUE");print(L[i,1]);}}\n'
        'print("END_LIFT");print("NONZERO");print(nz);quit;\n'
    )
    return code


def compress_diagonal_star_factor(core_labels, core_generators):
    """Replace the common two-port star scalar by one variable ``astar``.

    Each retained diagonal response row is a polynomial in
    ``p_i(1)s_i(4)+p_i(4)s_i(1)`` (after the family permutation).  Top rows
    have no star variables.  We check the two equal literal copies before
    performing the source-faithful scalar substitution.
    """
    compressed = []
    common_star_pairs = None
    for label, generator in zip(core_labels, core_generators, strict=True):
        if label.startswith("top:"):
            compressed.append(generator)
            continue
        grouped = {}
        constant = Counter()
        for monomial, coefficient in generator.items():
            stars = tuple(variable for variable in monomial
                          if variable.startswith(("p1_", "p2_", "s1_", "s2_")))
            q_part = tuple(variable for variable in monomial
                           if variable not in stars)
            if stars:
                require(len(stars) == 2,
                        f"a retained response term has {len(stars)} stars")
                grouped.setdefault(q_part, []).append((stars, coefficient))
            else:
                constant[monomial] += coefficient
        result = Counter(constant)
        for q_part, entries in grouped.items():
            coefficients = tuple(coefficient for _stars, coefficient in entries)
            star_pairs = tuple(sorted(stars for stars, _coefficient in entries))
            require(len(coefficients) == 2 and coefficients[0] == coefficients[1],
                    "the diagonal response row lost its common two-port factor")
            if common_star_pairs is None:
                common_star_pairs = star_pairs
            require(star_pairs == common_star_pairs,
                    "the retained response rows do not share one star scalar")
            add_term(result, ("astar",) + q_part, coefficients[0])
        compressed.append(Counter({m: c for m, c in result.items() if c}))
    require(common_star_pairs is not None,
            "the retained core has no diagonal response factor")
    return tuple(compressed), common_star_pairs


def transformed_core_labels(site_permutation, colour_permutation):
    transformed = []
    for label in FIRST_CORE_LABELS:
        prefix, word_text = label.split(":", 1)
        word = tuple(map(int, word_text))
        image_word = [None] * 6
        for site, colour in enumerate(word):
            image_word[site_permutation[site]] = colour_permutation[colour]
        if prefix != "top":
            left_colour = colour_permutation[int(prefix[1])]
            right_colour = colour_permutation[int(prefix[3])]
            prefix = f"p{left_colour}s{right_colour}"
        transformed.append(prefix + ":" + "".join(map(str, image_word)))
    return tuple(transformed)


CORE_LABELS = tuple(
    transformed_core_labels(*transformation)
    for transformation in FAMILY_TRANSFORMS
)


def audit_support(context, support_index, timeout):
    support = SUPPORTS[support_index]
    anchor, support_h, weights_h, face_labels, grade_zero_diagonal_labels = context
    variables, labels, generators = build_generators(
        anchor, support_h, weights_h, face_labels,
        grade_zero_diagonal_labels, support
    )
    label_to_generator = dict(zip(labels, generators, strict=True))
    core_labels = CORE_LABELS[FAMILY_FOR_SUPPORT[support_index]]
    require(all(label in label_to_generator for label in core_labels),
            f"a transported core row is absent on support {support_index}")
    core_generators = tuple(label_to_generator[label] for label in core_labels)
    compressed_generators, star_factor_terms = compress_diagonal_star_factor(
        core_labels, core_generators
    )
    used_variables = {
        variable for generator in compressed_generators for monomial in generator
        for variable in monomial
    }
    core_variables = tuple(variable for variable in variables
                           if variable in used_variables) + ("astar",)
    require(set(core_variables) == used_variables,
            "the compressed core variable inventory changed")
    generator_stream = "\n".join(
        f"{label}={expression(generator)}"
        for label, generator in zip(
            core_labels, compressed_generators, strict=True
        )
    ) + "\n"
    result = subprocess.run(
        ("/usr/local/bin/Singular", "-q"),
        input=singular_lift_program(core_variables, compressed_generators),
        text=True, capture_output=True, timeout=timeout, check=False,
    )
    require(result.returncode == 0,
            f"Singular failed on {'+'.join(support)}: {result.stderr or result.stdout}")
    require("UNIT_SHAPE_FAILED" not in result.stdout
            and "LIFT_SHAPE_FAILED" not in result.stdout
            and "SOURCE_LIFT_FAILED" not in result.stdout,
            f"the exact source lift failed on {'+'.join(support)}")
    lift = result.stdout.split("BEGIN_LIFT\n", 1)[1].split("\nEND_LIFT", 1)[0]
    lines = lift.splitlines()
    indices = tuple(int(lines[index + 1]) for index, value in enumerate(lines)
                    if value == "INDEX")
    nonzero = int(result.stdout.split("NONZERO\n", 1)[1].splitlines()[0])
    require(len(indices) == nonzero, "the active lift-row count changed")
    require(all(1 <= index <= len(core_labels) for index in indices),
            "a lift row index is out of range")
    return {
        "support": support,
        "family": FAMILY_FOR_SUPPORT[support_index],
        "full_envelope_variables": len(variables),
        "core_variables": len(core_variables),
        "full_nonzero_source_rows": len(generators),
        "ordinary_core_rows": len(core_generators),
        "compressed_star_scalar": {
            "name": "astar",
            "literal_terms": star_factor_terms,
        },
        "core_stream_sha256": sha256(generator_stream.encode()).hexdigest(),
        "active_source_rows": tuple(core_labels[index - 1]
                                    for index in indices),
        "active_source_row_count": nonzero,
        "lift_sha256": sha256(lift.encode()).hexdigest(),
    }


def main(support_index=None, workers=4, timeout=300):
    anchor, frontier_hash, anchor_hash = load_dependencies()
    support_hash = sha256(json.dumps(
        SUPPORTS, separators=(",", ":")
    ).encode()).hexdigest()
    require(support_hash == EXPECTED_SUPPORTS_SHA256,
            f"the certified minimum-support list changed: {support_hash}")
    context = source_context(anchor)
    support_indices = (tuple(range(len(SUPPORTS))) if support_index is None
                       else (support_index,))
    audits = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(audit_support, context, index, timeout): index
            for index in support_indices
        }
        for completed, future in enumerate(as_completed(futures), start=1):
            index = futures[future]
            audit = future.result()
            audits[index] = audit
            print(f"exact ordinary unit {completed}/{len(support_indices)}: "
                  f"{'+'.join(audit['support'])}; family {audit['family']}; "
                  f"active {audit['active_source_row_count']}", flush=True)
    ordered = [audits[index] for index in support_indices]
    ledger = {
        "dependency": {"path": str(FRONTIER.relative_to(ROOT)),
                       "sha256": frontier_hash},
        "anchor_dependency": {"path": str(ANCHOR.relative_to(ROOT)),
                              "sha256": anchor_hash},
        "minimum_supports_sha256": support_hash,
        "minimum_positive_q_supports": len(support_indices),
        "grade_zero_optional_face_cells": 24,
        "grade_zero_optional_diagonal_cells": 21,
        "arbitrary_star_coordinates": 24,
        "allowed_positive_q_coordinates_per_support": 6,
        "ordinary_core_rows_per_support": 19,
        "exact_Q_ordinary_units": len(ordered),
        "audits": ordered,
        "verdict": (
            "every certified minimum six-positive-q envelope has an ordinary "
            "19-row exact-Q unit for all grade-zero q and star completions"
        ),
        "scope": (
            "the exact minimum associated-graded layer; supports with seven "
            "or more positive-q coordinates are not covered"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if support_index is None and EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"minimum-saturation ledger changed: {digest}")
    print("N=8 filtered minimum-support ordinary units: PASS")
    print("exact Q ordinary units:", len(ordered), "/", len(support_indices))
    print("sha256:", digest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--support-index", type=int)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=300)
    arguments = parser.parse_args()
    main(arguments.support_index, arguments.workers, arguments.timeout)
