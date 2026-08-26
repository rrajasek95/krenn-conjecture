#!/usr/bin/env python3
"""Exact first homogeneous-D12 root interface on the chart1 A0200 boundary."""

from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXPORT_PATH = HERE / "export_chart1_boundary.py"
ATLAS_PATH = (ROOT / "computations/unaudited-codex-n8-chart-c4-boundary-atlas-2026-08-23"
              / "audit_c4_boundary_atlas.py")
RESULT = HERE / "results_d12_root_interface.json"
QQ = Fraction


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError(path)
    spec.loader.exec_module(module)
    return module


E = load(EXPORT_PATH, "chart1_boundary_export")
A = load(ATLAS_PATH, "chart1_boundary_atlas")
D5 = E.D5


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def transformed_identifier(identifier, element):
    vp, cp = element
    i, j, a, b = D5.COORDINATES[identifier]
    ni, nj, na, nb = vp[i], vp[j], cp[a], cp[b]
    if ni > nj:
        ni, nj, na, nb = nj, ni, nb, na
    return E.COORDINATE_ID[ni, nj, na, nb]


def transformed_code(code, element):
    vp, cp = element
    word = D5.decode_word(code)
    image = [None] * 8
    for site, colour in enumerate(word):
        image[vp[site]] = cp[colour]
    return D5.word_code(tuple(image))


