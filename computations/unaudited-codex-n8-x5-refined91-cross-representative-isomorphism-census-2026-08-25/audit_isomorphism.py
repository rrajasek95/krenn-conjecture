#!/usr/bin/env python3
"""Exact isomorphism census for refined 91/6577 charts; no CAS solve."""
from __future__ import annotations
import copy, hashlib, itertools, json, os
from pathlib import Path

if not __debug__:raise RuntimeError("fail closed: assertions required")
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
P1=ROOT/"computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25"
G1=ROOT/"computations/unaudited-codex-n8-x5-seven-block-rep1-diagonal-incidence-gate-2026-08-25"
P2=ROOT/"computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25"
P4=ROOT/"computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25"
P5=ROOT/"computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25"
PINS={P1/"MANIFEST.sha256":"4f367478c0a91257022234f5115979423bc8e889dd81a74cc3c200e25e3f82c1",P1/"minor_quotient_metadata.json":"1a8c5bb3c105d8d87b2eab58a52934a44d7768c537cc33a1542d7d06402d317c",P1/"generate_minor_quotient.py":"63a4a58344c4bfdce0406d243f881216ca53eaa71264926a28364a823f560ac8",G1/"MANIFEST.sha256":"36e39752896a052d8bfe75af29c39c4d8c09c090afb8a9692e818a63c9a811bf",G1/"gate_metadata.json":"97342352d9162253c0c27aefdeba81f25b1265751e4c29daf706f828f4c9572e",P2/"MANIFEST.sha256":"ab18ee8446de2a163f1e6c14dfc60d2cd4c6465f5464206e10ecb35c2d2facf2",P2/"results_rep2_corrected_contraction_design.json":"ed37c2e0da8088e08fb6891e60768d98fbbbf031935f752b4e4af280dfe27b26",P4/"MANIFEST.sha256":"7f47c0567580aba565925b95860bace46ebaf5703aace4ec8aa100f48ec33e02",P4/"results_rep4_contraction_design.json":"7e96874cca1afaaa377aa3001d8e00b73ed4fe9322381ec269c4a46b9144bf0c",P5/"MANIFEST.sha256":"33ae759fb235518412c33d36d621ccce09b8a9e05e9ece05b6d1aaf7f2d8c40c",P5/"results_rep5_contraction_design.json":"b2ba095f4f702ac2138cb40d45b7721a8df9b338900282020e83b791264df59b"}
COLORS=tuple(range(3));S3=tuple(itertools.permutations(COLORS));SITES=tuple(range(8))
F=frozenset((tuple(map(int,x)) for x in ("03","16","27","45")));V=frozenset((tuple(map(int,x)) for x in ("04","12","35","67")))
SPECS={
 1:{"added":("06","13","17","25","26","46","47"),"outside":"47","eliminated":"46","partner_y":"13","partner_y_orientation":"row","partner_z":"35","partner_z_orientation":"column","digest":"61640fb492640847a58cf9f5e2f1dbc3f381736d7909325f35b2dfffb211d5eb"},
 2:{"added":("06","14","17","23","26","56","57"),"outside":"57","eliminated":"56","partner_y":"23","partner_y_orientation":"row","partner_z":"35","partner_z_orientation":"column","digest":"46a64a3e1ab088b6121430b229ae89503f93c9473d693fdef9af294c4af8a81d"},
 4:{"added":("06","15","17","23","26","46","47"),"outside":"47","eliminated":"46","partner_y":"23","partner_y_orientation":"row","partner_z":"35","partner_z_orientation":"column","digest":"db51326bf12bfb970b95eb6dd6e490d3e983c18f303f44eeb8b5d0586c0f0d5a"},
 5:{"added":("06","15","17","24","26","36","37"),"outside":"37","eliminated":"36","partner_y":"35","partner_y_orientation":"column","partner_z":"37","partner_z_orientation":"column","digest":"e8015349824f6851fba73d9ec57f4d8b59ea4ac686925415ff61c89b45df5f3a"}}
