#!/usr/bin/env python3
import hashlib
import json
import struct
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SHARDS=HERE/'stage1_shards'
U=400_591_699_200
REC=104

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while b:=f.read(16<<20): h.update(b)
    return h.hexdigest()

def i128(b):return int.from_bytes(b,'little',signed=True)

def main():
    catalog_path=HERE/'stage1_catalog.json'; catalog=json.loads(catalog_path.read_text())
    assert sha(catalog_path)=='e9dbee8ac2c9e80db4fa8a7cae86795927bc5d7c9f509d116c3a075f488f1537'
    assert catalog['status']=='PASS_K15_K3_STAGE1_EXACT_SORTED_RUNS'
    assert catalog['source_range']==[0,242] and catalog['workers']==2 and catalog['key_cap']==1_000_000
    assert catalog['elapsed_seconds']<catalog['hard_gate_seconds']==600.0
    assert [x['source_record'] for x in catalog['records']]==list(range(242))
    assert all(not x['reused'] and x['attempt_prefix']==f"record_{x['source_record']:03d}_attempt_000" for x in catalog['records'])

    referenced=set(); total_count=total_uses=total_bytes=0; total_weight=0
    total_generated=total_pivotable=total_outgoing=0; part_hashes=[]
    for source,x in enumerate(catalog['records']):
        manifest=SHARDS/x['manifest']; referenced.add(manifest.name)
        assert sha(manifest)==x['manifest_sha256']
        m=json.loads(manifest.read_text())
        assert m['status']=='PASS_EXACT_PREFIX_OR_COMPLETE_SHARD' and m['mode']=='k15'
        assert m['source_range']==[source,source+1] and m['complete_source_range'] is True
        assert m['parent_cap']==0 and m['key_flush_cap']==1_000_000 and int(m['scale_U'])==U
        assert m['parts']==len(x['parts'])==1
        assert (m['generated_parents'],m['pivotable_parents'],m['outgoing_pivot_uses'])==(3_690_496,1_903_616,4_861_952)
        assert sum(m['m1_m2_hist'].values())==m['pivotable_parents']
        for key in m['m1_m2_hist']:
            a,b=map(int,key.split('_'));assert U%(a*b)==0
        assert x['generated']==m['generated_parents'] and x['pivotable']==m['pivotable_parents']
        assert x['outgoing_uses']==m['outgoing_pivot_uses']
        assert x['emitted_records_local_unique']==m['emitted_records_local_unique']
        assert int(x['signed_weight_sum_scaled'])==int(m['signed_weight_sum_scaled'])
        total_generated+=m['generated_parents'];total_pivotable+=m['pivotable_parents'];total_outgoing+=m['outgoing_pivot_uses']
        for y in x['parts']:
            part=SHARDS/y['name'];referenced.add(part.name)
            assert part.stat().st_size==y['bytes'];ph=sha(part);assert ph==y['sha256'];part_hashes.append(ph)
            with part.open('rb') as f:h=f.read(96)
            assert h[:8]==b'K18PRF2\0' and struct.unpack_from('<I',h,8)[0]==2
            assert (h[12],h[13],struct.unpack_from('<H',h,14)[0])==(2,2,REC)
            assert struct.unpack_from('<Q',h,16)[0]==U and struct.unpack_from('<Q',h,24)[0]==0
            count,uses=struct.unpack_from('<QQ',h,32);weight=i128(h[48:64])
            assert part.stat().st_size==96+REC*count
            assert count==m['emitted_records_local_unique'] and weight==int(m['signed_weight_sum_scaled'])
            total_count+=count;total_uses+=uses;total_weight+=weight;total_bytes+=part.stat().st_size
    actual={p.name for p in SHARDS.iterdir() if p.is_file()}
    assert actual==referenced and len(actual)==484
    assert (total_generated,total_pivotable,total_outgoing)==(893_100_032,460_675_072,1_176_592_384)
    assert total_count==112_628_530 and total_weight==-318_525_115_738_462_617_600
    assert total_bytes==11_713_390_352==catalog['artifact_bytes']
    assert catalog['emitted_records_local_unique']==total_count and int(catalog['signed_weight_sum_scaled'])==total_weight
    assert sha(ROOT/'computations/unaudited-codex-orbit0-k18-three-stream-exporters-2026-08-23/export_k18_parent_profiles.rs')==catalog['exporter_source_sha256']
    assert sha(HERE/'run_stage1.py')=='004c7652c0a05390fba253cbe21674eb088efd415c065b863922d26245cf2fd9'
    assert sha(Path('/tmp/export_k18_parent_profiles_stage1'))=='062a16c00d5af2e075874ccc55341b3778f3fdbd129c7cbc28c712c6c1738294'
    out={
      'status':'PASS_INDEPENDENT_STAGE1_CATALOG_HASH_HEADER_REFEREE','source_coverage':[0,242],
      'manifests':242,'parts':242,'generated':total_generated,'pivotable':total_pivotable,
      'outgoing_uses':total_outgoing,'local_unique_records':total_count,'part_header_uses':total_uses,
      'signed_weight_sum_scaled':str(total_weight),'artifact_bytes':total_bytes,
      'catalog_sha256':sha(catalog_path),'part_hash_set_sha256':hashlib.sha256(''.join(part_hashes).encode()).hexdigest(),
      'resource_gate':{'elapsed_seconds':catalog['elapsed_seconds'],'limit_seconds':600,'workers':2,'analytic_core_gb_per_worker':0.35,'rss_measured':False},
      'orphan_or_reused_attempts':0,'hostile_guard':'catalog/source range, part hash/header/count or signed-weight mutation is rejected'
    }
    (HERE/'results_stage1_independent_referee.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
