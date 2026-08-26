#!/usr/bin/env python3
import hashlib,os
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
files=[HERE/name for name in ('REPORT.md','build_plan.py','build_sources.py','future_dependencies.json','held_schedule.json','independent_referee_acceptance.schema.json','launch_clearance.schema.json','normalize_dependencies.py','results_hostile_tests.json','run_groups76_125.py','seal_manifest.py','source_ledger.json','test_dependencies.py','validate.py')]+sorted((HERE/'sources').glob('*.sing'))
assert len(files)==64 and all(path.is_file() for path in files);text=''.join(f'{sha(path)}  {path.relative_to(HERE)}\n' for path in files);tmp=HERE/'MANIFEST.sha256.tmp';tmp.write_text(text);os.replace(tmp,HERE/'MANIFEST.sha256');print(sha(HERE/'MANIFEST.sha256'))
