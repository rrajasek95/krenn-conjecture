#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r=json.loads((H/'results_terminal_promotion.json').read_text())
assert r['status']=='PASS_ALL_RANKS_CLOSED_FOR_ALL_12_RECTANGLE_RECORDS' and r['records']==list(range(12)) and r['rank_partition']==[0,1,2,3]
assert r['A12_states']['both_closed'] and r['coverage']=={'records':12,'ranks_per_record':4,'rank1_raw_chart_cases':324,'rank2_raw_chart_cases':324,'rank0_cases':12,'rank3_cases':12,'total_stratified_record_chart_cases':672,'missing_ranks':[],'missing_rank1_charts':0,'missing_rank2_charts':0}
assert r['scope']=={'rectangle_records_0_through_11_closed':True,'records_12_through_15_excluded':True,'excluded_records':[12,13,14,15],'full_conjecture':False,'new_solver_runs':0}
print(json.dumps({'status':'PASS','result_sha256':h(H/'results_terminal_promotion.json')},sort_keys=True))
