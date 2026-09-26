# Common factors for all odd pure responses and an exact null-pair transfer

**Status.** Independently audited all-order research theorem, 2026-09-12.
See the [complete mathematical audit](UNIFORM-ALL-ODD-DIAGONAL-RESPONSE-FACTORS-AND-NULL-PAIR-TRANSFER-AUDIT.md).
Written by `/root`, with the reflection independently derived by
`/root/audit_tree_chords`; audit by `/root/dense_nontree`.
This remains outside the formally certified dependency spine.
The general conjecture is open.
The theorem controls pure coefficients; it does not remove mixed errors.

## 1. Actual odd core and its entire diagonal-response space

Work over C in the commutative physical-site-square-zero algebra,
with three independent designated axes a,b,c at each physical site.
Let Omega have N=2m+1>=3 sites and let R be any actual ordinary
quadratic on distinct physical pairs. Write R^[j]=R^j/j! and

    Phi_R(L)=L R^[m],
    D_R={L : Phi_R(L) is in span{a^Omega,b^Omega,c^Omega}},
    Phi_R(L)=sum_h f_h(L) h^Omega    for L in D_R.

The f_h are linear functions on the finite-dimensional space D_R.
Assume that their joint image has dimension at least TWO. No pure
omission cofactor, support bound, positivity, or injectivity is assumed.
Every full ordinary ternary source, viewed at a root, supplies a core
with image dimension three and therefore satisfies this premise.

For 0<=r<=m define the actual homogeneous polynomial on D_R

    t_(h,r)(L)=[h^Omega] L^(2r+1) R^[m-r].

**Theorem.** There is a unique homogeneous polynomial q_r of degree
2r on D_R, independent of h, such that

    t_(h,r)=f_h q_r      for each h in {a,b,c}.           (1)

In particular q_0=1. A target color with f_h identically zero also
has t_(h,r) identically zero. Neither the full odd response nor its
mixed coefficients are asserted to be diagonal.

## 2. Formal Wick reflection and the antisymmetric identity

Here is a self-contained proof of the identity used in (1). Define
a formal Wick functional: the moment of an even list of variables
is the sum over its perfect pairings of the products of the specified
symmetric pair covariances, and an odd moment is zero. This is a
polynomial definition. It does not require a positive, invertible,
or real covariance matrix and does not invoke a probability measure.

Use one variable X_(i,h) for each physical coordinate and an auxiliary
variable g. Give different-site physical pairs their actual R
coefficients, same-site pairs zero, and set

    cov(g,X_(i,h))=L_i(h),       cov(g,g)=0.

For odd d=2r+1<=N, the Wick moment with d copies of g and one
physical variable at each site is exactly the corresponding coefficient
of L^d R^[m-r]. Every g must pair with a different physical variable.
The d! assignments to labeled auxiliary occurrences agree with the
coefficient of L^d; the divided power counts each remaining physical
matching once. Thus there is no missing auxiliary factorial.

Take two independent replicas X,Y, with auxiliaries g_X,g_Y and
zero covariances between replicas. Fix two distinct colors a,b and put

    Delta_i=X_(i,a)Y_(i,b)-X_(i,b)Y_(i,a).

For formal parameters s,t with s^2+t^2!=0, apply to every replica pair
the same matrix

    M=(s^2+t^2)^(-1) [[s^2-t^2, 2st],
                      [2st, t^2-s^2]].

It satisfies M^T M=I, det(M)=-1, and fixes the row (s,t). It
preserves the full replicated covariance, hence every Wick moment,
fixes s g_X+t g_Y, and multiplies each Delta_i by -1. Since N is odd,
for every nonnegative integer d the polynomial moment

    Wick((s g_X+t g_Y)^d product_i Delta_i)

equals its own negative and is zero. Its vanishing for generic s,t
is a polynomial identity; no inference is needed on the isotropic
set s^2+t^2=0 separately.

Choose d=p+q for odd p,q<=N and extract s^p t^q. The nonzero binomial
factor may be divided out. Replica independence gives

    sum_(I subset Omega) (-1)^|I|
      H_p(a off I,b on I) H_q(b off I,a on I)=0,         (2)

where H_d is the entire actual tensor L^d R^[(N-d)/2]. Equation (2)
holds for ANY row L, not only diagonal-response rows, and retains
every matching and every color word in the antisymmetrization.

## 3. Diagonal specialization and polynomial divisibility

Now take L in D_R and q=1 in (2). The second factor is Phi_R(L).
Only I=empty and I=Omega can contribute: every other word in that
factor mixes a and b. Since N is odd, their signs are opposite.
Consequently, for every pair of designated colors,

    f_b(L) t_(a,r)(L)=f_a(L) t_(b,r)(L).                (3)

The same identity holds for every L in D_R, so it is an identity
in the polynomial ring C[D_R]. By the rank premise, some two f
functions, say f_a,f_b after relabeling, are independent linear
polynomials. They are relatively prime. Equation (3) forces f_a
to divide t_(a,r), say t_(a,r)=f_a q_r, and then forces
t_(b,r)=f_b q_r. Applying (3) to a and the remaining color gives
t_(c,r)=f_c q_r, including the case f_c=0 identically.

