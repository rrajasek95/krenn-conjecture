#!/usr/bin/env python3
"""Exact transport census for the twelve no-anchor rectangle records; no solve."""
from __future__ import annotations
import copy, hashlib, itertools, json, os
from pathlib import Path
if not __debug__:raise RuntimeError("fail closed: assertions required")
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
BASE=ROOT/"computations/unaudited-codex-n8-x5-unmapped16-carrier-incidence-design-2026-08-25"
QREF=ROOT/"computations/unaudited-codex-n8-x5-rectangle-rank3-adjugate-exact-q-referee-2026-08-25"
R12=ROOT/"computations/unaudited-codex-n8-x5-unmapped16-rectangle-rank12-incidence-ideal-design-2026-08-25"
R12REF=ROOT/"computations/unaudited-codex-n8-x5-unmapped16-rectangle-rank12-incidence-ideal-referee-2026-08-25"
PINS={BASE/"MANIFEST.sha256":"5cb72ac4af5a3ad3decbf3ba59ec858e23dcf2810c289d586feb14aeea1e61fe",BASE/"results_unmapped16_design.json":"2fe9e2a561397b58941b0f4210b3e4fb4a5457f377d4e23b7fc1dd6d0d22c008",QREF/"FINAL_MANIFEST.sha256":"94f1fe61337bfc8bb2b11aa3d528d219cd7b440d2ad19be2739109e693ab53a9",QREF/"results_referee.json":"459e403a6afc70d643ddfb37918513ded6eb79580169e796ab19be60a919b35f",R12/"MANIFEST.sha256":"743f3e526b21890509e32077ed5bf0c38b1240d25d475e71e2e78520445c85cf",R12/"results_rank12_incidence_design.json":"96b13ad342acd0fb02c37015b86303c9d6d7d880abe0e2a4e21f5e9e1aea5a28",R12REF/"FINAL_MANIFEST.sha256":"e3e7974ae201f5915e7eeec95f7b01e3db37f0ddfe69619d00a4c1a84a92838f"}
SITES=tuple(range(8));COLORS=tuple(range(3));S3=tuple(itertools.permutations(COLORS));P8=tuple(itertools.permutations(SITES))
F=frozenset(tuple(map(int,x)) for x in ("03","16","27","45"));VF=frozenset(tuple(map(int,x)) for x in ("04","12","35","67"))
def sha(path):
 h=hashlib.sha256()
 with path.open("rb") as stream:
  while chunk:=stream.read(1<<20):h.update(chunk)
 return h.hexdigest()
def edge(x):return tuple(map(int,x))
def label(e):return f"{e[0]}{e[1]}"
def map_edge(e,p):return tuple(sorted((p[e[0]],p[e[1]])))
def map_edges(es,p):return frozenset(map_edge(e,p) for e in es)
def make_matchings(vertices):
 if not vertices:yield ();return
 first=vertices[0]
 for pos in range(1,len(vertices)):
  for tail in make_matchings(vertices[1:pos]+vertices[pos+1:]):yield tuple(sorted(((first,vertices[pos]),)+tail))
PM8=tuple(sorted(make_matchings(SITES)));assert len(PM8)==105
def support(record):return F|frozenset(edge(x) for x in record["added"]+record["nonzero_variable_blocks"])
def added(record):return frozenset(edge(x) for x in record["added"])
def variables(record):return frozenset(edge(x) for x in record["nonzero_variable_blocks"])
def site_maps(source,target):
 return [p for p in P8 if map_edges(F,p)==F and map_edges(VF,p)==VF and map_edges(added(source),p)==added(target) and map_edges(variables(source),p)==variables(target)]
def supported_matchings(record):return tuple(m for m in PM8 if set(m)<=support(record))
def amplitude_terms(record,word):
 answer=[]
 for matching in supported_matchings(record):
  factors=[]
  for e in matching:
   a,b=word[e[0]],word[e[1]]
   if e in F:
    if a!=b:break
   else:factors.append((e,a,b))
  else:answer.append(tuple(factors))
 return tuple(answer)
def map_word(word,p,c):
 out=[None]*8
 for site in SITES:out[p[site]]=c[word[site]]
 return tuple(out)
def map_factor(factor,p,c):
 e,a,b=factor;u,v=p[e[0]],p[e[1]]
 return (tuple(sorted((u,v))),c[a],c[b]) if u<v else (tuple(sorted((u,v))),c[b],c[a])
