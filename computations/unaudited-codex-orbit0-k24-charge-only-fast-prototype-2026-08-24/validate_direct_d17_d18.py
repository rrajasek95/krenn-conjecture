#!/usr/bin/env python3
"""Fail-closed validator for exact charge-only K24 direct D17/D18 intervals."""
import argparse, hashlib, json
from pathlib import Path

U = 400_591_699_200
GROUPS = {
    "source_D17_R3_4": [
        "D17:234|R:3-4","D17:243|R:3-4","D17:324|R:3-4",
        "D17:333|R:3-4","D17:342|R:3-4","D17:423|R:3-4","D17:432|R:3-4"],
    "source_D18_R2_4": [
        "D18:244|R:2-4","D18:334|R:2-4","D18:343|R:2-4",
        "D18:424|R:2-4","D18:433|R:2-4","D18:442|R:2-4"],
}
SOURCE_SHA256 = "57a82f19a4d304b4c2696257c821866ef1713d854274847c0ffaa230af41bd21"
BINARY_SHA256 = "c7b2e223f84dfa0fdea77d1ecb26f72a4d0cf8087961723fec522f289942d6be"
SOURCE = Path(__file__).with_name("run_k24_charge_direct_d17_d18.rs")
BINARY = Path(__file__).with_name("run_k24_charge_direct_d17_d18")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate(d, require_full=False):
    assert d["status"] == "PASS_BOUNDED_K24_CHARGE_ONLY_DIRECT_D17_D18"
    assert d["degree"] == 24 and int(d["scale_U"]) == U
    lo, hi = d["source_interval"]
    assert 0 <= lo < hi <= 485 and d["source_slices"] == hi-lo
    if require_full: assert [lo, hi] == [0, 485]
    assert d["covered_ids"] == 13 and d["scalar_groups"] == 2
    assert len(d["groups"]) == 2
    assert [g["group_id"] for g in d["groups"]] == list(GROUPS)
    assert sum(len(x) for x in GROUPS.values()) == 13
    for g in d["groups"]:
        assert g["ids"] == GROUPS[g["group_id"]]
        assert len(set(g["ids"])) == len(g["ids"])
        assert g["K24_terminal_occurrences"] == 60*g["p2_uses"]
        assert g["full_occurrences"] == g["irreducible_occurrences"] == g["K24_terminal_occurrences"]
        assert int(g["full_charge_scaled_U"]) == int(g["irreducible_charge_scaled_U"])
        hist = {tuple(map(int,k.split("_"))): v for k,v in g["denominator_hist"].items()}
        assert sum(hist.values()) == g["pivotable_intermediate_children"]
        assert sum(m2*n for (_,m2),n in hist.items()) == g["p2_uses"]
        assert all(U % (m1*m2) == 0 for m1,m2 in hist)
    assert d["column_or_row_output"] is False
    assert "anchor mass zero" in d["terminality"]
    assert d["cache"]["literal_first_hits"] + d["cache"]["literal_first_misses"] == sum(g["p1_uses"] for g in d["groups"])
    assert d["cache"]["terminal_hits"] + d["cache"]["terminal_misses"] == sum(g["p2_uses"] for g in d["groups"])
    return {"interval":[lo,hi],"ids":13,"groups":2}

def hostile_tests(good):
    cases=[]
    def reject(name, mutate):
        x=json.loads(json.dumps(good)); mutate(x)
        try: validate(x)
        except (AssertionError,KeyError,TypeError,ValueError): cases.append(name); return
        raise AssertionError("hostile case accepted: "+name)
    reject("missing_group", lambda x:x["groups"].pop())
    reject("duplicate_id", lambda x:x["groups"][0]["ids"].__setitem__(1,x["groups"][0]["ids"][0]))
    reject("wrong_U", lambda x:x.__setitem__("scale_U","1"))
    reject("wrong_group_scalar", lambda x:x["groups"][0].__setitem__("full_charge_scaled_U","0"))
    reject("nonterminal_occurrence", lambda x:x["groups"][0].__setitem__("full_occurrences",0))
    reject("row_output", lambda x:x.__setitem__("column_or_row_output",True))
    return cases

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("result"); ap.add_argument("--require-full",action="store_true"); ap.add_argument("--audit-out")
    a=ap.parse_args()
    assert sha(SOURCE)==SOURCE_SHA256 and sha(BINARY)==BINARY_SHA256
    d=json.loads(Path(a.result).read_text()); summary=validate(d,a.require_full)
    out={"status":"PASS_INDEPENDENT_K24_DIRECT_D17_D18_CHARGE_ONLY_VALIDATOR",
         "result":a.result,"result_sha256":sha(Path(a.result)),
         "source_sha256":SOURCE_SHA256,"binary_sha256":BINARY_SHA256,
         "summary":summary,"hostile_rejections":hostile_tests(d)}
    text=json.dumps(out,indent=2,sort_keys=True)+"\n"
    if a.audit_out: Path(a.audit_out).write_text(text)
    print(text,end="")
if __name__=="__main__": main()

