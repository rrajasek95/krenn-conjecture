#!/usr/bin/env python3
"""W26 -- the vertex disjunction over F_p.  UNAUDITED.  Exact (F_p).

Small characteristic is the hard stress test: LETTER COLLAPSE (two clean
slice rows proportional) is far more frequent there, and it was exactly a
small-field artefact that produced W21's false kill (ledger 19).  If the
{R5,R6,L2} exclusion and the disjunction survive F_p, they are not
artefacts of generic position over Q.
"""
import json, os, random, sys
from itertools import combinations
sys.dont_write_bytecode=True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import w26_core as C
import w26_charp as CP
RES=os.path.join(HERE,"results_fpdisj.json")
OUT={"_header":"UNAUDITED W26 vertex disjunction over F_p."}
def ck(): json.dump(OUT,open(RES,"w"),indent=1,default=str)
V=['R4','R5','R6','R7','L0','L1','L2','L3']; TRI=['R5','R6','L2']

def rankp(rows,p):
    if not rows: return 0
    n=len(rows[0]); M=[[x%p for x in r] for r in rows]; r=0
    for c in range(n):
        sel=None
        for i in range(r,len(M)):
            if M[i][c]%p: sel=i; break
        if sel is None: continue
        M[r],M[sel]=M[sel],M[r]
        iv=pow(M[r][c],p-2,p); M[r]=[(x*iv)%p for x in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]%p:
                f=M[i][c]; M[i]=[(a-f*b)%p for a,b in zip(M[i],M[r])]
        r+=1
        if r==len(M): break
    return r

def analyse_p(m,bl,p,nsample=60,seed=5):
    gs=set(C.gamma_edges(C.TEMPLATES[m])); T=C.TEMPLATES[m]
    sg=C.single_edges(T); lv=set(C.live_singles(m))
    sat={}
    for e,(a,b) in sg.items():
        if e not in lv: continue
        sat.setdefault(('R',e[1]),[]).append((e,e[0],a,b))
        sat.setdefault(('L',e[0]),[]).append((e,e[1],b,a))
    rng=random.Random(seed); rec={}
    def cl(u,v,a,b):
        e=(u,v) if u<v else (v,u)
        if e not in gs: return 0
        return bl[e][a][b]%p if u<v else bl[e][b][a]%p
    for kind,v in [('R',4),('R',5),('R',6),('R',7),('L',0),('L',1),('L',2),('L',3)]:
        lab="%s%d"%(kind,v); deliv=False; nidx=0; ncol=0; nd=0
        for _ in range(nsample):
            w=[rng.randrange(3) for _ in range(8)]
            fire=set()
            for (e,trig,tv,letter) in sat.get((kind,v),[]):
                if w[trig]==tv: fire.add(letter)
            if not fire: continue
            def word(t):
                ww=list(w); ww[v]=t; return tuple(ww)
            clean_ts=[t for t in range(3) if t not in fire]
            ok=True
            for t in clean_ts:
                ww=word(t)
                if len(set(ww))==1: ok=False; break
                if [f for f in lv if ww[f[0]]==sg[f][0] and ww[f[1]]==sg[f][1]]: ok=False; break
            if not ok: continue
            for t in fire:
                ww=word(t)
                if len(set(ww))==1: ok=False; break
                act=[f for f in lv if ww[f[0]]==sg[f][0] and ww[f[1]]==sg[f][1]]
                if any((f[1] if kind=='R' else f[0])!=v for f in act): ok=False; break
            if not ok: continue
            x,y=w[:4],w[4:]
            ll={(a,b):cl(a,b,x[a],x[b]) for a,b in combinations(range(4),2)}
            h=(ll[(0,1)]*ll[(2,3)]+ll[(0,2)]*ll[(1,3)]+ll[(0,3)]*ll[(1,2)])%p
            hR=(cl(4,5,y[0],y[1])*cl(6,7,y[2],y[3])+cl(4,6,y[0],y[2])*cl(5,7,y[1],y[3])
                +cl(4,7,y[0],y[3])*cl(5,6,y[1],y[2]))%p
            cols=[]
            if kind=='R':
                if h%p==0: continue
                pp=C.SIGINV[v]
                for q in range(4):
                    if q==pp: continue
                    i,j=[t for t in range(4) if t not in (pp,q)]
                    lij=ll[(min(i,j),max(i,j))]; Dq=cl(q,C.SIG[q],x[q],y[C.SIG[q]-4])
                    colv=[]
                    for t in range(3):
                        gsl=cl(pp,v,x[pp],t); u2=C.SIG[q]; e2=(min(v,u2),max(v,u2))
                        if e2 in gs:
                            la=t if e2[0]==v else y[e2[0]-4]
                            lb=t if e2[1]==v else y[e2[1]-4]
                            rsl=bl[e2][la][lb]%p
                        else: rsl=0
                        colv.append((Dq*lij*gsl+h*rsl)%p)
                    cols.append(colv)
            else:
                if hR%p==0: continue
                pp=v
                for a in range(4):
                    if a==pp: continue
                    b,c=[t for t in range(4) if t not in (pp,a)]
                    rbc=cl(C.SIG[b],C.SIG[c],y[C.SIG[b]-4],y[C.SIG[c]-4])
                    Da=cl(a,C.SIG[a],x[a],y[C.SIG[a]-4])
                    colv=[]
                    for s in range(3):
                        sg2=cl(pp,C.SIG[pp],s,y[C.SIG[pp]-4])
                        e2=(min(pp,a),max(pp,a))
                        lsl=bl[e2][s][x[a]]%p if e2[0]==pp else bl[e2][x[a]][s]%p
                        colv.append((Da*rbc*sg2+hR*lsl)%p)
                    cols.append(colv)
            nidx+=1
            rows=[[cols[j][t] for j in range(3)] for t in range(3)]
            cleanrows=[rows[t] for t in clean_ts]
            rc=rankp(cleanrows,p)
            if rc<=1 and len(clean_ts)>1: ncol+=1
            if all(rankp(cleanrows+[rows[t]],p)==rc for t in fire): nd+=1; deliv=True
        rec[lab]=dict(n_idx=nidx,n_deliver=nd,n_collapse=ncol,DELIVERS=deliv)
    rec["fails"]=[l for l in V if not rec[l]["DELIVERS"]]
    rec["DISJUNCTION_holds"]=len(rec["fails"])<8
    rec["TRI_violation"]=len([l for l in TRI if l in rec["fails"]])>=2
    return rec

