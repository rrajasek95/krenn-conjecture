#!/usr/bin/env python3
"""Test closure of the relative-order-three P5 newest-bend state."""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
QQ = Fraction


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


UNIFORM = load_module(
    "n8_p5_uniform_for_relative3_closure",
    "verify_n8_p5_newest_bend_uniform_coefficient.py",
)
G = UNIFORM.G
F2 = UNIFORM.F2
WARD = UNIFORM.WARD

EXPECTED_LEDGER_SHA256 = (
    "a1ad238cb8894402d4d8ed7e1673e4ef3226ab6b204d57e163031ba406cdf002"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def family_digest(items):
    digest = sha256()
    for variable, source in sorted(items):
        digest.update(str(variable).encode())
        digest.update(b":")
        digest.update(WARD.polynomial_digest(source).encode())
        digest.update(b"\n")
    return digest.hexdigest()


def response(graph, marker, absolute_order):
    return {
        variable: derivative
        for variable, series in graph["series"].items()
        if (derivative := UNIFORM.derivative(series[absolute_order], marker))
    }


def state_label(layout, variable):
    for family in ("y", "n"):
        inverse = {value: key for key, value in layout[family].items()}
        if variable in inverse:
            return f"{family}{inverse[variable]}"
    inverse_a = {value: key for key, value in layout["a"].items()}
    if variable in inverse_a:
        return f"z{inverse_a[variable]}"
    return f"x{variable}"


def audit():
    base = F2.audit(return_data=True)
    graph = G.source_graph(base, maximum_order=8, additional_bends=2)
    marker = graph["bend_variables"][1]
    layout = base["layout"]

    responses = {
        relative: response(graph, marker, 4 + relative)
        for relative in range(5)
    }
    supports = {relative: set(values) for relative, values in responses.items()}
    relative3 = supports[3]
    relative4 = supports[4]
    new_at_relative4 = relative4 - relative3
    lost_at_relative4 = relative3 - relative4
    raw_block_labels = {
        "y110", "y113", "y116", "y155", "y158", "y161", "y191", "y197"
    }
    relative3_labels = {
        state_label(layout, variable) for variable in relative3
    }

    require(
        [len(supports[relative]) for relative in range(4)]
        == [1, 11, 11, 22],
        "known newest-bend response supports changed",
    )
    require(len(relative3 - supports[2]) == 11,
            "relative-order-three state increment changed")
    require(raw_block_labels <= relative3_labels,
            "selected raw 2+1 cascade left the relative-three support")
    require(len(relative3_labels - raw_block_labels) == 14,
            "relative-three complement of the raw 2+1 block changed")
    expected_new = {
        "n12", "n13", "n18", "n19", "y56", "y83", "y86", "y126",
        "y127", "y129", "y130", "y162", "y198", "y199", "y200",
        "y201", "y202", "y203", "y207", "y209", "y210", "y212",
        "y214", "y224", "y225", "y226",
    }
    require(
        {state_label(layout, variable) for variable in new_at_relative4}
        == expected_new,
        "relative-order-four escaping state support changed",
    )
    require(not lost_at_relative4,
            "a relative-three state disappeared at relative order four")

    records = []
    for relative, values in responses.items():
        records.append({
            "relative_order": relative,
            "nonzero_variables": len(values),
            "terms": sum(map(len, values.values())),
            "maximum_terms": max(map(len, values.values()), default=0),
            "support": [state_label(layout, variable)
                        for variable in sorted(values)],
            "sha256": family_digest(values.items()),
        })

    ledger = {
        "marker": "r4=z46^(4)",
        "audited_absolute_orders": [4, 5, 6, 7, 8],
        "response_records": records,
        "relative3_state_count": len(relative3),
        "relative3_new_state_count": len(relative3 - supports[2]),
        "raw_2plus1_coordinate_count": len(raw_block_labels),
        "relative3_complement_of_raw_2plus1": sorted(
            relative3_labels - raw_block_labels
        ),
        "relative4_state_count": len(relative4),
        "relative4_new_outside_relative3": [
            state_label(layout, variable) for variable in sorted(new_at_relative4)
        ],
        "relative3_missing_at_relative4": [
            state_label(layout, variable) for variable in sorted(lost_at_relative4)
        ],
        "closure_verdict": (
            "the full relative-order-three coordinate support is closed at "
            "the next response order" if not new_at_relative4 else
            "the full relative-order-three coordinate support is not closed "
            "at the next response order"
        ),
        "transfer_consequence": (
            "there is no time-homogeneous state evolution on the proposed "
            "22 literal relative-order-three coordinates: its next exact "
            "response has 26 nonzero coordinates outside that state space"
        ),
        "scope_guard": (
            "this rules out only closure of the proposed 22 literal Schur "
            "coordinates; it does not rule out an enlarged or quotient "
            "realization, pole cancellation after output projection, or the "
            "finite rational full-Rees identity"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "relative-order-three closure ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
