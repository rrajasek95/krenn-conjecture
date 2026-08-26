#!/usr/bin/env python3
"""Independent strict-family and hostile-mode audit of complete K22 assembly."""
from fractions import Fraction
from pathlib import Path
import copy,hashlib,importlib.util,json
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
MAN=HERE/'k22_manifest_complete_76.json';RES=HERE/'results_k22_complete_76_exact.json'
ASM=ROOT/'computations/unaudited-codex-orbit0-k22-availability-schedule-2026-08-24/assemble_k22_76_exact.py'
CONTRACT=ROOT/'computations/unaudited-codex-orbit0-k22-availability-schedule-2026-08-24/k22_expected_scalar_groups.json'
PINS={MAN:'731f6a111ce02ce2bfb40ccf465f0c7c631f1ed68106647ab5ca33288c82fdfe',RES:'7e955126cf391d2b6cfcbbb694004a2a5a8915981332cd9cc80e26460d7624f1',ASM:'e6aedd18c64a2847488bd18b65c342dd92169787d6741d9145625a9a9e52ffb5',CONTRACT:'e2e2ba53158365cdd03a380bcaa8699c11cbe34d2937d52f706ccc56d10cf65a'}
FAMILIES={'profile16':4,'hidden_collected2':2,'direct23':4,'hidden_pair2':2,'K15_grouped12':4,'K14_source3':3,'K16_grouped18':3}
def req(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rejection(module,manifest,needle):
 try:module.assemble(manifest)
 except ValueError as e:req(needle in str(e),(needle,str(e)))
 else:raise ValueError('hostile accepted: '+needle)
def main():
 for p,h in PINS.items():req(sha(p)==h,'pin '+str(p))
 spec=importlib.util.spec_from_file_location('frozen_k22_assembler',ASM);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 m=json.loads(MAN.read_text());r=json.loads(RES.read_text());c=json.loads(CONTRACT.read_text())['expected_scalar_groups']
 req(m['sealed_families']==FAMILIES,'seven-family partition')
 req(len(m['groups'])==len(c)==22,'group count')
 req([(g['group_id'],g['ids']) for g in m['groups']]==[(g['group_id'],g['ids']) for g in c],'frozen group order/IDs')
 flat=[x for g in m['groups'] for x in g['ids']];req(len(flat)==len(set(flat))==76,'strict ID union')
 rebuilt=mod.assemble(m);req(rebuilt==r,'exact replay mismatch')
 req((r['status'],r['complete_K22_claim'],r['required_paths'],r['covered_paths'],r['scalar_groups'])==('PASS_COMPLETE_K22_76_ID_EXACT_Q',True,76,76,22),'complete result guards')
 req(not r['missing_paths'] and not r['duplicate_paths'] and not r['extra_paths'],'coverage lists')
 req(Fraction(r['full']['numerator'],r['full']['denominator'])==Fraction(4753487002993355488,173867925)==Fraction(r['irreducible']['numerator'],r['irreducible']['denominator']),'charge')
 tests=[]
 x=copy.deepcopy(m);x['groups'].pop();tests.append((x,'missing'))
 x=copy.deepcopy(m);x['groups'].append(copy.deepcopy(x['groups'][-1]));tests.append((x,'duplicate'))
 x=copy.deepcopy(m);x['groups'][-1]['ids']=['D99:hostile|R:9'];tests.append((x,'extra'))
 x=copy.deepcopy(m);x['scale_U']+=1;tests.append((x,'degree/U'))
 x=copy.deepcopy(m);x['groups'][0]['irreducible_scaled_U']='0';x['groups'][0]['irreducible']='0';tests.append((x,'full!=irreducible'))
 x=copy.deepcopy(m);x['groups'][0]['evidence_sha256']='0'*64;tests.append((x,'hash mismatch'))
 for x,s in tests:rejection(mod,x,s)
 out={'status':'PASS_INDEPENDENT_COMPLETE_K22_76_AUDIT','covered_ids':76,'scalar_groups':22,'sealed_families':FAMILIES,'full':'4753487002993355488/173867925','manifest_sha256':PINS[MAN],'result_sha256':PINS[RES],'byte_replay_exact':True,'hostile_missing_duplicate_extra_U_terminality_hash_rejected':True,'scope':'K22 only; no K23/K24 inference'}
 print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
