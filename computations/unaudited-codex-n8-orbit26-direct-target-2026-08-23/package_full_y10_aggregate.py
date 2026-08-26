#!/usr/bin/env python3
"""Replay the compact census emitted by the exact partitioned y10 reducer."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RAW = HERE / "results_full_y10_aggregate.txt"
RUST = HERE / "src" / "aggregate_full_y10.rs"
RESULTS = HERE / "results_full_y10_aggregate.json"
REPORT = HERE / "REPORT.md"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def parse_histogram(line, prefix):
    fields = line.split()
    require(fields[0] == prefix, f"missing {prefix}")
    return {int(key): int(value) for key, value in
            (field.split(":", 1) for field in fields[1:])}


def main():
    lines = RAW.read_text(encoding="ascii").splitlines()
    require(lines[0] == "KRENN_N8_DIRECT_FH_FULL_Y10_AGGREGATE_V1", "aggregate magic changed")
    require(lines[1] == "FORMULA C10=R10-R8*h2+R7*S3+R6*S4+L(R9) SCALE 4",
            "aggregate formula changed")
    emitted = int(lines[2].split()[1])
    support = int(lines[3].split()[1])
    coefficient_histogram = parse_histogram(lines[4], "COEFFICIENT_HIST")
    incidence_histogram = parse_histogram(lines[5], "INCIDENCE_HIST")
    require(emitted == 142_520_100, "emitted contribution count changed")
    require(support == 140_185_881, "terminal support changed")
    require(sum(coefficient_histogram.values()) == support, "coefficient histogram does not cover support")
    require(sum(incidence_histogram.values()) == support, "incidence histogram does not cover support")
    require(incidence_histogram[0] == 12_195 and incidence_histogram[1] == 113_790,
            "low-incidence census changed")
    dead = lines[6].split()
    live = lines[7].split()
    require(dead == ["LEX_DEAD", "0111202020494f4f50f8", "-4"], "lex dead row changed")
    require(live == ["LEX_LIVE", "010304084576aeccd6f8", "4", "INCIDENT", "10"],
            "lex live row changed")
    output_coefficients = []
    columns = 0
    for line in lines[8:]:
        fields = line.split()
        if fields[0] == "COLUMN":
            columns += 1
        elif fields[0] == "OUTPUT":
            output_coefficients.append(int(fields[2].split("=")[1]))
    require(columns == 10 and len(output_coefficients) == 30, "one-hop packet changed")
    # Each column repeats the pivot coefficient 4 once.  Eight columns have
    # zero on both other rows; two columns have both other rows live.
    other = []
    for index in range(0, len(output_coefficients), 3):
        triple = output_coefficients[index:index + 3]
        require(triple[0] == 4, "one-hop pivot ordering changed")
        other.append(tuple(triple[1:]))
    require(Counter(pair == (0, 0) for pair in other) == Counter({True: 8, False: 2}),
            "one-hop singleton census changed")

    factored = json.loads((HERE / "results_factored_y10_transfer.json").read_text())
    skeleton = json.loads((HERE / "results_s3_physical_skeleton.json").read_text())
    closure = json.loads((HERE / "results_s3_source_closure.json").read_text())
    result = {
        "format": "n8-direct-Fh-full-y10-aggregate-v1",
        "status": "EXACT_CHOSEN_RIGHT_INVERSE_DEAD_AT_Y10",
        "formula": "C10=R10-R8*h2+R7*S3+R6*S4+L(R9)",
        "scale": 4,
        "emitted_contributions": emitted,
        "terminal_support": support,
        "PM4_incidence": {
            "zero": incidence_histogram[0],
            "one": incidence_histogram[1],
            "histogram": incidence_histogram,
            "lex_dead_row": dead[1],
            "lex_dead_coefficient": int(dead[2]),
            "lex_live_row": live[1],
            "lex_live_incident_columns": int(live[4]),
            "lex_live_singleton_columns_against_terminal_support": 8,
            "lex_live_three-live-row_columns": 2,
        },
        "meaning": (
            "the frozen degree-five certificate followed by the specified deterministic monic "
            "right inverse through y9 cannot be extended using minimum-degree-two columns, "
            "because 12,195 nonzero y10 rows have no literal PM4 leading divisor"
        ),
        "nonclaim": (
            "this is not nonmembership for the full truncated Macaulay map: alternative lower-degree "
            "kernel choices may change C10"
        ),
        "raw_result": str(RAW.relative_to(ROOT)),
        "raw_result_sha256": sha256(RAW.read_bytes()).hexdigest(),
        "rust_source": str(RUST.relative_to(ROOT)),
        "rust_source_sha256": sha256(RUST.read_bytes()).hexdigest(),
        "factored_transfer_logical_sha256": factored["logical_sha256"],
        "s3_skeleton_logical_sha256": skeleton["logical_sha256"],
        "s3_source_closure_logical_sha256": closure["logical_sha256"],
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    report = f"""# Orbit26 direct pure-target transfer through y10

## Exact result

The complete original residual of the frozen degree-five certificate was
contracted through y9 with the frozen deterministic monic providers.  Its
exact y10 circuit is

`C10 = R10 - R8*h2 + R7*S3 + R6*S4 + L(R9)` (scale 4).

The circuit emits {emitted:,} contributions and aggregates to **{support:,}**
nonzero y10 rows.  Against all 2,206 literal N4/PM4 three-term leading blocks,
**{incidence_histogram[0]:,}** rows have no quadratic divisor and
**{incidence_histogram[1]:,}** have exactly one.  The lex-first dead row is
`{dead[1]}` with coefficient {dead[2]}.

Thus this particular right inverse is exactly dead at y10.  This is not a
full-Macaulay nonmembership statement: changing the lower-degree kernel
choices may change the terminal y10 class.

## Transfer structure

The small exact kernels have support 66 (cubic S3) and 244 (quartic S4).
S3 has physical profile 28 `3P2`, 28 `P3+P2`, and 10 `P4`, spanning 65
uncoloured skeletons.  Only 14 of the 28 matching-skeleton rows are literal
normalized Hafnian terms; the other 52 rows are endpoint-colour or physical
product/collision terms.  The unrelated archived 66-row attachment lives in
degree 8 and has literal intersection zero with S3.

The 52-row nonliteral class is not closed under the twelve source-labelled
linear contractions used to construct S3.  Five contractions have all six
tails in the 52 rows, while seven also meet literal `h3` rows.  The unique
tail collision is `05c0d5`, reached from the two distinct `h2` source rows
`30c0` and `72d5`; this is the smallest exact obstruction to treating the
52 rows as an autonomous contraction class.

## Replay

Run:

```text
python3 computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/audit_factored_y10_transfer.py
python3 computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/audit_s3_physical_skeleton.py
python3 computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/audit_s3_source_closure.py
python3 computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/package_full_y10_aggregate.py
```

The 140-million-row aggregation itself is replayed by the Rust binary
`aggregate-full-y10` using a disposable partition directory.  Its compact
raw result has SHA-256 `{result['raw_result_sha256']}`.

The old file `r6_lex_correction_y10_tail.txt` is an isolated R6 correction
control only and is not the scope-correct terminal residual.
"""
    REPORT.write_text(report, encoding="utf-8")
    print("full y10 aggregate package: PASS")
    print("support/incidence0:", support, incidence_histogram[0])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
