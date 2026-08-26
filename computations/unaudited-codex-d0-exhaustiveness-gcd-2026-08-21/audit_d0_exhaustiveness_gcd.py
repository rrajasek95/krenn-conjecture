#!/usr/bin/env python3
"""Audit the bounded alternative-resultant failure and exact A/B boundary."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE=Path(__file__).resolve().parent
IO_PATH=HERE.parent/"toolkit/groebner/msolve_io.py"


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    assert spec.loader is not None;spec.loader.exec_module(module);return module


IO=load("d0_exhaustiveness_audit_io",IO_PATH)


def digest(path): return sha256(path.read_bytes()).hexdigest()
def require(c,m):
    if not c: raise RuntimeError(m)


def main():
    probe_path=HERE/"results_d0_alternative_resultant_gcd.json"
    probe=json.loads(probe_path.read_text())
    require(probe["resultant_pairs"]["selected_alternative"] is None,
            "an alternative pair unexpectedly appeared")
    expected={(0,1),(0,2),(0,3),(2,3)}
    screened={tuple(row["pair"]):row["zero"]
              for row in probe["runs"][0]["screened_pairs"]}
    require(screened=={pair:True for pair in expected},
            "alternative-pair zero census changed")
    for run in probe["runs"]:
        require(run["R13_zero_diagnostic"] is True,
                "R13 zero diagnostic changed")
        require(run["all_four_gcd_over_fraction_field_guard"]["b0_degree"]==0,
                "all-four positive-b0 common factor appeared")
    factors=probe["exact_pairwise_factorization"]
    require(factors["A"]["terms"]==10 and factors["B"]["terms"]==10,
            "A/B support changed")
    require(factors["gcd_A_B"]["total_degree"]==0 and
            factors["gcd_all_four"]["total_degree"]==0,
            "exact coprimality changed")
    require(factors["pivot_gcd_A"]["total_degree"]==0 and
            factors["pivot_gcd_B"]["total_degree"]==0,
            "A or B became a declared pivot factor")

    export_path=HERE/"results_d0_pairwise_factor_component_export.json"
    export=json.loads(export_path.read_text())
    input_path=HERE/export["input"]
    require(digest(input_path)==export["input_sha256"],"A/B input hash changed")
    parsed=IO.read_msolve_input(input_path,strict=True,
                                allow_characteristic_zero=True)
    require(parsed.characteristic==0 and len(parsed.polynomials)==3,
            "A/B exact input shape changed")
    output_path=HERE/"d0_pairwise_AB_pivot_open_char0.out"
    require(output_path.read_text().strip()=="[-1]:",
            "A/B pivot-open exact unit output changed")
    require(output_path.read_text().replace("-1","1").strip()!="[-1]:",
            "output mutation failed")

    result={
        "status":"UNAUDITED D0 exhaustiveness bounded audit PASS",
        "probe":{"path":probe_path.name,"file_sha256":digest(probe_path),
                 "logical_sha256":probe["logical_sha256"]},
        "component_export":{"path":export_path.name,
                            "file_sha256":digest(export_path),
                            "logical_sha256":export["logical_sha256"]},
        "component_output":{"path":output_path.name,
                            "file_sha256":digest(output_path),
                            "literal":"[-1]:"},
        "conclusion":(
            "No alternative primitive raw compatibility pair has nonzero "
            "b0-resultant. Pairwise zero resultants are explained exactly by "
            "coprime 10-term factors A,B; A=B is empty after pivot localization."
        ),
        "remaining_gap":(
            "The raw-pair resultant strategy cannot prove exhaustiveness. The "
            "remaining pivot-open source cases are A=0,U2=0; B=0,U1=0; and "
            "A,B nonzero with all reduced U rows zero. These are frozen, not closed."
        ),
        "scope_guard":(
            "The exact degree-21 factor closures remain valid. This audit does "
            "not upgrade E=F0F1 from an exact resultant divisor to the full "
            "saturated source projection."
        ),
        "mutation_control":"Changing exact [-1]: output fires.",
    }
    logical=json.dumps(result,sort_keys=True,separators=(",",":"))
    result["logical_sha256"]=sha256(logical.encode()).hexdigest()
    out=HERE/"results_d0_exhaustiveness_gcd_audit.json"
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("D0 exhaustiveness gcd audit PASS",result["logical_sha256"])


if __name__=="__main__":main()
