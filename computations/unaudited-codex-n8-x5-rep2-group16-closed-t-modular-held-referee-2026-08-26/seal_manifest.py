#!/usr/bin/env python3
import hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;M=H/'MANIFEST.sha256';M.write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in sorted(H.iterdir()) if p.is_file() and p!=M))
