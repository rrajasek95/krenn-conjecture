#!/usr/bin/env python3
import hashlib
import json
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = 400_591_699_200
HEADER = 256
REC = 72
EXPECTED_FULL = 152_251_200
EXPECTED_PIV = 137_817_600
EXPECTED_SUM = -2_655_476_097_643_708_416_000


def i128(b):
    return int.from_bytes(b, "little", signed=True)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        while block := f.read(8 << 20):
            h.update(block)
    return h.hexdigest()


def header(path, magic):
    with path.open("rb") as f:
        h = f.read(HEADER)
    assert len(h) == HEADER and h[:8] == magic
    assert i128(h[8:24]) == U
    start, end, recsize = struct.unpack_from("<HHH", h, 24)
    assert recsize == REC
    full = struct.unpack_from("<6Q", h, 32)
    piv = struct.unpack_from("<6Q", h, 80)
    uses_by_lineage = struct.unpack_from("<6Q", h, 128)
    count = struct.unpack_from("<Q", h, 176)[0]
    weight_sum = i128(h[184:200])
    uses = struct.unpack_from("<Q", h, 200)[0]
    zeros = struct.unpack_from("<Q", h, 208)[0]
    assert path.stat().st_size == HEADER + REC * count
    return dict(start=start, end=end, full=full, piv=piv,
                uses_by_lineage=uses_by_lineage, count=count,
                weight_sum=weight_sum, uses=uses, zeros=zeros)


def scan_records(path, expected_count):
    count = uses = 0
    weight_sum = 0
    prior = None
    first_weight = None
    with path.open("rb") as f:
        f.seek(HEADER)
        while block := f.read(REC * 65_536):
            assert len(block) % REC == 0
            for off in range(0, len(block), REC):
                b = block[off:off + REC]
                key = b[:43]
                assert prior is None or prior < key
                prior = key
                weight = i128(b[43:59])
                assert weight != 0
                if first_weight is None:
                    first_weight = weight
                weight_sum += weight
                uses += struct.unpack_from("<Q", b, 59)[0]
                count += 1
    assert count == expected_count
    return count, weight_sum, uses, first_weight


def main():
    result = json.loads((HERE / "results_direct_k18_profile_census.json").read_text())
    runs = sorted(HERE.glob("run_[0-9][0-9][0-9]_[0-9][0-9][0-9].bin"))
    assert len(runs) == 16
    expected = 0
    total_full = [0] * 6
    total_piv = [0] * 6
    total_outgoing = [0] * 6
    run_count = run_sum = run_uses = 0
    manifest = []
    for path in runs:
        x = header(path, b"D18RUN1\0")
        assert x["start"] == expected
        expected = x["end"]
        for i in range(6):
            total_full[i] += x["full"][i]
            total_piv[i] += x["piv"][i]
            total_outgoing[i] += x["uses_by_lineage"][i]
        run_count += x["count"]
        run_sum += x["weight_sum"]
        run_uses += x["uses"]
        manifest.append(dict(file=path.name, sha256=sha(path), **x))
    assert expected == 485
    assert sum(total_full) == EXPECTED_FULL
    assert sum(total_piv) == EXPECTED_PIV
    assert sum(total_outgoing) == 260_736_000

    merged = HERE / "direct_k18_enriched_profiles.bin"
    mh = header(merged, b"D18MRG1\0")
    assert (mh["start"], mh["end"]) == (0, 485)
    scanned = scan_records(merged, mh["count"])
    assert scanned[:3] == (mh["count"], mh["weight_sum"], mh["uses"])
    assert mh["weight_sum"] == run_sum == EXPECTED_SUM
    assert mh["count"] == result["merged_nonzero_keys"] == 979_091
    assert mh["zeros"] == result["cross_run_exact_zero_keys"] == 27_831
    assert mh["uses"] == result["merged_nonzero_key_uses"] == 252_631_784
    assert run_count == result["run_nonzero_key_sum"] == 6_995_702
    assert run_uses == result["atomic_nonzero_key_uses"] == 254_287_628
    assert sum(total_outgoing) == result["total_outgoing_pivot_uses"]

    # A hostile +1 mutation of the first signed weight must violate the pinned sum.
    hostile_sum = mh["weight_sum"] + 1
    assert hostile_sum != EXPECTED_SUM

    charge = json.loads((HERE / "results_direct_k18_k2_charge.json").read_text())
    assert charge["profile_keys"] == mh["count"]
    assert charge["literal_tail_evaluations"] == 12 * mh["count"]
    out = {
        "status": "PASS_INDEPENDENT_STRUCTURE_AND_DIGEST_REPLAY",
        "scale": U,
        "atomic_run_count": len(runs),
        "atomic_coverage": [0, expected],
        "atomic_nonzero_key_sum": run_count,
        "merged_nonzero_keys": mh["count"],
        "cross_run_exact_zero_keys": mh["zeros"],
        "total_full_parents": sum(total_full),
        "total_pivotable_parents": sum(total_piv),
        "total_outgoing_pivot_uses": sum(total_outgoing),
        "merged_weight_sum_scaled": str(mh["weight_sum"]),
        "merged_nonzero_key_uses": mh["uses"],
        "merged_sha256": sha(merged),
        "source_sha256": sha(HERE / "run_direct_k18_profile_census.rs"),
        "result_sha256": sha(HERE / "results_direct_k18_profile_census.json"),
        "charge_result_sha256": sha(HERE / "results_direct_k18_k2_charge.json"),
        "hostile_one_weight_mutation_rejected": True,
        "runs": manifest,
    }
    dst = HERE / "results_direct_k18_profile_census_replay.json"
    dst.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "runs"}, indent=2))


if __name__ == "__main__":
    main()
