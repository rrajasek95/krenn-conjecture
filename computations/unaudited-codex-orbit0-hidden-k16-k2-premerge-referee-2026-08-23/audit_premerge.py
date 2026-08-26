#!/usr/bin/env python3
"""Independent scoped referee of the full K2 pre-final-merge state."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import struct

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PACK=ROOT/'computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23'
PAIR=PACK/'hidden_k16_decorated_pair_orbits_full.bin'
SOURCE=PACK/'run_full_hidden_k16_k2_orbits.rs'
RESULT=PACK/'results_full_k2_premerge.json'
RESUME=PACK/'results_resume_safety.json'
DESIGN=ROOT/'computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23/filtered_k24_reducer.py'
OUT=HERE/'results_premerge_referee.json'
U=400_591_699_200

def require(x,d):
    if not x: raise RuntimeError(d)

def load(path):
    s=importlib.util.spec_from_file_location('premerge_design',path);m=importlib.util.module_from_spec(s)
    require(s.loader is not None,path);s.loader.exec_module(m);return m

D=load(DESIGN)

def header(path,magic,recsize):
    with path.open('rb') as f:h=f.read(80)
    require(len(h)==80 and h[:8]==magic,(path,h[:8]))
    require(int.from_bytes(h[8:24],'little',signed=True)==U,(path,'scale'))
    require(int.from_bytes(h[28:30],'little')==recsize,(path,'recsize'))
    count=int.from_bytes(h[48:56],'little')
    require(path.stat().st_size==80+recsize*count,(path,path.stat().st_size,count))
    return h

def canonical(row):
    s=D.CTX.signature(row);best=min(D.CTX.move_signature(s,g) for g in D.H)
    return min(D.F.move_row(row,g) for g in D.H if D.CTX.move_signature(s,g)==best)

def subtract(row,anchor):
    values=list(row)
    for c in anchor: values.remove(c)
    return bytes(values)

def pair_at(stream,index):
    stream.seek(80+53*index);b=stream.read(53);require(len(b)==53,index)
    return (b[:25],int.from_bytes(b[25:41],'little',signed=True),
            int.from_bytes(b[41:49],'little'),int.from_bytes(b[49:51],'little'),
            int.from_bytes(b[51:53],'little'))

def find_pair(stream,count,key):
    lo,hi=0,count
    while lo<hi:
        mid=(lo+hi)//2;k,*rest=pair_at(stream,mid)
        if k<key:lo=mid+1
        else:hi=mid
    k,*rest=pair_at(stream,lo);require(k==key,(key.hex(),k.hex()));return lo,rest

def main():
    frozen=json.loads(RESULT.read_text());require(frozen['status']=='PASS_COMPLETE_RESUMABLE_PRE_FINAL_MERGE',frozen)
    # Exact-pair atomic runs: headers alone prove disjoint source-slice coverage
    # and the stated engineering totals, without replaying the 75.7M parents.
    runs=sorted(PACK.glob('exact_pairs_*.bin'));require(len(runs)==31,len(runs))
    expected=0;parents=outgoing=records=0;weight=0
    for path in runs:
        h=header(path,b'H16EXA1\0',49);start,end=struct.unpack_from('<HH',h,24)
        require(start==expected and end>start,(path,start,end,expected));expected=end
        parents+=struct.unpack_from('<Q',h,32)[0];outgoing+=struct.unpack_from('<Q',h,40)[0]
        records+=struct.unpack_from('<Q',h,48)[0];weight+=int.from_bytes(h[64:80],'little',signed=True)
    require((expected,parents,outgoing,records,weight)==(485,75_691_040,511_477_120,126_544_084,146_230_609_431_055_564_800),(expected,parents,outgoing,records,weight))

    ph=header(PAIR,b'H16ORM1\0',53);pair_count=struct.unpack_from('<Q',ph,48)[0]
    require((struct.unpack_from('<Q',ph,40)[0],pair_count,int.from_bytes(ph[64:80],'little',signed=True))==
            (305,101_545_723,146_230_609_431_055_564_800),ph.hex())

    chunks=sorted(PACK.glob('pchild_chunk_*.bin'));require(len(chunks)==291,len(chunks))
    expected=0;generated=rows=0;child_weight=0;samples=[]
    with PAIR.open('rb') as ps:
        for i,path in enumerate(chunks):
            require(path.name==f'pchild_chunk_{i:04}.bin',path.name);h=header(path,b'H18CHC1\0',80)
            start,end,count,raw=struct.unpack_from('<QQQQ',h,32)
            require(start==expected and end>start and raw==12*(end-start),(i,start,end,raw));expected=end
            generated+=raw;rows+=count;child_weight+=int.from_bytes(h[64:80],'little',signed=True)
            with path.open('rb') as stream:
                for ri in sorted({0,count//2,count-1}):
                    stream.seek(80+80*ri);b=stream.read(80);require(len(b)==80,(i,ri))
                    row=b[:24];w=int.from_bytes(b[24:40],'little',signed=True);pairrow=b[40:64]
                    p2,tail=b[64],b[65];uses=struct.unpack_from('<Q',b,66)[0]
                    orbit,stab=struct.unpack_from('<HH',b,74);piv=b[78];m2=b[79]
                    require(w and p2<78 and tail<12 and uses and orbit*stab==384 and piv<2,(i,ri))
                    key=pairrow+bytes([p2]);pi,(pw,pu,po,pss)=find_pair(ps,pair_count,key)
                    require(start<=pi<end and (uses,orbit,stab)==(pu,po,pss),(i,ri,pi,start,end))
                    rawrow=bytes(sorted(subtract(pairrow,D.CTX.anchors[p2])+D.CTX.tails[p2][2][tail]))
                    require(canonical(rawrow)==row,(i,ri,row.hex(),rawrow.hex()))
                    require(bool(D.CTX.pivots(D.CTX.signature(row)))==bool(piv),(i,ri,'pivot'))
                    require(len(D.CTX.pivots(D.CTX.signature(pairrow)))==m2,(i,ri,m2))
                    samples.append((i,ri,pi))
    require((expected,generated,rows,child_weight)==(pair_count,1_218_548_676,516_225_702,1_754_767_313_172_666_777_600),(expected,generated,rows,child_weight))

    src=SOURCE.read_text()
    resume=json.loads(RESUME.read_text())
    require(resume['status']=='PASS_RESUME_SAFETY_GUARDS',resume)
    require(resume['hostile_truncation_failed'] and resume['hostile_histogram_reset_failed'] and
            resume['hostile_eager_cleanup_failed'] and resume['retained_chunks_after_cleanup_hostile']==291,resume)
    # The 8-byte magic fix and the hardened skip/merge validator are present.
    require('b"H18CHC1\\0"' in src, 'header patch absent')
    require('fn validate_child_chunk' in src and
            'validate_child_chunk(&path,Some((start,end)))' in src and
            'let stab_hist=scan_pair_stabilizers' in src,
            'hardened resume validator/stabilizer replay absent')

    unsafe_eager_cleanup=';for p in &child_chunks{remove_file(p).unwrap()}' in src
    cleanup_is_gated=('fn cleanup_refereed_child_chunks' in src and
                      'PASS_INDEPENDENT_K18_REFEREE' in src and
                      'assert!(child_chunks.iter().all' in src)
    require(cleanup_is_gated,'post-merge retention / separately gated cleanup absent')
    result={'status':'PASS_SCOPED_PREMERGE_REJECT_MERGE_LAUNCH' if unsafe_eager_cleanup else 'PASS_SCOPED_PREMERGE_ACCEPT_MERGE_LAUNCH',
      'scope':'All atomic pair runs, full decorated-pair ledger, and 291 premerge child chunks; no cross-chunk merge or K18 split.',
      'atomic_runs':31,'source_slices':[0,expected if False else 485],'parents':parents,'second_pivot_uses':outgoing,
      'run_pair_records':records,'pair_orbits':pair_count,'pair_orbit_zero_keys':305,
      'pair_weight_sum_scaled':str(weight),'child_chunks':291,'covered_pair_interval':[0,pair_count],
      'generated_K2_children':generated,'within_chunk_nonzero_rows':rows,'child_weight_sum_scaled':str(child_weight),
      'sampled_nested_witnesses':len(samples),
      'resume_hostile_guards':{'truncation':resume['hostile_truncation_failed'],'empty_stabilizer_histogram':resume['hostile_histogram_reset_failed'],'premature_cleanup':resume['hostile_eager_cleanup_failed'],'retained_chunks':resume['retained_chunks_after_cleanup_hostile']},
      'resume_verdict':'PASS_FOR_CURRENT_ATOMIC_STATE: driver now validates U, record size, interval, raw count, file size and expected coverage for every skipped/merged child chunk, and rescans the full pair ledger for strict order/mass/stabilizers. Child row order and coefficient sums are re-consumed by the final merge but are not separately content-hashed beforehand.',
      'merge_launch_verdict':'REJECT until the main path stops deleting all 291 child chunks immediately after merge; cleanup must be a separate post-referee operation gated by final checkpoint validation and an independent-referee marker.' if unsafe_eager_cleanup else 'ACCEPT: child chunks are retained after merge and cleanup is separately gated by final checkpoint validation plus an independent-referee marker.',
      'provenance_guard':'Each sampled child has a literal decorated-pair/tail witness landing on the canonical row. It is a support witness, not a decomposition of an aggregated coefficient into every raw source occurrence.',
      'unfrozen_claims':['global exact-key pre-H zero count 52 is report/log only, not encoded in the final pair header','cross-chunk exact-zero count','K18 pivotable/irreducible support and masses'],
      'pinned':{str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in(SOURCE,RESULT,RESUME,PACK/'audit_full_k2_premerge.py',PACK/'audit_full_pair_stabilizers.rs',DESIGN)}}
    logical=json.dumps(result,sort_keys=True,separators=(',',':'));result['logical_sha256']=sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