def map_terms(terms,p,c):return tuple(sorted(tuple(sorted((map_factor(f,p,c) for f in monomial))) for monomial in terms))
def canonical_terms(terms):return tuple(sorted(tuple(sorted(monomial)) for monomial in terms))
def verify_word_transport(source,target,p):
 checks=0
 for c in S3:
  for word in itertools.product(COLORS,repeat=8):
   transported=map_word(word,p,c)
   assert map_terms(amplitude_terms(source,word),p,c)==canonical_terms(amplitude_terms(target,transported))
   assert (len(set(word))==1)==(len(set(transported))==1);checks+=1
 return checks
def carrier_transport(source,target,p):
 selected=next(x for x in source["two_sandwich_carriers"] if x["kind"]=="star" and x["cap"]=="27" and x["defining_sites"]==[1])
 cap=label(map_edge(edge(selected["cap"]),p));center=p[1];responses=sorted(label(map_edge(edge(x["response_pair"]),p)) for x in selected["terms"]);common=label(map_edge(edge(selected["common_block"]),p))
 candidates=[x for x in target["two_sandwich_carriers"] if x["kind"]=="star" and x["cap"]==cap and x["defining_sites"]==[center] and sorted(y["response_pair"] for y in x["terms"])==responses and x["common_block"]==common]
 assert len(candidates)==1 and candidates[0]["identity_cap"]
 return {"source_cap":"27","target_cap":cap,"source_center":1,"target_center":center,"target_response_pairs":responses,"source_common":"47","target_common":common,"target_factorization":candidates[0]["factorization_up_to_response_transposes"]}
def guard_transport(source,target,p):
 mapped=sorted(label(map_edge(edge(x["response_pair"]),p)) for x in source["guard_equations"]);actual=sorted(x["response_pair"] for x in target["guard_equations"]);assert mapped==actual
 return {"source_response_pairs":["14","24"],"target_response_pairs":actual}
def validate(result):
 assert result["schema"]=="KRENN_X5_RECTANGLE12_TRANSPORT_CENSUS_V1"
 assert result["status"]=="PASS_ALL_12_TRANSPORTED_TWO_SOURCE_CLASSES"
 assert result["census"]=={"records":12,"source_support_classes":2,"records_per_class":6,"rank3_exact_Q_closed_records":12,"rank1_exact_design_records":12,"rank2_exact_design_records":12,"solver_runs":0}
 assert result["scope"]=={"rank3_transport_closed":True,"rank1_rank2_transport_design_only":True,"remaining_no_anchor_rectangle_records":0,"other_unmapped_records":4,"full_conjecture":False}
def hostile(result,mutation):
 candidate=copy.deepcopy(result);mutation(candidate)
 try:validate(candidate)
 except (AssertionError,KeyError,TypeError):return True
 return False