def main():
    rows = tuple(sorted(A.SOURCE.target_orbit_rows()))
    full_group = A.stabilizer(rows[0])
    group = tuple(element for element in full_group
                  if A.transform_edge((0, 6), element) == (0, 6))
    require(len(full_group) == 2304 and len(group) == 32,
            "boundary stabilizer changed")
    transforms = tuple(tuple(transformed_identifier(i, element)
                             for i in range(252)) for element in group)
    for transform in transforms:
        require({transform[i] for i in E.SUPPORT} == set(E.SUPPORT)
                and transform[E.BOUNDARY] == E.BOUNDARY,
                "boundary symmetry does not preserve the source quotient")

    @lru_cache(None)
    def row_orbit(row):
        return tuple(sorted(set(bytes(sorted(transform[i] for i in row))
                                for transform in transforms)))

    def canonical_row(row):
        return row_orbit(row)[0]

    @lru_cache(None)
    def code_orbit(code):
        return tuple(sorted(set(transformed_code(code, element)
                                for element in group)))

    def transformed_column(column, element, transform):
        code, multiplier = column
        return (transformed_code(code, element),
                bytes(sorted(transform[value] for value in multiplier)))

    @lru_cache(None)
    def column_orbit(column):
        return tuple(sorted(set(
            transformed_column(column, element, transform)
            for element, transform in zip(group, transforms)
        )))

    def canonical_column(column):
        return column_orbit(column)[0]

    @lru_cache(None)
    def invariant_entries(column):
        entries = defaultdict(int)
        for code, multiplier in column_orbit(column):
            for term, coefficient in E.normalized_generator(code).items():
                output = bytes(sorted(multiplier + term))
                if output == canonical_row(output):
                    entries[output] += coefficient
        return dict(entries)

    constant_codes = tuple(code for code in range(3 ** 8)
                           if len(set(D5.decode_word(code))) > 1
                           and b"" in E.normalized_generator(code))
    require(len(constant_codes) == 78, "constant mixed words changed")
    representatives = sorted({min(code_orbit(code)) for code in constant_codes})

    columns = []
    all_rows = {b""}
    for representative in representatives:
        column = canonical_column((representative, b""))
        entries = invariant_entries(column)
        require(entries.get(b"") == len(code_orbit(representative)),
                "constant orbit root coefficient changed")
        columns.append((column, entries))
        all_rows.update(entries)

    pure = tuple(E.normalized_generator(D5.word_code((colour,) * 8))
                 for colour in range(3))

    def quotient(row, divisor):
        answer = list(row)
        for value in divisor:
            try:
                answer.remove(value)
            except ValueError:
                return None
        return bytes(answer)

    @lru_cache(None)
    def target_coefficient(row, colour=0):
        if colour == 3:
            return int(not row)
        total = 0
        for term, coefficient in pure[colour].items():
            remainder = quotient(row, term)
            if remainder is not None:
                total += coefficient * target_coefficient(remainder, colour + 1)
        return total

    target = {row: target_coefficient(row) for row in all_rows
              if target_coefficient(row)}
    require(target.get(b"") == 1, "Fh root coefficient changed")

    ordered_rows = tuple(sorted(all_rows, key=lambda row: (len(row), row)))
    row_index = {row: index for index, row in enumerate(ordered_rows)}
    pivots = {}
    for position, (_code, entries) in enumerate(columns):
        vector = {row_index[row]: QQ(value) for row, value in entries.items()}
        source = {position: QQ(1)}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                inverse = 1 / value
                pivots[pivot] = (
                    {key: coefficient * inverse for key, coefficient in vector.items()},
                    {key: coefficient * inverse for key, coefficient in source.items()},
                )
                break
            basis, expression = pivots[pivot]
            for key, coefficient in basis.items():
                result = vector.get(key, QQ(0)) - value * coefficient
                if result: vector[key] = result
                else: vector.pop(key, None)
            for key, coefficient in expression.items():
                result = source.get(key, QQ(0)) - value * coefficient
                if result: source[key] = result
                else: source.pop(key, None)

    work = {row_index[row]: QQ(value) for row, value in target.items()}
    solution = {}
    while work:
        pivot = min(work)
        value = work[pivot]
        if pivot not in pivots:
            break
        basis, expression = pivots[pivot]
        for key, coefficient in basis.items():
            result = work.get(key, QQ(0)) - value * coefficient
            if result: work[key] = result
            else: work.pop(key, None)
        for key, coefficient in expression.items():
            result = solution.get(key, QQ(0)) + value * coefficient
            if result: solution[key] = result
            else: solution.pop(key, None)

    remainder = {ordered_rows[index]: value for index, value in work.items()}
    dual = {}
    target_pairing = QQ(0)
    candidates = set()
    violating = {}
    if remainder:
        selected = min(work)
        dual_by_index = {selected: QQ(1)}
        for pivot in sorted(pivots, reverse=True):
            basis, _expression = pivots[pivot]
            value = -sum(coefficient * dual_by_index.get(index, QQ(0))
                         for index, coefficient in basis.items()
                         if index != pivot)
            if value:
                dual_by_index[pivot] = value
        dual = {ordered_rows[index]: value for index, value in dual_by_index.items()}
        for _column, entries in columns:
            require(sum(QQ(coefficient) * dual.get(row, QQ(0))
                        for row, coefficient in entries.items()) == 0,
                    "finite root dual lost a root column")
        target_pairing = sum(QQ(coefficient) * dual.get(row, QQ(0))
                             for row, coefficient in target.items())
        require(target_pairing != 0, "finite root dual lost target pairing")

        term_index = defaultdict(list)
        for code in range(3 ** 8):
            if len(set(D5.decode_word(code))) == 1:
                continue
            for term in E.normalized_generator(code):
                term_index[term].append(code)

        def quotient_if_divides(row, divisor):
            answer = list(row)
            for value in divisor:
                try: answer.remove(value)
                except ValueError: return None
            return bytes(answer)

        for row in dual:
            seen = set()
            for degree in range(min(4, len(row)) + 1):
                for positions in combinations(range(len(row)), degree):
                    term = bytes(row[position] for position in positions)
                    if term in seen:
                        continue
                    seen.add(term)
                    multiplier = quotient_if_divides(row, term)
                    if multiplier is None or len(multiplier) > 8:
                        continue
                    for code in term_index.get(term, ()):
                        candidates.add(canonical_column((code, multiplier)))
        known = {column for column, _entries in columns}
        for column in candidates:
            value = sum(QQ(coefficient) * dual.get(row, QQ(0))
                        for row, coefficient in invariant_entries(column).items())
            if value and column not in known:
                violating[column] = value

    status = ("FINITE_ROOT_PROJECTION_MEMBER_REPAIR_REQUIRED"
              if not remainder else "FINITE_ROOT_DUAL_KILLED_BY_NEXT_CELLS")
    payload = {
        "format": "n8-chart1-boundary-d12-root-interface-v1",
        "status": status,
        "boundary_stabilizer_order": len(group),
        "constant_mixed_word_codes": len(constant_codes),
        "constant_mixed_word_orbits": len(representatives),
        "root_interface_rows": len(ordered_rows),
        "root_interface_row_degree_histogram": dict(sorted(Counter(
            map(len, ordered_rows)).items())),
        "root_interface_columns": len(columns),
        "root_interface_rank": len(pivots),
        "target_rows_on_interface": len(target),
        "target_projection_member": not remainder,
        "target_remainder": [[row.hex(), value.numerator, value.denominator]
                             for row, value in sorted(remainder.items())],
        "partial_target_reduction_columns": [
            {
                "word_code": columns[index][0][0],
                "word": "".join(map(str, D5.decode_word(columns[index][0][0]))),
                "coefficient": [value.numerator, value.denominator],
            }
            for index, value in sorted(solution.items())
        ],
        "finite_dual": {
            "support": len(dual),
            "target_pairing": [target_pairing.numerator, target_pairing.denominator],
            "rows": [[row.hex(), value.numerator, value.denominator]
                     for row, value in sorted(dual.items())],
            "incident_column_orbits": len(candidates),
            "new_violating_column_orbits": len(violating),
            "lex_first_killing_cell": (None if not violating else {
                "word_code": min(violating)[0],
                "word": "".join(map(str, D5.decode_word(min(violating)[0]))),
                "multiplier_hex": min(violating)[1].hex(),
                "pairing": [violating[min(violating)].numerator,
                            violating[min(violating)].denominator],
            }),
        },
        "next_target": (
            "Adjoin every displayed violating column orbit, close its D12 row incidence, "
            "and repeat. The present finite dual is explicitly killed and is neither full "
            "Fh membership nor nonmembership."
        ),
        "scope": (
            "Exact boundary-stabilizer quotient of the t^12 root and all constant-word "
            "columns only; no full D12 membership/nonmembership inference."
        ),
        "source_sha256": {
            str(EXPORT_PATH.relative_to(ROOT)): sha256(EXPORT_PATH.read_bytes()).hexdigest(),
            str(ATLAS_PATH.relative_to(ROOT)): sha256(ATLAS_PATH.read_bytes()).hexdigest(),
        },
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
