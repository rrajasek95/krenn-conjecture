#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];PARENT=ROOT/"computations/unaudited-codex-n8-x5-rep2-group16-a57V0-a04_11-residual-split-design-2026-08-26";SOURCE=PARENT/"sources/rep2_group16_Dt1_a04_11_D1_Q_design.sing";sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r=json.loads((HERE/"results_design.json").read_text())
assert sha(PARENT/"MANIFEST.sha256")==r["parent"]["manifest_sha256"]=="8c4b3e4c82076e7cd8b61cd40e86eaa8a8ea3bd10ace7c1f8ac7f8c4ce52b835" and sha(SOURCE)==r["parent"]["source_sha256"]=="2998353c04d390b7dadae6a2bb364d5ad9866b1911d39dfb9f039b40cef70bab"
digests=["90237bf6776ef753aa0659ba4da773c7f1c6bd770a7f1f94c39dd3295b845cef","4d0288a47044307c6faed2e7a10aebd341525cf466b8b7f4101841a1b87642e9","e8371b7db88b1c21a3d3cbd231be9d01f8b54deea0f55a59a89f35f4845611a3","9b0afa9524d7ab54f682aa07a5b0034fa06c448da165726200f90ec29bc81dc2","abc266771f064bca22c524ae7159795c0c0ede3f5999a82042413f14fcdbb179","4018891047763238d0ddc98b426d36e11638e5275fae9ee2ff10caf40f61138a","a69591f4719e2477671ef15e5dffd6b198fb61d7a5742c260f9b9572b7369b5f","fcf3c7eb4cfe90372b11666b9cfce765f576068b504f3c0ec3ade4df27cff53f","c2a15f2816321528aadef2ad0b32a6f13c83ce0e04a2ace535bbad4239237954","0b705d969c47d5d600711ecdb7d88edaeed145c5b4f01afc10b3412ac68d5af6"]
for step,digest in zip(r["ledger"],digests,strict=True):assert sha(HERE/step["path"])==step["after"]["sha256"]==digest
probe=HERE/"intermediate/torus_probe_11/results_design.json";assert sha(probe)=="8c03652355096adb179644360d8e9d5d92f0c5fd29ce1faf1897f21c9871a1aa"
for name,digest in [("held_D1_a04_12.sing","e6a983ae8e50e30def6ca8b608098470052602ff96e713ad54036b86a2624b80"),("held_V0_a04_12.sing","a8ef7d7ea39cda9bd2d382f0a2ddc91b2355d511124a8d7dd7ce72c7a63bd768")]:
 p=HERE/"sources"/name;assert sha(p)==digest and "slimgb" not in p.read_text()
subprocess.run([sys.executable,str(HERE/"test_design.py")],cwd=HERE,env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"},capture_output=True,text=True,check=True,timeout=20);h=json.loads((HERE/"results_hostiles.json").read_text());assert h["status"]=="PASS" and h["hostile_count"]==12
assert not list(HERE.glob("*.tmp")) and not list(HERE.rglob("__pycache__"));print(json.dumps({"status":"PASS_EXACT_A04_12_TWO_BRANCH_HELD_REPLAY","parent_reductions":10,"branches":[[48,5994,140394],[48,5913,126316]],"global_nonempty_leaves":3,"solver_runs":0},sort_keys=True))
