# Every higher odd response has zero two-color mixed coefficients

**Status.** Independently audited all-order research theorem, 2026-09-12.
See the [complete mathematical audit](UNIFORM-ALL-ODD-TWO-COLOR-MIXED-VANISHING-AND-KERNEL-PENCIL-AUDIT.md).
This remains outside the formally certified dependency spine.
This statement concerns actual ordinary complex quadratics. The surviving
mixed words using all three colors are retained explicitly.

## 1. Actual response space and statement

Let Omega have N=2m+1 sites, m>=1, with ternary local color spaces
having coordinate basis a,b,c at every site. Work in the commutative
site-square-zero algebra, and let R be an ordinary quadratic on distinct-site pairs.
Put R^[j]=R^j/j!. Let D be a linear space of actual linear rows such that

    Phi_R(L)=L R^[m]=sum_h f_h(L) h^Omega,    L in D,     (1)

where f_a,f_b,f_c are independent linear functionals. Thus the diagonal
target image has rank three. Define, for 0<=r<=m,

    T_(2r+1)(L)=L^(2r+1) R^[m-r].                       (2)

**Theorem.** For any mixed word w on Omega using exactly two of the
three designated colors,

    [w] T_(2r+1)(L)=0          for every L in D.         (3)

More generally, (3) requires only that w is mixed and avoids some
color h for which f_h is not identically zero on the diagonal-response
space D. No injectivity of Phi_R, selected support, source minimum,
anchor condition, or restriction on the physical density is needed.

## 2. Site-dependent pairs in the reflection identity

The following gives the needed reflection argument directly. For the
fixed actual R,L, introduce formal variables X_(i,d) and one variable g.
Their symmetric covariances are the R edge coefficients between distinct
sites, zero within one site, cov(g,X_(i,d))=[d_i]L, and cov(g,g)=0.
Define their Wick functional E by summing products of covariances over
pairings of labeled factors. Odd moments are zero. This is finite
algebra over C; a positive covariance or probability model is not used.

For p=2r+1, the moment with p copies of g and one specified coordinate
at each original site is exactly the coefficient of T_p(L). Indeed,
the g factors must pair to distinct original sites; their p! labeled
assignments reproduce L^p, and the remaining pairs reproduce R^[m-r].

Take two independent identical replicas (X,g_1),(Y,g_2). At EVERY site
i choose any two distinct coordinate colors alpha_i,beta_i; the pair
is allowed to depend on i. Put

    Delta_i=X_(i,alpha_i)Y_(i,beta_i)
              -X_(i,beta_i)Y_(i,alpha_i).

Over C(s,t), simultaneously transform every replica pair by

    M=(s^2+t^2)^(-1) [[s^2-t^2,2st],[2st,t^2-s^2]].

This matrix preserves the two-copy covariance, fixes s g_1+t g_2,
and has determinant -1. Every Delta_i therefore changes sign,
irrespective of its chosen local colors. Since N is odd,

    E[(s g_1+t g_2)^d product_i Delta_i]=0.              (4)

The pairing definition is invariant under any covariance-preserving
linear substitution, so (4) is an algebraic identity. Its left side
is polynomial in s,t; equality in C(s,t) allows coefficient extraction
without a specialization at a pole.

