# Every full ternary source has monochromatic edge cells and inverse cofactors

**Status.** Independently audited all-order research theorem, 2026-09-13,
by `/root/one_bad_tree`, using the scalar matrix argument of `/root`;
[complete independent audit PASS](UNIFORM-GLOBAL-EDGE-MONOCHROMATICITY-AND-COFACTOR-INVERSE-AUDIT.md).
Both the source and complete audit were independently reviewed by `/root`.
The earlier conditional source remains frozen. The separate
[foundation recheck](ALL-EVEN-OMISSION-COVARIANCE-ADVERSARIAL-RECHECK.md)
is the original author's additional challenge, not a substitute for the
independent audits. This composition reduces the problem to weighted
diagonal cancellation; the general conjecture remains open.
It has not been promoted into the formally certified dependency spine.

## 1. Actual full source and the claimed all-order theorem

Let V have even size n=2m+2>=4. Each local space is C^3 with fixed
basis a,b,c. Work over C with an actual ordinary quadratic A in the
commutative physical-site-square-zero algebra.
Use A^[j]=A^j/j!, and suppose the WHOLE matching tensor is

    A^[m+1]=sum_(h=a,b,c) tau_h h^V,    tau_a tau_b tau_c!=0.  (1)

**Theorem.** Every off-color cell A_pr(i,j), i!=j, is zero in the
ORIGINAL target bases. For each color h, the scalar same-color matrix
M_h and its zero-diagonal deleted-pair cofactor matrix C_h satisfy

    M_h C_h=tau_h I_n,       C_h=tau_h M_h^(-1).

No source minimum, sparsity, positivity or basis change is assumed.
The exact definitions and proof, including n=4, follow.

For distinct ordered vertices p,r, let A_pr(i,h) be the coefficient
with color i at p and color h at r. Reversing the vertices reverses
the local coordinates: A_rp(h,i)=A_pr(i,h). This does not make the
matrix in (3) below symmetric when i!=h.

Fix a target color h. Define symmetric n-by-n scalar matrices

    M_h[p,r]=A_pr(h,h)  for p!=r,     M_h[p,p]=0,
    C_h[r,q]=haf(M_h restricted off r,q)  for r!=q,
    C_h[q,q]=0.                                             (2)

Here haf is the ordinary unsigned perfect-matching sum, including
haf(empty)=1. The zero diagonal of C_h is a DEFINITION; it is not
a deletion cofactor at a repeated vertex. Also define, for i=a,b,c,

    B_ih[p,r]=A_pr(i,h)  for p!=r,     B_ih[p,p]=0.            (3)

Thus B_hh=M_h. Every entry in (2)--(3) comes from the SAME A.

For each p!=q put S=V without p,q and Q=A restricted to S. The
three original p-exterior rows are

    X_i^(p,q)=sum_(r in S) sum_k A_pr(i,k) k_r.

The reviewed positive-even omission theorem gives

    [h^S] X_i^(p,q) X_h^(p,q) Q^[m-1]=0
       for every p!=q and every i,h in {a,b,c}.             (EV1)

This is the r=1 instance of the
[all-even omission theorem](UNIFORM-ALL-EVEN-OMISSION-PURE-RESPONSE-VANISHING.md),
whose [earlier independent audit](UNIFORM-ALL-EVEN-OMISSION-PURE-RESPONSE-VANISHING-AUDIT.md)
is separately recorded. Only this positive-even degree-two instance
is needed here; no whole mixed response is asserted to vanish.

The stated theorem's source-relative application is exact: delete p
first, take its three original rows with whole responses tau_i i^(V\p),
then omit q. Their response image has rank three and every target is
active. The restricted rows are exactly the X_i^(p,q) above. The
product contains TWO rows from this one p family; it does not mix
different original root families. At r=1 the remaining divided power
is Q^[m-1], including Q^[0]=1 when n=4.

## 2. Diagonal matrix entries are complete original one-defect words

Ordinary matrix multiplication gives

    (B_ih C_h)[p,p]
      =sum_(r!=p) A_pr(i,h) haf(M_h restricted off p,r).
                                                                    (4)

This is precisely the whole coefficient of the word with i at p
and h at every other vertex. In every matching, p is matched to
one r, the first factor is its edge cell, and all remaining vertices
carry h. Different choices of r partition all the matchings. The
coefficient is therefore, by (1),

    (B_ih C_h)[p,p]=delta_(i,h) tau_h.                     (5)

No omission identity is used for these diagonal entries, and no
assumption about any individual cofactor being nonzero is needed.

## 3. Every off-diagonal entry is one same-root quadratic response

Let p!=q. In the sum defining (B_ih C_h)[p,q], the r=p term is
zero because B_ih[p,p]=0, and r=q is zero because C_h[q,q]=0.
For every remaining r, p is a RETAINED vertex of the scalar core
M_h restricted off r,q. Expand its hafnian at that retained p:

    C_h[r,q]
      =sum_(s outside {p,q,r}) M_h[p,s]
          haf(M_h restricted off p,q,r,s).                 (6)

Hence the exact off-diagonal matrix entry is

    (B_ih C_h)[p,q]
      =sum_(r,s in S, r!=s) A_pr(i,h) A_ps(h,h)
          haf(M_h restricted off p,q,r,s).                 (7)

