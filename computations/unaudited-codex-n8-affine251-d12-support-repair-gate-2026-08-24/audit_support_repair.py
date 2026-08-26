#!/usr/bin/env python3
"""Independent streaming replay of all 315,301 exposed equations."""
import argparse,hashlib,json,struct
from pathlib import Path
PRIME=1_073_741_827
PINS={"r730":"8bfd09b0b810933957cae3191c4725fc79e4734512da2a060ff398ad8566c7b2","r731":"8f2e0779d64ca14a46d019519280a33cb60633ffe1909cacc96885fbbbcefc65","vectors":"475a62b585429d3f0c96cd59c922124f5f46909a5bbe96266b989049afa2d523"}
def sha(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for b in iter(lambda:f.read(8<<20),b""):h.update(b)
 return h.hexdigest()
def ck(x,m):
 if not x:raise ValueError(m)
def mono(f):
 b=f.read(13);ck(len(b)==13 and b[0]<=12 and all(b[i]<=b[i+1] for i in range(1,b[0])),"bad mono");return b
def checkpoint(path):
 with open(path,"rb") as f:
  ck(f.read(12)==b"AFF12CEG1\0\0\0" and struct.unpack("<Q",f.read(8))[0]==PRIME,"checkpoint header")
  round,nc,ns=struct.unpack("<QQQ",f.read(24));cols=set()
  for _ in range(nc):
   key=f.read(2)+mono(f);ck(key not in cols,"duplicate column");cols.add(key)
  cand={}
  for _ in range(ns):
   row=mono(f);value=struct.unpack("<Q",f.read(8))[0];ck(row not in cand and 0<value<PRIME,"bad candidate");cand[row]=value
  ck(not f.read(1),"checkpoint trailing")
 return round,cols,cand
def candidate(path):
 lines=Path(path).read_text().splitlines();head=lines[0].split();ck(head[0]=="KRENN_AFF251_RESTRICTED_CANDIDATE_V1" and int(head[1])==len(lines)-1,"candidate header");out={};previous=None
 for line in lines[1:]:
  tag,h,v=line.split();row=bytes([12])+bytes.fromhex(h);value=int(v);ck(tag=="ROW" and len(row)==13 and row not in out and 0<value<PRIME and (previous is None or previous<row),"candidate row");out[row]=value;previous=row
 return out
def frontier(path):
 lines=Path(path).read_text().splitlines();head=lines[0].split();ck(head[0]=="KRENN_AFF251_RESTRICTED_FRONTIER_V1" and int(head[1])==len(lines)-1,"frontier header");previous=None
 for line in lines[1:]:
  tag,w,h=line.split();key=(int(w),bytes.fromhex(h));ck(tag=="COLUMN" and len(key[1])==8 and (previous is None or previous<key),"frontier order");previous=key
 return len(lines)-1
def main():
 p=argparse.ArgumentParser();
 for x in ["raw","round730","round731","vectors","candidate_new_only","candidate_new_union","candidate_reference","frontier_new_only","frontier_new_union","frontier_reference","output"]:p.add_argument("--"+x.replace('_','-'),dest=x,required=True)
 a=p.parse_args();ck(sha(a.round730)==PINS["r730"] and sha(a.round731)==PINS["r731"] and sha(a.vectors)==PINS["vectors"],"input pin")
 raw=json.load(open(a.raw));r730,c730,b730=checkpoint(a.round730);r731,c731,b731=checkpoint(a.round731);ck((r730,r731,len(c730),len(c731),len(c731-c730),len(b730),len(b731))==(730,731,314080,315301,1221,484,499),"state census")
 c1=candidate(a.candidate_new_only);c2=candidate(a.candidate_new_union);cref=candidate(a.candidate_reference);ck(c1==c2 and cref==b731,"candidate/reference mismatch");target=bytes([12])+bytes([251])*12;ck(c1.get(target)==cref.get(target)==1,"target normalization")
 repair_rows=set(c1);new_seen=set();old_seen=set();viol1=violr=0;seen=set();entries=0
 with open(a.vectors,"rb") as f:
  ck(f.read(12)==b"AFF12VEC1\0\0\0" and struct.unpack("<Q",f.read(8))[0]==PRIME,"vector header");provider_fp,vector_fp,count=struct.unpack("<QQQ",f.read(24));ck(count==315301,"vector count")
  for _ in range(count):
   col=f.read(2)+mono(f);ck(col in c731 and col not in seen,"vector column scope");seen.add(col);size=struct.unpack("<Q",f.read(8))[0];s1=sr=0;is_new=col not in c730
   for _ in range(size):
    row=mono(f);value=struct.unpack("<Q",f.read(8))[0];ck(0<value<PRIME,"vector coefficient");entries+=1
    if row in repair_rows:
     s1=(s1+value*c1[row])%PRIME
     if is_new:new_seen.add(row)
     else:old_seen.add(row)
    if row in cref:sr=(sr+value*cref[row])%PRIME
   viol1+=s1!=0;violr+=sr!=0
  ck(not f.read(1),"vector trailing")
 ck(seen==c731 and viol1==violr==0,"global annihilation replay")
 ck(all(row in b730 or row in new_seen for row in repair_rows),"repair escaped new-column union")
 ck(all(row in b730 or (row in new_seen and row not in old_seen) for row in repair_rows),"repair escaped new-only restriction")
 f1=frontier(a.frontier_new_only);f2=frontier(a.frontier_new_union);fr=frontier(a.frontier_reference);ck((f1,f2,fr)==(10466,10466,1268),"frontier census")
 outcomes=raw["outcomes"];ck(len(outcomes)==2 and all(x["consistent"] and x["full_violations"]==0 and x["support"]==1688 and x["frontier"]==10466 for x in outcomes),"raw result mismatch")
 speedups=[raw["baseline_solve_seconds"]/x["solve_seconds"] for x in outcomes];ratio=f1/fr;promote=all(x>=2 for x in speedups) and f1<=fr
 out={"schema":"KRENN_AFF251_D12_SUPPORT_REPAIR_AUDIT_V1","status":"PASS","equations_replayed":len(seen),"vector_entries_replayed":entries,"repair_violations":viol1,"reference_violations":violr,"candidate_sha256":sha(a.candidate_new_only),"candidate_variants_equal":sha(a.candidate_new_only)==sha(a.candidate_new_union),"reference_candidate_sha256":sha(a.candidate_reference),"frontier_sha256":sha(a.frontier_new_only),"frontier_variants_equal":sha(a.frontier_new_only)==sha(a.frontier_new_union),"reference_frontier_sha256":sha(a.frontier_reference),"speedups":speedups,"frontier_ratio":ratio,"promotion":promote,"verdict":"REJECT_FRONTIER_REGRESSION" if not promote else "PROMOTE","continued_beyond_round731":False,"peak_rss_kib":raw["peak_rss_kib"],"elapsed_seconds":raw["elapsed_seconds"]}
 Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out,sort_keys=True))
if __name__=="__main__":main()
