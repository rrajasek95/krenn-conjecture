#!/usr/bin/env python3
"""Fail-closed exact merge for bounded direct-K16 R:2-2-2 K22 shards."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import argparse, json, os, tempfile

N=24_097_095
U=400_591_699_200
SUM_FIELDS=(
    'source_rows','signed_source_coefficient','l1_source_coefficient',
    'pivotable_K16_rows','p1_uses','K18_children','pivotable_K18_children',
    'p2_uses','K20_children','pivotable_K20_children','p3_uses',
    'K22_terminal_occurrences','full_occurrences','irreducible_occurrences',
    'full_charge_scaled_U','irreducible_charge_scaled_U',
)

def atomic(path,text):
    path=Path(path); tmp=Path(str(path)+'.tmp'); tmp.write_text(text); tmp.replace(path)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('output');ap.add_argument('shards',nargs='+');a=ap.parse_args()
    docs=[]
    for p in a.shards:
        d=json.loads(Path(p).read_text())
        assert d['status']=='PASS_BOUNDED_GROUPED_SIX_D16_R_2_2_2_K22_GATE'
        assert (d['group_id'],d['degree'],int(d['scale_U']),d['records_declared'],d['distributed_prefix'])==('source_D16_R2_2_2',22,U,N,False)
        docs.append((Path(p),d))
    docs.sort(key=lambda x:x[1]['record_interval'])
    cursor=0
    for _,d in docs:
        lo,hi=d['record_interval']; assert lo==cursor and hi>lo;cursor=hi
    assert cursor==N
    ids=docs[0][1]['ids'];assert len(ids)==len(set(ids))==6
    assert all(d['ids']==ids for _,d in docs)
    sums={k:sum(int(d[k]) for _,d in docs) for k in SUM_FIELDS}
    assert (sums['source_rows'],sums['signed_source_coefficient'],sums['l1_source_coefficient'])==(N,1_464_625_152,13_978_655_136)
    assert (sums['pivotable_K16_rows'],sums['p1_uses'])==(24_003_767,129_939_187)
    assert sums['K18_children']==12*sums['p1_uses']
    assert sums['K20_children']==12*sums['p2_uses']
    assert sums['K22_terminal_occurrences']==12*sums['p3_uses']==sums['full_occurrences']==sums['irreducible_occurrences']
    assert sums['full_charge_scaled_U']==sums['irreducible_charge_scaled_U']
    hist=Counter()
    for _,d in docs:hist.update({k:int(v) for k,v in d['m1_m2_m3_hist'].items()})
    assert sum(hist.values())==sums['pivotable_K20_children']
    assert sum(int(k.rsplit('_',1)[1])*v for k,v in hist.items())==sums['p3_uses']
    samples={}
    header=None
    for p,d in docs:
        lines=Path(d['sample_ledger']).read_text().splitlines()
        if header is None:header=lines[0]
        assert lines[0]==header
        for line in lines[1:]:
            f=line.split('\t');j=int(f[0]);idx=int(f[1]);assert 0<=j<=256 and int(f[14])!=0
            if j not in samples or idx<int(samples[j].split('\t')[1]):samples[j]=line
    assert sorted(samples)==list(range(257))
    sample_path=Path(str(a.output)+'.samples.tsv')
    atomic(sample_path,header+'\n'+'\n'.join(samples[j] for j in range(257))+'\n')
    q=Fraction(sums['full_charge_scaled_U'],U)
    out={
      'status':'PASS_COMPLETE_MERGED_GROUPED_SIX_D16_R_2_2_2_K22',
      'group_id':'source_D16_R2_2_2','degree':22,'scale_U':str(U),'ids':ids,
      'covered_ids':6,'individual_id_charges':None,'record_interval':[0,N],
      'records_declared':N,'shard_count':len(docs),
      'shards':[{'path':str(p),'record_interval':d['record_interval'],'elapsed_seconds':d['elapsed_seconds']} for p,d in docs],
      **{k:str(v) if 'coefficient' in k or 'charge' in k else v for k,v in sums.items()},
      'm1_m2_m3_hist':dict(sorted(hist.items())),
      'terminal_cache':{
        'hits':sum(int(d['terminal_cache']['hits']) for _,d in docs),
        'misses':sum(int(d['terminal_cache']['misses']) for _,d in docs),
        'peak_keys_per_piece':max(int(d['terminal_cache']['peak_keys_per_piece']) for _,d in docs),
      },
      'full':{'numerator':q.numerator,'denominator':q.denominator,'text':str(q)},
      'irreducible':{'numerator':q.numerator,'denominator':q.denominator,'text':str(q)},
      'literal_samples':257,'sample_ledger':str(sample_path),
      'packet_grouping_guard':'checkpoint retains collected canonical rows and coefficients but not packet labels; only the grouped six-ID scalar is source-faithful',
      'sign_rule':'stored v is the direct coefficient in P; three normalized response flips give -v/(m1*m2*m3)',
      'terminality':'literal terminal K2 response asserts every child has no available frozen pivot and full equals irreducible',
      'scope':'strict complete grouped six-ID K22 R2-2-2 sink only; exact shard merge, no individual reconstruction or membership claim',
    }
    atomic(a.output,json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':out['status'],'shards':len(docs),'charge':str(q),'samples':257},sort_keys=True))
if __name__=='__main__':main()
