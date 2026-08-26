#!/usr/bin/env python3
import hashlib,json,struct
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];SHARDS=HERE/'stage2_shards';U=400_591_699_200;REC=104
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  while b:=f.read(16<<20):h.update(b)
 return h.hexdigest()
def i128(b):return int.from_bytes(b,'little',signed=True)
def main():
 cp=HERE/'stage2_catalog.json';c=json.loads(cp.read_text());assert sha(cp)=='855df701663cc08313c44b924ca7dc80c13e04dee45b6adfe93a1c8c59e70a9f'
 assert c['status']=='PASS_K15_K3_STAGE2_EXACT_SORTED_RUNS' and c['source_range']==[242,485]
 assert c['stage1_referee_logical_sha256']=='256bc673' and c['workers']==2 and c['key_cap']==1_000_000
 assert c['elapsed_seconds']<c['hard_gate_seconds']==600.0
 assert [x['source_record'] for x in c['records']]==list(range(242,485))
 assert all(not x['reused'] and x['attempt_prefix']==f"record_{x['source_record']:03d}_attempt_000" for x in c['records'])
 ref=set();gen=piv=out=count=uses=bytes_=0;weight=0;hashes=[]
 for x in c['records']:
  source=x['source_record'];mp=SHARDS/x['manifest'];ref.add(mp.name);assert sha(mp)==x['manifest_sha256'];m=json.loads(mp.read_text())
  assert m['status']=='PASS_EXACT_PREFIX_OR_COMPLETE_SHARD' and m['mode']=='k15' and m['source_range']==[source,source+1]
  assert m['complete_source_range'] is True and m['parent_cap']==0 and m['key_flush_cap']==1_000_000 and int(m['scale_U'])==U
  assert m['parts']==len(x['parts'])==1 and (m['generated_parents'],m['pivotable_parents'],m['outgoing_pivot_uses'])==(3_690_496,1_903_616,4_861_952)
  assert sum(m['m1_m2_hist'].values())==m['pivotable_parents']
  for k in m['m1_m2_hist']:
   a,b=map(int,k.split('_'));assert U%(a*b)==0
  assert (x['generated'],x['pivotable'],x['outgoing_uses'])==(m['generated_parents'],m['pivotable_parents'],m['outgoing_pivot_uses'])
  assert x['emitted_records_local_unique']==m['emitted_records_local_unique'] and int(x['signed_weight_sum_scaled'])==int(m['signed_weight_sum_scaled'])
  gen+=m['generated_parents'];piv+=m['pivotable_parents'];out+=m['outgoing_pivot_uses']
  y=x['parts'][0];part=SHARDS/y['name'];ref.add(part.name);assert part.stat().st_size==y['bytes'];ph=sha(part);assert ph==y['sha256'];hashes.append(ph)
  with part.open('rb') as f:h=f.read(96)
  assert h[:8]==b'K18PRF2\0' and struct.unpack_from('<I',h,8)[0]==2 and (h[12],h[13],struct.unpack_from('<H',h,14)[0])==(2,2,REC)
  assert struct.unpack_from('<Q',h,16)[0]==U and struct.unpack_from('<Q',h,24)[0]==0
  n,u=struct.unpack_from('<QQ',h,32);w=i128(h[48:64]);assert part.stat().st_size==96+REC*n
  assert n==m['emitted_records_local_unique'] and w==int(m['signed_weight_sum_scaled'])
  count+=n;uses+=u;weight+=w;bytes_+=part.stat().st_size
 actual={p.name for p in SHARDS.iterdir() if p.is_file()};assert actual==ref and len(actual)==486
 assert (gen,piv,out)==(896_790_528,462_578_688,1_181_454_336)
 assert count==89_716_017 and weight==2_183_623_986_207_050_956_800 and bytes_==9_330_489_096
 assert (c['emitted_records_local_unique'],int(c['signed_weight_sum_scaled']),c['artifact_bytes'])==(count,weight,bytes_)
 assert sha(ROOT/'computations/unaudited-codex-orbit0-k18-three-stream-exporters-2026-08-23/export_k18_parent_profiles.rs')==c['exporter_source_sha256']
 assert sha(HERE/'run_stage2.py')=='163636f9e171ccbfd1a99569c42fe0f0d5aa8717baf3a98cfac8535c32b2f8f3' and sha(Path('/tmp/export_k18_parent_profiles_stage1'))=='062a16c00d5af2e075874ccc55341b3778f3fdbd129c7cbc28c712c6c1738294'
 ans={'status':'PASS_INDEPENDENT_STAGE2_CATALOG_HASH_HEADER_REFEREE','source_coverage':[242,485],'manifests':243,'parts':243,'generated':gen,'pivotable':piv,'outgoing_uses':out,'local_unique_records':count,'part_header_uses':uses,'signed_weight_sum_scaled':str(weight),'artifact_bytes':bytes_,'catalog_sha256':sha(cp),'part_hash_set_sha256':hashlib.sha256(''.join(hashes).encode()).hexdigest(),'resource_gate':{'elapsed_seconds':c['elapsed_seconds'],'limit_seconds':600,'workers':2,'analytic_core_gb_per_worker':0.35,'rss_measured':False},'orphan_or_reused_attempts':0}
 (HERE/'results_stage2_independent_referee.json').write_text(json.dumps(ans,indent=2)+'\n');print(json.dumps(ans,indent=2))
if __name__=='__main__':main()