The ring is an integral domain and f_a!=0, which also proves
uniqueness. Homogeneity supplies degree 2r. This proves (1).
Rank at least two is essential to this argument; a single pure
response direction does not give two relatively prime f functions.

## 4. Polarization and the full odd-kernel consequence

Let Q_r be the symmetric 2r-linear polarization of q_r, normalized
by Q_r(L,...,L)=q_r(L). Polarizing (1) gives the exact identity

    (2r+1) [h^Omega] (product_(i=0)^(2r) L_i) R^[m-r]
      =sum_(i=0)^(2r) f_h(L_i) Q_r(L_0,...,omit L_i,...,L_(2r))
                                                               (4)

for arbitrary L_i in D_R. In particular, if every L_i belongs to
K_R=ker Phi_R, every PURE coefficient on the left is zero. This
holds for every allowed odd number of kernel insertions, including
repeated rows. It does not say that their full tensor is zero.

For the cubic case put B=Q_1, so q_1(L)=B(L,L). Then

    3 [h^Omega] C U V R^[m-1]
      =f_h(C) B(U,V)                                  (5)

whenever C is in D_R and U,V are in K_R. The factor 3 comes from
polarization and must be retained. Three kernel rows give zero
pure coefficients in every designated color.

As another consequence, a kernel row U that has no component in
some active receiving color h lies in the radical of B on D_R.
Indeed the left side of (4) for U,L,L and that color is zero,
so 2 f_h(L)B(U,L)=0 for every L; polynomial cancellation gives
B(U,L)=0. Thus each one-coordinate kernel row is in the radical
when all three target colors are active. This is only a statement
about B, not about the entire tensor-valued response map.

## 5. One common pair matrix for two null extensions

Add two new physical sites q,r, with the usual three axes, and form
the ACTUAL ordinary quadratic

    Q0=R+sum_i e_i(q) A_i+sum_j e_j(r) B_j+J,

where all A_i,B_j belong to K_R and J is an arbitrary q,r pair
tensor. The notation B_j for a row is distinct from the bilinear
form B(U,V). Its two entire omission cofactors satisfy

    F_q(Q0)=sum_j e_j(r) B_j R^[m]=0,
    F_r(Q0)=sum_i e_i(q) A_i R^[m]=0.                    (6)

Allow a row C_total=C+C_q+C_r, with C supported on Omega. The
q,r row components have zero whole response by (6). The exact
remaining expansion is

    C_total Q0^[m+1]
      =J C R^[m]+sum_(i,j) e_i(q)e_j(r) C A_i B_j R^[m-1]. (7)

No higher q,r occupancy is possible, and the two star insertions
have coefficient one in divided powers.

Suppose C is in D_R. Project ONLY the Omega factor of (7) onto
its three pure words, retaining the ENTIRE q,r tensor. Equation (5)
gives

    projection_(pure words on Omega)(C_total Q0^[m+1])
       =sum_h f_h(C) M h^Omega,

    M=J+(1/3) sum_(i,j) B(A_i,B_j) e_i(q)e_j(r).        (8)

There is ONE common pair matrix M for all colors and all C in D_R.
Adding any pair correction E changes it to M+E. Mixed words on
Omega remain outside this formula; (8) does not assert their absence.

## 6. Exact obstructions and a conditional descent

If the full actual response in (7) is tau c_q c_r c^Omega with
tau!=0 and C is in D_R, (8) implies

    f_c(C)!=0,       M=(tau/f_c(C)) c_q c_r,
    f_a(C)=f_b(C)=0.                                   (9)

Thus the lower response C R^[m] must already be a nonzero pure-c
tensor. In particular a zero lower response is impossible. This
rules out a pure target generated solely from THREE lower kernel
rows, even if its coefficient grid is taken from an actual quadratic.

The same fixed pair matrix cannot yield two different nonzero pure
target colors from two rows whose lower responses are both diagonal.
Equation (9) would require M to lie on two independent pair axes.
This remains true after ANY correction E on q,r.

If R already has actual pure-a and pure-b preimages, and a pure-c
preimage of Q0 has a diagonal lower response, (9) supplies a pure-c
preimage on R as well. Attaching one new ternary root to those three
rows constructs an ordinary full source two sites smaller than the
source with root and Q0. Nonzero amplitudes can be fitted by rescaling
the three new root rows. This is a minimum-order contradiction only
when the smaller order is forbidden; the allowed four-site case
must not be counted as a contradiction.

For the binary four-site repair programme, its lower two-pure-cofactor
branch has exactly the rows A_i,B_j in (6). Therefore its proposed
zero third lower response is incompatible with the ORIGINAL full
third target, not merely with a chosen repair. If the third lower
response is diagonal, the stated smaller-source construction applies.
A nonzero MIXED lower response remains possible under these deductions.

## 7. Scope of progress toward the conjecture

The common factors (1), the kernel consequences (4)-(5), and the
common pair matrix (8) are uniform in order, density, and complex
weights. They retain actual powers throughout. The first theorem
applies to every full ternary source through its root response space.

These results do not make the higher odd responses diagonal, force
a useful pair or small support, or show that a third lower response
must be diagonal. They do not establish that a prescribed response
belongs to an actual row image. The general existence or contradiction
step remains unproved; no general source-order bound is claimed.
