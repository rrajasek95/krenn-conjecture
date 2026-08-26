#!/usr/bin/env python3
"""Fail-closed checkpoint/schema mutations for the isolated gate."""
import argparse, json, struct, subprocess, tempfile
from pathlib import Path

def invoke(binary,path): return subprocess.run([binary,"validate",str(path)],capture_output=True,text=True)
def main():
    p=argparse.ArgumentParser();p.add_argument("--binary",required=True);p.add_argument("--checkpoint",required=True);p.add_argument("--output",required=True);a=p.parse_args()
    with open(a.checkpoint,"rb") as f: src=f.read(46+13)
    nr=struct.unpack_from("<Q",src,14)[0]
    with open(a.checkpoint,"rb") as f:
        f.seek(46+13*nr); col=f.read(15)
    header=bytearray(src[:46]);struct.pack_into("<QQQQ",header,14,1,1,0,0)
    good=bytes(header)+src[46:59]+col
    cases={}
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); gp=td/"good.bin";gp.write_bytes(good)
        r=invoke(a.binary,gp);cases["positive_control"]=(r.returncode==0 and json.loads(r.stdout)["status"]=="PASS")
        muts={
          "bad_magic":lambda b:b.__setitem__(0,b[0]^1),
          "bad_degree":lambda b:b.__setitem__(12,11),
          "bad_row_len":lambda b:b.__setitem__(46,11),
          "unsorted_row":lambda b:(b.__setitem__(47,b[48]),b.__setitem__(48,0xff)),
          "bad_column_word":lambda b:b.__setitem__(slice(59,61),struct.pack("<H",6561)),
          "trailing_byte":lambda b:b.extend(b"x"),
        }
        for name,mut in muts.items():
            b=bytearray(good);mut(b);q=td/(name+".bin");q.write_bytes(b);r=invoke(a.binary,q);cases[name]=(r.returncode!=0)
    status="PASS" if all(cases.values()) else "FAIL"
    result={"status":status,"cases":cases,"fail_closed":True}
    Path(a.output).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result));raise SystemExit(0 if status=="PASS" else 1)
if __name__=="__main__":main()
