#!/usr/bin/env python3
"""Bounded exact counterowner for every r13 shell column; no solve."""

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import importlib.util, json, resource, time
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=HERE/'run_d12_lazy_cegar.py'
CHECKPOINT=HERE/'checkpoint_d12_incremental_cegar.json'
RESULT=HERE/'results_d12_shell_counterowners.json'
P=1_073_741_827; WALL=600; RSS=4*1024**3

def load(path,name):
 s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
S=load(SOURCE,'boundary_counterowner_source')
def require(c,m):
 if not c: raise RuntimeError(m)
def peak():
 v=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss; return int(v if v>10_000_000 else v*1024)

def main():
 started=time.monotonic(); p=S.Provider()
 def guard(label): require(time.monotonic()-started<WALL and peak()<RSS,f'cap {label}')
 def orbit(row): return tuple(sorted(set(bytes(sorted(t[v] for v in row)) for t in p.transforms)))
 def entries(column):
  a=defaultdict(int)
  for code,mult in p.column_orbit(column):
   for term,coefficient in p.generator(code).items():
    row=bytes(sorted(mult+term))
    if row==orbit(row)[0]: a[row]+=coefficient
  return {r:v for r,v in a.items() if v}
 def incident_uncached(row):
  answer=set()
  for degree in range(min(4,len(row))+1):
   seen=set()
   for positions in combinations(range(len(row)),degree):
    term=bytes(row[i] for i in positions)
    if term in seen: continue
    seen.add(term); multiplier=p.quotient(row,term)
    if multiplier is None or len(multiplier)>8: continue
    for code in p.term_index.get(term,()):
     answer.add(p.canonical_column((code,multiplier)))
  return tuple(sorted(answer))
 def lift(v):
  values={Fraction(n,d) for d in range(1,65) for n in range(-64,65)
          if n*pow(d,-1,P)%P==v}
  require(len(values)==1,f'lift {v}'); return values.pop()

 checkpoint=json.loads(CHECKPOINT.read_text())
 sequence=[(int(c),bytes.fromhex(m)) for c,m in checkpoint['column_insertion_sequence']]
 selected=set(sequence)
 dual={bytes.fromhex(r):lift(int(v)) for r,v in checkpoint['last_modular_dual']}
 candidates=p.incident_columns(dual)
 pending=[]; outputs=[]
 for col in sorted(candidates):
  e=entries(col); pairing=sum(Fraction(a)*dual.get(r,0) for r,a in e.items())
  if pairing and col not in selected: pending.append(col); outputs.append(e)
 require((len(candidates),len(pending))==(1204,1186),'shell census')
 pending_set=set(pending)
 count=defaultdict(int)
 for e in outputs:
  for row in e: count[row]+=1

 records=[]; incident_hist=Counter(); tried_hist=Counter()
 for index,(col,e) in enumerate(zip(pending,outputs)):
  record=None; tried=0
  for row in sorted((r for r in e if count[r]==1),key=lambda r:(-len(r),r)):
   tried+=1
   if p.target_coefficient(row)!=0: continue
   incident=incident_uncached(row)
   if any(owner in selected for owner in incident): continue
   external=[owner for owner in incident if owner!=col]
   if not external: continue
   owner=external[0]; oe=entries(owner)
   require(row in oe,'external incidence replay')
   record={
    'shell_column':[col[0],col[1].hex()],
    'shell_coefficient':e[row],
    'shell_private_row':row.hex(),
    'target_coefficient':0,
    'full_incident_count':len(incident),
    'external_column':[owner[0],owner[1].hex()],
    'external_coefficient':oe[row],
    'external_is_selected':owner in selected,
    'external_is_pending':owner in pending_set,
    'shell_private_rows_tried':tried,
   }; incident_hist[len(incident)]+=1; tried_hist[tried]+=1; break
  require(record is not None,f'no external owner for pending {index}')
  records.append(record)
  if (index+1)%128==0:
   print('COUNTEROWNER',index+1,'/',len(pending),'rss',peak(),flush=True); guard(index)
 payload={
  'format':'n8-chart1-boundary-d12-shell-counterowners-v1',
  'status':'EXACT_ALL_SHELL_PRIVATE_ROWS_HAVE_EXTERNAL_OWNERS',
  'incident_column_orbits':len(candidates),'pending_column_orbits':len(pending),
  'counterowner_records':records,
  'full_incident_count_histogram':sorted(incident_hist.items()),
  'shell_private_rows_tried_histogram':sorted(tried_hist.items()),
  'all_external_owners_unselected':all(not r['external_is_selected'] for r in records),
  'all_external_owners_outside_pending':all(not r['external_is_pending'] for r in records),
  'scope':'Exact no-solve counterguard: shell-private ownership does not yield a terminal separator.',
  'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
  'checkpoint_sha256':sha256(CHECKPOINT.read_bytes()).hexdigest(),
  'peak_rss_bytes_nonlogical':peak(),'elapsed_seconds_nonlogical':time.monotonic()-started,
 }
 logical={k:v for k,v in payload.items() if not k.endswith('_nonlogical')}
 payload['logical_sha256']=sha256(json.dumps(logical,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 RESULT.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
 print(payload['status'],payload['logical_sha256'])
if __name__=='__main__': main()