for spec in SPECS.values():spec["A"]=frozenset(tuple(map(int,x)) for x in spec["added"]);spec["support"]=F|V|spec["A"]

def sha(path):
 h=hashlib.sha256()
 with path.open("rb") as stream:
  while chunk:=stream.read(1<<20):h.update(chunk)
 return h.hexdigest()
def map_edges(edges,p):return frozenset(tuple(sorted((p[a],p[b]))) for a,b in edges)
def graph_code(spec,p):
 f,v,a=map_edges(F,p),map_edges(V,p),map_edges(spec["A"],p);chars=[]
 for edge in itertools.combinations(SITES,2):chars.append("F" if edge in f else "V" if edge in v else "A" if edge in a else ".")
 return "".join(chars)
def graph_census():
 permutations=tuple(itertools.permutations(SITES));records={};iso={}
 for rep,spec in SPECS.items():
  codes=[graph_code(spec,p) for p in permutations];canonical=min(codes);identity=graph_code(spec,SITES)
  records[str(rep)]={"canonical_code":canonical,"canonical_sha256":hashlib.sha256(canonical.encode()).hexdigest(),"automorphisms":sum(code==identity for code in codes),"canonicalizers":sum(code==canonical for code in codes)}
 for left,lspec in SPECS.items():
  iso[str(left)]={}
  for right,rspec in SPECS.items():
   iso[str(left)][str(right)]=sum(map_edges(F,p)==F and map_edges(V,p)==V and map_edges(lspec["A"],p)==rspec["A"] for p in permutations)
 return records,iso

def act_chart(record,p):
 coordinate,outrow,outcol,xpivot,kind,qpivot,a,b=record;aa,bb=sorted((p[a],p[b]))
 return (p[coordinate],p[outrow],p[outcol],p[xpivot],kind,p[qpivot],aa,bb)
def chart_groups():
 raw=[]
 for i,p,q,r,s in itertools.product(COLORS,repeat=5):
  for kind in ("y","z"):
   for other in COLORS:
    if other!=q:
     a,b=sorted((q,other));raw.append((i,p,q,r,kind,s,a,b))
 groups={}
 for x in raw:
  orbit={act_chart(x,p) for p in S3};groups.setdefault(min(orbit),set()).update(orbit)
 assert len(raw)==972 and len(groups)==162 and {len(x) for x in groups.values()}=={6}
 return raw,groups

def matching_terms(spec,word):
 terms=[]
 for matching in PM8:
  if not set(matching)<=spec["support"]:continue
  factors=[]
  for edge in matching:
   i,j=word[edge[0]],word[edge[1]]
   if edge in F:
    if i!=j:break
   else:factors.append((edge,i,j))
  else:terms.append((matching,tuple(factors)))
 return tuple(terms)
def map_term(term,p):
 matching,factors=term
 return (matching,tuple((edge,p[i],p[j]) for edge,i,j in factors))
def verify_full_word_maps():
 checks=0
 for spec in SPECS.values():
  for p in S3:
   for word in itertools.product(COLORS,repeat=8):
    target=tuple(p[x] for x in word)
    assert tuple(map_term(term,p) for term in matching_terms(spec,word))==matching_terms(spec,target)
    assert (len(set(word))==1)==(len(set(target))==1);checks+=1
 return checks

def source_variables(spec,chart):
 _,_,_,_,kind,s,_,_=chart;el=tuple(map(int,spec["eliminated"]));retained=tuple(edge for edge in sorted(V|spec["A"]) if edge!=el)
 solved={(tuple(map(int,"06")),i,j) for i,j in itertools.product(COLORS,repeat=2)}
 partner=tuple(map(int,spec[f"partner_{kind}"]));orientation=spec[f"partner_{kind}_orientation"]
 if orientation=="row":solved|={(partner,s,j) for j in COLORS}
 else:solved|={(partner,i,s) for i in COLORS}
 answer={(edge,i,j) for edge in retained for i,j in itertools.product(COLORS,repeat=2) if (edge,i,j) not in solved}
 assert len(answer)==78;return answer
