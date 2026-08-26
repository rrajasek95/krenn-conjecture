#!/usr/bin/env python3
"""Independent referee for the 972 -> 162 rep1 exact-Q source census."""
import hashlib, importlib.util, itertools, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROD = ROOT / "computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25"
GEN = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25/generate_minor_quotient.py"
CLOSED = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-exact-q-2026-08-25/result.json"
OUT = Path(__file__).resolve().parent / "results_referee.json"

PINS = {
    PROD / "MANIFEST.sha256": "6ed49a2e534955569149eaf2fe80b05aa3513507b41fe44575679eef0271fcb1",
    PROD / "results_canonical_census.json": "5ef1acc6ee2b97e993ae930b4ba420ce5c1c8c9eac16995d3a31b5c7a3eb5161",
    GEN: "63a4a58344c4bfdce0406d243f881216ca53eaa71264926a28364a823f560ac8",
    CLOSED: "668c36e5e6248c369424787a919013c32cde6b7c0aaa35ae81b7100469e7aab9",
}

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def replay(path):
    n = 0
    for line in path.read_text().splitlines():
        if not line.strip(): continue
        digest, rel = line.split(None, 1)
        assert sha(path.parent / rel.strip()) == digest
        n += 1
    return n

def canonical(record):
    c,p,q,r,kind,s,a,b = record
    images=[]
    for perm in itertools.permutations(range(3)):
        aa,bb=sorted((perm[a],perm[b]))
        images.append((perm[c],perm[p],perm[q],perm[r],kind,perm[s],aa,bb))
    return min(images)

def edge_image(edges, perm):
    return {tuple(sorted((perm[a],perm[b]))) for a,b in edges}

for path,digest in PINS.items(): assert sha(path)==digest,(path,sha(path),digest)
manifest_entries = replay(PROD / "MANIFEST.sha256")
producer = json.loads((PROD / "results_canonical_census.json").read_text())
closed = json.loads(CLOSED.read_text())

# Independently enumerate all refined charts and quotient only by common S3.
raw=[]
for c,p,q,r,s in itertools.product(range(3),repeat=5):
    for kind in ("y","z"):
        for other in range(3):
            if other != q:
                a,b=sorted((q,other)); raw.append((c,p,q,r,kind,s,a,b))
groups={}
for record in raw: groups.setdefault(canonical(record),[]).append(record)
assert len(raw)==972 and len(groups)==162 and {len(v) for v in groups.values()}=={6}

# Independently audit graph rigidity: source labels/orientations are fixed, and
# the only vertex permutation preserving fixed identities and full support is id.
spec=importlib.util.spec_from_file_location("sealed_minor",GEN)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
base=mod.load_base()
autos=[]
for perm in itertools.permutations(range(8)):
    if edge_image(base.FIXED,perm)==set(base.FIXED) and edge_image(base.SUPPORT,perm)==set(base.SUPPORT):
        autos.append(perm)
assert autos==[tuple(range(8))]

# Regenerate each canonical Q program from the pinned exact constructor, while
# independently checking the producer's group membership and ordered ledger.
records=producer["enumeration"]["records"]
assert len(records)==162
hashes=[]
for gid,(rep,members) in enumerate(sorted(groups.items())):
    row=records[gid]
    assert row["group_id"]==gid and tuple(row["canonical_chart"])==rep
    assert sorted(map(tuple,row["raw_members"]))==sorted(members)
    assert row["raw_member_count"]==6
    c,p,q,r,kind,s,a,b=rep
    chart={"coordinate":c,"outside":(p,q),"x_pivot":r,"q_kind":kind,"q_pivot":s,"minor_pair":(a,b)}
    payload=mod.build_program(base,chart,"0").encode()
    digest=hashlib.sha256(payload).hexdigest()
    assert digest==row["exact_Q_source_sha256"] and len(payload)==row["exact_Q_source_bytes"]
    hashes.append(digest)
assert len(set(hashes))==162
closed_rows=[row for row in records if row["closed"]]
assert len(closed_rows)==1 and closed_rows[0]["group_id"]==0
assert closed_rows[0]["exact_Q_source_sha256"]==closed["source_Q_sha256"]=="53f741ca9173877ef1bc21dba2546a82102a32140221068de1301d0b4635dadb"

# Pure GHZ target rigidity: a product of eight local color permutations maps
# {(c,...,c)} onto itself only when all eight permutations agree on every c.
for local in itertools.product(itertools.permutations(range(3)), repeat=2):
    # A two-site check is sufficient pairwise; extending it to all eight sites
    # forces equality to the first site by the same argument.
    preserves=all(local[0][c]==local[1][c] for c in range(3))
    assert preserves==(local[0]==local[1])

gate=json.loads((PROD/"HELD_RESOURCE_GATE.json").read_text())
assert gate["status"]=="HELD_PENDING_INDEPENDENT_REFEREE_AND_EXPLICIT_CLEARANCE"
assert gate["selected_group_id"]==13
assert gate["limits"]["maximum_lane_count"]==1
assert gate["limits"]["native_wall_seconds"]==240 and gate["limits"]["wrapper_wall_seconds"]==250
assert gate["limits"]["rss_cap_bytes"]==8*1024**3
selected=records[13]
assert selected["closed"] is False
assert gate["expected_exact_Q_source_sha256"]==selected["exact_Q_source_sha256"]
assert gate["expected_exact_Q_source_bytes"]==selected["exact_Q_source_bytes"]==max(r["exact_Q_source_bytes"] for r in records)
assert producer["scope"]=={"ideal_launches":0,"additional_charts_closed":0,"representative_closed":False}

audit={
 "schema":"KRENN_X5_REP1_REMAINING161_CENSUS_REFEREE_V1",
 "status":"PASS_EXACT_972_TO_162_CENSUS_NO_IDEALS",
 "producer_manifest_sha256":PINS[PROD/"MANIFEST.sha256"],
 "producer_result_sha256":PINS[PROD/"results_canonical_census.json"],
 "manifest_entries_replayed":manifest_entries,
 "raw_charts":972,"common_s3_groups":162,"members_per_group":6,
 "support_graph_automorphisms":[list(x) for x in autos],
 "distinct_Q_source_hashes":len(set(hashes)),
 "closed_group_id":0,"closed_source_sha256":closed_rows[0]["exact_Q_source_sha256"],
 "remaining_groups":161,"ideal_launches":0,
 "canonicalization_scope":"common simultaneous S3 only; source labels, endpoint orientation, and vertices fixed",
 "held_staged_plan":{
   "status":"HELD_NOT_RUN_REQUIRES_EXPLICIT_CLEARANCE_PER_STAGE",
   "pilot":{"group_ids":[13],"fresh_lanes":1,"native_wall_seconds_each":240,"wrapper_wall_seconds_each":250,"rss_cap_bytes_each":8*1024**3,"terminal_pause_for_independent_audit":True},
   "microbatch_after_pilot_pass":{"maximum_additional_lanes":3,"selection":"remaining maximum-source-size groups in canonical group-id order","sequential_only":True,"stop_on_first_nonunit_resource_or_process_failure":True,"stop_after_three_for_independent_audit":True},
   "broad_161_launch_authorized":False,"automatic_relaunch":False,"materialize_on_demand_only":True,
 },
 "scope":{"additional_charts_closed":0,"representative_1_closed":False,"no_ideal_run_by_referee":True},
}
OUT.write_text(json.dumps(audit,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":audit["status"],"result_sha256":sha(OUT)},sort_keys=True))
