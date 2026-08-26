#!/usr/bin/env python3
"""Mechanically specialize final plan/validation/report/seal from sealed rep2 package."""
import hashlib,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];BASE=ROOT/'computations/unaudited-codex-n8-x5-rep2-groups126-161-exact-q-conditional-held-2026-08-26';BASE_MANIFEST='83c87103e2414b48d37724ce803c747ee0d2c9a9f757353c172bb17226477147'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
assert sha(BASE/'MANIFEST.sha256')==BASE_MANIFEST
replacements=[('REP2','REP4'),('rep2','rep4'),('c34b3616bef36d49c63904e676c540208a24dd2057eb176153ad03034db0b8a6','fa301fd4d1e61626781cedd3ecb362189671b042c9cba8cfbe68977bb79ceb38'),('ab8198b3c9745368e51f1f5c481d81b62823f7255d046a80e3d94a7c2cad0e9c','18b7cae58e965187bcbb97ef7a319aacd92fccb6be4010d9630caad83ef77e75'),('b784729f817f2986fac597009b65698e62fc8a0ba944447c21b95cd5dde29ff5','fc44d47caef2915dc8cf7dc384d544e8c858e4be8de372b08d01a30abb3b90eb'),('07281312d1b227c0a629b917485b39c04a976df9bb4fbbf17c2bd92459743407','959ab7cfa85ddf23f328ae03edeaefabc0a775ede98b4768953b46c91fe0022a'),('6feb616a9ad037934eed7dc8b21b44745a3cd1ceeb734424edb85d434466f497','b15cdacc3ff88d14b43760f430bd9ba327fe332d1d34a99d1b5ffb989dcfcc90'),('66529596','65177850'),('66,529,596','65,177,850'),('5ee661f3','12773aac'),('provenance-replay v2 groups 76–125','groups 76–125')]
for name in ('build_plan.py','validate.py','REPORT.md','seal_manifest.py'):
 text=(BASE/name).read_text()
 for old,new in replacements:text=text.replace(old,new)
 if name=='seal_manifest.py':
  old="local=['REPORT.md','build_contract.py','build_plan.py','build_runner.py','build_sources.py','dependency_verifier.py'";new="local=['REPORT.md','bootstrap_remaining.py','bootstrap_symbolic_contract.py','build_contract.py','build_plan.py','build_runner.py','build_sources.py','dependency_verifier.py'";assert text.count(old)==1;text=text.replace(old,new).replace("assert len(local)==53","assert len(local)==55").replace("len(entries)==58","len(entries)==60").replace("'lines':58","'lines':60")
 tmp=HERE/(name+'.tmp');tmp.write_text(text);os.replace(tmp,HERE/name)
print({'status':'PASS_SPECIALIZED_FINAL_PACKAGE_FILES_ZERO_RUN','hashes':{name:sha(HERE/name) for name in ('build_plan.py','validate.py','REPORT.md','seal_manifest.py')}})
