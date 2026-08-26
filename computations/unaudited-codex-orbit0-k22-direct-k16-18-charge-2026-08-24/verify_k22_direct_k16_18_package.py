#!/usr/bin/env python3
from fractions import Fraction
from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parent; R=H.parents[1]; U=400_591_699_200
PINS={
 'results_k22_direct_k16_33.json':'38787f52064bf3e1ae8e7028b1f69a17695862867a652880fa322f70280dd0d2',
 'results_k22_direct_k16_33.json.samples.tsv':'04341ea0de3e505ca2f34b51711fd6a304c2cb2686abd6a78562bdce2aa56e83',
 'results_k22_direct_k16_42.json':'26e645e191c9e5521a1b6d84e50d09e00ce80bed952515cd005bd203a1f20415',
 'results_k22_direct_k16_42.json.samples.tsv':'b59dbd19bf23862c53a3a4e33c2a91bb8e9854a359e2ff38b89591ac6752369e',
 'results_k22_direct_k16_222.json':'6dc3bbabe34c6479b360da62f29579e5737db62fbb9e655a22e226f9d2bf2887',
 'results_k22_direct_k16_222.json.samples.tsv':'1a751b5249077884bf522e5e27faf7dacdc1c85341d2b56f86314acf7fb861ff',
 'results_k22_direct_k16_42_candidate_census.json':'52cf061f786aec5b583390d4feda5eb599b198231ffd5ea9d09736aae5851246',
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for p,x in PINS.items():assert sha(H/p)==x,(p,sha(H/p))
assert sha(R/'computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k16.bin')=='93c1b21eaa1723b98eb4d3b59ada6d6a867c434573a255d2a48fcdeead0656d3'
docs=[json.loads((H/p).read_text()) for p in ('results_k22_direct_k16_33.json','results_k22_direct_k16_42.json','results_k22_direct_k16_222.json')]
expect={
 'source_D16_R3_3':(2041782688,65337046016,1094959064000491683840),
 'source_D16_R4_2':(1186804200,14241650400,44519435361881948160),
 'source_D16_R2_2_2':(2745607644,32947291728,516173272311762616320),
}
ids=[];total=0
for d in docs:
 assert (d['degree'],int(d['scale_U']),d['covered_ids'],d['source_rows'],d['signed_source_coefficient'],d['l1_source_coefficient'],d['pivotable_K16_rows'],d['p1_uses'],d['literal_samples'])==(22,U,6,24097095,'1464625152','13978655136',24003767,129939187,257)
 puses=d.get('p3_uses',d['p2_uses']);p,n,q=expect[d['group_id']]
 assert (puses,d['K22_terminal_occurrences'],int(d['full_charge_scaled_U']))==(p,n,q)
 assert d['full_occurrences']==d['irreducible_occurrences']==n and d['full_charge_scaled_U']==d['irreducible_charge_scaled_U']
 ids+=d['ids'];total+=q
assert len(ids)==len(set(ids))==18 and total==1655651771674136248320 and Fraction(total,U)==Fraction(1591211034496,385)
for d in docs:
 lines=Path(d['sample_ledger']).read_text().splitlines();assert len(lines)==258
 assert [int(x.split('\t')[0]) for x in lines[1:]]==list(range(257))
 assert all(int(x.split('\t')[-3])!=0 for x in lines[1:])
m=json.loads((H/'k22_direct_k16_18_fragment_manifest.json').read_text());assert sum(len(x['ids']) for x in m['groups'])==18 and sum(int(x['full_scaled_U']) for x in m['groups'])==total
z=json.loads((H/'results_k22_direct_k16_18.json').read_text());assert (z['covered_ids'],z['scalar_groups'],int(z['full_charge_scaled_U']),z['full'])==(18,3,total,'1591211034496/385')
print(json.dumps({'status':'PASS_K22_DIRECT_K16_18_PACKAGE','covered_ids':18,'scalar_groups':3,'subtotal_scaled_U':str(total),'subtotal':'1591211034496/385','literal_samples':771},sort_keys=True))
