#!/usr/bin/env python3
"""Independent bounded referee of the terminal K20 [2,2,2] charge packet."""
from fractions import Fraction
from hashlib import sha256
import csv, importlib.util, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PACK=ROOT/'computations/unaudited-codex-orbit0-k20-222-consumer-design-2026-08-23'
RESULT=PACK/'results_k20_222_charge.json'
SAMPLES=PACK/'results_k20_222_charge.json.samples.tsv'
SOURCE=PACK/'consume_k18_222_to_k20.rs'
DESIGN=ROOT/'computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23/filtered_k24_reducer.py'
CYCLE=ROOT/'computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin'
PARTIAL=PACK/'results_partial_k20_charge_and_34_path_gap.json'
DAG=ROOT/'computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json'
P24=ROOT/'computations/unaudited-codex-orbit0-hidden-k16-full-charge-2026-08-23/results_full_hidden_k3_k4_charge.json'
BINARY=PACK/'consume_k18_222_to_k20'
OUT=HERE/'results_k20_222_referee.json'
U=400_591_699_200

def req(x,d):
    if not x: raise AssertionError(d)

def load(path):
    s=importlib.util.spec_from_file_location('k20_ref_design',path);m=importlib.util.module_from_spec(s)
    req(s.loader is not None,path);s.loader.exec_module(m);return m
D=load(DESIGN)

def canonical(row):
    s=D.CTX.signature(row);best=min(D.CTX.move_signature(s,g) for g in D.H)
    return min(D.F.move_row(row,g) for g in D.H if D.CTX.move_signature(s,g)==best)

def remove4(row,anchor):
    x=list(row)
    for c in anchor:x.remove(c)
    return x

def cycle_env():
    b=CYCLE.read_bytes();req(b[:8]==b'K17CYC1\0',b[:8]);p=8
    cells=[]
    for _ in range(252):cells.append(tuple(b[p:p+4]));p+=4
    n=int.from_bytes(b[p:p+4],'little');p+=4;dual={}
    for _ in range(n):
        k=bytes(b[p:p+13]);p+=13;v=int.from_bytes(b[p:p+8],'little',signed=True);p+=8;dual[k]=v
    req(p==len(b),(p,len(b)));return cells,dual
CELLS,DUAL=cycle_env()

def ckey(row):
    adj=[[] for _ in range(24)]
    for cell in row:
        u,v,a,b=CELLS[cell];x=3*u+a;y=3*v+b;adj[x].append(y);adj[y].append(x)
    req(all(len(x)==2 for x in adj),'not balanced')
    seen=set();parts=[]
    for st in range(24):
        if st in seen:continue
        stack=[st];seen.add(st);n=0
        while stack:
            x=stack.pop();n+=1
            for y in adj[x]:
                if y not in seen:seen.add(y);stack.append(y)
        parts.append(n)
    parts.sort();return bytes([len(parts),*parts,*([0]*(12-len(parts)))])

def q(row):return DUAL.get(ckey(row),0)

