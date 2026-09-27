#!/usr/bin/env python3
"""Optional numerical probe of the OPEN six-site scalar W inequality.

Requires NumPy and SciPy. Exact verification never imports this module.
The first start is the known extremizer; other starts are seeded complex
Gaussian vectors. Feasible local results do not certify a global minimum.
"""
import numpy as np
from scipy.optimize import minimize
from itertools import combinations
import json,time,sys
import scipy
from scipy.optimize._numdiff import approx_derivative
edges=list(combinations(range(6),2)); ix={e:k for k,e in enumerate(edges)}
def match(v):
 if not v:yield ();return
 for k in range(1,len(v)):
  for r in match(v[1:k]+v[k+1:]):yield ((v[0],v[k]),)+r
M=np.array([[ix[e] for e in t] for t in match(tuple(range(6)))])
inc=np.zeros((6,15))
for e,(i,j) in enumerate(edges):inc[i,e]=inc[j,e]=1

def vals(x):
 z=x[:15]+1j*x[15:]
 terms=z[M]
 h=np.prod(terms,axis=1).sum()
 c=np.zeros(15,complex);J=np.zeros((15,15),complex)
 for row in M:
  a,b,d=row
  c[a]+=z[b]*z[d];c[b]+=z[a]*z[d];c[d]+=z[a]*z[b]
  J[a,b]+=z[d];J[b,a]+=z[d];J[a,d]+=z[b];J[d,a]+=z[b];J[b,d]+=z[a];J[d,b]+=z[a]
 r=inc@abs(c)**2; S=np.vdot(z,z).real
 inv=1/np.maximum(r,1e-14)
 f=S*S*inv.sum()
 grad_c=-S*S*(inc.T@(inv**2))*np.conj(c)
 g=2*S*inv.sum()*np.conj(z)+grad_c@J
 grad=np.r_[2*g.real,-2*g.imag]
 return f,grad,h,c,S,r

def fun(x):return vals(x)[:2]
def cons(x):
 f,g,h,c,S,r=vals(x)
 return np.array([S-1,h.real,h.imag])
def jac(x):
 f,g,h,c,S,r=vals(x)
 return np.array([2*x,np.r_[c.real,-c.imag],np.r_[c.imag,c.real]])

rng=np.random.default_rng(819)
probe=rng.normal(size=30);probe/=np.linalg.norm(probe)
numerical=approx_derivative(lambda z:fun(z)[0],probe,method='3-point').ravel()
gradient_error=float(np.max(abs(numerical-fun(probe)[1]))/max(1,np.max(abs(numerical))))
if gradient_error>1e-5:raise ValueError('Analytic objective gradient failed finite-difference check')
best=None;feasible=0;successful=0;restarts=1000;start=time.monotonic()
for k in range(restarts):
 z=rng.normal(size=15)+1j*rng.normal(size=15)
 if k==0:z=np.array([1 if j!=5 else 0 for i,j in edges],complex)
 z/=np.linalg.norm(z);x=np.r_[z.real,z.imag]
 res=minimize(fun,x,jac=True,method='SLSQP',constraints={'type':'eq','fun':cons,'jac':jac},options={'maxiter':1000,'ftol':1e-11})
 f,g,h,c,S,r=vals(res.x)
 feasible+=int(np.linalg.norm(cons(res.x))<1e-7)
 successful+=int(res.success)
 if np.linalg.norm(cons(res.x))<1e-7 and (best is None or f<best['objective']):
  best={'objective':float(f),'rate_relaxation':float(8/(9*f)),'success':bool(res.success),'restart':k,'source_real':res.x[:15].tolist(),'source_imag':res.x[15:].tolist(),'rows':r.tolist()}
 if k%100==0:print('restart',k,'best objective',best['objective'] if best else None,file=sys.stderr,flush=True)
print(json.dumps(dict(evidence_status='Exploratory local optimization; not a proof',seed=819,restarts=restarts,feasible_runs=feasible,successful_runs=successful,gradient_relative_error=gradient_error,numpy_version=np.__version__,scipy_version=scipy.__version__,best=best),indent=2,sort_keys=True))
