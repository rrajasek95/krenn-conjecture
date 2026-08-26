#!/usr/bin/env python3
"""Compose the seven sealed K22 families into the frozen 76-ID interface."""
from fractions import Fraction
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;U=400_591_699_200
CONTRACT=ROOT/'computations/unaudited-codex-orbit0-k22-availability-schedule-2026-08-24/k22_expected_scalar_groups.json'
PARTIALS={
 'profile16':ROOT/'computations/unaudited-codex-orbit0-k22-profile-ready-charge-2026-08-24/k22_manifest_profile16_partial.json',
 'direct23':ROOT/'computations/unaudited-codex-orbit0-k22-direct23-source-fold-2026-08-24/k22_direct23_fragment_manifest.json',
 'hidden_pair2':ROOT/'computations/unaudited-codex-orbit0-k22-hidden-pair-fold-2026-08-24/k22_manifest_hidden_pair2_partial.json',
 'K14_source3':ROOT/'computations/unaudited-codex-orbit0-k22-d14-source-three-fold-2026-08-24/k22_manifest_d14_source_three_partial.json',
 'K16_grouped18':ROOT/'computations/unaudited-codex-orbit0-k22-direct-k16-18-charge-2026-08-24/k22_direct_k16_18_fragment_manifest.json',
}
RESULTS={
 'profile16':('computations/unaudited-codex-orbit0-k22-profile-ready-charge-2026-08-24/results_k22_profile_ready_charge.json','e784ebc4c004247b47b91375f6dc06cefaf6f85bae50588b3af204d02a6912e5'),
 'hidden_collected2':('computations/unaudited-codex-orbit0-k22-hidden-collected-k18-2026-08-24/results_k22_hidden_collected_k18.json','2c15fbf93a2f33a8d3819b8a8eca281b9b27326aa82e98d5610443937362bde5'),
 'direct23':('computations/unaudited-codex-orbit0-k22-direct23-source-fold-2026-08-24/results_k22_direct23.json','83a736ee104eabd1c250ca8d8351789a0657d7a909238181ac3725df9d8c7551'),
 'hidden_pair2':('computations/unaudited-codex-orbit0-k22-hidden-pair-fold-2026-08-24/results_hidden_pair_k22_charge.json','8dbe7573056067e8ae0d34ca126984e88fc5c00bc51cfa9d79a77439c0a98ce3'),
 'K15_grouped12':('computations/unaudited-codex-orbit0-k22-direct-k15-four-sink-2026-08-24/results_k22_direct_k15_four_sink.json','50ea88f5da6921db8017f9e2e7e143cc6d0426ddaeb2a6daf8050a07ac33e5da'),
 'K14_source3':('computations/unaudited-codex-orbit0-k22-d14-source-three-fold-2026-08-24/results_k22_d14_source_three.json','99bec5f72757b20449aff9d7869669e36faab0f61411d482eab13d7523a562cc'),
 'K16_grouped18':('computations/unaudited-codex-orbit0-k22-direct-k16-18-charge-2026-08-24/results_k22_direct_k16_18.json','32179485fc8e60f4cb4bd1876f15c946b1622ecb8155965a4a0d6efaaafdfa55'),
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def group(ids,scaled,path,digest):
 q=Fraction(int(scaled),U)
 return {'ids':ids,'full_scaled_U':str(scaled),'irreducible_scaled_U':str(scaled),'full':str(q),'irreducible':str(q),'evidence_path':path,'evidence_sha256':digest}
def main():
 for family,(p,d) in RESULTS.items():
  assert sha(ROOT/p)==d,(family,sha(ROOT/p))
 families={};groups=[]
 for family,p in PARTIALS.items():
  d=json.loads(p.read_text());assert (d['degree'],int(d['scale_U']))==(22,U)
  ep,eh=RESULTS[family]
  for g in d['groups']:
   if family=='K16_grouped18':assert sha(ROOT/g['evidence_path'])==g['evidence_sha256']
   else:assert (g['evidence_path'],g['evidence_sha256'])==(ep,eh)
   assert Fraction(int(g['full_scaled_U']),U)==Fraction(g['full'])==Fraction(g['irreducible'])
   assert g['full_scaled_U']==g['irreducible_scaled_U'];groups.append(dict(g))
  families[family]=len(d['groups'])
 ep,eh=RESULTS['hidden_collected2']
 hidden=json.loads((ROOT/ep).read_text())['sinks']
 hg=[]
 for name in ('D14:222|R:2-2-4','D14:222|R:2-2-2-2'):
  hg.append(group([name],hidden[name]['full_charge_scaled_U'],ep,eh))
  assert hidden[name]['full_charge_scaled_U']==hidden[name]['irreducible_charge_scaled_U']
 groups+=hg;families['hidden_collected2']=2
 ep,eh=RESULTS['K15_grouped12'];sinks=json.loads((ROOT/ep).read_text())['sinks'];kg=[]
 for name in ('D15:{223,232,322}|R:4-3','D15:{223,232,322}|R:2-2-3','D15:{223,232,322}|R:2-3-2','D15:{223,232,322}|R:3-2-2'):
  x=sinks[name];g=group(x['ids'],x['full_charge_scaled_U'],ep,eh);assert g['full']==x['full_charge']==x['irreducible_charge'];kg.append(g)
 groups+=kg;families['K15_grouped12']=4
 contract=json.loads(CONTRACT.read_text())['expected_scalar_groups'];by_ids={tuple(sorted(g['ids'])):g for g in groups};assert len(by_ids)==len(groups)==22
 ordered=[]
 for expected in contract:
  key=tuple(sorted(expected['ids']));assert key in by_ids,expected['group_id'];g=by_ids.pop(key);g['group_id']=expected['group_id'];ordered.append(g)
 assert not by_ids
 flat=[x for g in ordered for x in g['ids']];assert len(flat)==len(set(flat))==76
 assert families=={'profile16':4,'direct23':4,'hidden_pair2':2,'K14_source3':3,'K16_grouped18':3,'hidden_collected2':2,'K15_grouped12':4}
 manifest={'degree':22,'scale_U':U,'groups':ordered,'sealed_families':families,'sealed_evidence':{k:{'path':p,'sha256':d} for k,(p,d) in RESULTS.items()},'scope':'complete frozen 76-ID K22 exact-Q interface from exactly seven sealed families; no K23/K24'}
 out=HERE/'k22_manifest_complete_76.json';tmp=Path(str(out)+'.tmp');tmp.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n');tmp.replace(out)
 print(json.dumps({'status':'PASS_BUILT_K22_MANIFEST_76','covered_ids':76,'scalar_groups':22,'families':families},sort_keys=True))
if __name__=='__main__':main()
