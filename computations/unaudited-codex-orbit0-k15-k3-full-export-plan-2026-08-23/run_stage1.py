#!/usr/bin/env python3
import concurrent.futures, hashlib, json, os, pathlib, shutil, subprocess, sys, threading, time

ROOT=pathlib.Path(__file__).resolve().parents[2]
HERE=pathlib.Path(__file__).resolve().parent
OUT=HERE/'stage1_shards'; OUT.mkdir(exist_ok=True)
BIN=pathlib.Path('/tmp/export_k18_parent_profiles_stage1')
SOURCE=ROOT/'computations/unaudited-codex-orbit0-k18-three-stream-exporters-2026-08-23/export_k18_parent_profiles.rs'
N=242; WORKERS=2; KEY_CAP=1_000_000; GATE=600.0; STOP_LAUNCH=540.0
GEN=3_690_496; PIV=1_903_616; USES=4_861_952
HARD_BYTES=122_365_607_936; SPACE_MARGIN=20_000_000_000
begun=time.monotonic(); lock=threading.Lock(); completed=0

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        while True:
            b=f.read(8<<20)
            if not b:return h.hexdigest()
            h.update(b)

def valid_manifest(path,n):
    x=json.loads(path.read_text())
    assert x['status']=='PASS_EXACT_PREFIX_OR_COMPLETE_SHARD'
    assert x['mode']=='k15' and x['source_range']==[n,n+1]
    assert x['parent_cap']==0 and x['complete_source_range'] is True
    assert x['key_flush_cap']==KEY_CAP and x['scale_U']=='400591699200'
    assert x['generated_parents']==GEN and x['pivotable_parents']==PIV and x['outgoing_pivot_uses']==USES
    return x

def choose_prefix(n):
    for a in range(1000):
        p=OUT/f'record_{n:03d}_attempt_{a:03d}'
        m=pathlib.Path(str(p)+'.manifest.json')
        if m.exists():
            try:return p,m,valid_manifest(m,n),True
            except Exception:continue
        if not list(OUT.glob(p.name+'.part*.bin')):return p,m,None,False
    raise RuntimeError(f'no fresh attempt for record {n}')

def one(n):
    global completed
    if time.monotonic()-begun>=STOP_LAUNCH:raise RuntimeError('540s stop-launch gate')
    prefix,manifest,x,reused=choose_prefix(n)
    if not reused:
        cp=subprocess.run([str(BIN),'k15',str(n),str(n+1),'0',str(KEY_CAP),str(prefix)],cwd=ROOT,text=True,capture_output=True,timeout=40)
        if cp.returncode:raise RuntimeError(f'record {n} exporter failed: {cp.stderr[-2000:]}')
        x=valid_manifest(manifest,n)
    parts=[]
    files=sorted(OUT.glob(prefix.name+'.part*.bin'))
    assert len(files)==x['parts'] and [p.name for p in files]==[f'{prefix.name}.part{i:06d}.bin' for i in range(x['parts'])]
    for p in files:
        cp=subprocess.run([str(BIN),'verify','k15',str(p)],cwd=ROOT,text=True,capture_output=True,timeout=40)
        if cp.returncode:raise RuntimeError(f'{p.name} verifier failed: {cp.stderr[-2000:]}')
        parts.append({'name':p.name,'bytes':p.stat().st_size,'sha256':sha(p)})
    ans={'source_record':n,'attempt_prefix':prefix.name,'reused':reused,'manifest':manifest.name,'manifest_sha256':sha(manifest),'parts':parts,
         'generated':x['generated_parents'],'pivotable':x['pivotable_parents'],'outgoing_uses':x['outgoing_pivot_uses'],
         'emitted_records_local_unique':x['emitted_records_local_unique'],'signed_weight_sum_scaled':x['signed_weight_sum_scaled'],'exporter_seconds':x['elapsed_seconds']}
    with lock:
        completed+=1
        if completed%10==0 or completed==N:print(f'CHECKPOINT accepted={completed}/{N} elapsed={time.monotonic()-begun:.1f}s',flush=True)
    return ans

def main():
    assert BIN.is_file();free0=shutil.disk_usage(ROOT).free
    assert free0>=HARD_BYTES+SPACE_MARGIN,(free0,HARD_BYTES+SPACE_MARGIN)
    print(f'PRECHECK free_bytes={free0} required={HARD_BYTES+SPACE_MARGIN} workers={WORKERS} gate={GATE}',flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex: rows=list(ex.map(one,range(N)))
    elapsed=time.monotonic()-begun;assert elapsed<GATE
    rows.sort(key=lambda x:x['source_record']);assert [x['source_record'] for x in rows]==list(range(N))
    assert sum(x['generated'] for x in rows)==893_100_032
    assert sum(x['pivotable'] for x in rows)==460_675_072
    assert sum(x['outgoing_uses'] for x in rows)==1_176_592_384
    free1=shutil.disk_usage(ROOT).free
    result={'status':'PASS_K15_K3_STAGE1_EXACT_SORTED_RUNS','scope':'K15/K3 records [0,242) only; no stage2/merge/charge/K16',
      'workers':WORKERS,'key_cap':KEY_CAP,'hard_gate_seconds':GATE,'elapsed_seconds':elapsed,'free_bytes_before':free0,'free_bytes_after':free1,
      'source_range':[0,N],'accepted_shards':len(rows),'parts':sum(len(x['parts']) for x in rows),'artifact_bytes':sum(p['bytes'] for x in rows for p in x['parts']),
      'exact_generated':893_100_032,'exact_pivotable':460_675_072,'exact_outgoing_uses':1_176_592_384,
      'emitted_records_local_unique':sum(x['emitted_records_local_unique'] for x in rows),'signed_weight_sum_scaled':str(sum(int(x['signed_weight_sum_scaled']) for x in rows)),
      'exporter_source_sha256':sha(SOURCE),'records':rows}
    tmp=HERE/'stage1_catalog.json.tmp';dst=HERE/'stage1_catalog.json';tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');os.replace(tmp,dst)
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2,sort_keys=True),flush=True)
if __name__=='__main__':main()
