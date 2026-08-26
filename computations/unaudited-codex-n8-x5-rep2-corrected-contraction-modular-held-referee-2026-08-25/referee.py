#!/usr/bin/env python3
import ast,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
DES=ROOT/"computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25";HELD=ROOT/"computations/unaudited-codex-n8-x5-rep2-corrected-all-equal-y-modular-held-2026-08-25"
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def replay(manifest):
 for line in manifest.read_text().splitlines():
  if not line.strip():continue
  digest,name=line.split(None,1);p=Path(name.strip());p=p if p.is_absolute() else manifest.parent/p
  assert p.is_file() and h(p)==digest,(p,h(p) if p.exists() else None,digest)
replay(DES/"MANIFEST.sha256");replay(HELD/"MANIFEST.sha256")
assert h(DES/"MANIFEST.sha256")=="ab18ee8446de2a163f1e6c14dfc60d2cd4c6465f5464206e10ecb35c2d2facf2"
assert h(DES/"results_rep2_corrected_contraction_design.json")=="ed37c2e0da8088e08fb6891e60768d98fbbbf031935f752b4e4af280dfe27b26"
assert h(HELD/"MANIFEST.sha256")=="174d817976688a75ef1826b6a5fb24f9b259cf7324a4022682abdf3e8f7bc214"
result=json.loads((DES/"results_rep2_corrected_contraction_design.json").read_text());held=json.loads((HELD/"held_pilot.json").read_text())
edges=set("03 16 27 45 04 12 35 67 06 14 17 23 26 56 57".split())
def matchings(rem,chosen=()):
 if not rem:return {"|".join(sorted(chosen))}
 a=min(rem);out=set()
 for b in rem-{a}:
  e="".join(sorted((a,b)))
  if e in edges:out|=matchings(rem-{a,b},chosen+(e,))
 return out
expected=set(result["independent_source_reconstruction"]["supported_matchings"]);assert matchings(set("01234567"))==expected and len(expected)==13
assert result["corrected_system"]["original_guard"]==["A06*A57^T=0","A57^T+A17*A56^T=0","A26*A57^T+A56^T=0"]
assert result["corrected_system"]["elimination"]=="A56=-A57*A26^T"
assert result["corrected_system"]["reduced_guard"]==["A06*A57^T=0","(I-A17*A26)*A57^T=0"]
carrier=result["corrected_system"]["carrier"];assert carrier=={"cap":"03","center":4,"terms":["R26=A06^T*K*A23^T","R56=A06^T*K*A35"],"factorization":"A06^T*K*[A23^T|A35]"}
assert result["corrected_system"]["superseded_carrier"].startswith("A04^T")
ledger=json.loads((DES/"chart_orbit_ledger.json").read_text());groups=ledger["groups"]
assert ledger["raw"]==972 and len(groups)==162 and all(g["size"]==len(g["members"])==6 for g in groups)
members=[tuple(x) for g in groups for x in g["members"]];assert len(members)==len(set(members))==972
assert sum(g["representative"][4]=="y" for g in groups)==81 and sum(g["representative"][4]=="z" for g in groups)==81
def counts(path):
 s=path.read_text();a=s.index("ring r=0,(")+len("ring r=0,(");b=s.index("),dp;",a);variables=s[a:b].split(",")
 a=s.index("ideal I=")+len("ideal I=");b=s.index(';\nprint("INPUT_VARIABLES',a);body=s[a:b];depth=0;n=1
 for c in body:
  if c=="(":depth+=1
  elif c==")":depth-=1
  elif c=="," and depth==0:n+=1
 assert depth==0;return variables,n,s
for kind,digest in [("y","0285c34fcae56db7dc60830197d645799f5f1c90d84467868436ee453916aedf"),("z","3cc285cf29b2416b674f325c7afb891570c5bd4b92e0da458d8926c0f958fae4")]:
 path=DES/f"rep2_corrected_guard_minor_tiny_{kind}_Q.sing";assert h(path)==digest;variables,n,s=counts(path);assert len(variables)==91 and n==6577 and not any(v.startswith("a06_") for v in variables) and "slimgb" not in s and "reduce(1" not in s
assert result["counts"]=={"old_variables":100,"old_generators":6586,"new_variables":91,"new_generators":6577,"full_x5":6561,"remaining_guard":15,"combined_saturation":1}
assert result["substitution"]["A06"]=="all nine entries solved" and result["substitution"]["tautologies_removed"]==["six incidence equations","three row-p A06*A57^T equations"]
q=(DES/"rep2_corrected_guard_minor_tiny_y_Q.sing").read_text();p=(HELD/"rep2_all_equal_y_i0_p00_x0_y0_d01_p32003.sing").read_text()
ep="\n".join(["ideal G=slimgb(I);",'print("GROEBNER_SIZE="+string(size(G)));',"poly remainder=reduce(1,G);",'print("UNIT_REMAINDER="+string(remainder));','if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',"quit;"])
derived=q.replace("ring r=0,","ring r=32003,",1).replace("quit;",ep,1)
assert q.count("ring r=0,")==q.count("quit;")==1 and derived==p and h(HELD/"rep2_all_equal_y_i0_p00_x0_y0_d01_p32003.sing")=="95147044a1703357db2045f393bea44759a854cf5d178b9329b150460ca9abe1"
runner=(HELD/"run_one_lane.py").read_text();ast.parse(runner);assert h(HELD/"run_one_lane.py")=="845bf7928d88b0c1109bc157fbca104423adc76408d1f98b9d470a93df0a180a"
assert runner.count("subprocess.Popen(")==1 and runner.index('assert not (HERE / "result.json").exists()')<runner.rindex("require_clearance()")<runner.index("subprocess.Popen(")
assert 'NATIVE_WALL = 180' in runner and 'WRAPPER_WALL = 195' in runner and 'RSS_CAP = 8 * 1024**3' in runner
assert 'os.replace(temporary, path)' in runner and 'gtimeout 195 python3 run_one_lane.py' in json.dumps(held)
assert not (HELD/"result.json").exists() and not (HELD/"independent_referee_acceptance.json").exists() and not (HELD/"launch_clearance.json").exists() and not list(HELD.glob("*.tmp"))
accept=json.loads((HERE/"INDEPENDENT_ACCEPTANCE_PAYLOAD.json").read_text());assert accept["held_manifest_sha256"]==h(HELD/"MANIFEST.sha256") and accept["source_sha256"]==h(HELD/"rep2_all_equal_y_i0_p00_x0_y0_d01_p32003.sing") and accept["runner_sha256"]==h(HELD/"run_one_lane.py")
audit=json.loads((HERE/"results_referee.json").read_text());assert audit["status"]=="PASS_DESIGN_AND_APPROVE_HELD_ONE_MODULAR_DIAGNOSTIC" and audit["execution"]=={"design_ideal_runs":0,"modular_runs":0,"result_absent":True,"clearance_files_absent":True}
print(json.dumps({"status":audit["status"],"result_sha256":h(HERE/"results_referee.json")}))
