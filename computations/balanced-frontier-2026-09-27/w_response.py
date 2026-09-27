"""Exact unrestricted W response bounds, with cancellation negative controls."""
from math import prod, comb
from triangle import *
from exact import matchings


def support_census():
    edges=tuple(combinations(range(6),2));ix={e:i for i,e in enumerate(edges)}
    mask=lambda es:sum(1<<ix[e] for e in es)
    perfect=[mask(M) for M in matchings(tuple(range(6)))]
    minors={e:[mask(M) for M in matchings(tuple(v for v in range(6) if v not in e))] for e in edges}
    counts={'1+5':0,'3+3':0}
    for G in range(1<<15):
        if any(G&M==M for M in perfect):continue
        active={v for e,ms in minors.items() if any(G&M==M for M in ms) for v in e}
        if len(active)!=6:continue
        remaining=set(range(6));components=[]
        while remaining:
            component={remaining.pop()};frontier=list(component)
            while frontier:
                v=frontier.pop()
                for u in list(remaining):
                    if G&(1<<ix[tuple(sorted((u,v)))]):
                        remaining.remove(u);component.add(u);frontier.append(u)
            components.append(component)
        sizes=sorted(map(len,components))
        require(sizes in ([1,5],[3,3]),'Support reduction to exactly two odd components')
        for component in components:
            for v in component:
                require(any(G&mask(M)==mask(M) for M in matchings(tuple(sorted(component-{v})))),
                        'Each odd component is factor-critical')
        counts['+'.join(map(str,sizes))]+=1
    return dict(graphs_examined=1<<15,no_perfect_matching_with_all_response_rows_supported=counts)


def split_bounds():
    f=lambda s:Q(prod(range(1,2*s,2))**2,(2*s+1)**(s-1)) if s else Q(1)
    records=[]
    for n in range(4,82,2):
        m=n//2;s=m-1
        B=Q(prod(range(1,n,2))**2,comb(n,2)**m)
        optimum=n*B/((n-1)**2+1)
        require(Q(n,m**m)*f(s)/(1+(2*s+1)**2)==optimum,'Singleton split equals the all-even one-root rate')
        ratios=[]
        for alpha in range(1,s):
            beta=s-alpha;p=2*alpha+1;q=2*beta+1
            bound=Q(n,m**m)*f(alpha)*f(beta)/(p*p+q*q)
            ratio=bound/optimum
            require(ratio<1,'Every non-singleton odd split has a strict gap')
            require(f(alpha)*f(beta)<=f(s-1),'Log-convex product consequence')
            if n>=8:require(ratio<Q(98,125),'Uniform strict gap beyond six sites')
            ratios.append(ratio)
        records.append(dict(sites=n,largest_non_singleton_ratio=str(max(ratios)) if ratios else None))
    require(records[1]['largest_non_singleton_ratio']=='65/81','Sharp response comparison at the 3+3 split')
    return records


def data(ground,n=6):
    a=sum(z.abs2() for z in ground.values())
    C={(i,j):hafnian(ground,tuple(v for v in range(n) if v not in (i,j))) for i,j in combinations(range(n),2)}
    rows=[sum(z.abs2() for e,z in C.items() if i in e) for i in range(n)]
    require(all(rows),'Every site must have a nonzero ground-core response')
    b=sum(Q(1)/r for r in rows)
    m=n//2
    bound=Q(n*(m-1)**(m-1),m**m)/(a**(m-1)*b)
    return a,C,rows,b,bound


def minimum_single_entries(ground,n=6):
    a,C,rows,b,bound=data(ground,n)
    source={(i,j,0,0):z for (i,j),z in ground.items()}
    for i in range(n):
        for j in range(n):
            if i!=j:
                z=C[tuple(sorted((i,j)))].conjugate()/rows[i]
                if z:source[cell(i,j,1,0)]=z
    H=outputs(source,n=n,colors=2)
    W={tuple(int(v==i) for v in range(n)):ONE for i in range(n)}
    require(all(H.get(w,ZERO)==ONE for w in W),'Every required single-excitation coefficient equals one')
    mixed=sum(z.abs2() for (i,j,h,k),z in source.items() if h+k==1)
    require(mixed==b,'Exact minimum norm of the independent response rows')
    return source,H,W,dict(ground_energy=str(a),row_norms_squared=list(map(str,rows)),
                         harmonic_sum=str(b),scale_invariant_objective=str(a**(n//2-1)*b),rate_bound=str(bound))


def check():
    star={(i,j):ONE for i,j in combinations(range(5),2)}
    A,H,W,optimal=minimum_single_entries(star)
    require(H==W and optimal['rate_bound']=='1/65','The relaxation is attained by the known one-root family after relative scaling')
    require(optimal['scale_invariant_objective']=='520/9','Exact sufficient scalar threshold at six sites')
    triangle={(i,j):ONE for triple in ((0,1,2),(3,4,5)) for i,j in combinations(triple,2)}
    a,C,rows,b,bound=data(triangle)
    require(bound==Q(1,81),'Two scalar triangles give the core-dependent upper bound 1/81')
    cube={(0,1):ONE,(2,3):ONE,(0,2):OMEGA,(1,3):OMEGA,(0,3):OMEGA*OMEGA,(1,2):OMEGA*OMEGA}
    require(not hafnian(cube,tuple(range(4))),'Four-site ground output cancels exactly')
    A,H,W,four=minimum_single_entries(cube,n=4)
    require(four['rate_bound']=='1/8' and four['scale_invariant_objective']=='8','Four-site scalar threshold of 10 would be false')
    bad={w:z for w,z in H.items() if w not in W}
    require(bool(bad) and all(sum(w)==2 for w in bad),'Relaxed optimum leaves unwanted two-excitation output')
    dense={(i,j,h,k):E(1+(i+j+h)%3,(j+k)%3-1) for i,j in combinations(range(6),2) for h,k in product(range(2),repeat=2)}
    D={(i,j):dense[i,j,0,0] for i,j in combinations(range(6),2)}
    full=outputs(dense,colors=2)
    for i,j in combinations(range(6),2):
        remaining=tuple(v for v in range(6) if v not in (i,j))
        expected=dense[i,j,1,1]*hafnian(D,remaining)
        for k,l in product(remaining,repeat=2):
            if k!=l:
                expected+=dense[cell(i,k,1,0)]*dense[cell(j,l,1,0)]*hafnian(D,tuple(v for v in remaining if v not in (k,l)))
        word=tuple(int(v in (i,j)) for v in range(6))
        require(full.get(word,ZERO)==expected,'Exact two-excitation completion equation')
    table=[]
    for n in range(4,18,2):
        m=n//2;B=Q(prod(range(1,n,2))**2,comb(n,2)**m)
        K=Q(prod(range(1,n-2,2))**2,comb(n,2)**(m-2))
        universal=B*Q(m-1,m)**(m-1)
        require(K==m*m*B and universal==Q(2*K*(m-1)**(m-1),n*m**m),'Uniform Roos response constant')
        table.append(dict(sites=n,unrestricted_upper_bound=str(universal),two_root_optimum=str(n*B/((n-1)**2+1))))
    return dict(one_root_equality=optimal,two_triangles_bound=str(bound),four_site_negative_control=four,
                no_ground_matching_supports=support_census(),all_even_odd_split_checks=split_bounds(),
                four_site_unwanted_words=len(bad),two_excitation_identities_checked=15,unrestricted_upper_bounds=table,
                six_site_scalar_inequality='OPEN: a^2 sum_i 1/r_i^2 >= 520/9 when haf(D)=0')
