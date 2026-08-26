#!/usr/bin/env python3
"""Memoized exact D/V factor-tree engine. HELD: manager clearance required externally."""
from __future__ import annotations
import argparse,gzip,hashlib,json,math,os,re
from collections import deque
from pathlib import Path

SCHEMA='KRENN_X5_REP5_MEMOIZED_FACTOR_TREE_V1';UNIT=((((),1),),)
def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def sha_file(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic_bytes(path,data):
 tmp=path.with_suffix(path.suffix+'.tmp');tmp.parent.mkdir(parents=True,exist_ok=True)
 with tmp.open('wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 os.replace(tmp,path)
def atomic_json(path,value):atomic_bytes(path,(json.dumps(value,indent=2,sort_keys=True)+'\n').encode())
def gz_json(value):
 import io
 out=io.BytesIO()
 with gzip.GzipFile(fileobj=out,mode='wb',mtime=0) as g:g.write((json.dumps(value,separators=(',',':'),sort_keys=True)+'\n').encode())
 return out.getvalue()
def parse_source(path):
 text=path.read_text();names=text.split('ring r=0,(',1)[1].split('),dp;',1)[0].split(',');exprs=text.split('ideal I=',1)[1].split(';\nprint',1)[0].split(',\n');index={n:i for i,n in enumerate(names)};values=[]
 for expression in exprs:
  polynomial={}
  for raw in re.findall(r'[+-]?[^+-]+',expression):
   sign=-1 if raw.startswith('-') else 1;parts=raw.lstrip('+-').split('*');coefficient=sign
   if parts[0].isdigit():coefficient*=int(parts.pop(0))
   monomial=tuple(sorted(index[x] for x in parts if x));polynomial[monomial]=polynomial.get(monomial,0)+coefficient
  polynomial={m:c for m,c in polynomial.items() if c};assert polynomial;values.append(polynomial)
 return names,values
def primitive_key(polynomial):
 if not polynomial:return None
 g=0
 for c in polynomial.values():g=math.gcd(g,abs(c))
 q={m:c//g for m,c in polynomial.items() if c};lead=min(q,key=lambda m:(len(m),m))
 if q[lead]<0:q={m:-c for m,c in q.items()}
 return tuple(sorted(q.items()))
def canonical(values):
 keys=set()
 for polynomial in values:
  key=primitive_key(polynomial)
  if key is None:continue
  if len(key)==1 and key[0][0]==():return UNIT
  keys.add(key)
 return tuple(sorted(keys))
def reduce_state(base,zero,unit,variables):
 assert zero&unit==0 and zero>>(variables)==0 and unit>>(variables)==0
 values=[]
 for original in base:
  polynomial={m:c for m,c in original.items() if not any((zero>>x)&1 for x in m)}
  if not polynomial:continue
  for x in range(variables):
   if not (unit>>x)&1:continue
   power=min(m.count(x) for m in polynomial)
   if power:
    reduced={}
    for m,c in polynomial.items():
     w=list(m)
     for _ in range(power):w.remove(x)
     reduced[tuple(w)]=reduced.get(tuple(w),0)+c
    polynomial=reduced
  values.append(polynomial)
 return canonical(values)
def digest_generators(gens):return sha_bytes(json.dumps(gens,separators=(',',':')).encode())
def state_key(source_sha,zero,unit,gens):return sha_bytes(f'{SCHEMA}|{source_sha}|{zero:016x}|{unit:016x}|{digest_generators(gens)}'.encode())
def candidates(gens,names,zero,unit,base,source_sha):
 decided=zero|unit;counts={}
 for polynomial in gens:
  intersection=None
  for monomial,coefficient in polynomial:
   here=set(monomial);intersection=here if intersection is None else intersection&here
  for x in intersection or ():
   if not (decided>>x)&1:counts[x]=counts.get(x,0)+1
 values=[]
 for x,count in counts.items():
  child=reduce_state(base,zero|(1<<x),unit,len(names));values.append((-count,sum(len(p) for p in child),len(child),names[x],x))
 return sorted(values)
def derive_roots(base,names,source_sha):
 zero=unit=0;roots=[];steps=[]
 for step in range(1,100):
  parent=reduce_state(base,zero,unit,len(names))
  if parent==UNIT:break
  choices=candidates(parent,names,zero,unit,base,source_sha);assert choices
  neg_count,terms,generators,name,x=choices[0];D=reduce_state(base,zero,unit|(1<<x),len(names));V=reduce_state(base,zero|(1<<x),unit,len(names))
  record={'step':step,'pivot':name,'count':-neg_count,'zero_before':f'{zero:016x}','unit_before':f'{unit:016x}','D_unit':D==UNIT,'V_unit':V==UNIT}
  if V==UNIT:unit|=1<<x;record['continuation']='D'
  else:
   if D!=UNIT:roots.append((zero,unit|(1<<x)))
   zero|=1<<x;record['continuation']='V'
  steps.append(record)
 assert len(steps)==22 and reduce_state(base,zero,unit,len(names))==UNIT and len(roots)==18
 return sorted(set(roots)),steps
def load_checkpoint(directory,config_hash):
 current=directory/'CURRENT.json'
 if not current.exists():return {},deque(),[],0,0
 pointer=json.loads(current.read_text());assert pointer['schema']==SCHEMA and pointer['config_sha256']==config_hash
 records={}
 for shard in pointer['shards']:
  path=directory/shard['path'];data=path.read_bytes();assert len(data)==shard['bytes'] and sha_bytes(data)==shard['sha256'];payload=json.loads(gzip.decompress(data));assert payload['schema']==SCHEMA
  for record in payload['records']:
   key=record['key'];assert key not in records;records[key]=record
 frontier_record=pointer['frontier'];data=(directory/frontier_record['path']).read_bytes();assert len(data)==frontier_record['bytes'] and sha_bytes(data)==frontier_record['sha256'];frontier_payload=json.loads(gzip.decompress(data));assert frontier_payload['schema']==SCHEMA
 return records,deque(frontier_payload['frontier']),pointer['shards'],pointer['generation'],pointer['expanded_total']
def commit(directory,config_hash,records,new_keys,frontier,shards,generation,expanded_total):
 generation+=1
 shard_payload={'schema':SCHEMA,'generation':generation,'records':[records[k] for k in new_keys]};shard_data=gz_json(shard_payload);shard_path=directory/f'shards/shard_{generation:08d}.json.gz';atomic_bytes(shard_path,shard_data);shards=shards+[{'path':str(shard_path.relative_to(directory)),'bytes':len(shard_data),'sha256':sha_bytes(shard_data)}]
 frontier_payload={'schema':SCHEMA,'generation':generation,'frontier':list(frontier)};frontier_data=gz_json(frontier_payload);frontier_path=directory/f'frontiers/frontier_{generation:08d}.json.gz';atomic_bytes(frontier_path,frontier_data)
 pointer={'schema':SCHEMA,'config_sha256':config_hash,'generation':generation,'expanded_total':expanded_total,'shards':shards,'frontier':{'path':str(frontier_path.relative_to(directory)),'bytes':len(frontier_data),'sha256':sha_bytes(frontier_data)}};atomic_json(directory/'CURRENT.json',pointer);return shards,generation
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True);parser.add_argument('--source-sha256',required=True);parser.add_argument('--checkpoint-dir',type=Path,required=True);parser.add_argument('--max-new-nodes',type=int,required=True);parser.add_argument('--global-node-cap',type=int,required=True);parser.add_argument('--checkpoint-every',type=int,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 if sha_file(args.source)!=args.source_sha256:raise SystemExit('source hash mismatch')
 if not 1<=args.max_new_nodes<=25000 or args.global_node_cap!=2000000 or not 1<=args.checkpoint_every<=500:raise SystemExit('sealed node/checkpoint caps refused')
 if args.output.exists():raise SystemExit('refuse existing result')
 names,base=parse_source(args.source);assert len(names)==64 and len(base)==3321;roots,path=derive_roots(base,names,args.source_sha256)
 config={'schema':SCHEMA,'source_sha256':args.source_sha256,'variables':names,'roots':[[z,u] for z,u in roots],'global_node_cap':args.global_node_cap,'branch_rule':'max-factor-count,min-V-terms,min-V-generators,name'};config_hash=sha_bytes(json.dumps(config,separators=(',',':'),sort_keys=True).encode());args.checkpoint_dir.mkdir(parents=True,exist_ok=True)
 records,frontier,shards,generation,expanded_total=load_checkpoint(args.checkpoint_dir,config_hash);pending_new=[]
 if not records and not frontier:
  for z,u in roots:
   gens=reduce_state(base,z,u,len(names));key=state_key(args.source_sha256,z,u,gens);records[key]={'key':key,'zero':z,'unit':u,'generator_sha256':digest_generators(gens),'assigned':(z|u).bit_count(),'status':'pending'};frontier.append(key);pending_new.append(key)
 lane_expanded=0
 while frontier and lane_expanded<args.max_new_nodes and len(records)<args.global_node_cap:
  key=frontier.popleft();record=records[key]
  if record['status']!='pending':continue
  z,u=record['zero'],record['unit'];gens=reduce_state(base,z,u,len(names));assert state_key(args.source_sha256,z,u,gens)==key and digest_generators(gens)==record['generator_sha256']
  if gens==UNIT:record['status']='unit'
  else:
   choices=candidates(gens,names,z,u,base,args.source_sha256)
   if not choices:record['status']='factor_exhausted_nonunit'
   else:
    neg_count,terms,generator_count,name,x=choices[0];children=[]
    for cz,cu in ((z,u|(1<<x)),(z|(1<<x),u)):
     child_gens=reduce_state(base,cz,cu,len(names));child_key=state_key(args.source_sha256,cz,cu,child_gens);children.append(child_key)
     if child_key not in records:records[child_key]={'key':child_key,'zero':cz,'unit':cu,'generator_sha256':digest_generators(child_gens),'assigned':(cz|cu).bit_count(),'status':'pending'};frontier.append(child_key);pending_new.append(child_key)
    record.update({'status':'expanded','pivot':name,'factor_count':-neg_count,'children':children})
  lane_expanded+=1;expanded_total+=1
  if lane_expanded%args.checkpoint_every==0:
   shards,generation=commit(args.checkpoint_dir,config_hash,records,pending_new,frontier,shards,generation,expanded_total);pending_new=[]
 if pending_new or lane_expanded%args.checkpoint_every:shards,generation=commit(args.checkpoint_dir,config_hash,records,pending_new,frontier,shards,generation,expanded_total)
 progress={'schema':SCHEMA,'status':'PARTIAL_FRONTIER_SEALED' if frontier else 'TERMINAL_DAG','config_sha256':config_hash,'generation':generation,'records':len(records),'frontier':len(frontier),'lane_expanded':lane_expanded,'expanded_total':expanded_total,'unit_records':sum(r['status']=='unit' for r in records.values()),'factor_exhausted_nonunit_records':sum(r['status']=='factor_exhausted_nonunit' for r in records.values())};atomic_json(args.checkpoint_dir/'progress.json',progress)
 if frontier:return 0
 truth={}
 for record in sorted(records.values(),key=lambda r:r['assigned'],reverse=True):
  if record['status']=='unit':truth[record['key']]=True
  elif record['status']=='factor_exhausted_nonunit':truth[record['key']]=False
  elif record['status']=='expanded':truth[record['key']]=all(truth[c] for c in record['children'])
  else:raise AssertionError(record)
 root_keys=[state_key(args.source_sha256,z,u,reduce_state(base,z,u,len(names))) for z,u in roots];accepted=all(truth[k] for k in root_keys);result={'schema':SCHEMA,'status':'PASS_EXACT_ALL_18_ROOTS_STRUCTURAL_UNIT' if accepted else 'REJECT_FACTOR_EXHAUSTED_NONUNIT_LEAF','accepted':accepted,'source_sha256':args.source_sha256,'config_sha256':config_hash,'root_keys':root_keys,'roots':18,'records':len(records),'expanded_total':expanded_total,'unit_records':sum(r['status']=='unit' for r in records.values()),'factor_exhausted_nonunit_records':sum(r['status']=='factor_exhausted_nonunit' for r in records.values()),'all_root_truth':[truth[k] for k in root_keys],'strict_path_steps':len(path),'checkpoint_generation':generation};atomic_json(args.output,result);return 0
if __name__=='__main__':raise SystemExit(main())