For I subset Omega, let w_I use alpha_i outside I and beta_i inside I,
and let w'_I use the complementary local choices. Extracting s^p t
in (4), with d=p+1, and dividing by the nonzero binomial coefficient
p+1 gives

    sum_I (-1)^|I| T_p(L)(w_I) Phi_R(L)(w'_I)=0.         (5)

No source operation is performed by this auxiliary calculation.
All moments in (5) return to coefficients of the same actual R,L.

## 3. Isolate a two-color mixed word and polarize

Fix a mixed word w avoiding an active color h. At each site choose
alpha_i=w_i and beta_i=h. These are distinct. In (5), a diagonal
second-factor word can only be the all-h word: a different constant
color would have to occur in w at every site, contrary to w being
mixed. The all-h word occurs only at I=empty. Consequently

    f_h(L) [w] T_p(L)=0                                 (6)

as a polynomial identity on D. The coordinate ring of the finite
dimensional vector space D is an integral domain, and f_h is a nonzero
linear polynomial. Thus [w]T_p(L) vanishes identically on D. This
proves (3), including at L for which the particular value f_h(L) is
zero. For rank-three (1), every mixed two-color word omits an active h.

Substitute L=sum_(j=1)^p z_j L_j with arbitrary L_j in D. The coefficient
of z_1...z_p in (3) is p! times the corresponding product response.
Therefore

    [w](L_1 ... L_p R^[m-r])=0,
    p=2r+1,             L_1,...,L_p in D.                (7)

This is full polarization, not merely a statement about repeated rows.

## 4. The exact kernel-pair pencil

For completeness, the same reflection with constant local pairs a,b
and a diagonal second factor also gives

    f_b(L)[a^Omega]T_p(L)=f_a(L)[b^Omega]T_p(L).

Independent f_a,f_b are relatively prime linear polynomials. Hence
there is a unique homogeneous polynomial q_r on D of degree 2r with

    [h^Omega]T_(2r+1)(L)=f_h(L) q_r(L)   for every h.    (8)

It may be zero; q_0=1. Let Q_r be its symmetric multilinear polarization,
normalized by Q_r(L,...,L)=q_r(L). Polarizing (8) gives

    [h^Omega](L_1...L_p R^[m-r])
      =(1/p) sum_j f_h(L_j) Q_r(L_1,...,omit L_j,...,L_p).
                                                               (9)

Set K=D intersect ker Phi_R. For U,V in K and C in D, the literal
ordinary quadratic pencil R_t=R+t UV satisfies

    C R_t^[m]=sum_(r=0)^m (t^r/r!) C U^r V^r R^[m-r].  (10)

This retains every power of UV; no square-zero claim about UV is made.
Equations (7) and (9) yield the exact whole-response decomposition

    C R_t^[m]=p_(U,V)(t) Phi_R(C)+M_C(t),               (11)

where every word in M_C(t) uses ALL THREE designated colors, and

    p_(U,V)(t)
      =1+sum_(r=1)^m t^r Q_r(U repeated r,V repeated r)
                            /[r!(2r+1)].               (12)

The scalar polynomial is common to every C in D and all three target
colors; p_(U,V)(0)=1. The remainder is linear in C and satisfies
M_C(0)=0. Thus neither pure coefficients nor mixed two-color words
create an independent color-dependent error in this pencil.

If an actual full source has root rows C_h in D with
Phi_R(C_h)=tau_h h^Omega, and a value t satisfies M_(C_h)(t)=0 for all
three rows and p_(U,V)(t)!=0, use the ordinary core R_t and root rows
C_h/p_(U,V)(t). They have exactly the original three target amplitudes.

Equation (11) does NOT assert M_C(t)=0. There is no proved relation
q_r=q_1^r, no anchor-preservation claim for the core change, and no
assertion of a nontrivial kernel, or that a useful nonzero t makes all
relevant remainders vanish. No decrease in source complexity is forced.
Although p(t) has only finitely many zeros, this alone does not solve
the simultaneous three-color mixed equations. The pencil may add
physical pairs and scalar entries; it is not by itself a normalization
or a descent theorem.

## 5. The surviving gap is present in an actual source

Take Omega={1,2,3} and

    R=a_2 a_3+b_1 b_3+c_1 c_2,
    D=span{a_1,b_2,c_3}.

For L=alpha a_1+beta b_2+gamma c_3, actual multiplication gives

    L R=alpha a^Omega+beta b^Omega+gamma c^Omega,
    L^3=6 alpha beta gamma a_1 b_2 c_3.                 (13)

This is the core of the ordinary four-site ternary source, with
the three displayed pure rows at the fourth vertex. Its higher odd
response has a nonzero all-three-color mixed coefficient. Thus the
remainder in the general odd-response statement cannot be discarded.
This example does not claim a nonzero kernel-pair pencil at that core.

The proved restriction is universal for (1). Closing the remaining
argument still requires actual control of the all-three-color mixed
responses, or an independent source normalization/descent that avoids
them. Neither their disappearance nor existence of such an operation
follows from the common pure factor.

The original proof was frozen in /tmp before this research promotion.
Its unchanged 219-record input baseline was
/tmp/krenn_pruning_frame_transfer_final.json, with SHA256
f07014765f39f83dba4ac9fdb627fe466b4ebaa05aea7d7f58ff3990f2c31338.
