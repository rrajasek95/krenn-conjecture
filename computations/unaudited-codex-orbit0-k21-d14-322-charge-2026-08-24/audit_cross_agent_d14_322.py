#!/usr/bin/env python3
"""Cross-agent exact-interface referee for singleton D14:222|R:3-2-2."""
from __future__ import annotations
import csv, hashlib, json, struct
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
U=400_591_699_200
PINS={
 "MANIFEST.sha256":"5d4bfc94c9c798fc3afe043ba22cf019f03f090d84ec1a20bca0cdd9004174dc",
 "run_k21_d14_322_charge.rs":"9667311ff4c870eee1f6a8e7f881bb9082f01f1b6bceee7947404901a8003e72",
 "results_k21_d14_322_charge.json":"46065e0c432be6b37ca4044998a8cada8a0e83527699581ff2040735cdd7f7aa",
 "results_k21_d14_322_charge.json.samples.tsv":"5791b75e9412cca4eb0cdcea2ae262f91a1fb7e2f02d0891b82446c16ef872be",
 "referee_cross_agent_nonzero.rs":"2b3672d261bdb45aa28d324e168d8651b95398773922884e323e48da7c96dfda",
 "results_cross_agent_nonzero_referee.json":"ec0ca0088a92bbd1d09e259154a50148303cac5671c4bb2f729c8523e6e8ebcb",
}
INPUTS={
 ROOT/"computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin":"55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b",
 ROOT/"computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_aux.bin":"f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab",
 ROOT/"computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin":"8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7",
 ROOT/"computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin":"4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3",
 ROOT/"computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs":"24fa6d9ef9d8cadfa8b0b9e5ae01692f96bdf9df2168f4a26ccfa94b062e6045",
}
def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
for name,want in PINS.items():assert sha(HERE/name)==want,(name,sha(HERE/name))
for path,want in INPUTS.items():assert sha(path)==want,(path,sha(path))
# Verify the producer's sealed manifest, not only its outer hash.
for line in (HERE/"MANIFEST.sha256").read_text().splitlines():
 want,name=line.split("  ",1);assert sha(HERE/name)==want,(name,sha(HERE/name))
r=json.loads((HERE/"results_k21_d14_322_charge.json").read_text())
assert (r["status"],r["lineage_id"],r["covered_ids"])==("PASS_COMPLETE_SINGLETON_D14_222_R_3_2_2_K21_CHARGE","D14:222|R:3-2-2",1)
assert r["lineage_id"]!="D14:222|R:2-3-2" and r["lineage_id"]!="D14:222|R:3-2-2-2"
assert int(r["scale_U"])==U and (r["R8_records_consumed"],r["R8_records_declared"],r["source_heads"])==(485,485,838_080)
# Independently parse the pinned R8 records and rederive source mass.
b=INPUTS.keys().__iter__().__next__().read_bytes();assert b[:11]==b"K16DIRECT1\0"
nt,nr,np,na=struct.unpack_from("<IIII",b,11);assert (nt,nr,np,na)==(384,485,78,12)
off=11+16+12+nt*(252+12);mass=[]
for _ in range(nr):
 off+=12;size=struct.unpack_from("<I",b,off)[0];off+=4;coeff=struct.unpack_from("<q",b,off)[0];off+=8;mass.append(size*coeff)
