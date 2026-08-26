#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
PARENT=ROOT/"computations/unaudited-codex-n8-x5-rep2-group16-a57V0-a04_11V0-monic-next-cover-design-2026-08-26"
SOURCE=PARENT/"sources/rep2_group16_Dt1_a14_01_V0_Q_design.sing"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r=json.loads((HERE/"results_design.json").read_text())
assert sha(PARENT/"MANIFEST.sha256")==r["parent"]["manifest_sha256"]=="0c5b330359676432e3fddbff7451fb6f9fe28a8f16d20ab42f55128196194a2a"
assert sha(SOURCE)==r["parent"]["source_sha256"]=="53cebaf3d4a6b85d9058374423e91bd02da0c4a6e8c5b70d09c661c27b297535"
expected=[
("108d5ba7bafaffe8a0d87be453051683ac477f7106506c2db827dff0fb8ffb2d",56,5967,109953),
("507c4eebaea7b2c610cc866621987122c2b17a8ea02e3bd3d04c6fc94ee5673e",55,5919,108360),
("5eb412cd67af5779ed0d44a25c88530c752cf67058c517a567fa3ed6650264f9",54,5918,109853),
("17c021d833589903c587893e8dacd9b5f24afd6a1ca16d6bdd60c614e35c1d17",53,5917,111346),
("73db8faf284c2202440a333f168d86525b2a1dda5767cc72f9bc8317e7447c57",52,5916,114419),
("25c6dbee1f87e05c1c43f12fd0c953342fa004cceed5e4d1d34880dd93e4d9e4",51,5915,117355),
("8106402716735987c2c939fcf4e99a164ca4a9c8229741e6ea897f5d818c389b",50,5914,120291),
("cd9fbe297c20607b836c031740a5374e52215cc12f7b1e68f495a550eff4b654",49,5913,126316),
("697dfff656a2257d41d2d5e384ac2e39ad244390e23c44468a63bf5a96091f8b",48,5913,126316),
("e54aeb2eb7b28b029b3a177c7c63ce6c4b34ac7f445b124414b3f3ab89b775ce",47,5904,118901),
("d2fa03ba377d019d8fcfe20a8cb61894afd32f3e0cfe9d2f5db316d2d83f8df0",46,1,1),]
for step,(digest,n,g,t) in zip(r["ledger"],expected,strict=True):
    path=HERE/step["path"];assert sha(path)==step["after"]["sha256"]==digest
    assert [step["after"][k] for k in ("variables","generators","terms")]==[n,g,t]
    text=path.read_text();assert "slimgb" not in text and "reduce(" not in text
probe=HERE/"intermediate/torus_probe_09/results_design.json";p=json.loads(probe.read_text())
assert p["status"]=="PASS_EXACT_MAXIMAL_GLOBAL_UNIT_TORUS_GAUGE" and p["grading"]["rank"]==45 and p["grading"]["nullity"]==4
assert p["cover"]["maximal_primitive_global_gauge_coordinates"]==["a17_01"]
assert sha(probe)=="94238ce6b7bb5723c4834d91072d448621985c725ca071f3e7ccb89c2a394bd7"
assert (HERE/r["final"]["path"]).read_text().split("ideal I=",1)[1].split(";\nprint",1)[0]=="1"
subprocess.run([sys.executable,str(HERE/"test_design.py")],cwd=HERE,env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"},capture_output=True,text=True,check=True,timeout=20)
h=json.loads((HERE/"results_hostiles.json").read_text());assert h["status"]=="PASS" and h["hostile_count"]==17 and h["solver_runs"]==0
assert not list(HERE.glob("*.tmp")) and not list(HERE.rglob("__pycache__"))
print(json.dumps({"status":"PASS_EXACT_STRICT_SURVIVOR_STRUCTURAL_UNIT_REPLAY","steps":11,"final":[46,1,1],"remaining_global_leaves":2,"hostiles":17,"solver_runs":0},sort_keys=True))