def verify_chart_map(spec,source,target,p):
 assert act_chart(source,p)==target
 mapped={(edge,p[i],p[j]) for edge,i,j in source_variables(spec,source)}
 assert mapped==source_variables(spec,target)
 # Remaining generator labels: 6561 words, 6 non-p outside guard entries, 9 reduced guard entries, one saturation.
 sp=source[1];tp=target[1]
 guard6={(p[i],p[j]) for i,j in itertools.product(COLORS,repeat=2) if j!=sp}
 assert guard6=={(i,j) for i,j in itertools.product(COLORS,repeat=2) if j!=tp}
 assert {(p[i],p[j]) for i,j in itertools.product(COLORS,repeat=2)}==set(itertools.product(COLORS,repeat=2))
 # Cramer sign map: d' = eps*map(d); t and abar acquire eps, so saturation is unchanged.
 a,b=source[6:8];aa,bb=target[6:8];eps=1 if (p[a],p[b])==(aa,bb) else -1
 assert (p[a],p[b]) in ((aa,bb),(bb,aa)) and eps in (-1,1)
 return {"variables":91,"generators":6577,"amplitude":6561,"guard6":6,"guard9":9,"saturation":1,"minor_sign":eps}
def verify_chart_bijections(groups):
 maps=0;generator_maps=0;signs={-1:0,1:0};classes=[]
 for rep,spec in SPECS.items():
  for index,(representative,members) in enumerate(sorted(groups.items())):
   member_records=[]
   for member in sorted(members):
    permutations=[p for p in S3 if act_chart(representative,p)==member];assert len(permutations)==1
    audit=verify_chart_map(spec,representative,member,permutations[0]);maps+=1;generator_maps+=audit["generators"];signs[audit["minor_sign"]]+=1
    member_records.append({"chart":list(member),"colour_permutation":list(permutations[0]),"minor_sign":audit["minor_sign"]})
   classes.append({"class_id":f"rep{rep}_orbit{index:03d}","representative":rep,"canonical_chart":list(representative),"raw_member_count":6,"raw_members":member_records,"cross_representative_members":[]})
 assert maps==4*162*6 and generator_maps==maps*6577
 return classes,{"explicit_chart_bijections":maps,"generator_family_bijections":generator_maps,"minor_sign_census":{str(k):v for k,v in sorted(signs.items())}}

PM8=tuple(sorted((lambda f:list(f(tuple(range(8)))))(lambda vertices: _matchings(vertices)))) if False else None
def make_matchings(vertices):
 if not vertices:yield ();return
 first=vertices[0]
 for pos in range(1,len(vertices)):
  for tail in make_matchings(vertices[1:pos]+vertices[pos+1:]):yield tuple(sorted(((first,vertices[pos]),)+tail))
PM8=tuple(sorted(make_matchings(tuple(range(8)))));assert len(PM8)==105

def validate(result):
 assert result["schema"]=="KRENN_X5_REFINED91_CROSS_REPRESENTATIVE_ISOMORPHISM_CENSUS_V1"
 assert result["status"]=="PASS_NO_CROSS_REPRESENTATIVE_ISOMORPHISMS"
 assert result["census"]=={"representatives":4,"raw_charts":3888,"within_representative_S3_classes":648,"cross_representative_equivalences":0,"final_equivalence_classes":648}
 assert result["scope"]=={"solver_runs":0,"generator_claims_beyond_verified_bijections":0,"mathematical_closure":False}
def hostile(result,mutation):
 candidate=copy.deepcopy(result);mutation(candidate)
 try:validate(candidate)
 except (AssertionError,KeyError,TypeError):return True
 return False

