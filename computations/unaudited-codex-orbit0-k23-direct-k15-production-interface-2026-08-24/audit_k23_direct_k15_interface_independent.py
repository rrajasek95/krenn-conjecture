#!/usr/bin/env python3
"""Independent fail-closed audit of the held direct-K15 K23 production interface."""

import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GATE = ROOT / "computations/unaudited-codex-orbit0-k23-direct-k15-four-sink-2026-08-24"
PINS = {
    HERE / "MANIFEST.sha256": "3d479518035f5c4158e28f7f2d729e4dd4ebb2b74de5ed7540592dfc46c0075c",
    HERE / "k23_direct_k15_production_contract.json": "5bdf62a48b12835c275e8f6f3c693eb2cb6d6690a1b76608db7f0fe08c4461cc",
    HERE / "k23_direct_k15_contract.py": "e09b89cbbe81fccb7eb11f1c08641678c1838ea4c4a70a460464f9fa899920a1",
    HERE / "merge_k23_direct_k15_shards.py": "24c9af915dbb57b346b349c04c2edc935434defd5ee54799a91e2ebbfd75f09f",
    HERE / "validate_k23_direct_k15_shard.py": "2558b0bdc88adc78adae76ac8f0e3a0af1e6d1ecd9f9da941eed689ab56a3129",
    HERE / "validate_k23_direct_k15_literal_referee.py": "8ddb8a8d7175753a42645eebb74aed15ddaf21545be121c7df388b75df9b01db",
    GATE / "run_k23_direct_k15_four_sink.rs": "c3ea65b5ac1221e1b0020e2f0a9753bd774826059ae16e24c05cd4f6f5706e8c",
    GATE / "run_k23_direct_k15_four_sink": "a6bc9f1f1b217a4cfc8dc662ea1358e4c3ac012f40c49e6c07cf05b1e52faa04",
    GATE / "referee_k23_direct_k15_literal.rs": "0678d51c89228109f62a141d8e9f39637686124101155df0b10842e733e5e6ca",
    GATE / "referee_k23_direct_k15_literal": "b53f0733f4e549633b072d4df688b20c90feccfefea6d2d03311a7deb296b5c4",
    GATE / "k23_direct_k15_literal_samples.tsv": "9a685bc1d1ead2bb92f6757cc7dcf1f27c4ab90594d9e297e6e11562290158da",
    GATE / "results_k23_direct_k15_literal_referee.json": "da28e1d4402ef0903b25e1048bfbc5e614128a3bcc8d7623c7de975e3394ebb6",
}

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):h.update(block)
    return h.hexdigest()

def main():
    for path,digest in PINS.items(): assert sha(path)==digest,path
    for line in (HERE/"MANIFEST.sha256").read_text().splitlines():
        digest,relative=line.split(None,1);assert sha(ROOT/relative)==digest
    contract=json.loads((HERE/"k23_direct_k15_production_contract.json").read_text())
    intervals=[[0,60],[60,121],[121,181],[181,242],[242,303],[303,363],[363,424],[424,485]]
    assert contract["status"]=="PASS_K23_DIRECT_K15_PRODUCTION_READINESS_HELD"
    assert [x["interval"] for x in contract["shards"]]==intervals
    assert contract["producer"]["source_sha256"]==PINS[GATE/"run_k23_direct_k15_four_sink.rs"]
    assert contract["producer"]["binary_sha256"]==PINS[GATE/"run_k23_direct_k15_four_sink"]
    assert contract["literal_referee"]["sink_witnesses"]==1028 and contract["literal_referee"]["distributed_sources"]==257
    spec=importlib.util.spec_from_file_location("C",HERE/"k23_direct_k15_contract.py");C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
    C.verify_pins();C.validate_interval_set([tuple(x) for x in intervals])
    ref=json.loads((GATE/"results_k23_direct_k15_literal_referee.json").read_text())
    assert ref["status"]=="PASS_INDEPENDENT_257_DISTRIBUTED_LITERAL_DIRECT_K15_FOUR_SINK_K23_REPLAY"
    assert ref["source_samples"]==257 and ref["first_slice"]==0 and ref["last_slice"]==484
    assert ref["all_divisions_exact"] and ref["all_literal_K23_children_terminal"] and not ref["cache_abstraction_used"]
    payload={"status":"PASS_INDEPENDENT_K23_DIRECT_K15_PRODUCTION_INTERFACE_REFEREE","degree":23,"strict_ids":12,"strict_groups":4,"intervals":intervals,"no_gap_no_overlap":True,"producer":{"source_sha256":PINS[GATE/"run_k23_direct_k15_four_sink.rs"],"binary_sha256":PINS[GATE/"run_k23_direct_k15_four_sink"]},"interface":{"manifest_sha256":PINS[HERE/"MANIFEST.sha256"],"contract_sha256":PINS[HERE/"k23_direct_k15_production_contract.json"],"shared_contract_sha256":PINS[HERE/"k23_direct_k15_contract.py"],"merger_sha256":PINS[HERE/"merge_k23_direct_k15_shards.py"]},"literal_referee":{"source_sha256":PINS[GATE/"referee_k23_direct_k15_literal.rs"],"binary_sha256":PINS[GATE/"referee_k23_direct_k15_literal"],"ledger_sha256":PINS[GATE/"k23_direct_k15_literal_samples.tsv"],"result_sha256":PINS[GATE/"results_k23_direct_k15_literal_referee.json"],"distributed_sources":257,"sink_witnesses":1028},"all_source_engine_hashes_replayed":True,"no_shards_launched_by_referee":True,"scope":"production-interface referee only; shard results accepted separately as they land; no heavy rerun or K24"}
    logical=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest();payload["logical_sha256"]=logical
    out=HERE/"results_k23_direct_k15_interface_independent_audit.json";tmp=Path(str(out)+".tmp");tmp.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n");tmp.replace(out)
    print(json.dumps({"status":payload["status"],"logical_sha256":logical},indent=2))

if __name__=="__main__":main()
