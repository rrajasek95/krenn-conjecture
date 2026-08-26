#!/usr/bin/env python3
"""Extend the corrected exact 77-cycle charge ledger through complete K22."""
from fractions import Fraction
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
K21=ROOT/'computations/unaudited-codex-orbit0-filtered-charge-ledger-through-k21-2026-08-24/results_charge_ledger_through_k21.json'
K22=ROOT/'computations/unaudited-codex-orbit0-k22-charge-assembly-2026-08-24/results_k22_complete_76_exact.json'
MAN=ROOT/'computations/unaudited-codex-orbit0-k22-charge-assembly-2026-08-24/k22_manifest_complete_76.json'
PINS={K21:'10d99f336bdbb0c98036cd9467a87c505a8b6a5ca5dff4623d6d399c95efb500',K22:'7e955126cf391d2b6cfcbbb694004a2a5a8915981332cd9cc80e26460d7624f1',MAN:'731f6a111ce02ce2bfb40ccf465f0c7c631f1ed68106647ab5ca33288c82fdfe'}
def req(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def logical(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def rat(x):return Fraction(int(x['numerator']),int(x['denominator']))
def render(x):return {'numerator':x.numerator,'denominator':x.denominator,'text':str(x)}
def build(k21,k22,manifest):
 req(k21['status']=='PASS_CORRECTED_COMPLETE_CHARGE_LEDGER_THROUGH_K21','K21 ledger status')
 req((k22['status'],k22['complete_K22_claim'],k22['required_paths'],k22['covered_paths'],k22['scalar_groups'])==('PASS_COMPLETE_K22_76_ID_EXACT_Q',True,76,76,22),'K22 completion')
 req(not k22['missing_paths'] and not k22['duplicate_paths'] and not k22['extra_paths'],'K22 coverage lists')
 req(k22['manifest_logical_sha256']==logical(manifest),'K22 manifest logical digest')
 q22=rat(k22['irreducible']);req(q22==rat(k22['full'])==Fraction(4753487002993355488,173867925),'K22 charge')
 q21=rat(k21['cumulative_K14_through_K21']);req(q21==Fraction(-2580518875863179008,173867925),'K21 cumulative')
 cumulative=q21+q22;req(cumulative==Fraction(144864541808678432,11591195),'K22 cumulative')
 charges=dict(k21['charges']);charges['K22']=render(q22);coverage=dict(k21['coverage']);coverage['K22']=76
 return {'status':'PASS_CORRECTED_COMPLETE_CHARGE_LEDGER_THROUGH_K22','charges':charges,'coverage':coverage,'cumulative_K14_through_K22':render(cumulative),'unallocated_conservation_residual_after_K22':render(-cumulative),'future_degree_allocation':None,'sources':{'through_K21':{'path':str(K21.relative_to(ROOT)),'sha256':PINS[K21]},'K22_manifest':{'path':str(MAN.relative_to(ROOT)),'sha256':PINS[MAN],'logical_sha256':logical(manifest)},'K22_result':{'path':str(K22.relative_to(ROOT)),'sha256':PINS[K22]}},'scope':'Exact 77-cycle conservation ledger through complete K22 only; the unallocated residual is aggregate arithmetic and assigns no value or membership claim to K23 or K24.'}
def load():
 for p,h in PINS.items():req(sha(p)==h,'pin '+str(p))
 return json.loads(K21.read_text()),json.loads(K22.read_text()),json.loads(MAN.read_text())
def main():
 a=load()
 if sys.argv[1:]==['--self-test']:
  good=build(*a);req(good['coverage']['K22']==76,'good coverage')
  x=json.loads(json.dumps(a[1]));x['covered_paths']=75
  try:build(a[0],x,a[2])
  except ValueError as e:req('completion' in str(e),'bad incomplete rejection')
  else:raise ValueError('incomplete K22 accepted')
  x=json.loads(json.dumps(a[2]));x['groups'].pop()
  try:build(a[0],a[1],x)
  except ValueError as e:req('logical digest' in str(e),'bad manifest rejection')
  else:raise ValueError('deleted group accepted')
  print(json.dumps({'status':'PASS_CHARGE_LEDGER_THROUGH_K22_SELFTEST','pinned_hashes':True,'incomplete_K22_rejected':True,'manifest_deletion_rejected':True},sort_keys=True));return
 req(not sys.argv[1:],'usage: assembler [--self-test]');out=build(*a);p=HERE/'results_charge_ledger_through_k22.json';t=Path(str(p)+'.tmp');t.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');t.replace(p);print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
