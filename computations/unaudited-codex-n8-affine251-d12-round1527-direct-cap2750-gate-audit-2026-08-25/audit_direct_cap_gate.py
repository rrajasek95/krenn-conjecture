#!/usr/bin/env python3
"""Independent fail-closed r1527 cap-2.5m→2.75m equivalence audit."""
import hashlib,json,os,struct
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1];P=json.loads((H/"AUDIT_PLAN.json").read_text());ROOT=R/P["producer_root"]
LABELS=["control_cap2500","candidate_cap2750"];CAPS={LABELS[0]:P["control_cap"],LABELS[1]:P["candidate_cap"]}
SOURCE="3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59";BINARY="79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048";WATCH="48fe528b15c31b8ed6446eb10628b0bcb598191efaac64dd59021881b80b1522";PRIME=1073741827;LIMIT=36*1024*1024
PRODUCER={"GATE_PLAN.json":"820e208470fcee362926ea001700bd74e4392560f7a7c426867ea712efb4d7e0","check_gate.py":"a50357c42cbc673dc653940f5d58bd6977ec08deca55b3a555513f3a595ef72e","results_round1527_direct_cap2750_gate.json":"8fde70b72e0a0145bb7096d8229d226d0a8e6a0c37124081f573e272e349d689","REPORT.md":"45a8ee6e3b330476db70ebb2b7fa375c4ac10ae8e037b38d98616c4f436ea918","MANIFEST.sha256":"1b6f6013a28edbf06cedb398ea81ba5ef3983b8e23d0dc859edb1de6bd939e88"}
def need(x,m):
 if not x:raise SystemExit("REJECT: "+m)
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(8<<20),b""):h.update(b)
 return h.hexdigest()
def load(p):return json.loads(p.read_text())
def arg(c,f):need(c.count(f)==1,"command "+f);return c[c.index(f)+1]
def header(p):
 with p.open("rb") as f:d=f.read(44)
 need(d[:12]==b"AFF12CEG1\0\0\0","checkpoint magic");prime,round_,cols,support=struct.unpack_from("<QQQQ",d,12);need(p.stat().st_size==44+15*cols+21*support,"checkpoint length");return {"prime":prime,"round":round_,"columns":cols,"support":support,"bytes":p.stat().st_size}
def norm(c,label):return [x.replace(f"/{label}/","/RUN/") for x in c]
need(sha(R/P["input_audit"])==P["input_audit_sha256"] and sha(R/P["input_manifest"])==P["input_manifest_sha256"],"input seal")
ia=load(R/P["input_audit"]);need(ia["status"]=="PASS_EXACT_FULLY_TELEMETERED_ROUND1526_CAP2500_CHAIN" and ia["final"]["round"]==1526 and ia["artifact_sha256"]["stage01_checkpoint"]==P["input_checkpoint_sha256"] and ia["artifact_sha256"]["stage01_vectors"]==P["input_vectors_sha256"],"input audit contents")
for n,h in PRODUCER.items():need(sha(ROOT/n)==h,"producer "+n)
for label in LABELS:
 for n in ("result.json","checkpoint.bin","vectors.bin","watchdog.json","stderr.log"):need((ROOT/label/n).is_file(),"missing "+label+"/"+n)
 need(not any((ROOT/label).glob("*.tmp")),"temporary "+label)