def main():
    r=json.loads(RESULT.read_text());req(r['status']=='PASS_K20_222_IMMEDIATE_CHARGE',r)
    hist=r['m2_m3_provenance'];tot={k:0 for k in('parents','signed_parent_mass','pivot_uses','children','irreducible_children','full_charge_scaled','irreducible_charge_scaled')}
    for key,a in hist.items():
        m2,m3=map(int,key.split('_'));req(U%(m2*m3)==0,key)
        a={k:int(v) for k,v in a.items()};req(a['pivot_uses']==m3*a['parents'],(key,a));req(a['children']==12*a['pivot_uses'],(key,a));req(a['irreducible_children']<=a['children'],key)
        for k in tot:tot[k]+=a[k]
    expected={'parents':r['input_pivotable_parent_orbits'],'signed_parent_mass':int(r['input_weight_sum_scaled']),'pivot_uses':r['selected_p3_uses'],'children':r['representative_tail_terms'],'irreducible_children':r['irreducible_tail_terms'],'full_charge_scaled':int(r['full_charge_scaled']),'irreducible_charge_scaled':int(r['irreducible_charge_scaled'])}
    req(tot==expected,(tot,expected))

    n=0
    with SAMPLES.open() as f:
        for x in csv.DictReader(f,delimiter='\t'):
            n+=1;row=bytes.fromhex(x['row']);parent=bytes.fromhex(x['witness_pair']);w=int(x['weight_before_p3']);m2=int(x['m2']);m3=int(x['m3']);p2=int(x['p2']);t2=int(x['t2'])
            req(int(x['orbit'])*int(x['stabilizer'])==384,x);req(int(x['pair_uses'])>0,x)
            ps2=D.CTX.pivots(D.CTX.signature(parent));req(len(ps2)==m2 and p2 in ps2,x)
            raw=bytes(sorted(remove4(parent,D.CTX.anchors[p2])+list(D.CTX.tails[p2][2][t2])));req(canonical(raw)==row,(n,'p2 landing'))
            ps3=D.CTX.pivots(D.CTX.signature(row));req(len(ps3)==m3 and int(x['pivot_uses'])==m3,x);req(U%(m2*m3)==0 and w%m3==0,x)
            w3=-w//m3;full=irr=nt=ni=0
            for p3 in ps3:
                for tail in D.CTX.tails[p3][2]:
                    child=bytes(sorted(remove4(row,D.CTX.anchors[p3])+list(tail)));z=q(child);full+=w3*z;nt+=1
                    if not D.CTX.pivots(D.CTX.signature(child)):irr+=w3*z;ni+=1
            req((nt,ni,full,irr)==tuple(map(int,(x['tails'],x['irreducible_tails'],x['full_charge_scaled'],x['irreducible_charge_scaled']))),(n,nt,ni,full,irr,x))
    req(n==257,n)
    src=SOURCE.read_text();req('-x.weight_before_p3 / m3' in src and 'assert_eq!(x.weight_before_p3 % m3, 0);' in src,'sign/division source guard');req('available(signature(&child.0, e), e).is_empty()' in src,'pivot filter guard')
    irr=Fraction(int(r['irreducible_charge_scaled']),U);req(irr==Fraction(2_839_639_920_238_347_136,521_603_775),irr)
    part=json.loads(PARTIAL.read_text());dag=json.loads(DAG.read_text());p24=json.loads(P24.read_text())
    required=dag['required_reachable_lineage_ids_by_degree']['20'];req(len(required)==len(set(required))==36,len(required))
    covered=['D14:222|R:2-2-2','D14:222|R:2-4'];remaining=[x for x in required if x not in covered];req(len(remaining)==34,remaining)
    req(part['complete_K20_claim'] is False and part['dag']['required_paths']==36 and part['dag']['covered_paths']==covered and part['dag']['remaining_paths']==remaining,part['dag'])
    p24f=int(p24['K20_path_24']['full_charge_scaled']);p24i=int(p24['K20_path_24']['irreducible_charge_scaled'])
    req(part['certified_two_path_partial']['full']['scaled_numerator']==str(expected['full_charge_scaled']+p24f),'partial full')
    req(part['certified_two_path_partial']['irreducible']['scaled_numerator']==str(expected['irreducible_charge_scaled']+p24i),'partial irr')
    out={'status':'PASS_INDEPENDENT_K20_222_IMMEDIATE_CHARGE_REFEREE','scope':'Immediate occurrencewise cycle charge for D14:222|R:2-2-2 only; no canonical K20 checkpoint or later tails.','parents':expected['parents'],'selected_p3_uses':expected['pivot_uses'],'tails':expected['children'],'irreducible_tails':expected['irreducible_children'],'full_charge_scaled':str(expected['full_charge_scaled']),'irreducible_charge_scaled':str(expected['irreducible_charge_scaled']),'irreducible_charge_unscaled':f'{irr.numerator}/{irr.denominator}','m2_m3_types':len(hist),'sample_literal_replays':n,'aggregate_identities':True,'sign_and_division_source_guards':True,'K20_DAG':{'required_paths':36,'certified_paths':2,'missing_paths':34,'complete_K20_claim':False},'certified_two_path_partial_scaled':{'full':str(expected['full_charge_scaled']+p24f),'irreducible':str(expected['irreducible_charge_scaled']+p24i)},'pinned':{str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in (SOURCE,BINARY,RESULT,SAMPLES,PARTIAL,DAG,P24,DESIGN,CYCLE)}}
    logical=json.dumps(out,sort_keys=True,separators=(',',':')).encode();out['logical_sha256']=sha256(logical).hexdigest();OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
