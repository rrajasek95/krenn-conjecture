#!/usr/bin/env python3
from fractions import Fraction
from pathlib import Path
import hashlib, json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
U=400_591_699_200
PINS={
 "results_k22_direct23.json":"83a736ee104eabd1c250ca8d8351789a0657d7a909238181ac3725df9d8c7551",
 "results_k22_direct23.json.samples.tsv":"74d21b962521531f70e143d1aa4fae3defb7b1ea07200d820b84cee179624d31",
 "run_k22_direct23_source_fold.rs":"ccfd1af09fced6d05f0aeb40cf3ee482f8d8a26565f2448cbc30fb5c0952241b",
 "referee_k22_direct23_literals.rs":"d5b655ca6244174770b673dc425364340a2a27aca23f337cfe0ad320ef4363a7",
}
SOURCE_PINS={
 "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin":"55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b",
 "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_aux.bin":"f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab",
 "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin":"8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7",
 "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin":"4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3",
 "computations/unaudited-codex-orbit0-k22-availability-schedule-2026-08-24/k22_expected_scalar_groups.json":"e2e2ba53158365cdd03a380bcaa8699c11cbe34d2937d52f706ccc56d10cf65a",
}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
for name,digest in PINS.items(): assert sha(HERE/name)==digest,(name,sha(HERE/name))
for name,digest in SOURCE_PINS.items(): assert sha(ROOT/name)==digest,(name,sha(ROOT/name))
d=json.loads((HERE/'results_k22_direct23.json').read_text())
assert (d['status'],d['degree'],int(d['scale_U']),d['source_interval'],d['covered_ids'],d['scalar_groups'],d['literal_samples'])==('PASS_COMPLETE_K22_DIRECT_D17_D19_23_ID_SOURCE_FOLD',22,U,[0,485],23,4,257)
expected={
 'source_D17_R2_3':((82938880,81076480,267564800,1448947200,46366310400),784632481068586106880),
 'source_D17_R3_2':((82938880,81076480,267564800,842301440,10107617280),50007380854859366400),
 'source_D18_R2_2':((152251200,137817600,260736000,230937600,2771251200),-15902862330455654400),
 'source_D19_R3':((167616000,111744000,111744000,0,3575808000),91513654638516633600),
}
total=0; ids=[]
for g in d['groups']:
    counts=(g['source_heads'],g['pivotable_source_heads'],g['p1_uses'],g['p2_uses'],g['K22_terminal_occurrences'])
    assert (counts,int(g['full_charge_scaled_U']))==expected[g['group_id']]
    assert g['full_occurrences']==g['irreducible_occurrences']==g['K22_terminal_occurrences']
    assert g['full_charge_scaled_U']==g['irreducible_charge_scaled_U']
    total+=int(g['full_charge_scaled_U']); ids+=g['ids']
assert len(ids)==len(set(ids))==23 and total==910250654231506452480 and Fraction(total,U)==Fraction(79529288704,35)
ledger=(HERE/'results_k22_direct23.json.samples.tsv').read_text().splitlines()
assert len(ledger)==258
for j,line in enumerate(ledger[1:]):
    f=line.split('\t'); assert len(f)==16 and int(f[1])==j and int(f[2])==j*484//256 and int(f[13])!=0
manifest=json.loads((HERE/'k22_direct23_fragment_manifest.json').read_text())
assert len(manifest['groups'])==4 and sum(len(x['ids']) for x in manifest['groups'])==23
assert sum(int(x['full_scaled_U']) for x in manifest['groups'])==total
print(json.dumps({'status':'PASS_K22_DIRECT23_PACKAGE','covered_ids':23,'scalar_groups':4,'subtotal_scaled_U':str(total),'subtotal':'79529288704/35','literal_samples':257},sort_keys=True))