results={x:load(ROOT/x/"result.json") for x in LABELS};watches={x:load(ROOT/x/"watchdog.json") for x in LABELS}
record_fields=["round","columns","new_columns","dual_support","new_support_rows","selected_strategy","selected_pivot"]
semantic_fields=["schema","status","incomplete_reason","degree","prime","group_order","provider_equations","provider_terms_parsed","provider_distinct_terms","seed_support","column_orbits_exposed","dual_support","rounds_completed","global_annihilation","target_pairing","workers","pivot_mode","strategy","elimination_kernel","incremental_basis","portfolio_period","portfolio_parallel","support_cap","wall_limit_seconds","rss_limit_gib","cached_vectors_loaded","vectors_materialized_on_restore","vector_cache_bytes"]
records={};semantics={}
for label in LABELS:
 r,w=results[label],watches[label]
 need((r["status"],r["incomplete_reason"],r["rounds_completed"],len(r["rounds"]))==("INCOMPLETE_SEARCH_CAP","ROUND_CAP",1527,1),label+" result")
 need(r["cached_vectors_loaded"]==P["input_columns"] and r["vectors_materialized_on_restore"]==0 and r["column_cap"]==CAPS[label],label+" restore/cap")
 need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"],label+" watchdog")
 need(w["elapsed_seconds"]<150 and w["peak_rss_kib"]<LIMIT and all(x["rss_kib"]<LIMIT for x in w["samples"]),label+" resources")
 need((w["source_sha256"],w["binary_sha256"],w["watchdog_sha256"])==(SOURCE,BINARY,WATCH),label+" pins")
 need(w["result_sha256"]==sha(ROOT/label/"result.json"),label+" result pin")
 for f,v in (("--round-cap","1527"),("--column-cap",str(CAPS[label])),("--wall-seconds","120"),("--rss-gib","36"),("--workers","16"),("--pivot","rare"),("--strategy","cold"),("--elimination","hierarchical"),("--incremental","no"),("--prime",str(PRIME))):need(arg(w["command"],f)==v,label+" "+f)
 records[label]={k:r["rounds"][0][k] for k in record_fields};semantics[label]={k:r[k] for k in semantic_fields}
control,candidate=LABELS;need(records[control]==records[candidate],"round record differs");need(semantics[control]==semantics[candidate],"semantics differ")
left,right=norm(watches[control]["command"],control),norm(watches[candidate]["command"],candidate);need(len(left)==len(right),"command length")
diff=[(i,a,b) for i,(a,b) in enumerate(zip(left,right)) if a!=b];need(diff==[(left.index("2500000"),"2500000","2750000")],"not sole cap diff: "+repr(diff))
cph={x:sha(ROOT/x/"checkpoint.bin") for x in LABELS};vch={x:sha(ROOT/x/"vectors.bin") for x in LABELS};need(len(set(cph.values()))==len(set(vch.values()))==1,"output bytes differ")
heads={x:header(ROOT/x/"checkpoint.bin") for x in LABELS};need(heads[control]==heads[candidate],"headers differ");head=heads[control]
need((head["prime"],head["round"],head["columns"],head["support"])==(PRIME,1527,records[control]["columns"],records[control]["dual_support"]),"endpoint header")
need(all(not (ROOT/x/"dual.tsv").exists() for x in LABELS),"dual output present")
out={"schema":"KRENN_AFFINE251_D12_ROUND1527_DIRECT_CAP2750_AUDIT_V1","status":"PASS_EXACT_DIRECT_CAP2500_TO_CAP2750_EQUIVALENCE","input":{"round":1526,"columns":P["input_columns"],"support":P["input_support"],"audit_sha256":P["input_audit_sha256"],"manifest_sha256":P["input_manifest_sha256"]},"round_record":records[control],"checkpoint_header":head,"checkpoint_sha256":cph[control],"vectors_sha256":vch[control],"control_result_sha256":sha(ROOT/control/"result.json"),"candidate_result_sha256":sha(ROOT/candidate/"result.json"),"control_watchdog_sha256":sha(ROOT/control/"watchdog.json"),"candidate_watchdog_sha256":sha(ROOT/candidate/"watchdog.json"),"maximum_elapsed_seconds":max(watches[x]["elapsed_seconds"] for x in LABELS),"maximum_peak_rss_kib":max(watches[x]["peak_rss_kib"] for x in LABELS),"only_normalized_command_difference_is_cap":True,"exact_byte_equality":{"checkpoint":True,"vectors":True},"producer_pins":PRODUCER,"dual_outputs_absent":True,"accepted_candidate":"candidate_cap2750","continued_beyond_round1527":False,"production_mutated":False}
t=H/"results_round1527_direct_cap2750_audit.json.tmp";t.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");os.replace(t,H/"results_round1527_direct_cap2750_audit.json");print(json.dumps(out,sort_keys=True))
