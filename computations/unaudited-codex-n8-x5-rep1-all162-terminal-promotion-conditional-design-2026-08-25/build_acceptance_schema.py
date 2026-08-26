#!/usr/bin/env python3
"""Build the future terminal promotion acceptance schema; no acceptance instance."""
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
hex64={'type':'string','pattern':'^[0-9a-f]{64}$'}
properties={'schema':{'const':'KRENN_X5_REP1_ALL162_TERMINAL_PROMOTION_ACCEPTANCE_V1'},'status':{'const':'PASS_PROMOTE_REP1_ALL_162_CANONICAL_GROUPS_ONLY'},'held_design_manifest_sha256':hex64,'promotion_design_sha256':{'const':sha(HERE/'results_terminal_promotion_design.json')},'future_dependencies_sha256':{'const':sha(HERE/'future_dependencies.json')},'groups38_87_manifest_sha256':hex64,'groups38_87_result_sha256':hex64,'groups88_137_manifest_sha256':hex64,'groups88_137_result_sha256':hex64,'groups138_161_manifest_sha256':hex64,'groups138_161_result_sha256':hex64,'closed_group_ids':{'const':list(range(162))},'raw_charts_closed':{'const':972},'canonical_groups_closed':{'const':162},'y_groups_closed':{'const':81},'z_groups_closed':{'const':81},'representative':{'const':'rep1'},'cross_representative_transport':{'const':False},'full_conjecture':{'const':False}}
schema={'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','additionalProperties':False,'required':list(properties),'properties':properties};tmp=HERE/'terminal_promotion_acceptance.schema.json.tmp';tmp.write_text(json.dumps(schema,indent=2,sort_keys=True)+'\n');os.replace(tmp,HERE/'terminal_promotion_acceptance.schema.json');print(sha(HERE/'terminal_promotion_acceptance.schema.json'))