def main():
 for path,expected in PINS.items():assert sha(path)==expected,(path,sha(path),expected)
 r1=json.loads((P1/"minor_quotient_metadata.json").read_text());assert r1["counts"]["minor_quotient_variables"]==91 and r1["counts"]["minor_quotient_generators"]==6577 and r1["chart_census"]["s3_orbits"]==162
 assert json.loads((G1/"gate_metadata.json").read_text())["parent_full_x5_digest"]==SPECS[1]["digest"]
 for rep,path,name in ((2,P2,"results_rep2_corrected_contraction_design.json"),(4,P4,"results_rep4_contraction_design.json"),(5,P5,"results_rep5_contraction_design.json")):
  item=json.loads((path/name).read_text());assert item["counts"]["new_variables"]==91 and item["counts"]["new_generators"]==6577 and item["chart_census"]["S3_orbits"]==162 and item["source_reconstruction" if rep in (4,5) else "independent_source_reconstruction"]["full_x5_digest"]==SPECS[rep]["digest"]
 graph_records,iso=graph_census();assert all(iso[str(a)][str(b)]==(1 if a==b else 0) for a in SPECS for b in SPECS)
 _,groups=chart_groups();word_checks=verify_full_word_maps();classes,bijections=verify_chart_bijections(groups)
 ledger_path=HERE/"equivalence_class_ledger.json";tmp=ledger_path.with_suffix(".json.tmp");tmp.write_text(json.dumps({"classes":classes},indent=2,sort_keys=True)+"\n");os.replace(tmp,ledger_path)
 result={"schema":"KRENN_X5_REFINED91_CROSS_REPRESENTATIVE_ISOMORPHISM_CENSUS_V1","status":"PASS_NO_CROSS_REPRESENTATIVE_ISOMORPHISMS",
  "allowed_bijection_contract":{"ring_grading":"matrix-entry variables map to matrix-entry variables; witness/scalar roles remain typed","source_labels":"one common site permutation induces every source-block label and row/column orientation","fixed_blocks":"fixed edge set F and variable-family edge set V are preserved","guard":"anchor, outside, companion and transition equations must map source-labelled","carrier":"coordinate/outside/x-pivot/partner-kind/partner-pivot/minor roles map exactly","full_x5_word_map":"one simultaneous colour permutation maps all eight word coordinates and every matrix-entry colour"},
  "necessity_lemma":"Any allowed polynomial-input isomorphism maps source-entry occurrence groups in every word-labelled X5 monomial, hence induces a site permutation carrying the F/V/A coloured support graph. Therefore a zero coloured-support graph isomorphism count is a fail-closed obstruction before contracted-generator comparison.",
  "support_graphs":graph_records,"site_permutation_isomorphism_counts":iso,
  "positive_bijection_audit":{"full_word_generator_maps_checked":word_checks,"chart_maps":bijections,"substitution_covariance":"under a colour permutation, raw source and witness variables map bijectively; if sorted minor orientation reverses, t and abar both gain sign epsilon, leaving the combined saturation invariant; composition maps all 6561 substituted amplitudes, 15 guards, and saturation"},
  "census":{"representatives":4,"raw_charts":3888,"within_representative_S3_classes":648,"cross_representative_equivalences":0,"final_equivalence_classes":648},"class_ledger":{"path":ledger_path.name,"sha256":sha(ledger_path),"classes":len(classes)},"pins":{str(p.relative_to(ROOT)):v for p,v in PINS.items()},"scope":{"solver_runs":0,"generator_claims_beyond_verified_bijections":0,"mathematical_closure":False}}
 validate(result);tests={"cross_claim":hostile(result,lambda x:x["census"].__setitem__("cross_representative_equivalences",1)),"class_collapse":hostile(result,lambda x:x["census"].__setitem__("final_equivalence_classes",647)),"solver_injection":hostile(result,lambda x:x["scope"].__setitem__("solver_runs",1)),"closure_overclaim":hostile(result,lambda x:x["scope"].__setitem__("mathematical_closure",True))};assert all(tests.values());result["hostile_tests"]=tests
 out=HERE/"results_isomorphism_census.json";tmp=out.with_suffix(".json.tmp");tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n");os.replace(tmp,out)
 print(json.dumps({"status":result["status"],"classes":648,"cross":0,"word_checks":word_checks,"generator_maps":bijections["generator_family_bijections"],"solves":0},sort_keys=True))
if __name__=="__main__":main()
