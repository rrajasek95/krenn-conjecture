#!/usr/bin/env python3
"""Replay, hash, and package the full hidden-K16 parent recovery."""
from __future__ import annotations
from collections import Counter
import hashlib,json,struct
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];U=400_591_699_200
MERGED=HERE/'hidden_k16_second_pivot_profiles_full.bin';OUT=HERE/'results_full_hidden_k16_parent_recovery.json'
UPSTREAM=[ROOT/'computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin',ROOT/'computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_aux.bin',ROOT/'computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin']
SOURCES=[HERE/'reconstruct_hidden_k16_parent_runs.rs',HERE/'merge_hidden_k16_profiles.rs',HERE/'stream_hidden_k16_children.rs']
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(4<<20):h.update(b)
 return h.hexdigest()
def addhist(dst,src):
 for k,v in src.items():dst[k]+=v
def main():
 runs=[];expected=0;tot=Counter();m1=Counter();m2=Counter();prod=Counter();parent_sum=0;profile_sum=0;led=[]
 for mp in sorted(HERE.glob('run_*.json')):
  j=json.loads(mp.read_text());assert j['status']=='PASS_ATOMIC_RUN' and j['start']==expected and j['end']>j['start'];expected=j['end'];runs.append(j);p=HERE/j['parent_file'];q=HERE/j['profile_file']
  hb=p.open('rb').read(40);hq=q.open('rb').read(40);assert hb[:8]==b'H16RUN2\0' and hq[:8]==b'H16PF2\0\0';assert int.from_bytes(hb[8:24],'little',signed=True)==int.from_bytes(hq[8:24],'little',signed=True)==U
  for h,rs,count in ((hb,64,j['hidden_parent_occurrences']),(hq,59,j['unique_nonzero_profiles'])):
   assert struct.unpack_from('<HHH',h,24)==(j['start'],j['end'],rs);assert struct.unpack_from('<Q',h,32)[0]==count
  assert p.stat().st_size==j['parent_bytes']==40+64*j['hidden_parent_occurrences'];assert q.stat().st_size==j['profile_bytes']==40+59*j['unique_nonzero_profiles']
  for k in ('heads','first_pivot_uses','hidden_parent_occurrences','outgoing_second_pivot_uses','unique_nonzero_profiles','parent_bytes','profile_bytes'):tot[k]+=j[k]
  parent_sum+=int(j['parent_weight_sum_scaled']);profile_sum+=int(j['profile_weight_sum_scaled']);assert int(j['profile_raw_weight_sum_scaled'])==int(j['profile_weight_sum_scaled'])
  addhist(m1,j['first_denominator_hist']);addhist(m2,j['second_denominator_hist']);addhist(prod,j['product_denominator_hist'])
  led.append({'start':j['start'],'end':j['end'],'parents':j['hidden_parent_occurrences'],'profiles':j['unique_nonzero_profiles'],'parent_sha256':sha(p),'profile_sha256':sha(q)})
 assert expected==485 and len(runs)==31 and tot['heads']==838080 and tot['hidden_parent_occurrences']==75_691_040 and tot['outgoing_second_pivot_uses']==511_477_120
 assert parent_sum==-146_230_609_431_055_564_800 and profile_sum==-parent_sum
 merge=json.loads((HERE/'results_profile_merge.json').read_text());assert merge['input_records']==tot['unique_nonzero_profiles']==21_116_357 and merge['output_nonzero_profiles']==6_229_700 and int(merge['output_weight_sum_scaled'])==profile_sum
 with MERGED.open('rb') as f:
  h=f.read(32);assert h[:8]==b'H16MER2\0' and int.from_bytes(h[8:24],'little',signed=True)==U;count=struct.unpack_from('<Q',h,24)[0];assert count==merge['output_nonzero_profiles'] and MERGED.stat().st_size==32+59*count
  prior=None;sm=0
  for _ in range(count):
   rec=f.read(59);key=rec[:43];v=int.from_bytes(rec[43:],'little',signed=True);assert key[42]==0 and v and (prior is None or prior<key);prior=key;sm+=v
  assert not f.read(1) and sm==profile_sum
 guards={}
 for d,n in ((2,36),(3,96),(4,180)):
  p=HERE/f'provider_guard_k{d}.bin';h=p.open('rb').read(64);assert h[:8]==b'H16CHD2\0' and int.from_bytes(h[8:24],'little',signed=True)==U and h[24]==d
  assert struct.unpack_from('<H',h,25)[0]==0 and struct.unpack_from('<Q',h,32)[0]==0 and struct.unpack_from('<Q',h,40)[0]==1 and struct.unpack_from('<Q',h,48)[0]==n and struct.unpack_from('<H',h,56)[0]==52 and p.stat().st_size==64+52*n
  guards[str(d)]={'children':n,'bytes':p.stat().st_size,'sha256':sha(p)}
 result={'status':'PASS_FULL_HIDDEN_K16_PARENT_RECOVERY','scope':'parents/profiles/providers only; no child-tail charge evaluation','scale':U,'atomic_runs':31,'H_slices':485,'heads':tot['heads'],'first_pivot_uses':tot['first_pivot_uses'],'hidden_parent_occurrences':tot['hidden_parent_occurrences'],'parent_weight_sum_scaled':str(parent_sum),'outgoing_second_pivot_uses':tot['outgoing_second_pivot_uses'],'input_profile_records':tot['unique_nonzero_profiles'],'input_profile_weight_sum_scaled':str(profile_sum),'merged_profile_records':count,'merged_profile_weight_sum_scaled':str(sm),'exact_zero_profile_keys':merge['exact_zero_keys'],'parent_bytes_total':tot['parent_bytes'],'profile_run_bytes_total':tot['profile_bytes'],'merged_profile_bytes':MERGED.stat().st_size,'first_denominator_hist':dict(sorted(m1.items(),key=lambda x:int(x[0]))),'second_denominator_hist':dict(sorted(m2.items(),key=lambda x:int(x[0]))),'product_denominator_hist':dict(sorted(prod.items(),key=lambda x:int(x[0]))),'child_provider':{'restart_key':'(run_start,parent_start,parent_count,degree)','tail_counts':{'2':12,'3':32,'4':60},'guard_runs':guards},'run_ledger':led,'sha256':{'merged_profiles':sha(MERGED),**{p.name:sha(p) for p in UPSTREAM+SOURCES},'profile_merge_result':sha(HERE/'results_profile_merge.json')}}
 logical=hashlib.sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest();result['logical_sha256']=logical;tmp=OUT.with_suffix('.json.tmp');tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');tmp.replace(OUT);print(json.dumps({k:result[k] for k in ('status','atomic_runs','hidden_parent_occurrences','outgoing_second_pivot_uses','input_profile_records','merged_profile_records','exact_zero_profile_keys','logical_sha256')},indent=2))
if __name__=='__main__':main()
