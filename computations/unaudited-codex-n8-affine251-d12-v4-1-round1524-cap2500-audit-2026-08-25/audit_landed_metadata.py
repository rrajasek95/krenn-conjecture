#!/usr/bin/env python3
"""Execute the pinned r1484 metadata referee template for the r1524 plan."""
import hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
TEMPLATE=HERE.parent/"unaudited-codex-n8-affine251-d12-v4-1-round1484-cap2500-audit-2026-08-25/audit_landed_metadata.py"
EXPECTED="546c9a77eb152096d2ee144bcd6a97aabff35708799c06fa30f78026e8b71431"
raw=TEMPLATE.read_bytes()
assert hashlib.sha256(raw).hexdigest()==EXPECTED
source=raw.decode()
assert source.count("1484")==2 and "1524" not in source
source=source.replace("1484","1524")
old='if stages[-1]["last_round"]==PLAN["target_round"]:need((stages[-1]["status"],stages[-1]["reason"])==("INCOMPLETE_SEARCH_CAP","ROUND_CAP"),"terminal stop")'
new='if stages[-1]["last_round"]==PLAN["target_round"]:need((stages[-1]["status"],stages[-1]["reason"]) in (("INCOMPLETE_SEARCH_CAP","ROUND_CAP"),("INCOMPLETE_RESOURCE_GATE","WALL_CAP")),"terminal stop")'
assert source.count(old)==1
source=source.replace(old,new)
exec(compile(source,str(HERE/"audit_landed_metadata.py"),"exec"),{"__file__":str(HERE/"audit_landed_metadata.py"),"__name__":"__main__"})
