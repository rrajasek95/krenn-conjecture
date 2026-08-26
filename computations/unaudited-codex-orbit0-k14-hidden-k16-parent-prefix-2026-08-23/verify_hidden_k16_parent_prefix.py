#!/usr/bin/env python3
"""Exhaustive format/source replay for the measured hidden-K16 prefix."""
from __future__ import annotations
import hashlib, json, mmap, struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STRUCTURE = ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin"
AUX = ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_aux.bin"
PARENTS = HERE / "hidden_k16_parents_prefix.bin"
PROFILES = HERE / "hidden_k16_second_pivot_profiles_prefix.bin"
RESULT = HERE / "results_hidden_k16_parent_prefix.json"
OUT = HERE / "results_hidden_k16_parent_prefix_replay.json"
U = 400_591_699_200

def take(data, pos, n): return data[pos:pos+n], pos+n
def parse_inputs():
    b = STRUCTURE.read_bytes(); p = 11
    nt,nr,np,na = struct.unpack_from("<4I", b, p); p += 16
    assert (nt,nr,np,na) == (384,485,78,12)
    anchor_cells = b[p:p+12]; p += 12 + nt*(252+12)
    records=[]
    for _ in range(nr):
        row=b[p:p+12]; size=struct.unpack_from("<I",b,p+12)[0]; coeff=struct.unpack_from("<q",b,p+16)[0]; p+=24
        records.append((row,size,coeff))
    p += np*12
    factors=[[None]*3 for _ in range(3)]
    for f in range(3):
        for d in range(3):
            n=struct.unpack_from("<I",b,p)[0];p+=4
            factors[f][d]=[b[p+4*i:p+4*i+4] for i in range(n)];p+=4*n
    assert p==len(b)
    a=AUX.read_bytes();q=0;assert a[:8]==b"K17AUX1\0";q=8
    scale=struct.unpack_from("<Q",a,q)[0];q+=8;assert scale==281_801_520
    nc,npa=struct.unpack_from("<2I",a,q);q+=8+12*nc;assert npa==78
    anchors=[];k2=[]
    for _ in range(npa):
        anchors.append(a[q:q+4]);q+=4
        k2.append([a[q+4*i:q+4*i+4] for i in range(12)]);q+=48+128
    assert q==len(a)
    return anchor_cells,records,factors,anchors,k2

def subtract(row, anchor):
    out=[];j=0
    for c in row:
        if j<4 and c==anchor[j]: j+=1
        else: out.append(c)
    assert j==4 and len(out)==20
    return out

def main():
    frozen=json.loads(RESULT.read_text()); anchor_cells,records,factors,anchors,k2=parse_inputs(); apos={c:i for i,c in enumerate(anchor_cells)}
    assert PARENTS.stat().st_size==36+64*frozen["hidden_parent_occurrences"]
    seen=0; signed=0; m1hist={};m2hist={}
    with PARENTS.open("rb") as f:
        mm=mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)
        assert mm[:8]==b"H16PAR1\0" and int.from_bytes(mm[8:24],"little",signed=True)==U
        assert struct.unpack_from("<I",mm,24)[0]==16 and struct.unpack_from("<Q",mm,28)[0]==frozen["hidden_parent_occurrences"]
        for off in range(36,len(mm),64):
            row=mm[off:off+24]; w1=int.from_bytes(mm[off+24:off+40],"little",signed=True); sig=mm[off+40:off+52]
            ri=struct.unpack_from("<H",mm,off+52)[0];ia,ib,ic,p1,t1,m1,m2,z0,z1,z2=mm[off+54:off+64]
            assert ri%16==0 and ia<12 and ib<12 and ic<12 and p1<78 and t1<12 and m1 and m2 and (z0,z1,z2)==(0,0,0)
            head=sorted(records[ri][0]+factors[0][0][ia]+factors[1][0][ib]+factors[2][0][ic])
            expect=bytes(sorted(subtract(head,anchors[p1])+list(k2[p1][t1])))
            assert row==expect and list(row)==sorted(row)
            sc=[0]*12
            for c in row:
                if c in apos:sc[apos[c]]+=1
            assert sig==bytes(sc)
            mass=records[ri][1]*records[ri][2];assert mass*U%m1==0 and w1==mass*U//m1 and w1%m2==0
            seen+=1;signed+=w1;m1hist[m1]=m1hist.get(m1,0)+1;m2hist[m2]=m2hist.get(m2,0)+1
        mm.close()
    assert seen==frozen["hidden_parent_occurrences"]
    assert PROFILES.stat().st_size==36+59*frozen["unique_nonzero_second_pivot_profiles"]
    with PROFILES.open("rb") as f:
        mm=mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)
        assert mm[:8]==b"H16PRO1\0" and int.from_bytes(mm[8:24],"little",signed=True)==U
        assert struct.unpack_from("<I",mm,24)[0]==16 and struct.unpack_from("<Q",mm,28)[0]==frozen["unique_nonzero_second_pivot_profiles"]
        prior=None; psum=0
        for off in range(36,len(mm),59):
            key=mm[off:off+43];value=int.from_bytes(mm[off+43:off+59],"little",signed=True)
            assert key[42]==0 and value and (prior is None or prior<key);prior=key;psum+=value
        mm.close()
    assert str(psum)==frozen["profile_weight_sum_scaled"]
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (STRUCTURE,AUX,PARENTS,PROFILES,RESULT,HERE/"reconstruct_hidden_k16_parent_prefix.rs")}
    out={"status":"PASS_EXHAUSTIVE_PREFIX_REPLAY","parent_records":seen,"parent_weight_sum_scaled":str(signed),"profile_records":frozen["unique_nonzero_second_pivot_profiles"],"profile_weight_sum_scaled":str(psum),"profile_degree_tag":"0=wildcard K2/K3/K4","first_denominator_hist_from_records":{str(k):v for k,v in sorted(m1hist.items())},"second_denominator_hist_from_records":{str(k):v for k,v in sorted(m2hist.items())},"sha256":hashes}
    tmp=OUT.with_suffix(".json.tmp");tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");tmp.replace(OUT);print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__":main()
