#!/usr/bin/env python3
"""Canonical exact-Q input census for all 162 refined rep1 chart orbits."""
from __future__ import annotations

import collections, copy, hashlib, importlib.util, itertools, json, os, time
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE=ROOT/"computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25"
CLOSED=ROOT/"computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-exact-q-2026-08-25"
PINS={
 BASE/"MANIFEST.sha256":"4f367478c0a91257022234f5115979423bc8e889dd81a74cc3c200e25e3f82c1",
 BASE/"generate_minor_quotient.py":"63a4a58344c4bfdce0406d243f881216ca53eaa71264926a28364a823f560ac8",
 CLOSED/"MANIFEST.sha256":"58c112efd1b889796337030bc08965c98195ef3b927bce257db82fe220e8d809",
 CLOSED/"result.json":"668c36e5e6248c369424787a919013c32cde6b7c0aaa35ae81b7100469e7aab9",
}


def sha256(path):
 h=hashlib.sha256()
 with path.open("rb") as stream:
  while chunk:=stream.read(1<<20): h.update(chunk)
 return h.hexdigest()


def load_base():
 spec=importlib.util.spec_from_file_location("sealed_minor_quotient",BASE/"generate_minor_quotient.py")
 assert spec and spec.loader
 module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module


def chart_dict(record):
 coordinate,p,q,r,kind,s,a,b=record
 return {"coordinate":coordinate,"outside":(p,q),"x_pivot":r,"q_kind":kind,"q_pivot":s,"minor_pair":(a,b)}


def image(edges,permutation):
 return {tuple(sorted((permutation[a],permutation[b]))) for a,b in edges}


def vertex_automorphisms(base):
 values=[]
 for permutation in itertools.permutations(range(8)):
  if image(base.FIXED,permutation)==set(base.FIXED) and image(base.SUPPORT,permutation)==set(base.SUPPORT):
   values.append(permutation)
 return values


def validate(result):
 assert result["schema"]=="KRENN_X5_REP1_REMAINING161_CANONICAL_CENSUS_V1"
 assert result["status"]=="PASS_EXACT_ENUMERATION_NO_IDEALS"
 assert result["census"]["raw_refined_charts"]==972
 assert result["census"]["canonical_polynomial_groups"]==162
 assert result["census"]["closed_groups"]==1 and result["census"]["remaining_groups"]==161
 assert result["census"]["raw_members_per_group"]==6
 assert result["scope"]=={"ideal_launches":0,"additional_charts_closed":0,"representative_closed":False}


def hostile(result,mutation):
 candidate=copy.deepcopy(result); mutation(candidate)
 try: validate(candidate)
 except (AssertionError,KeyError,TypeError): return True
 return False


