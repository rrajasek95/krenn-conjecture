#!/usr/bin/env python3
"""Run the pinned metadata-only referee for the r1575->r1587 schedule."""
import hashlib
from pathlib import Path
H=Path(__file__).resolve().parent
T=H.parent/"unaudited-codex-n8-affine251-d12-v4-1-round1562-cap2750-audit-2026-08-25/audit_landed_metadata.py"
raw=T.read_bytes();assert hashlib.sha256(raw).hexdigest()=="81ad56dcb2260e3c4ccfa91d8a5f21444529d98781d9cacaca34d19648f2cf84"
s=raw.decode().replace("r1550->r1562 cap-2.75m","r1575->r1587 cap-3.0m").replace("ROUND1562_CAP2750_METADATA_V1","ROUND1587_CAP3000_METADATA_V1")
exec(compile(s,str(H/"audit_landed_metadata.py"),"exec"),{"__file__":str(H/"audit_landed_metadata.py"),"__name__":"__main__"})
