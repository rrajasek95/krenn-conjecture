#!/usr/bin/env python3
"""Byte-accounted mechanical specialization of the sealed rep2 final contract to rep4."""
import hashlib,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];BASE=ROOT/'computations/unaudited-codex-n8-x5-rep2-groups126-161-exact-q-conditional-held-2026-08-26';BASE_MANIFEST='83c87103e2414b48d37724ce803c747ee0d2c9a9f757353c172bb17226477147'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
assert sha(BASE/'MANIFEST.sha256')==BASE_MANIFEST
common=[('REP2','REP4'),('rep2','rep4'),('ab8198b3c9745368e51f1f5c481d81b62823f7255d046a80e3d94a7c2cad0e9c','18b7cae58e965187bcbb97ef7a319aacd92fccb6be4010d9630caad83ef77e75'),('groups76_125_v2','groups76_125'),('groups_closed_by_third_v2','groups_closed_by_third')]
for source_name,target_name in [('dependency_verifier.py','dependency_verifier.py'),('normalize_dependencies.py','normalize_dependencies.py'),('test_dependencies.py','test_dependencies.py')]:
 text=(BASE/source_name).read_text()
 for old,new in common:text=text.replace(old,new)
 tmp=HERE/(target_name+'.tmp');tmp.write_text(text);os.replace(tmp,HERE/target_name)
print({'status':'PASS_SPECIALIZED_THREE_CONTRACT_FILES_ZERO_RUN','base_manifest':BASE_MANIFEST,'hashes':{name:sha(HERE/name) for name in ('dependency_verifier.py','normalize_dependencies.py','test_dependencies.py')}})