def main():
 for path,expected in PINS.items():assert sha(path)==expected,(path,sha(path),expected)
 parent=json.loads((BASE/"results_unmapped16_design.json").read_text());records=parent["records"][:12]
 assert all(x["classification"]=="NO_GUARD_ANCHOR_06_OR_07" for x in records)
 qref=json.loads((QREF/"results_referee.json").read_text());assert qref["status"]=="PASS_EXACT_Q_UNIT_IDEAL_RANK3_TWO_LIFTS_ONLY"
 rank12=json.loads((R12/"results_rank12_incidence_design.json").read_text());assert rank12["counts"]["rank1"]=={"variables":76,"generators":6571,"canonical_inputs":5} and rank12["counts"]["rank2"]=={"variables":80,"generators":6574,"canonical_inputs":5}
 on=[x["record_index"] for x in records if "12" in x["nonzero_variable_blocks"]];off=[x["record_index"] for x in records if "12" not in x["nonzero_variable_blocks"]];assert on==[0,1,4,5,8,9] and off==[2,3,6,7,10,11]
 assert supported_matchings(records[0])==supported_matchings(records[2]) and all("12" not in "|".join(label(e) for e in m) for m in supported_matchings(records[0]))
 entries=[];word_checks=0
 for target in records:
  reference=records[0] if "12" in target["nonzero_variable_blocks"] else records[2]
  maps=site_maps(reference,target);assert len(maps)==1;p=maps[0]
  # No map crosses the A12 support boundary.
  opposite=records[2] if reference["record_index"]==0 else records[0];assert site_maps(opposite,target)==[]
  word_checks+=verify_word_transport(reference,target,p)
  carrier=carrier_transport(reference,target,p);guard=guard_transport(reference,target,p)
  mapped_outside=label(map_edge(edge("47"),p));mapped_companion=label(map_edge(edge("46"),p))
  entries.append({"record_index":target["record_index"],"orbit_id":target["orbit_id"],"A12_state":"present" if reference["record_index"]==0 else "absent","reference_record":reference["record_index"],"site_permutation":list(p),"site_maps_from_reference":1,"colour_maps_per_site_map":6,"word_generators_checked":6*6561,"guard":guard,"carrier":carrier,"mapped_outside_factor":mapped_outside,"mapped_companion":mapped_companion,"rank3":{"status":"CLOSED_BY_EXACT_Q_TRANSPORT","rank_condition":f"rank(A{mapped_outside})=3","variables":56,"generators":6563},"rank1":{"status":"EXACT_DESIGN_TRANSPORTED_NOT_SOLVED","rank_condition":f"rank(A{mapped_outside})=1","variables":76,"generators":6571,"raw_charts":27,"S3_orbits":5},"rank2":{"status":"EXACT_DESIGN_TRANSPORTED_NOT_SOLVED","rank_condition":f"rank(A{mapped_outside})=2","variables":80,"generators":6574,"raw_charts":27,"S3_orbits":5}})
 # Exhaustive pairwise source-support class matrix.
 matrix={}
 for a in records:
  matrix[str(a["record_index"])]={str(b["record_index"]):len(site_maps(a,b)) for b in records}
  assert sum(value>0 for value in matrix[str(a["record_index"])].values())==6
 # Each class is transitive and has a unique site map for every ordered pair.
 assert all(matrix[str(a)][str(b)]==1 for cls in (on,off) for a in cls for b in cls)
 assert all(matrix[str(a)][str(b)]==0 for a in on for b in off) and all(matrix[str(a)][str(b)]==0 for a in off for b in on)
 ledger={"records":entries,"source_support_isomorphism_counts":matrix};lp=HERE/"transport_ledger.json";tmp=lp.with_suffix(".json.tmp");tmp.write_text(json.dumps(ledger,indent=2,sort_keys=True)+"\n");os.replace(tmp,lp)
 result={"schema":"KRENN_X5_RECTANGLE12_TRANSPORT_CENSUS_V1","status":"PASS_ALL_12_TRANSPORTED_TWO_SOURCE_CLASSES","source_classes":[{"class":"A12_present","representative_record":0,"members":on},{"class":"A12_absent","representative_record":2,"members":off}],"source_class_inequivalence":"A12 presence changes the supported source-edge set, so no site/support automorphism crosses the two classes.","reduced_ideal_equivalence":"A12 occurs in no supported perfect matching, cap67 guard, or selected carrier. Dropping/free-lifting A12 identifies the reduced rank ideals; use A12=I3 for present and A12=0 for absent.","transport_theorem":"Every member has a unique fixed/variable-family/added-support site map from its same-A12 reference. All six simultaneous colour maps carry every word-labelled X5 generator, the guard response set, and the selected identity-cap carrier. Rank of the mapped outside factor and every rank-chart equation are therefore preserved.","word_generator_transport_checks":word_checks,"source_support_isomorphism_counts":matrix,"census":{"records":12,"source_support_classes":2,"records_per_class":6,"rank3_exact_Q_closed_records":12,"rank1_exact_design_records":12,"rank2_exact_design_records":12,"solver_runs":0},"transport_ledger":{"path":lp.name,"sha256":sha(lp)},"pins":{str(p.relative_to(ROOT)):v for p,v in PINS.items()},"scope":{"rank3_transport_closed":True,"rank1_rank2_transport_design_only":True,"remaining_no_anchor_rectangle_records":0,"other_unmapped_records":4,"full_conjecture":False}}
 validate(result);tests={"cross_class_overclaim":hostile(result,lambda x:x["census"].__setitem__("source_support_classes",1)),"rank3_underclaim":hostile(result,lambda x:x["census"].__setitem__("rank3_exact_Q_closed_records",11)),"solver_injection":hostile(result,lambda x:x["census"].__setitem__("solver_runs",1)),"conjecture_overclaim":hostile(result,lambda x:x["scope"].__setitem__("full_conjecture",True))};assert all(tests.values());result["hostile_tests"]=tests
 out=HERE/"results_transport_census.json";tmp=out.with_suffix(".json.tmp");tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n");os.replace(tmp,out)
 print(json.dumps({"status":result["status"],"classes":2,"rank3_closed":12,"rank12_designed":12,"word_checks":word_checks,"solves":0},sort_keys=True))
if __name__=="__main__":main()
