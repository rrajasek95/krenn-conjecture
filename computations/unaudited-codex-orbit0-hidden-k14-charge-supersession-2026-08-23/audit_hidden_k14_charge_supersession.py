#!/usr/bin/env python3
"""Machine-readable scope correction for the K18/K19 charge ledgers."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FILES = {
    "k16_literal": ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22/results_orbit0_k16_literal_residual.json",
    "k18_charge": ROOT / "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/results_k18_charge.json",
    "ledger18": ROOT / "computations/unaudited-codex-orbit0-filtered-charge-ledger-through-k18-2026-08-23/results_charge_ledger_through_k18.json",
    "k19_charge": ROOT / "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/results_k19_charge.json",
    "ledger19": ROOT / "computations/unaudited-codex-orbit0-filtered-charge-ledger-through-k19-2026-08-23/results_charge_ledger_through_k19.json",
    "k20_supersession": ROOT / "computations/unaudited-codex-orbit0-filtered-k20-interface-audit-2026-08-23/results_filtered_k20_interface.json",
    "arithmetic": ROOT / "computations/unaudited-codex-orbit0-k19-k24-arithmetic-plan-2026-08-23/results_k19_k24_arithmetic.json",
}
OUT = HERE / "results_hidden_k14_charge_supersession.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    data = {name: json.loads(path.read_text()) for name, path in FILES.items()}
    require(data["k16_literal"]["collection"]["reducible_K16_tail_occurrences"]
            == 75_691_040, "discarded K16 count changed")
    require(data["k20_supersession"]["status"]
            == "RETRACTED_INCOMPLETE_K20_DAG_NO_PREFIX_RUN",
            data["k20_supersession"]["status"])
    require([row["path"] for row in data["k20_supersession"]
            ["missing_primitive_paths"]] == [[2, 4], [2, 2, 2]],
            data["k20_supersession"]["missing_primitive_paths"])
    require(data["k18_charge"]["total"]["K18_irreducible_charge"]["text"]
            == "2590664898048/935", "K18 visible subtotal changed")
    require(data["k19_charge"]["combined"]["K19_irreducible_charge"]["text"]
            == "-14857399077330176/1436925", "K19 visible subtotal changed")
    require(data["arithmetic"]["hidden_higher_tail_guard"]
            ["K20_depth3_product_lcm"] == 400_591_699_200,
            "global scale changed")

    result = {
        "status": "RETRACT_FULL_K18_K19_CHARGES_AND_CUMULATIVE_LEDGERS",
        "cause": (
            "The K14/K2 collector discarded 75,691,040 pivotable K16 tail "
            "occurrences without serializing their later tails. Consequently "
            "K14 path [2,2] is absent from K18 and [2,3] is absent from K19."
        ),
        "claims_that_remain_exact": {
            "K14_normal_charge": "0",
            "K15_normal_charge": "0",
            "K16_normal_charge": "375127296",
            "K17_normal_charge": "-9747200926208/6545",
            "K18_visible_component_subtotal": "2590664898048/935",
            "K18_visible_components": ["direct", "K14[4]", "K15[3]", "direct-K16[2]"],
            "K19_visible_component_subtotal": "-14857399077330176/1436925",
            "K19_visible_components": [
                "direct", "K15[4]", "direct-K16[3]", "direct-K17[2]",
                "K14[3,2]", "K15[2,2]"
            ],
            "denominator_scale": "U=400591699200 remains certified",
        },
        "claims_retracted": {
            "K18_full_normal_charge": "missing additive K14[2,2] contribution",
            "K14_through_K18_cumulative": "depends on incomplete K18",
            "required_K19_through_K24_compensating_charge": "depends on incomplete cumulative",
            "K19_full_normal_charge": "missing additive K14[2,3] contribution",
            "K14_through_K19_cumulative": "depends on incomplete K18 and K19",
            "required_K20_through_K24_compensating_charge": "depends on incomplete cumulative",
        },
        "linearity_guard": (
            "The stored component scalars remain exact for the enumerated "
            "source lineages because collection, the structural pivotability "
            "projection, and the 77-functional are linear. They are partial "
            "subtotals, not the complete normal-page charges."
        ),
        "missing_provenance": {
            "K18": "replay K14[2] pivotable K16 parents and emit K2 tails",
            "K19": "replay K14[2] pivotable K16 parents and emit K3 tails",
        },
        "pinned": {
            str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
            for path in FILES.values()
        },
        "scope": "Read-only supersession audit; no missing tails or charges computed.",
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
