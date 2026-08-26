#!/usr/bin/env python3
"""Freeze the strict 281-input catalog and exact grouped-six DAG interface."""
from pathlib import Path
import hashlib, json, os

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
LEDGER=ROOT/"computations/unaudited-codex-orbit0-k20-36-path-availability-ledger-2026-08-23/results_k20_36_path_ledger.json"
DAG=ROOT/"computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
EXPORT=HERE/"results_k16_cached_export.json"
CAT=HERE/"k16_merge_inputs.tsv"
OUT=HERE/"results_k16_merge_charge_design.json"

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def logical(x):
 y=dict(x);y.pop("logical_sha256",None)
 return hashlib.sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def main():
 ledger=json.loads(LEDGER.read_text());dag=json.loads(DAG.read_text());exp=json.loads(EXPORT.read_text())
 ids=sorted(x["lineage_id"] for x in ledger["lineages"] if x.get("group")=="K16_R22" and x["availability"]=="SCALAR_ONLY_IMMEDIATE_PARENT_RECONSTRUCTION_REQUIRED")
 assert ids==["D16:224|R:2-2","D16:233|R:2-2","D16:242|R:2-2","D16:323|R:2-2","D16:332|R:2-2","D16:422|R:2-2"]
 req=dag["required_reachable_lineage_ids_by_degree"]["20"]
 assert len(ids)==len(set(ids))==6 and set(ids)<=set(req)
 manifests=sorted(HERE.glob("shards/shard_*.accepted.json"))
 assert len(manifests)==64
 rows=[]
 for i,p in enumerate(manifests):
  x=json.loads(p.read_text());assert x["shard"]==i and x["status"]=="PASS_ACCEPTED_K16_CACHED_SHARD"
  for part in x["part_files"]:
   q=ROOT/part["path"]
   assert q.stat().st_size==part["bytes"]
   rows.append((part["path"],part["bytes"],part["sha256"],i))
 assert len(rows)==281 and len({x[0] for x in rows})==281
 assert sum(x[1] for x in rows)==exp["part_bytes"]==6647540680
 text="path\tbytes\tsha256\tshard\n"+"".join(f"{p}\t{b}\t{h}\t{s}\n" for p,b,h,s in rows)
 tmp=Path(str(CAT)+".tmp");tmp.write_text(text);tmp.replace(CAT)
 out={"status":"PASS_K16_281_WAY_MERGE_CHARGE_DESIGN_INTERFACE","scope":"Design/catalog only; no merge or charge production launched and all source parts retained.","dag_lineage_ids":ids,"coverage_count":6,"input":{"accepted_shards":64,"parts":281,"part_bytes":6647540680,"local_records":63918401,"outgoing_pivot_uses":2049974172,"signed_weight_scaled":"3218269567887566438400","schema":"K18PRF2 version2 shifts(3,2), header96, record104"},"catalog_sha256":sha(CAT),"accepted_manifest_set_sha256":hashlib.sha256("".join(sha(p) for p in manifests).encode()).hexdigest(),"pinned":{"availability_ledger_sha256":sha(LEDGER),"dag_sha256":sha(DAG),"export_result_sha256":sha(EXPORT)},"production_launch_guard":"BLOCKED until independent export referee passes; merge and charge binaries require explicit --merge/--charge."}
 out["logical_sha256"]=logical(out)
 tmp=Path(str(OUT)+".tmp");tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");tmp.replace(OUT)
 print(json.dumps({"status":out["status"],"ids":ids,"parts":len(rows),"catalog_sha256":out["catalog_sha256"],"logical_sha256":out["logical_sha256"]},indent=2))

if __name__=="__main__":main()
