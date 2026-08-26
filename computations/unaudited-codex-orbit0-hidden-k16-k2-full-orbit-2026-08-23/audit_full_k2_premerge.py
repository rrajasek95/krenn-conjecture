#!/usr/bin/env python3
"""Header/file-size audit for the complete, bounded pre-final-merge state."""
from pathlib import Path
import hashlib, json, struct

HERE = Path(__file__).resolve().parent
U = 400_591_699_200
PAIR = HERE / "hidden_k16_decorated_pair_orbits_full.bin"
SOURCE = HERE / "run_full_hidden_k16_k2_orbits.rs"
RESUME_RESULT = HERE / "results_resume_safety.json"

def hdr(path, magic, recsize):
    with path.open("rb") as f:
        h = f.read(80)
    assert h[:8] == magic and int.from_bytes(h[8:24], "little", signed=True) == U
    assert struct.unpack_from("<H", h, 28)[0] == recsize
    return h

ph = hdr(PAIR, b"H16ORM1\0", 53)
pair_zero = struct.unpack_from("<Q", ph, 40)[0]
pair_count = struct.unpack_from("<Q", ph, 48)[0]
pair_sum = int.from_bytes(ph[64:80], "little", signed=True)
assert PAIR.stat().st_size == 80 + 53 * pair_count

chunks = sorted(HERE.glob("pchild_chunk_*.bin"))
assert len(chunks) == 291
expected = 0
rows = generated = 0
weight_sum = 0
ledger = []
for i, p in enumerate(chunks):
    assert p.name == f"pchild_chunk_{i:04}.bin"
    h = hdr(p, b"H18CHC1\0", 80)
    start, end, count, raw = struct.unpack_from("<QQQQ", h, 32)
    sm = int.from_bytes(h[64:80], "little", signed=True)
    assert start == expected and end > start and raw == 12 * (end - start)
    assert p.stat().st_size == 80 + 80 * count
    expected = end
    rows += count
    generated += raw
    weight_sum += sm
    ledger.append((i, start, end, count, sm))
assert expected == pair_count
assert generated == 12 * pair_count == 1_218_548_676
assert weight_sum == 12 * pair_sum

core = {
    "status": "PASS_COMPLETE_RESUMABLE_PRE_FINAL_MERGE",
    "scope": "all full K2 child chunks complete; final cross-chunk merge not run under original 600s gate",
    "scale": U,
    "global_decorated_pair_orbits": pair_count,
    "global_decorated_pair_exact_zeros": pair_zero,
    "pair_weight_sum_scaled": str(pair_sum),
    "child_chunks": len(chunks),
    "covered_pair_interval": [0, expected],
    "generated_K2_children": generated,
    "sum_chunk_nonzero_rows_before_cross_chunk_merge": rows,
    "sum_chunk_weight_scaled": str(weight_sum),
    "expected_total_weight_scaled": str(12 * pair_sum),
    "first_chunk": ledger[0][1:4],
    "last_chunk": ledger[-1][1:4],
    "record_schema": "row24,weight_i128,witness_pair_row24,p2,tail2,pair_uses_u64,orbit_u16,stabilizer_u16,pivotable,m2",
    "resume_source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "resume_safety_result_sha256": hashlib.sha256(RESUME_RESULT.read_bytes()).hexdigest(),
    "pair_content_validation": "full ordered record stream and weight/stabilizer replay",
    "child_content_validation": "atomic-generation provenance plus full header/schema/interval/size audit; no stored per-chunk content digests, and final merge has not yet streamed all child records",
}
core["logical_sha256"] = hashlib.sha256(json.dumps(core, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
out = HERE / "results_full_k2_premerge.json"
out.write_text(json.dumps(core, indent=2, sort_keys=True) + "\n")
print(json.dumps(core, indent=2, sort_keys=True))
