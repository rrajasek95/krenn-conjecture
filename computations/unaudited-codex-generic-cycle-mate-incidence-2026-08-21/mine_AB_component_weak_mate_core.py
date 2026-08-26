#!/usr/bin/env python3
"""Mine an exact-component-wide fixed-left mate core."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parent
HELPER_PATH = HERE / "mine_Q3_C6_intersection_mate_core.py"
EXPORT = HERE / "results_AB_component_weak_mate_export.json"
OUT = HERE / "results_AB_component_weak_mate_core.json"
PRIMES = (1073741827, 1073741789)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


HELPER = load("AB_component_weak_core_helper", HELPER_PATH)


def main():
    export = json.loads(EXPORT.read_text())
    aliases = export["generator_aliases"]
    source = HERE / "AB_component_weak_mate_p1073741827.msolve"
    variables, prime, rows = HELPER.parse_input(source)
    ordinary, hrow = rows[:-1], rows[-1]
    if len(ordinary) != len(aliases):
        raise RuntimeError("weak mate label/input count changed")
    active, trials = list(range(len(ordinary))), []
    with tempfile.TemporaryDirectory(prefix="AB-weak-core-") as tmp:
        directory = Path(tmp)
        for counter, index in enumerate(tuple(active), 1):
            candidate = [value for value in active if value != index]
            unit = HELPER.is_unit(variables, prime,
                                  [ordinary[value] for value in candidate],
                                  hrow, directory, counter)
            trials.append({"removed_index": index,
                           "removed_aliases": aliases[index], "unit": unit})
            if unit:
                active = candidate
        mutations = []
        for offset, index in enumerate(active, len(trials)+1):
            candidate = [value for value in active if value != index]
            unit = HELPER.is_unit(variables, prime,
                                  [ordinary[value] for value in candidate],
                                  hrow, directory, offset)
            mutations.append({"removed_index": index,
                              "removed_aliases": aliases[index], "unit": unit})
            if unit is True:
                raise RuntimeError("weak core failed greedy minimality replay")
    outputs = []
    for replay_prime in (0, *PRIMES):
        tag = "exact" if replay_prime == 0 else f"p{replay_prime}"
        path = HERE / f"AB_component_weak_mate_core_{tag}.msolve"
        HELPER.write_input(path, variables, replay_prime,
                           [ordinary[value] for value in active], hrow)
        unit = None
        if replay_prime:
            with tempfile.TemporaryDirectory(prefix="AB-weak-replay-") as tmp:
                unit = HELPER.is_unit(
                    variables, replay_prime,
                    [ordinary[value] for value in active], hrow,
                    Path(tmp), 0)
            if not unit:
                raise RuntimeError(f"weak core failed replay p{replay_prime}")
        outputs.append({"characteristic": replay_prime, "path": path.name,
                        "sha256": sha256(path.read_bytes()).hexdigest(),
                        "unit": unit})
    result = {
        "status": "UNAUDITED two-prime component-wide weak mate core UNIT PASS",
        "active_indices": active,
        "active_aliases": [aliases[index] for index in active],
        "ordinary_row_count": len(active),
        "trials": trials,
        "minimality_mutations": mutations,
        "minimality_timeouts": sum(x["unit"] is None for x in mutations),
        "outputs": outputs,
        "scope": "Only chart-forced incidence data on the exact A=B component.",
        "source_sha256": sha256(EXPORT.read_bytes()).hexdigest(),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("AB component weak core PASS")
    print(len(active), [aliases[index][0] for index in active])
    print(result["result_sha256"])


if __name__ == "__main__":
    main()
