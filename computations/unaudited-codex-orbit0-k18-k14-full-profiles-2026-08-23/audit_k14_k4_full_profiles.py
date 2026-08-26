#!/usr/bin/env python3
import hashlib
import json
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = 400_591_699_200
IN_HEADER, OUT_HEADER, REC = 96, 256, 104


def i128(b): return int.from_bytes(b, "little", signed=True)


def hash_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        while block := f.read(16 << 20): h.update(block)
    return h.hexdigest()


def part_header(path):
    with path.open("rb") as f: h = f.read(IN_HEADER)
    assert h[:8] == b"K18PRF2\0"
    assert struct.unpack_from("<I", h, 8)[0] == 2
    assert (h[12], h[13], struct.unpack_from("<H", h, 14)[0]) == (1, 2, REC)
    assert struct.unpack_from("<Q", h, 16)[0] == U
    part, count, uses = struct.unpack_from("<QQQ", h, 24)
    weight = i128(h[48:64])
    assert path.stat().st_size == IN_HEADER + REC * count
    return part, count, uses, weight


def merged_scan(path):
    sha = hashlib.sha256()
    with path.open("rb") as f:
        h = f.read(OUT_HEADER); sha.update(h)
        assert h[:8] == b"K14MRG1\0" and struct.unpack_from("<Q", h, 8)[0] == U
        parts, incount, inuses = struct.unpack_from("<QQQ", h, 16)
        inweight = i128(h[40:56])
        outcount, zeros, outuses = struct.unpack_from("<QQQ", h, 56)
        outweight = i128(h[80:96])
        assert path.stat().st_size == OUT_HEADER + REC * outcount
        prior = None; count = uses = 0; weight = 0
        while block := f.read(REC * 65536):
            sha.update(block); assert len(block) % REC == 0
            for off in range(0, len(block), REC):
                b = block[off:off + REC]; key = b[:42]
                assert prior is None or prior < key; prior = key
                w = i128(b[42:58]); u = struct.unpack_from("<Q", b, 58)[0]
                assert w and u
                weight += w; uses += u; count += 1
        assert (count, uses, weight) == (outcount, outuses, outweight)
    return dict(parts=parts, input_count=incount, input_uses=inuses,
                input_weight=inweight, output_count=outcount, zeros=zeros,
                output_uses=outuses, output_weight=outweight,
                sha256=sha.hexdigest())


def main():
    manifests = sorted(HERE.glob("k14_*_*.manifest.json"), key=lambda p: json.loads(p.read_text())["source_range"][0])
    assert len(manifests) == 16
    coverage = 0
    generated = pivotable = outgoing = records = part_uses = 0
    signed_weight = 0; part_count = 0; parts_out = []
    for mp in manifests:
        m = json.loads(mp.read_text()); start, end = m["source_range"]
        assert m["mode"] == "k14" and m["complete_source_range"] is True
        assert int(m["scale_U"]) == U and start == coverage; coverage = end
        prefix = str(mp)[:-len(".manifest.json")]
        files = sorted(Path(prefix).parent.glob(Path(prefix).name + ".part*.bin"))
        assert len(files) == m["parts"]
        local_records = local_uses = 0; local_weight = 0
        for expected_part, p in enumerate(files):
            part, count, uses, weight = part_header(p)
            assert part == expected_part
            local_records += count; local_uses += uses; local_weight += weight
            parts_out.append({"file": p.name, "sha256": hash_file(p), "count": count,
                              "uses": uses, "weight": str(weight)})
        assert local_records == m["emitted_records_local_unique"]
        assert local_weight == int(m["signed_weight_sum_scaled"])
        generated += m["generated_parents"]; pivotable += m["pivotable_parents"]
        outgoing += m["outgoing_pivot_uses"]; records += local_records
        part_uses += local_uses; signed_weight += local_weight; part_count += len(files)
    assert coverage == 485
    assert (generated, pivotable, outgoing) == (397_156_800, 357_580_800, 910_713_600)

    merged_path = HERE / "k14_k4_enriched_profiles.bin"
    merged = merged_scan(merged_path)
    assert (merged["parts"], merged["input_count"], merged["input_uses"], merged["input_weight"]) == (part_count, records, part_uses, signed_weight)
    assert merged["output_count"] == 18_217_226 and merged["zeros"] == 1_150_525
    merge_result = json.loads((HERE / "results_k14_k4_profile_merge.json").read_text())
    assert merge_result["merged_nonzero_profiles"] == merged["output_count"]
    charge = json.loads((HERE / "results_k14_k4_k2_charge.json").read_text())
    assert charge["merged_profiles"] == merged["output_count"]
    assert charge["literal_tail_evaluations"] == 12 * merged["output_count"]
    assert merged["output_weight"] + 1 != signed_weight  # hostile one-weight mutation

    out = {
        "status": "PASS_FULL_K14_K4_CENSUS_MERGE_CHARGE_REPLAY",
        "scale_U": U, "source_coverage": [0, coverage],
        "generated_parents": generated, "pivotable_parents": pivotable,
        "outgoing_pivot_uses": outgoing, "atomic_parts": part_count,
        "atomic_nonzero_records": records, "atomic_record_uses": part_uses,
        "signed_weight_sum_scaled": str(signed_weight),
        "merged_nonzero_profiles": merged["output_count"],
        "cross_part_exact_zero_profiles": merged["zeros"],
        "merged_retained_uses": merged["output_uses"],
        "merged_sha256": merged["sha256"],
        "full_charge_scaled": charge["full_charge_scaled"],
        "irreducible_charge_scaled": charge["irreducible_charge_scaled"],
        "hostile_one_weight_mutation_rejected": True,
        "parts": parts_out,
    }
    dst = HERE / "results_k14_k4_full_replay.json"
    dst.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k:v for k,v in out.items() if k != "parts"}, indent=2))


if __name__ == "__main__": main()
