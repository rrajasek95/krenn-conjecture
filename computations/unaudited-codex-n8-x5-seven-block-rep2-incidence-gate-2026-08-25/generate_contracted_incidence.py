#!/usr/bin/env python3
"""Exact contraction of rep2 cap03/star6 ladder through the A67 adjoint graph."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import os
import re
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
HELPER_PATH = HERE / "generate_incidence_subset_gates.py"
STAGES = ("pure", "distinguished")


def load_helper():
    specification = importlib.util.spec_from_file_location("contract_helper", HELPER_PATH)
    assert specification is not None and specification.loader is not None
    helper = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(helper)
    return helper


def words(stage):
    pure = {tuple([colour] * 8) for colour in range(3)}
    distinguished = {(a, b, b, a, a, a, b, b) for a, b in itertools.permutations(range(3), 2)}
    return tuple(sorted(pure if stage == "pure" else pure | distinguished))


def token_replace(expression, replacements):
    answer = expression
    for variable, value in replacements.items():
        answer = re.sub(rf"(?<![A-Za-z0-9_]){re.escape(variable)}(?![A-Za-z0-9_])", f"({value})", answer)
    return answer


def active_variables(variables, equations):
    body = "\n".join(equations)
    return [
        variable for variable in variables
        if re.search(rf"(?<![A-Za-z0-9_]){re.escape(variable)}(?![A-Za-z0-9_])", body)
    ]


def build(helper, module, stage, ordering):
    full = []
    ledger = []
    for word in words(stage):
        value = module.amplitude(word)
        target = int(len(set(word)) == 1)
        full.append(f"({value})-1" if target else value)
        ledger.append(("".join(map(str, word)), target))
    guard = module.guard_equations()
    adjoint = module.adjoint_equations()
    incidence, incidence_variables = helper.alternate_incidence(module)
    replacements = {}
    for equation in adjoint:
        variable = equation.split("-", 1)[0]
        assert variable.startswith("a67_") and equation.startswith(variable + "-")
        replacements[variable] = equation[len(variable) + 1:]
    assert len(replacements) == 9
    contracted_full = [token_replace(equation, replacements) for equation in full]
    assert not any(re.search(r"(?<![A-Za-z0-9_])a67_", equation) for equation in contracted_full)
    equations = contracted_full + guard + incidence
    ambient = (
        list(module.SOURCE.values()) + list(module.U) + list(module.V)
        + [item for name in "xyz" for item in module.DUAL[name]] + incidence_variables
    )
    active = active_variables(ambient, equations)
    absent = [variable for variable in ambient if variable not in active]
    assert all(variable.startswith(("a12_", "a14_", "a67_")) for variable in absent)
    incidence_set = set(incidence_variables)
    main = [variable for variable in active if variable not in incidence_set]
    witness = [variable for variable in active if variable in incidence_set]
    assert len(witness) == 9
    if ordering == "dp":
        order_text = "dp"
        variable_order = active
    else:
        variable_order = main + witness
        order_text = f"(dp({len(main)}),dp({len(witness)}))"
    lines = [
        "option(noredefine);",
        f"ring r=32003,({','.join(variable_order)}),{order_text};",
        "ideal I=" + ",\n".join(equations) + ";",
        'print("INPUT_GENERATORS="+string(size(I)));',
        "ideal G=slimgb(I);",
        'print("GROEBNER_SIZE="+string(size(G)));',
        "poly remainder=reduce(1,G);",
        'print("UNIT_REMAINDER="+string(remainder));',
        'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_CONTRACTED_SUBSET"); }',
        "quit;",
    ]
    return "\n".join(lines) + "\n", {
        "ambient_variables_before_absent_contraction": len(ambient),
        "active_variables": len(active), "main_variables": len(main),
        "incidence_witness_variables": len(witness), "absent_variables_removed": absent,
        "equations_before_adjoint_contraction": len(full) + len(guard) + len(adjoint) + len(incidence),
        "equations_after_adjoint_contraction": len(equations),
        "full_x5_subset": len(full), "guard": len(guard), "incidence": len(incidence),
        "adjoint_graph_variables_eliminated": sorted(replacements),
        "word_ledger_sha256": hashlib.sha256(json.dumps(ledger, separators=(",", ":")).encode()).hexdigest(),
        "ordering": ordering,
    }


def atomic_write(path, text):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text)
    os.replace(temporary, path)


def main():
    helper = load_helper()
    module = helper.load_core()
    records = {}
    inputs = {}
    for stage in STAGES:
        records[stage] = {}
        inputs[stage] = {}
        for ordering in ("dp", "block"):
            program, record = build(helper, module, stage, ordering)
            path = HERE / f"rep2_contracted_cap03_star6_{stage}_{ordering}_p32003.sing"
            atomic_write(path, program)
            records[stage][ordering] = record
            inputs[stage][ordering] = {"path": path.name, "sha256": hashlib.sha256(program.encode()).hexdigest()}
    assert records["pure"]["dp"]["active_variables"] == 84
    assert records["pure"]["dp"]["equations_after_adjoint_contraction"] == 15
    assert records["distinguished"]["dp"]["active_variables"] == 90
    assert records["distinguished"]["dp"]["equations_after_adjoint_contraction"] == 21
    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_REP2_CAP03_CONTRACTED_INCIDENCE_V1",
        "status": "READY_EXACT_EQUIVALENT_CONTRACTIONS",
        "carrier": "cap03/star6: A04^T*K*[A23^T|A35]",
        "records": records,
        "inputs": inputs,
        "equivalence_proof": {
            "adjoint_graph": (
                "Each of the nine adjoint equations is monic a67_ij-g_ij in a distinct A67 variable. "
                "Quotienting and substituting A67=g is a ring isomorphism, hence preserves unit/nonunit exactly."
            ),
            "absent_variables": (
                "Variables absent after substitution form a polynomial extension; contraction is unit iff its "
                "extension is unit."
            ),
            "block_order": "changes only Groebner presentation, not the ideal or unit criterion",
            "subset_unit": "a unit in either literal full-X5 subset is sufficient for the full ideal",
            "subset_nonunit": "diagnostic only",
        },
        "run_policy": "modular bounded gate only after exact count/equivalence review; no Q yet",
    }
    atomic_write(HERE / "rep2_contracted_incidence_metadata.json", json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "pure": {"variables": 84, "equations": 15},
        "distinguished": {"variables": 90, "equations": 21},
    }, sort_keys=True))


if __name__ == "__main__":
    main()