def main():
 for path,expected in PINS.items(): assert sha256(path)==expected,(path,sha256(path),expected)
 minor=load_base()
 base=minor.load_base()
 raw,groups=minor.orbit_ledger()
 assert len(raw)==972 and len(groups)==162 and set(map(len,groups.values()))=={6}
 assert all(minor.orbit_representative(member)==representative for representative,members in groups.items() for member in members)
 automorphisms=vertex_automorphisms(base)
 assert automorphisms==[tuple(range(8))]
 closed_record=(0,0,0,0,"y",0,0,1)
 closed_representative=minor.orbit_representative(closed_record)
 assert closed_representative==closed_record
 closed_result=json.loads((CLOSED/"result.json").read_text())
 assert closed_result["status"]=="UNIT_IDEAL_EXACT_Q_LOCALIZED_CHART"
 closed_sha=closed_result["source_Q_sha256"]

 started=time.monotonic(); records=[]; source_hashes=set(); sizes=[]
 for index,representative in enumerate(sorted(groups)):
  program=minor.build_program(base,chart_dict(representative),"0")
  payload=program.encode(); digest=hashlib.sha256(payload).hexdigest(); size=len(payload)
  assert digest not in source_hashes
  source_hashes.add(digest); sizes.append(size)
  records.append({
   "group_id":index,"canonical_chart":list(representative),"raw_member_count":len(groups[representative]),
   "raw_members":[list(value) for value in sorted(groups[representative])],
   "exact_Q_source_sha256":digest,"exact_Q_source_bytes":size,
   "closed":representative==closed_representative,
  })
 elapsed=time.monotonic()-started
 assert sum(item["closed"] for item in records)==1
 assert next(item for item in records if item["closed"])["exact_Q_source_sha256"]==closed_sha=="53f741ca9173877ef1bc21dba2546a82102a32140221068de1301d0b4635dadb"
 remaining=[item for item in records if not item["closed"]]
 size_hist=collections.Counter(sizes)
 closed_wall=closed_result["wall_seconds"]; closed_rss=closed_result["observed_peak_rss_bytes"]
 total_remaining_bytes=sum(item["exact_Q_source_bytes"] for item in remaining)
 result={
  "schema":"KRENN_X5_REP1_REMAINING161_CANONICAL_CENSUS_V1",
  "status":"PASS_EXACT_ENUMERATION_NO_IDEALS",
  "canonicalization_contract":{
   "source_labels":"each matrix block retains its tensor-edge label; transpose follows stored endpoint order",
   "allowed_color_renaming":"one common S3 permutation on all eight tensor color indices; induced source-entry and witness-variable renaming; equations permute by words",
   "target_rigidity":"the three normalized pure GHZ rows force the eight local color permutations to be the same common permutation",
   "vertex_automorphism_test":"all 8! vertex permutations tested preserving fixed-identity edges and the full supported source graph",
   "vertex_automorphism_count":len(automorphisms),"vertex_automorphisms":[list(value) for value in automorphisms],
   "conclusion":"the sealed common-S3 orbit representative is the exact canonical polynomial-group key; no further source-labelled vertex/transpose renaming exists",
  },
  "census":{
   "raw_refined_charts":len(raw),"canonical_polynomial_groups":len(groups),"closed_groups":1,
   "remaining_groups":len(remaining),"raw_members_per_group":6,"distinct_canonical_source_hashes":len(source_hashes),
  },
  "source_size":{
   "minimum_bytes":min(sizes),"maximum_bytes":max(sizes),"all_162_total_bytes":sum(sizes),
   "remaining_161_total_bytes":total_remaining_bytes,
   "remaining_161_total_mib":total_remaining_bytes/1024**2,
   "size_histogram_bytes":{str(k):v for k,v in sorted(size_hist.items())},
   "on_demand_peak_input_bytes":max(sizes),
  },
  "projection_from_closed_chart":{
   "closed_chart_wall_seconds":closed_wall,"closed_chart_peak_rss_bytes":closed_rss,
   "naive_sequential_remaining_wall_seconds":closed_wall*161,
   "naive_sequential_remaining_wall_minutes":closed_wall*161/60,
   "projection_warning":"single-chart measurement only; chart complexity may vary and this is not a production gate",
   "recommended_independent_gate":"after referee seal, run exactly one maximum-source-size remaining group under native240/wrapper250/RSS8GiB; accept evidence before scheduling another",
  },
  "enumeration":{
   "wall_seconds":elapsed,"materialized_sources":0,"records":records,
  },
  "pins":{str(path.relative_to(ROOT)):digest for path,digest in PINS.items()},
  "scope":{"ideal_launches":0,"additional_charts_closed":0,"representative_closed":False},
 }
 validate(result)
 tests={
  "group_collapse":hostile(result,lambda x:x["census"].__setitem__("canonical_polynomial_groups",161)),
  "launch_injection":hostile(result,lambda x:x["scope"].__setitem__("ideal_launches",1)),
  "closure_overclaim":hostile(result,lambda x:x["scope"].__setitem__("representative_closed",True)),
  "remaining_mutation":hostile(result,lambda x:x["census"].__setitem__("remaining_groups",160)),
 }
 assert all(tests.values()); result["hostile_tests"]=tests
 temporary=HERE/"results_canonical_census.json.tmp"
 temporary.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n"); os.replace(temporary,HERE/"results_canonical_census.json")
 print(json.dumps({"status":result["status"],"groups":162,"remaining":161,"source_mib":total_remaining_bytes/1024**2,"wall":elapsed},sort_keys=True))


if __name__=="__main__": main()
