#!/usr/bin/env python3
"""Independent terminal promotion referee for anchor records 12..15."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
DES=ROOT/"computations/unaudited-codex-n8-x5-anchor-no-rectangle-design-2026-08-25"
DREF=ROOT/"computations/unaudited-codex-n8-x5-anchor-no-rectangle-design-referee-2026-08-25"
QREF=ROOT/"computations/unaudited-codex-n8-x5-anchor-base81-exact-q-terminal-referee-2026-08-25"
QRUN=ROOT/"computations/unaudited-codex-n8-x5-anchor-base81-exact-q-held-plan-2026-08-25"
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pins={DREF/"MANIFEST.sha256":"e31c069a86041cd95d2d8e844a811032a2593ece33ad18a7a8ec12c58fff6074",DREF/"results_referee.json":"13c5f2b7ba1e3568a44cdad98924c65485f23e6eb0b9389e953ded594fe67c3c",DES/"results_anchor_no_rectangle_design.json":"237fd1c51283174f579ce68574a8b30d26fbb9673a76f2ab363ea613927cd274",DES/"canonical_reduced_full_x5_Q.sing":"25b25aac93a336c36c0299c5d6ee9b2a984b5ca0e644170ef235af92f01124f3",QREF/"FINAL_MANIFEST.sha256":"56fab72b563c1ff779d213d341fb82d8a7a3549be39813d0d14d61841735c218",QREF/"results_referee.json":"1f3acb12f7d358c25775fd477df6bbe20bcf151b407e34de1fb8ddbfa87746ca",QRUN/"attempt_exact_q/result.json":"d654c02c299638111c9d5498948165d9f76f8c6a3e79c9d2da35ce0c661ae1b9",QRUN/"attempt_exact_q/watchdog.json":"510f3b4275f1a4a600f9cbbc69f3454ab8acf90fd06158002164cb86628bc4ab",QRUN/"attempt_exact_q/base81_exact_Q.sing":"85f75e489e80a12109a82da607d6d1e21498f825f17eea8486f41078b73b39bc"}
for p,d in pins.items():assert h(p)==d,(p,h(p),d)
def replay(path,base):
 n=0
 for line in path.read_text().splitlines():
  if not line.strip():continue
  d,raw=line.split(None,1);p=Path(raw.strip())
  if not p.is_absolute():p=(ROOT/p) if raw.strip().startswith(("computations/","../")) and raw.strip().startswith("computations/") else base/p
  assert p.is_file() and h(p)==d,p;n+=1
 return n
dn=replay(DREF/"MANIFEST.sha256",DREF);qn=replay(QREF/"FINAL_MANIFEST.sha256",QREF)
design=json.loads((DES/"results_anchor_no_rectangle_design.json").read_text());dref=json.loads((DREF/"results_referee.json").read_text());qref=json.loads((QREF/"results_referee.json").read_text());raw=json.loads((QRUN/"attempt_exact_q/result.json").read_text());wd=json.loads((QRUN/"attempt_exact_q/watchdog.json").read_text())
assert design["status"]=="PASS_EXACT_ONE_REDUCED_REPRESENTATIVE_RANK_DESIGN_NO_SOLVE" and dref["status"]=="PASS_EXACT_DESIGN_AND_HELD_SMALLEST_PILOT_NO_SOLVE"
assert [r["record_index"] for r in design["records"]]==[12,13,14,15]
assert [r["A12_state"] for r in design["records"]]==["present","present","absent","absent"]
sym=design["source_symmetry"];assert sym["literal_classes"]==[{"members":[12,13],"representative":12},{"members":[14,15],"representative":14}]
assert sym["unique_mirror"]==[0,2,1,3,4,5,7,6]
assert all(sym["reduced_site_map_counts"][str(a)][str(b)]==1 for a in range(12,16) for b in range(12,16))
assert "A12 occurs in no supported perfect matching or selected carrier" in sym["A12_distinction"]
assert all("12" not in matching.split("|") for rec in design["records"] for matching in rec["supported_matchings"])
assert design["selected_rank_design"]["canonical_carrier"]["factorization"]=="[A25^T|A26^T]*K*A07^T"
assert design["census"]["word_transport_checks"]==157464 and design["factorization"]["transported_word_checks"]==157464 and design["factorization"]["verified_words"]==6561
canonical=(DES/"canonical_reduced_full_x5_Q.sing").read_text();assert "a12_" not in canonical.lower()
assert design["full_x5_ideal"]["sha256"]==pins[DES/"canonical_reduced_full_x5_Q.sing"] and design["full_x5_ideal"]["variables"]==81 and design["full_x5_ideal"]["generators"]==6561
assert qref["status"]=="PASS_EXACT_Q_UNIT_IDEAL_CANONICAL_BASE81_CHART" and qref["source_sha256"]==pins[QRUN/"attempt_exact_q/base81_exact_Q.sing"]
assert qref["variables"]==81 and qref["generators"]==6561 and qref["groebner_basis_size"]==1 and qref["unit_remainder"]==0
assert raw["status"]=="UNIT_IDEAL_EXACT_Q_BASE81" and raw["returncode"]==0 and raw["breach"] is None and raw["unit_ideal"] is True
assert raw["parsed_stdout"]=={"GROEBNER_SIZE":"1","INPUT_GENERATORS":"6561","INPUT_VARIABLES":"81","STATUS":"UNIT_IDEAL","UNIT_REMAINDER":"0"}
assert wd["status"]=="PASS" and wd["breach"] is None and wd["returncode"]==0 and wd["logs_atomic"] is True
assert raw["automatic_relaunch"] is raw["second_lane"] is False
print(json.dumps({"status":"PASS_CLOSE_EXACTLY_ANCHOR_RECORDS_12_15_OVER_Q","closed_records":[12,13,14,15],"canonical_source_sha256":h(DES/"canonical_reduced_full_x5_Q.sing"),"word_transport_checks":157464,"groebner_basis_size":1,"unit_remainder":0,"design_manifest_entries":dn,"exact_q_manifest_entries":qn},sort_keys=True))
