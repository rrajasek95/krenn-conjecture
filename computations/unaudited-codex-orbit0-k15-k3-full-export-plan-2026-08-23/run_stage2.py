#!/usr/bin/env python3
import concurrent.futures, hashlib, json, os, pathlib, shutil, time
import run_stage1 as core

START=242; END=485; N=END-START
core.OUT=core.HERE/'stage2_shards';core.OUT.mkdir(exist_ok=True)
core.N=N;core.HARD_BYTES=122_871_250_944;core.begun=time.monotonic();core.completed=0

def main():
    assert core.BIN.is_file();free0=shutil.disk_usage(core.ROOT).free
    assert free0>=143_000_000_000,(free0,143_000_000_000)
    print(f'PRECHECK free_bytes={free0} required=143000000000 workers={core.WORKERS} gate={core.GATE}',flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=core.WORKERS) as ex:rows=list(ex.map(core.one,range(START,END)))
    elapsed=time.monotonic()-core.begun;assert elapsed<core.GATE
    rows.sort(key=lambda x:x['source_record']);assert [x['source_record'] for x in rows]==list(range(START,END))
    assert sum(x['generated'] for x in rows)==896_790_528
    assert sum(x['pivotable'] for x in rows)==462_578_688
    assert sum(x['outgoing_uses'] for x in rows)==1_181_454_336
    free1=shutil.disk_usage(core.ROOT).free
    result={'status':'PASS_K15_K3_STAGE2_EXACT_SORTED_RUNS','scope':'K15/K3 records [242,485) only; no merge/charge/K16',
      'stage1_referee_logical_sha256':'256bc673','workers':core.WORKERS,'key_cap':core.KEY_CAP,'hard_gate_seconds':core.GATE,'elapsed_seconds':elapsed,
      'free_bytes_before':free0,'free_bytes_after':free1,'source_range':[START,END],'accepted_shards':len(rows),'parts':sum(len(x['parts']) for x in rows),
      'artifact_bytes':sum(p['bytes'] for x in rows for p in x['parts']),'exact_generated':896_790_528,'exact_pivotable':462_578_688,
      'exact_outgoing_uses':1_181_454_336,'emitted_records_local_unique':sum(x['emitted_records_local_unique'] for x in rows),
      'signed_weight_sum_scaled':str(sum(int(x['signed_weight_sum_scaled']) for x in rows)),'exporter_source_sha256':core.sha(core.SOURCE),'records':rows}
    tmp=core.HERE/'stage2_catalog.json.tmp';dst=core.HERE/'stage2_catalog.json';tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');os.replace(tmp,dst)
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2,sort_keys=True),flush=True)
if __name__=='__main__':main()
