#!/usr/bin/env python3
"""Hostile tests for the frozen hidden-collected fast validator/referee."""
from __future__ import annotations
import csv,importlib.util,json,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
V=HERE/"validate_hidden_collected_fast.py"; L=HERE/"referee_hidden_collected_fast"
R=HERE/"control_prefix1000000.json"; S=Path(str(R)+".samples.tsv")
def run(a):return subprocess.run(a,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
def main():
 cases=[]
 with tempfile.TemporaryDirectory(prefix="k24-hcol-fast-") as td:
  t=Path(td)
  q=run([sys.executable,"-I","-S",str(V),"--mode","gate","--result",str(R),"--samples",str(S),"--output",str(t/"baseline.json")]);cases.append({"case":"baseline_strict_with_hash_preflight","expected":"PASS","observed":q.returncode});
  if q.returncode:raise RuntimeError(q.stderr)
  spec=importlib.util.spec_from_file_location("hcv",V);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);mod.PINS={}
  base=json.loads(R.read_text())
  muts={
   "extra_field":lambda x:x.__setitem__("hostile",1),"wrong_U":lambda x:x.__setitem__("scale_U","1"),"wrong_id":lambda x:x.__setitem__("strict_id","bad"),
   "wrong_interval":lambda x:x.__setitem__("input_interval",[0,1]),"wrong_input":lambda x:x.__setitem__("input","bad"),"wrong_terminal":lambda x:x.__setitem__("terminal_K4_tails",0),
   "wrong_charge":lambda x:x.__setitem__("irreducible_charge_scaled_U","0"),"wrong_hist":lambda x:x["m2_m3_m4_hist"].__setitem__("3_1_1",0),"wrong_cache":lambda x:x["cache"].__setitem__("K18_hits",0),
  }
  for label,mut in muts.items():
   x=json.loads(json.dumps(base));mut(x);p=t/(label+".json");p.write_text(json.dumps(x)+"\n")
   try:mod.validate(p,S,"gate")
   except Exception:observed=1
   else:observed=0
   cases.append({"case":label,"expected":"REJECT","observed":observed})
   if not observed:raise RuntimeError(label)
  with S.open(newline="") as f: rows=list(csv.reader(f,delimiter="\t"))
  smuts={"wrong_index":lambda z:z[1].__setitem__(0,"1"),"wrong_source_row":lambda z:z[1].__setitem__(1,"00"+z[1][1][2:]),"wrong_witness":lambda z:z[1].__setitem__(2,"00"+z[1][2][2:]),"wrong_weight":lambda z:z[1].__setitem__(3,str(int(z[1][3])+1)),"wrong_m3":lambda z:z[1].__setitem__(10,str(int(z[1][10])+1)),"wrong_literal_charge":lambda z:z[1].__setitem__(15,str(int(z[1][15])+1))}
  for label,mut in smuts.items():
   z=[a[:] for a in rows];mut(z);p=t/(label+".tsv");
   with p.open("w",newline="") as f:csv.writer(f,delimiter="\t",lineterminator="\n").writerows(z)
   q=run([str(L),"--samples",str(p),"--sample-span","1000000","--output",str(t/(label+".literal.json"))]);cases.append({"case":"literal_"+label,"expected":"REJECT","observed":q.returncode});
   if not q.returncode:raise RuntimeError(label)
 out={"status":"PASS_HIDDEN_COLLECTED_FAST_LAUNCH_HOSTILES","cases":cases,"strict_hash_preflight":True,"mutation_checks_in_process_after_preflight":True,"full_production_launched":False};(HERE/"results_hostile_selftest.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps({"status":out["status"],"cases":len(cases)}))
if __name__=="__main__":main()