def main():
    OUT["records"]=[]
    for p in (7,13,31):
        for m in (25,26,27,28):
            gam=C.gamma_edges(C.TEMPLATES[m]); gs=set(gam); clean=C.clean_words(m)
            got=0
            for kk in range(4000):
                rng=random.Random(404_000+p*1000+m*17+kk)
                bl=CP.seed_p(gam,gs,rng,p)
                if bl is None: continue
                order=list(range(8)); rng.shuffle(order)
                for _ps in range(4):
                    for t in order: CP.site_p(bl,gs,gam,t,clean,rng,p)
                if any(CP.hafp(bl,gs,tuple(range(8)),w,p)!=0 for w in clean): continue
                if not all(bl[e][i][j]%p!=0 for e in gam for i in range(3) for j in range(3)): continue
                van=all(CP.hafp(bl,gs,tuple(range(8)),w,p)==0 for w in C.WORDS)
                r=analyse_p(m,bl,p)
                r2=dict(p=p,m=m,tag="p%d_%d"%(p,kk),van=van,
                        DISJUNCTION_holds=r['DISJUNCTION_holds'],
                        TRI_violation=r['TRI_violation'],fails=r['fails'],
                        n_collapse=sum(r[l]['n_collapse'] for l in V))
                OUT["records"].append(r2)
                print("p=%d m=%d #%-4d van=%-5s disj=%s TRIviol=%s collapse=%d fails=%s"%(
                    p,m,kk,van,r2['DISJUNCTION_holds'],r2['TRI_violation'],
                    r2['n_collapse'],r2['fails']),flush=True); ck()
                got+=1
                if got>=8: break
    recs=OUT["records"]
    OUT["summary"]=dict(n=len(recs),
        disj=sum(1 for r in recs if r['DISJUNCTION_holds']),
        tri_violations=sum(1 for r in recs if r['TRI_violation']),
        total_collapse=sum(r['n_collapse'] for r in recs))
    print("SUMMARY:",OUT["summary"]); ck(); print("DONE")
if __name__=="__main__": main()
