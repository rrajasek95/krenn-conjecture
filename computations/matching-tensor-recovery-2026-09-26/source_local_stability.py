#!/usr/bin/env python3
"""Exact local stability certificates for all means and cross-site blocks.

A floating-point eigensolver proposes a preconditioner. Integer arithmetic
certifies it; no floating singular value is used as a rigorous lower bound.
The source point is supplied to this checker. This is not a global inverse.
"""

import base64
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import itertools
import json
import math
import random
import zlib

import numpy as np
from scipy.linalg import eigh
from scipy.sparse import csr_matrix
from flint import fmpq_mat, fmpz_mat, nmod_mat

from blind_mean_search import scalar_bound
from restricted_source_inverse import serialize_edges
from source_calibration_conditioning import moment_directional_derivative

PRIME = 1000003


def ceil_sqrt(value):
    value = F(value)
    root = math.isqrt(value.numerator // value.denominator)
    return root + int(root*root*value.denominator < value.numerator)


def dyadic_upper_sqrt(value, bits=24):
    scale = 2**bits
    return F(ceil_sqrt(F(value)*scale*scale), scale)


def source_jacobian(means, edges):
    n = len(means)
    assert scalar_bound(means, edges) < 2**63
    assert all(edges[0,j][0][0] for j in range(1,n))

    @lru_cache(None)
    def tensor(sites):
        if not sites:
            return np.array(1,dtype=np.int64)
        i,*rest=sites
        value=np.asarray(means[i]).reshape((3,)+(1,)*len(rest))*tensor(tuple(rest))[None]
        for position,j in enumerate(rest,1):
            block=np.asarray(edges[i,j]).reshape((3,3)+(1,)*(len(rest)-1))
            value=value+np.moveaxis(block*tensor(tuple(k for k in rest if k!=j))[None,None],1,position)
        return value

    keys=[('mu',i,a) for i in range(n) for a in range(3)]
    keys += [('R',i,j,a,b) for i,j in edges for a in range(3) for b in range(3)
             if not (i==0 and a==0 and b==0)]
    jacobian=np.zeros((3**n,len(keys)),dtype=np.int64)
    for column,key in enumerate(keys):
        sites,colours=([key[1]],[key[2]]) if key[0]=='mu' else (list(key[1:3]),list(key[3:5]))
        index=[slice(None)]*n
        for i,a in zip(sites,colours):
            index[i]=a
        jacobian[:,column].reshape((3,)*n)[tuple(index)]=tensor(tuple(i for i in range(n) if i not in sites))
    return tensor(tuple(range(n))).reshape(-1),jacobian,keys


def exact_gram(jacobian):
    maximum=int(np.max(abs(jacobian)))
    assert jacobian.shape[0]*maximum*maximum < 2**63
    sparse=csr_matrix(jacobian)
    gram=(sparse.T@sparse).toarray()
    assert np.array_equal(gram,gram.T)
    for i,j in [(0,0),(0,len(gram)-1),(len(gram)//2,len(gram)//3),(len(gram)-1,len(gram)-1)]:
        assert int(gram[i,j])==sum(int(a)*int(b) for a,b in zip(jacobian[:,i],jacobian[:,j]))
    return gram


def conditioning_certificate(gram, mean_count):
    size=len(gram)
    values,vectors=eigh(gram.astype(float))
    assert values[0]>0
    proposed=(vectors/np.sqrt(values))@vectors.T
    denominator=2**48
    entries=[[int(round(x*denominator)) for x in row] for row in proposed]
    assert all(abs(x)<2**63 for row in entries for x in row)
    packed=np.asarray(entries,dtype='<i8').tobytes()
    encoded=base64.b64encode(zlib.compress(packed,9)).decode()
    # Decode the actual saved witness and verify only with exact arithmetic.
    decoded=zlib.decompress(base64.b64decode(encoded))
    assert decoded==packed
    witness=np.frombuffer(decoded,dtype='<i8').reshape(size,size).tolist()
    matrix=fmpz_mat(witness)
    product=matrix.transpose()*fmpz_mat(gram.tolist())*matrix
    residual_squared=sum((int(product[i,j])-(denominator**2 if i==j else 0))**2
                         for i in range(size) for j in range(size))
    residual_bound=ceil_sqrt(residual_squared)
    gap=denominator**2-residual_bound
    assert gap>0
    full_squared=sum(x*x for row in witness for x in row)
    mean_squared=sum(x*x for row in witness[:mean_count] for x in row)
    covariance_squared=full_squared-mean_squared
    determinant=int(nmod_mat(gram.tolist(),PRIME).det())
    assert determinant
    return {'dimension':size,'gram_determinant_prime':PRIME,'gram_determinant_residue':determinant,
            'mean_parameters':mean_count,'covariance_parameters':size-mean_count,
            'preconditioner':{'encoding':'zlib+base64; little-endian signed int64; row-major',
                              'scale':str(denominator),'sha256':hashlib.sha256(packed).hexdigest(),'data':encoded},
            'residual_frobenius_squared':str(residual_squared),'residual_frobenius_upper':str(residual_bound),
            'full_inverse_squared_bound':str(F(full_squared,gap)),
            'mean_inverse_squared_bound':str(F(mean_squared,gap)),
            'covariance_inverse_squared_bound':str(F(covariance_squared,gap)),
            'jacobian_sigma_min_estimate':float(math.sqrt(values[0])),
            'relative_preconditioner_residual_estimate':math.sqrt(residual_squared)/denominator**2,
            'exact_residual_inequality_verified':True}


def curvature_squared(means, edges):
    n=len(means)
    monomers=[max(abs(x) for x in row)+1 for row in means]
    pairs={edge:max(abs(x) for row in block for x in row)+1 for edge,block in edges.items()}

    @lru_cache(None)
    def majorant(sites):
        if not sites:
            return 1
        i,*rest=sites
        value=monomers[i]*majorant(tuple(rest))
        for j in rest:
            value+=pairs[i,j]*majorant(tuple(k for k in rest if k!=j))
        return value

    supports=[(frozenset([i]),3) for i in range(n)]
    supports += [(frozenset(edge),8 if edge[0]==0 else 9) for edge in edges]
    total=0
    for first,w1 in supports:
        for second,w2 in supports:
            if first.isdisjoint(second):
                rest=tuple(i for i in range(n) if i not in first|second)
                total+=w1*w2*3**len(rest)*majorant(rest)**2
    return total


def finite_noise_bounds(certificate, curvature):
    gamma=dyadic_upper_sqrt(F(certificate['full_inverse_squared_bound']))
    hessian=ceil_sqrt(curvature)
    radius=min(F(1),1/(2*gamma*hessian))
    noise=radius/(8*gamma)
    assert gamma*gamma>=F(certificate['full_inverse_squared_bound'])
    assert hessian*hessian>=curvature
    assert gamma*hessian*radius<=F(1,2)
    return {'curvature_squared_bound_on_unit_ball':str(curvature),
            'hessian_norm_upper':str(hessian),'inverse_norm_rational_upper':str(gamma),
            'parameter_ball_radius':str(radius),'noise_norm_threshold':str(noise),
            'source_error_multiplier':str(4*gamma),
            'frozen_left_inverse_iteration':{
                'candidate_data_residual_threshold':str(radius/(2*gamma)),
                'contraction_factor_upper':'1/2',
                'source_error_multiplier_when_true_source_is_in_ball':str(2*gamma),
                'scope':'Exact-arithmetic iteration with B=(J^T J)^(-1) J^T fixed at the center; solves the projected equations, not necessarily least squares.'},
            'scope':'Any point in the stated ball with residual at most the noise bound has source error at most 4 gamma epsilon.'}


def mean_span_certificate(means, bounds):
    matrix=fmpz_mat(list(map(list,zip(*[[x for row in mu for x in row] for mu in means]))))
    gram=matrix.transpose()*matrix
    inverse=fmpq_mat(gram).inv()
    trace=sum(F(str(inverse[i,i])) for i in range(inverse.nrows()))
    lower_squared=1/trace
    scale=2**24
    lower=F(math.isqrt((lower_squared*scale*scale).numerator//(lower_squared*scale*scale).denominator),scale)
    assert lower>0 and lower*lower<=lower_squared
    gamma=F(bounds['inverse_norm_rational_upper'])
    noise=min(F(bounds['noise_norm_threshold']),lower/(8*gamma))
    local_ranks=[nmod_mat(list(map(list,zip(*[mu[i] for mu in means]))),PRIME).rank()
                 for i in range(len(means[0]))]
    return {'observed_global_mean_rank':len(means),'local_mean_ranks':local_ranks,
            'mean_matrix_sigma_squared_lower_bound':str(lower_squared),
            'mean_matrix_sigma_rational_lower':str(lower),'noise_threshold':str(noise),
            'sine_angle_error_multiplier':str(8*gamma/lower),
            'scope':'Top-r mean span in the fixed covariance gauge; no unobserved directions are inferred.'}


def run_case(n,count):
    seed=272050+n
    rng=random.Random(seed)
    choices=[-2,-1,1,2]
    edges={edge:[[rng.choice(choices) for _ in range(3)] for _ in range(3)]
           for edge in itertools.combinations(range(n),2)}
    means=[[[rng.choice(choices) for _ in range(3)] for _ in range(n)] for _ in range(count)]
    tensors,jacobians,grams,certificates=[],[],[],[]
    shared_direction={edge:[[rng.choice([-1,1]) if not(edge[0]==0 and a==b==0) else 0
                              for b in range(3)] for a in range(3)] for edge in edges}
    for mu in means:
        tensor,jacobian,keys=source_jacobian(mu,edges)
        dmu=[[rng.choice([-1,1]) for _ in range(3)] for _ in range(n)]
        direction=[dmu[key[1]][key[2]] if key[0]=='mu' else shared_direction[key[1],key[2]][key[3]][key[4]]
                   for key in keys]
        check_tensor,derivative=moment_directional_derivative(mu,edges,dmu,shared_direction)
        assert np.array_equal(check_tensor.reshape(-1),tensor)
        assert np.array_equal(jacobian@np.asarray(direction),derivative.reshape(-1))
        gram=exact_gram(jacobian)
        tensors.append(tensor);jacobians.append(jacobian);grams.append(gram)
        certificates.append(conditioning_certificate(gram,3*n))
    covariance_count=jacobians[0].shape[1]-3*n
    joint=np.zeros((count*3**n,count*3*n+covariance_count),dtype=np.int64)
    for j,matrix in enumerate(jacobians):
        rows=slice(j*3**n,(j+1)*3**n)
        joint[rows,j*3*n:(j+1)*3*n]=matrix[:,:3*n]
        joint[rows,count*3*n:]=matrix[:,3*n:]
    joint_gram=exact_gram(joint)
    assert np.array_equal(joint_gram[count*3*n:,count*3*n:],sum(g[3*n:,3*n:] for g in grams))
    joint_certificate=certificates[0] if count==1 else conditioning_certificate(joint_gram,count*3*n)
    covariance_bounds=[F(c['covariance_inverse_squared_bound']) for c in certificates]
    harmonic=1/sum(1/x for x in covariance_bounds)
    if count>1:
        assert harmonic<min(covariance_bounds)
    curvature=sum(curvature_squared(mu,edges) for mu in means)
    bounds=finite_noise_bounds(joint_certificate,curvature)
    # Floating values below illustrate the exact additive information theorem.
    profiled=[]
    for gram in grams:
        a,b,c=gram[:3*n,:3*n].astype(float),gram[:3*n,3*n:].astype(float),gram[3*n:,3*n:].astype(float)
        profile=c-b.T@np.linalg.solve(a,b)
        profiled.append((profile+profile.T)/2)
    information=sum(profiled)
    numerical_covariance_constant=1/math.sqrt(float(eigh(information,eigvals_only=True)[0]))
    assert numerical_covariance_constant**2<=float(harmonic)*(1+1e-6)
    return {'sites':n,'outputs':count,'seed':seed,'source_means':means,'source_edges':serialize_edges(edges),
            'fixed_covariance_entries':[[0,j,0,0,edges[0,j][0][0]] for j in range(1,n)],
            'per_output_parameter_count':jacobians[0].shape[1],'joint_parameter_count':joint.shape[1],
            'all_forward_jacobian_directional_checks_passed':True,
            'individual_certificates':certificates,
            'joint_certificate':joint_certificate if count>1 else {'reference':'individual_certificates[0]'},
            'shared_covariance_inverse_squared_bound':str(harmonic),
            'shared_covariance_inverse_norm_estimate':numerical_covariance_constant,
            'covariance_information_blocks_add_exactly':True,
            'finite_noise_bounds':bounds,'mean_span':mean_span_certificate(means,bounds),
            'tensor_hashes':[hashlib.sha256(json.dumps(t.tolist()).encode()).hexdigest() for t in tensors]}


if __name__=='__main__':
    print(json.dumps({'cases':[run_case(7,4),run_case(9,1)],
                      'scope':'Supplied source points; exact certificates for local full-source and observed-span stability.'
                      ' Does not certify a global optimizer or exclude distant noisy alternatives.'},indent=2))
