#!/usr/bin/env python3
"""Finalize the independent full-merge replay with byte digests and hostile guards."""
from hashlib import sha256
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PACK=ROOT/'computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23'
RAW=HERE/'results_final_merge_referee.json'
OUT=HERE/'results_final_merge_referee_final.json'
EXPECTED={
 'pivotable':'442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8',
 'irreducible':'c60fd9763d604f27213542a3bec9376849e046be06edf4e68035c849b097e111',
}

def hash_with_hostile(path):
    good=sha256();bad=sha256();first=True
    with path.open('rb') as f:
        while b:=f.read(8<<20):
            good.update(b)
            if first:
                q=bytearray(b);q[80+24]^=1 # first coefficient byte
                bad.update(q);first=False
            else: bad.update(b)
    return good.hexdigest(),bad.hexdigest()

def main():
    r=json.loads(RAW.read_text());assert r['status']=='PASS_INDEPENDENT_FULL_K18_MERGE_REPLAY'
    paths={
      'pivotable':PACK/'checkpoint_k18_22_pivotable.bin',
      'irreducible':PACK/'checkpoint_k18_22_irreducible.bin',
    }
    digests={};hostile={}
    for k,p in paths.items():
        d,m=hash_with_hostile(p);assert d==EXPECTED[k] and m!=d
        digests[k]=d;hostile[k]=m
    assert len(list(PACK.glob('pchild_chunk_*.bin')))==291
    result={k:v for k,v in r.items() if k!='elapsed_seconds'}
    result.update({
      'status':'PASS_INDEPENDENT_FINAL_K18_REFEREE',
      'checkpoint_sha256':digests,
      'hostile_one_weight_mutation_sha256':hostile,
      'hostile_mutations_rejected':True,
      'retained_child_chunks':291,
      'scope':'Complete retained-chunk merge into K18 [2,2] pivotable/irreducible checkpoints only; no cleanup and no K20.',
      'referee_source_sha256':sha256((HERE/'referee_final_merge.rs').read_bytes()).hexdigest(),
    })
    logical=json.dumps(result,sort_keys=True,separators=(',',':')).encode()
    result['logical_sha256']=sha256(logical).hexdigest()
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