The sum is over ORDERED pairs (r,s). For fixed r,s, choose the
receiving-h component of X_i^(p,q) at r and of X_h^(p,q) at s.
The pure-h coefficient on all other sites of S in Q^[m-1] is
exactly the scalar hafnian in (7). Terms with r=s are zero in the
physical algebra. These observations prove the literal identity

    (B_ih C_h)[p,q]
      =[h^S] X_i^(p,q) X_h^(p,q) Q^[m-1].                  (8)

There is no factor of one half. Even when i=h, the two choices
(r,s) and (s,r) occur on BOTH sides: the left has the choice of
r in matrix multiplication and s in its hafnian expansion, while
the right is a raw product of two rows. The divided power applies
only to Q and supplies exactly one copy of each remaining matching.
By (EV1), every off-diagonal entry in (8) is zero.

## 4. Matrix inversion and every off-color physical cell

Combining (5) and (8) gives, for each h and i,

    B_ih C_h=delta_(i,h) tau_h I_n.
    M_h C_h=tau_h I_n.                                    (9)

Since tau_h!=0, the second equality shows that C_h and M_h are
invertible over C. This is ordinary finite-dimensional scalar matrix
inversion, not cancellation in the physical algebra. Explicitly,

    C_h=tau_h M_h^(-1).

For i!=h, right-multiplying the first equality in (9) by C_h^(-1)
then gives

    B_ih=0.                                               (10)

For any distinct physical endpoints p,r and distinct colors i,j,
choose h=j in (10). Equation (3) gives A_pr(i,j)=0. Thus EVERY
original physical block is diagonal in the fixed target
color bases. This conclusion uses no basis change, entry minimum,
anchor, support partition, bipartiteness, or selected pure row frame.
Its proof does not assume that the original same-color matrices
are invertible; their invertibility is part of (9).

## 5. The four-site boundary and actual-cofactor scope

At n=4, S has two vertices. In (6)--(8), r and s are those two
distinct vertices, and the four-deletion hafnian is haf(empty)=1.
The ordered sum and raw product still agree, including their factor
two when the two rows coincide. The familiar four-site source

    a_p a_q+a_r a_s+b_p b_r+b_q b_s+c_p c_s+c_q c_r

satisfies (9): each M_h is one weighted matching and its cofactor
matrix is its inverse when the displayed weights equal one.
There is no negative divided power. No n=2 application of the
positive-even omission theorem is asserted here.

The scalar matrices C_h are the ACTUAL mutually compatible deletion
cofactors of one M_h. Assigning arbitrary response tensors or unrelated
cofactors would not justify their expansion at p in (6). The calculation
uses the original full source at every root and the reviewed (EV1),
without any additional compatibility premise. No higher even degree,
zero-core theorem, cofactor-nonvanishing theorem or classification is
separately needed in the matrix argument.

## 6. Exact remaining diagonal weighted equations

Write the resulting original quadratic as

    A=sum_(p<q) sum_(h=a,b,c) M_h[p,q] h_p h_q.

For any ordered partition V=S_a disjoint_union S_b disjoint_union S_c,
with empty parts allowed, the WHOLE coefficient of the corresponding
color word is exactly

    product_(h=a,b,c) haf(M_h restricted to S_h).             (11)

Indeed every contributing edge joins two sites of the same color.
A perfect matching of V which contributes is therefore precisely
one perfect matching on EACH S_h. Expanding their product gives
all original matching terms once. Set haf(empty)=1 and haf of an
odd-cardinality restriction equal to zero, as there is no matching.
This proves (11) with every possible cancellation retained.

Consequently (1) is equivalent, in the diagonal setting, to

    haf(M_h)=tau_h!=0                 for h=a,b,c,
    product_h haf(M_h[S_h])=0         whenever at least two S_h
                                      are nonempty.          (12)

Conversely, any three complex symmetric zero-diagonal matrices
satisfying (12) give an actual ordinary diagonal source satisfying
(1), by the same expansion. Together with the theorem, this is an
exact reformulation of the full-source existence problem for n>=4.
The inverse identities (9) are additional necessary consequences;
they need not be added as independent hypotheses to the converse.

Equation (12) is the diagonal WEIGHTED cancellation problem. It is
not the stronger support condition that every individual supported
perfect matching be monochromatic (often called PMValid). A zero
hafnian factor may be a sum of nonzero matching monomials which
cancel. Neither (9) nor (12) permits replacing those sums by termwise
support exclusions or ordinary matrix-rank tests.

For n>=6 a nonexistence conclusion still requires exclusion of the
applicable diagonal weighted system. The existing
[finite diagonal certificate source](/Users/rishi/workplace/krenn-conjecture/proofs/eight-site-diagonal-obstruction.md)
records the separate six-site and eight-site diagonal results,
including nonzero unequal pure amplitudes, and expressly does not
provide a uniform result for n>=10. Those finite certificates are
not rerun, extended or formally re-registered here. In particular
this proposed research composition is not itself a new certified
proof of the general eight-site registry item, and no old proof or
status file is edited. The four-site exception above remains allowed.

**Integration provenance.** Independently audited frozen source: /tmp/krenn_global_edge_monochromaticity_and_cofactor_inverse_20260913.md
SHA256 2d04542fdbd6d772e5487e5276db8ba724df047cd6027b96f68c54c1848359f2.
Only review status, dependency links and this provenance paragraph changed.
The companion audit is byte-identical to its frozen input.
This research result remains outside the formally certified dependency spine.
