#!/usr/bin/env python3
"""Build strict future all-162 rep4 promotion acceptance schema; no instance."""
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
hex64={'type':'string','pattern':'^[0-9a-f]{64}$'};properties={'schema':{'const':'KRENN_X5_REP4_ALL162_TERMINAL_PROMOTION_ACCEPTANCE_V1'},'status':{'const':'PASS_PROMOTE_REP4_ALL_162_CANONICAL_GROUPS_ONLY'},'held_design_manifest_sha256':hex64,'promotion_design_sha256':{'const':sha(HERE/'results_terminal_promotion_design.json')},'future_dependencies_sha256':{'const':sha(HERE/'future_dependencies.json')},'group0_first_referee_manifest_sha256':{'const':'a8280c98344eb62f6df89ffec125e6cdba33a7dae63f47061c71114f7aabe805'},'group0_second_referee_manifest_sha256':{'const':'b2a543e59df1edf32df414f44938b418e35ea4ed258354642aff3d2b45e522b4'}}
for stem in ('groups1_25','groups26_75','groups76_125','groups126_161'):properties[stem+'_manifest_sha256']=hex64;properties[stem+'_result_sha256']=hex64
properties.update({'closed_group_ids':{'const':list(range(162))},'raw_charts_closed':{'const':972},'canonical_groups_closed':{'const':162},'y_groups_closed':{'const':81},'z_groups_closed':{'const':81},'representative':{'const':'rep4'},'cross_representative_transport':{'const':False},'full_conjecture':{'const':False}});schema={'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','additionalProperties':False,'required':list(properties),'properties':properties};tmp=HERE/'terminal_promotion_acceptance.schema.json.tmp';tmp.write_text(json.dumps(schema,indent=2,sort_keys=True)+'\n');os.replace(tmp,HERE/'terminal_promotion_acceptance.schema.json');print(sha(HERE/'terminal_promotion_acceptance.schema.json'))
