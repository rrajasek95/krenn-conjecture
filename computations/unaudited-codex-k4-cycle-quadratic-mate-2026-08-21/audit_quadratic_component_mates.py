#!/usr/bin/env python3
"""Finite-field fixed-left mate tests for genuine k4-cycle quadratics.

The six quadratic factors at each of two large primes are *special-fibre
controls only*.  For each factor this script independently reconstructs the
six oriented 2x2 blocks, evaluates the literal one-colour base, X, cofactor,
Q and H data in F_p[z]/(f), and specializes the complete diagonal pair
packet to an arbitrary 24-variable mate.  A Singular UNIT is a theorem only
over that displayed finite extension field.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
from pathlib import Path
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
NORMALIZED = HERE.parent / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20"
INPUTS = (
    BRIDGE / "results_branch0_cycle_delta_au_open_all_minor_components.json",
    BRIDGE / "results_branch0_cycle_delta_au_open_all_minor_components_p1073741789.json",
)
CORE_PATH = NORMALIZED / "audit_polarized_superpair_core_identity.py"
PROBE_PATH = NORMALIZED / "probe_cofactor_orientation_classes.py"
OUT = HERE / "results_quadratic_component_mates.json"
EDGE_ORDER = tuple(combinations(range(4), 2))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CORE = load("k4_quad_mate_core", CORE_PATH)
PROBE = load("k4_quad_mate_probe", PROBE_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def logical_digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


class Field:
    """F_p[z]/(z^2+c1*z+c0), represented as (constant,z coefficient)."""

    def __init__(self, prime, factor):
        require(len(factor) == 3 and factor[2] % prime == 1,
                "quadratic factor is not monic")
        self.p = prime
        self.c0 = factor[0] % prime
        self.c1 = factor[1] % prime
        discriminant = (self.c1*self.c1 - 4*self.c0) % prime
        require(pow(discriminant, (prime - 1)//2, prime) == prime - 1,
                "quadratic factor is reducible")

    def value(self, encoded):
        return encoded[0] % self.p, encoded[1] % self.p

    def scalar(self, value):
        return value % self.p, 0

    def add(self, left, right):
        return ((left[0] + right[0]) % self.p,
                (left[1] + right[1]) % self.p)

    def neg(self, value):
        return (-value[0] % self.p, -value[1] % self.p)

    def sub(self, left, right):
        return self.add(left, self.neg(right))

    def mul(self, left, right):
        a, b = left
        c, d = right
        return ((a*c - self.c0*b*d) % self.p,
                (a*d + b*c - self.c1*b*d) % self.p)

    def inv(self, value):
        a, b = value
        denominator = (a*(a-self.c1*b) + self.c0*b*b) % self.p
        require(denominator, "attempted to invert zero in quadratic field")
        inverse = pow(denominator, -1, self.p)
        return ((a-self.c1*b)*inverse % self.p,
                -b*inverse % self.p)

    def div(self, left, right):
        return self.mul(left, self.inv(right))

    def nonzero(self, value):
        return value != (0, 0)

    def encode(self, value):
        return [value[0], value[1]]

    def singular(self, value):
        a, b = value
        if not b:
            return str(a)
        if not a:
            return f"({b})*zz"
        return f"({a})+({b})*zz"


def evaluate(poly, entries, field):
    answer = field.scalar(0)
    for monomial, coefficient in poly.items():
        term = field.scalar(int(coefficient))
        for variable in monomial:
            term = field.mul(term, entries[variable])
        answer = field.add(answer, term)
    return answer


def scale_poly(poly, coefficient, field):
    """Singular polynomial over the current quadratic coefficient field."""
    pieces = []
    scalar = field.singular(coefficient)
    for monomial, integer in sorted(poly.items()):
        value = field.mul(coefficient, field.scalar(int(integer)))
        if not field.nonzero(value):
            continue
        factors = [f"x{variable}" for variable in monomial]
        body = "*".join(factors) or "1"
        pieces.append(f"({field.singular(value)})*{body}")
    return "+".join(pieces) or "0"


def word_pairconstant(values):
    return "".join(str(values[site // 2]) for site in range(8))


def raw_nonanchor_edge(raw_index):
    edge, position = divmod(raw_index, 4)
    i, j = EDGE_ORDER[edge]
    clone_i, clone_j = divmod(position, 2)
    return 2*i + clone_i, 2*j + clone_j


def word_six_two(majority, minority, raw_index):
    values = [majority] * 8
    for site in raw_nonanchor_edge(raw_index):
        values[site] = minority
    return "".join(map(str, values))


def word_four_four(left, right, orientation):
    values = []
    for site in range(4):
        bit = (orientation >> (3-site)) & 1
        values.extend((right, left) if bit else (left, right))
    return "".join(map(str, values))


def packet_ledger():
    pairconstant = sorted({
        word_pairconstant(values)
        for values in product(range(3), repeat=4)
        if len(set(values)) > 1
    })
    four_four = sorted({
        word_four_four(left, right, orientation)
        for left, right in combinations(range(3), 2)
        for orientation in range(16)
    })
    six_two = sorted({
        word_six_two(majority, minority, raw_index)
        for majority, minority in permutations(range(3), 2)
        for raw_index in range(24)
    })
    require((len(pairconstant), len(four_four), len(six_two)) == (78, 48, 144),
            "270-row word-orbit census changed")
    return {"pairconstant_78": pairconstant,
            "four_plus_four_48": four_four,
            "six_plus_two_144": six_two}


PACKET_LEDGER = packet_ledger()
H_POLY = CORE.pure_hafnian()
COFACTORS = tuple(PROBE.derivative(H_POLY, index) for index in range(24))
Q_POLYS = tuple(CORE.q_orientation(tuple(
    (value >> (3-site)) & 1 for site in range(4)))
    for value in range(16))
BASE_ROWS = tuple(
    [(f"pair_e_{i}{j}", CORE.e_pair(i, j)) for i, j in EDGE_ORDER]
    + [(f"triple_t_{i}{j}{k}", CORE.t_triple(i, j, k))
       for i, j, k in combinations(range(4), 3)]
)


def reconstruct(component, prime):
    factor = component["factor_coefficients"]
    field = Field(prime, factor)
    values = {name: field.value(value) for name, value in
              component["quadratic_field_values"].items()}
    one = field.scalar(1)
    zero = field.scalar(0)
    p = [zero, values["p1"], values["p2"], values["p3"],
         values["p4"], zero]
    b = [values["b0"], values["b1"], one, values["b3"], one, one]
    d = [zero, values["d1"], one, values["d3"], values["d4"], zero]
    a = [values["a0"], field.div(p[1], d[1]), p[2],
         field.div(p[3], d[3]), field.div(p[4], d[4]), values["a5"]]
    c = [field.neg(field.div(field.add(one, field.mul(a[index], d[index])),
                              b[index])) for index in range(6)]
    entries = tuple(value for edge in range(6)
                    for value in (a[edge], b[edge], c[edge], d[edge]))

    base_values = [(label, evaluate(poly, entries, field))
                   for label, poly in BASE_ROWS]
    cofactor_values = tuple(evaluate(poly, entries, field)
                            for poly in COFACTORS)
    q_values = tuple(evaluate(poly, entries, field) for poly in Q_POLYS)
    h_value = evaluate(H_POLY, entries, field)
    require(all(not field.nonzero(value) for _, value in base_values),
            "reconstructed component fails an e/t base row")
    selected_cofactor_failures = [
        f"cofactor_{edge}_{position}"
        for edge in range(6) for position in (0, 3)
        if field.nonzero(cofactor_values[4*edge + position])
    ]
    require(h_value == values["H"] and field.nonzero(h_value),
            "reconstructed H differs from frozen component export")
    for edge in range(1, 5):
        require(field.nonzero(p[edge])
                and field.nonzero(field.add(one, p[edge])),
                f"cycle selected-live guard failed on edge {edge}")
        require(all(field.nonzero(entries[4*edge + position])
                    for position in range(4)),
                f"genuine full block guard failed on edge {edge}")
    require(all(field.nonzero(b[edge]) and field.nonzero(c[edge])
                for edge in range(6)), "selected anti-term guard failed")

    return (field, entries, cofactor_values, q_values, h_value, p,
            selected_cofactor_failures)


def mate_generators(field, entries, cofactors, q_values):
    rows = []
    # These ten literal consequences of the pairconstant 78-sector generate
    # the arbitrary mate's e/t base ideal on the normalized diagonal chart.
    for label, poly in BASE_ROWS:
        rows.append({"sector": "pairconstant_78", "label": label,
                     "source_word": None,
                     "left_coefficient": field.encode(field.scalar(1)),
                     "polynomial": scale_poly(poly, field.scalar(1), field)})
    # Fixed pair (left colour 0, mate colour 1): 16 of the global 48 rows.
    for orientation, value in enumerate(q_values):
        label = word_four_four(0, 1, orientation)
        poly = Q_POLYS[15-orientation]
        rows.append({"sector": "four_plus_four_48", "label": label,
                     "source_word": label,
                     "left_coefficient": field.encode(value),
                     "polynomial": scale_poly(poly, value, field)})
    # Fixed ordered pair directions: 48 of the global 144 rows.
    for raw_index, value in enumerate(entries):
        label = word_six_two(1, 0, raw_index)
        rows.append({"sector": "six_plus_two_144", "label": label,
                     "source_word": label,
                     "left_coefficient": field.encode(value),
                     "polynomial": scale_poly(COFACTORS[raw_index], value,
                                              field)})
    for raw_index, value in enumerate(cofactors):
        label = word_six_two(0, 1, raw_index)
        rows.append({"sector": "six_plus_two_144", "label": label,
                     "source_word": label,
                     "left_coefficient": field.encode(value),
                     "polynomial": scale_poly(Counter({(raw_index,): 1}),
                                              value, field)})
    require(len(rows) == 74, "fixed-pair specialization row count changed")
    return rows


def run_mate(field, factor, rows, component_tag, timeout):
    active = [row for row in rows if row["polynomial"] != "0"]
    h_guard = scale_poly(H_POLY, field.scalar(1), field)
    variables = ",".join([f"x{index}" for index in range(24)] + ["u"])
    minpoly = f"zz^2+({factor[1] % field.p})*zz+({factor[0] % field.p})"
    ideal = ",".join(row["polynomial"] for row in active)
    command = (
        f"ring R=({field.p},zz),({variables}),dp;minpoly={minpoly};"
        f"ideal I={ideal},u*({h_guard})-1;ideal G=slimgb(I);"
        'print("BEGIN");print(string(reduce(1,G)));print(size(G));'
        'print(dim(G));print("END");quit;'
    )
    command_sha = sha256(command.encode()).hexdigest()
    started = time.monotonic()
    try:
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   text=True, capture_output=True,
                                   timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "command_sha256": command_sha,
                "active_generator_count": len(active),
                "elapsed_seconds_nonlogical": round(time.monotonic()-started, 6)}
    elapsed = round(time.monotonic()-started, 6)
    lines = completed.stdout.splitlines()
    if completed.returncode or "BEGIN" not in lines or "END" not in lines:
        return {"status": "ERROR", "command_sha256": command_sha,
                "active_generator_count": len(active),
                "returncode": completed.returncode,
                "stdout_tail": completed.stdout[-500:],
                "stderr_tail": completed.stderr[-500:],
                "elapsed_seconds_nonlogical": elapsed}
    body = lines[lines.index("BEGIN")+1:lines.index("END")]
    require(len(body) == 3, f"unexpected Singular output for {component_tag}")
    return {"status": "UNIT" if body[0] == "0" else "NONUNIT",
            "basis_size": int(body[1]), "dimension": int(body[2]),
            "command_sha256": command_sha,
            "active_generator_count": len(active),
            "elapsed_seconds_nonlogical": elapsed}


def main():
    timeout = 120
    input_records = []
    results = []
    for path in INPUTS:
        payload = json.loads(path.read_text())
        copy = dict(payload)
        claimed = copy.pop("result_sha256")
        require(logical_digest(copy) == claimed,
                f"frozen component logical digest failed: {path.name}")
        prime = payload["prime"]
        quadratics = [row for row in payload["components"]
                      if row["degree"] == 2]
        require(len(quadratics) == 6,
                "quadratic component count changed")
        input_records.append({"path": str(path),
                              "file_sha256": sha256(path.read_bytes()).hexdigest(),
                              "logical_sha256": claimed, "prime": prime})
        for component in quadratics:
            (field, entries, cofactors, q_values, h_value, p_values,
             source_failures) = \
                reconstruct(component, prime)
            rows = mate_generators(field, entries, cofactors, q_values)
            verdict = ({
                "status": "NOT_A_FULL_SOURCE_POINT",
                "reason": "nonzero literal selected cofactor rows",
            } if source_failures else run_mate(
                field, component["factor_coefficients"], rows,
                f"p{prime}_c{component['index']}", timeout))
            supports = {
                "X": [index for index, value in enumerate(entries)
                      if field.nonzero(value)],
                "C": [index for index, value in enumerate(cofactors)
                      if field.nonzero(value)],
                "Q": [index for index, value in enumerate(q_values)
                      if field.nonzero(value)],
            }
            result = {
                "prime": prime, "component_index": component["index"],
                "factor_coefficients": component["factor_coefficients"],
                "factor_sha256": component["factor_sha256"],
                "left_entries": [field.encode(value) for value in entries],
                "left_cofactors": [field.encode(value) for value in cofactors],
                "left_Q": [field.encode(value) for value in q_values],
                "left_H": field.encode(h_value),
                "left_selected_p": [field.encode(p_values[index])
                                    for index in range(1, 5)],
                "literal_source_failures": source_failures,
                "supports": supports,
                "support_masks": {
                    name: sum(1 << index for index in support)
                    for name, support in supports.items()},
                "fixed_pair_rows": rows,
                "mate_H_guard": "u*H_mate-1",
                "verdict": verdict,
            }
            results.append(result)
            print(prime, component["index"],
                  {key: len(value) for key, value in supports.items()},
                  verdict["status"], flush=True)

    summary = Counter((row["prime"], row["verdict"]["status"])
                      for row in results)
    payload = {
        "status": "UNAUDITED two-prime quadratic special-fibre source/mate audit",
        "inputs": input_records,
        "packet_word_ledger": PACKET_LEDGER,
        "packet_word_ledger_sha256": logical_digest(PACKET_LEDGER),
        "global_packet_sector_counts": {"pairconstant": 78,
                                         "four_plus_four": 48,
                                         "six_plus_two": 144,
                                         "total": 270},
        "fixed_pair_specialization": (
            "10 mate e/t consequences of the pairconstant sector, 16 "
            "left-Q times complementary-mate-Q rows, and 48 directed "
            "entry/cofactor rows, with their literal word labels"
        ),
        "results": results,
        "verdict_histogram": {
            f"p{prime}_{status}": count
            for (prime, status), count in sorted(summary.items())},
        "selected_live_guard": (
            "left p1..p4, 1+p1..1+p4, every cycle-block entry, every b/c "
            "selected anti-term, and the exported literal H are nonzero"
        ),
        "scope_guard": (
            "The six quadratic factors at each prime are points only of the "
            "frozen determinantal necessary locus. A mate test is performed "
            "only after every literal selected cofactor row vanishes. A "
            "NOT_A_FULL_SOURCE_POINT verdict forbids using that factor as a "
            "fixed left component. Any UNIT would exclude an arbitrary "
            "H-live mate over that finite extension field only and would not "
            "lift a component to characteristic zero."
        ),
    }
    logical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("result sha256:", payload["result_sha256"])


if __name__ == "__main__":
    main()
