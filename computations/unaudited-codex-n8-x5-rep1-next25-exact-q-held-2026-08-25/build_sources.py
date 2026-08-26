#!/usr/bin/env python3
"""Regenerate the strict next-25 rep1 exact-Q source ledger; never solve."""
from __future__ import annotations
import hashlib,importlib.util,json,os
from pathlib import Path

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
BASE=ROOT/'computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25'
CENSUS=ROOT/'computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25'
CENSUS_REF=ROOT/'computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-referee-2026-08-25'
CLOSED0=ROOT/'computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-exact-q-2026-08-25'
CLOSED13=ROOT/'computations/unaudited-codex-n8-x5-rep1-group13-exact-q-pilot-2026-08-25'
CLOSED13_REF=ROOT/'computations/unaudited-codex-n8-x5-rep1-group13-exact-q-referee-2026-08-25'
CLOSED15_REF=ROOT/'computations/unaudited-codex-n8-x5-rep1-group15-exact-q-terminal-referee-2026-08-25'
CLOSED_NEXT10_REF=ROOT/'computations/unaudited-codex-n8-x5-rep1-next10-exact-q-terminal-referee-2026-08-25'
PINS={
 BASE/'MANIFEST.sha256':'4f367478c0a91257022234f5115979423bc8e889dd81a74cc3c200e25e3f82c1',
 BASE/'generate_minor_quotient.py':'63a4a58344c4bfdce0406d243f881216ca53eaa71264926a28364a823f560ac8',
 CENSUS/'MANIFEST.sha256':'6ed49a2e534955569149eaf2fe80b05aa3513507b41fe44575679eef0271fcb1',
 CENSUS/'results_canonical_census.json':'5ef1acc6ee2b97e993ae930b4ba420ce5c1c8c9eac16995d3a31b5c7a3eb5161',
 CENSUS_REF/'FINAL_MANIFEST.sha256':'f4779fdf166f008ac6ddf98b64a76cae1d1f81cccca1b51ef4b9a9a824b8cd5a',
 CLOSED0/'MANIFEST.sha256':'58c112efd1b889796337030bc08965c98195ef3b927bce257db82fe220e8d809',
 CLOSED0/'result.json':'668c36e5e6248c369424787a919013c32cde6b7c0aaa35ae81b7100469e7aab9',
 CLOSED13/'MANIFEST.sha256':'4cf21dec8926b66934fecf998616a31bc06f990b35662a2c48a67d3343dcb5a8',
 CLOSED13/'result.json':'66b92e09f73ec629cf09bd235000d64298d4d7987987b95d5f2be088d499e77b',
 CLOSED13_REF/'FINAL_MANIFEST.sha256':'aa7e6ef6457d18b8020dc1ece2566b83155a4f6d44bb569242e56c345f60a16e',
 CLOSED13_REF/'results_referee.json':'f156dd0fec67dcfe894e182a33778f4c0a688e39d71bf2d12b92d1cf4f377401',
 CLOSED15_REF/'FINAL_MANIFEST.sha256':'e9606d922c52dc79809249dbd6df98a0e61caa5a25bcc52d4d781f1d9a46c23d',
 CLOSED15_REF/'results_referee.json':'66d20e4a7991529826ee80288500c41707866d1fa7f0840bd680db927eb0f8a2',
 CLOSED_NEXT10_REF/'FINAL_MANIFEST.sha256':'3f3e91a3c63872371ad57014fada848ded4dd6bca0b829b824ed7d79d0f50b00',
 CLOSED_NEXT10_REF/'results_referee.json':'136d01596dc624804ae2073fec1e0227ecfe8ca2f7092994b84356871f919627',
}
EXCLUDED=tuple(range(0,11))+(13,15); SELECTED=(11,12,14)+tuple(range(16,38))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(p,text):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(text);os.replace(t,p)
def load_generator():
 spec=importlib.util.spec_from_file_location('sealed_rep1_generator',BASE/'generate_minor_quotient.py');assert spec and spec.loader
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
def chart_dict(v):
 coordinate,p,q,r,kind,s,a,b=v
 return {'coordinate':coordinate,'outside':(p,q),'x_pivot':r,'q_kind':kind,'q_pivot':s,'minor_pair':(a,b)}
for p,h in PINS.items(): assert sha(p)==h,(p,sha(p),h)
assert json.loads((CLOSED0/'result.json').read_text())['status']=='UNIT_IDEAL_EXACT_Q_LOCALIZED_CHART'
assert json.loads((CLOSED13/'result.json').read_text())['status']=='UNIT_IDEAL_EXACT_Q_GROUP13'
assert json.loads((CLOSED15_REF/'results_referee.json').read_text())['status']=='PASS_UNIT_IDEAL_EXACT_Q_GROUP15_ONLY'
next10=json.loads((CLOSED_NEXT10_REF/'results_referee.json').read_text())
assert next10['status']=='PASS_ALL_TEN_EXACT_Q_UNIT_IDEALS' and next10['groups_closed']==list(range(1,11))
census=json.loads((CENSUS/'results_canonical_census.json').read_text())
records=census['enumeration']['records']; assert [r['group_id'] for r in records]==list(range(162))
eligible=[r for r in records if r['group_id'] not in EXCLUDED]
assert tuple(r['group_id'] for r in eligible[:25])==SELECTED and len(SELECTED)==25
minor=load_generator(); base=minor.load_base(); lanes=[]
for ordinal,record in enumerate(eligible[:25],1):
 gid=record['group_id']; chart=record['canonical_chart']
 program=minor.build_program(base,chart_dict(chart),'0'); payload=program.encode()
 assert hashlib.sha256(payload).hexdigest()==record['exact_Q_source_sha256']
 assert len(payload)==record['exact_Q_source_bytes']
 assert program.count('ring r=0,')==1 and program.count('ideal G=slimgb(I);')==1
 assert program.count('poly remainder=reduce(1,G);')==1 and program.count('quit;')==1
 path=HERE/'sources'/f'rep1_group{gid:03d}_Q.sing'; atomic(path,program); assert sha(path)==record['exact_Q_source_sha256']
 lanes.append({'ordinal':ordinal,'group_id':gid,'canonical_chart':chart,'source_path':str(path.relative_to(HERE)),'source_sha256':sha(path),'source_bytes':path.stat().st_size,'variables':91,'generators':6577})
ledger={
 'schema':'KRENN_X5_REP1_NEXT25_EXACT_Q_SOURCE_LEDGER_V1','status':'PASS_REGENERATED_SOURCES_ZERO_SOLVES',
 'selection':{'excluded_closed_groups':list(EXCLUDED),'rule':'25 lowest eligible canonical group IDs in strict ascending order','selected_group_ids':list(SELECTED)},
 'lanes':lanes,'pins':{str(p.relative_to(ROOT)):h for p,h in PINS.items()},
 'scope':{'source_files_materialized':25,'solver_launches':0,'results_materialized':0,'clearances_materialized':0,'mathematical_coverage':False},
}
atomic(HERE/'source_ledger.json',json.dumps(ledger,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':ledger['status'],'groups':list(SELECTED),'source_ledger_sha256':sha(HERE/'source_ledger.json'),'total_bytes':sum(x['source_bytes'] for x in lanes)},sort_keys=True))