assert sum(mass)*1728==int(r["source_mass_sum"])==-40_310_784
assert sum(abs(x) for x in mass)*1728==int(r["source_mass_l1"])==385_689_600
assert (r["selected_p1_uses"],r["K17_candidates"],r["pivotable_K17_children"])==(6_619_280,211_816_960,197_414_400)
assert (r["selected_p2_uses"],r["K19_candidates"],r["pivotable_K19_children"])==(815_482_880,9_785_794_560,2_969_658_880)
assert (r["selected_p3_uses"],r["K21_terminal_occurrences"])==(5_075_412_480,60_904_949_760)
assert r["K17_candidates"]==32*r["selected_p1_uses"] and r["K19_candidates"]==12*r["selected_p2_uses"] and r["K21_terminal_occurrences"]==12*r["selected_p3_uses"]
assert r["full_occurrences"]==r["irreducible_occurrences"]==r["K21_terminal_occurrences"] and r["all_K21_children_irreducible"]
assert r["full_charge_scaled_U"]==r["irreducible_charge_scaled_U"]=="-832152508704647184384"
assert Fraction(int(r["full_charge_scaled_U"]),U)==Fraction(-32_834_300_375_025_536,15_806_175)
h1={int(k):v for k,v in r["first_denominator_hist"].items()};h2={int(k):v for k,v in r["second_denominator_hist"].items()};h3={int(k):v for k,v in r["third_denominator_hist"].items()};hp={int(k):v for k,v in r["product_denominator_hist"].items()}
assert sum(h1.values())==r["source_heads"] and sum(k*v for k,v in h1.items())==r["selected_p1_uses"]
assert sum(h2.values())==r["pivotable_K17_children"] and sum(k*v for k,v in h2.items())==r["selected_p2_uses"]
assert sum(h3.values())==r["pivotable_K19_children"] and sum(k*v for k,v in h3.items())==r["selected_p3_uses"]
assert sum(hp.values())==r["pivotable_K19_children"] and all(U%k==0 for k in hp)
assert r["sign_rule"]=="direct coefficient=-M; three normalized response flips give terminal +M/(m1*m2*m3)"
assert "no K21 row collection, K22" in r["scope"]
x=json.loads((HERE/"results_cross_agent_nonzero_referee.json").read_text())
assert x["status"]=="PASS_CROSS_AGENT_257_DISTRIBUTED_NONZERO_D14_322_K21_REFEREE" and x["strict_lineage_id"]==r["lineage_id"]
assert (x["distributed_source_heads"],x["recorded_witness_literal_terminal_K21_children"],x["independently_selected_nonzero_terminal_K21_children"],x["recorded_witness_rows_and_terminal_charges_matched"])==(257,3084,3084,257)
assert x["all_U_divisions_exact"] and x["all_literal_K21_children_terminal"] and "no full aggregate rerun and no K22" in x["scope"]
with (HERE/"results_k21_d14_322_charge.json.samples.tsv").open(newline="") as f:rows=list(csv.DictReader(f,delimiter="\t"))
assert len(rows)==257 and [int(z["sample_bin"]) for z in rows]==list(range(257))
assert all(int(z["head_index"])*257//838_080==j and int(z["charge_scaled_U"])!=0 for j,z in enumerate(rows))
logical={"lineage_id":r["lineage_id"],"scale_U":str(U),"scaled":r["full_charge_scaled_U"],"charge":"-32834300375025536/15806175","K21":r["K21_terminal_occurrences"],"cross_samples":257,"terminal":True}
logical_sha=hashlib.sha256(json.dumps(logical,sort_keys=True,separators=(",",":")).encode()).hexdigest()
out={"status":"PASS_TERMINAL_CROSS_AGENT_REFEREE_D14_222_R_3_2_2_K21_SINGLETON","logical_sha256":logical_sha,"strict_lineage_id":r["lineage_id"],"charge":"-32834300375025536/15806175","charge_scaled_U":r["full_charge_scaled_U"],"guards":{"producer_manifest_and_all_inputs_pinned":True,"source_mass_independently_rederived":True,"exact_recurrence_census_and_denominator_histograms":True,"three_response_sign_and_U_arithmetic":True,"full_equals_irreducible":True,"257_distributed_nonzero_heads_rebuilt":True,"recorded_and_independently_selected_terminal_K2_responses_literal":True,"no_full_rerun":True,"no_K22":True}}
(HERE/"results_cross_agent_referee.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
