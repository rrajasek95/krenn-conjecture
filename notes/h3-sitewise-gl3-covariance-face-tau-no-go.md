# Sitewise covariance is horizontal transport, not the five face homotopies

Research reduction only.  The local \(GL(3)^5\) covariance calculation is
exact, but it does not construct the five \(\tau_v\), a relative cap lift, or
a proof of Krenn's conjecture.

## Outcome

The mechanism proposed after
[the universal denominator reset no-go](h3-universal-denominator-reset-polynomial-no-go.md)
has a clean answer.

For every four-site deletion face, local color covariance does produce the
desired polynomial-output expression \(h_vY_0\).  It produces it twice:

\[
       L_{F_v}\,\delta(d_{v,0})
       =D_{F_v}\,\delta(d_{v,0})
       =h_vY_0.
\]

Thus \(h_vY_0\) is a horizontally transported denominator coefficient, not
the boundary of a new source chain.  Expanding the fourfold connection
\(\prod_{x\in F_v}(L_x-D_x)\) gives sixteen copies of the same
\(h_vY_0\), with alternating signs, and hence zero by \((1-1)^4\).  The
connection cube does not isolate one copy as a boundary.

The obstruction cannot cancel between faces.  The five all-derivation
companions have exactly the same pairwise-disjoint monomial supports as the
five desired \(h_v\).  Killing their sum at initial \(q\)-degree two kills the
desired sum as well.  The old pure denominator faces \(g_v\) form another
rank-five space disjoint from the \(h_v\)-space, reproducing the rank
\(5\to10\) obstruction of the preceding note.

Therefore bare sitewise equivariance does not realize any of the five
\(\tau_v\).  A successful construction still needs an additional
Spencer/de Rham contraction, jet generator, or physical full-nine row whose
boundary kills the all-derivation companion.  Declaring such a jet to exist
would simply rename the missing \(\tau_v\).

## The local covariance identity

Let \(F\) be a four-site face and write its universal matching tensor as

\[
 T_F(q)=\sum_{c\in\{0,1,2\}^{F}}
           \operatorname{Haf}(q_c)\,e_c.
\]

For \(x\in F\), define the contragredient source derivation

\[
 D_{x;a\leftarrow b}
   =\sum_{\substack{y\in F\\y\ne x}}\sum_{j=0}^2
        q_{xy}^{\,b j}\,
        {\partial\over\partial q_{xy}^{\,a j}},
\]

with the evident reversal of color indices when \(y<x\).  Define the output
matrix unit by

\[
 L_{x;a\leftarrow b}e_c=
 \begin{cases}
 e_{c[x:=a]},&c_x=b,\\
 0,&c_x\ne b.
 \end{cases}
\]

Every perfect matching has exactly one edge incident with \(x\).  Replacing
its \(x\)-color \(a\) by \(b\) proves the coefficientwise identity

\[
                 D_{x;a\leftarrow b}T_F
                  =L_{x;a\leftarrow b}T_F.
\]

The checker verifies this identity for all \(4\cdot3^2=36\) matrix units on
each of the five faces, not only for the selected lowering directions.
Actions at distinct sites commute, including on their shared edge variable,
because they act on its two different color indices.

## The five mixed faces

Put

\[
 \bar m=12112,\qquad
 F_v=\{1,2,3,4,5\}\setminus\{v\}.
\]

The exact face tags from commit f09cbfb are

\[
\begin{array}{c|c}
v&\bar m|_{F_v}\\ \hline
1&2112\\
2&1112\\
3&1212\\
4&1212\\
5&1211.
\end{array}
\]

For \(x\in F_v\), abbreviate

\[
 L_x=L_{x;0\leftarrow\bar m_x},\qquad
 D_x=D_{x;0\leftarrow\bar m_x}.
\]

Use the existing pure-exposed denominator column

\[
 \delta(d_{v,0})=e_0^{(v)}T_{F_v}(q).
\]

The all-output operator selects the mixed coefficient on the face, changes
its four output colors to zero, and leaves the exposed zero unchanged:

\[
 \prod_{x\in F_v}L_x\,\delta(d_{v,0})
   =\operatorname{Haf}
       \left(q_{\bar m}|_{F_v}\right)Y_0
   =h_vY_0.
\]

Covariance gives the identical formula with every \(L_x\) replaced by
\(D_x\).  More strongly, for every subset \(S\subseteq F_v\),

\[
 \left(\prod_{x\in S}L_x\right)
 \left(\prod_{x\in F_v\setminus S}D_x\right)
 \delta(d_{v,0})
 =h_vY_0.
\]

All output-lowered sites and all derivation-selected sites end at color zero,
while the coefficient has been recolored to \(\bar m|_{F_v}\).  Consequently

\[
\begin{aligned}
 \prod_{x\in F_v}(L_x-D_x)\,\delta(d_{v,0})
 &=\sum_{S\subseteq F_v}(-1)^{4-|S|}h_vY_0\\
 &=(1-1)^4h_vY_0=0.
\end{aligned}
\]

This is a flat connection identity, not a homological boundary with one
uncancelled face.

## Target, residue, and cross-face cancellation

There is no hidden diagonal-target error in this calculation.  Each
four-letter face tag contains both colors 1 and 2, so the all-\(L\) lowering
kills the diagonal tensor

\[
                       \Delta=\sum_{a=0}^2 e_a^{\otimes5}.
\]

The all-\(D\) operator kills it as well because \(\Delta\) is independent of
the internal \(q\)-variables.  Hence the candidate has zero physical target
facewise.

The failure is instead residue locking.  The desired \(L\)-residue and the
unwanted \(D\)-companion are the same \(h_vY_0\).  The five \(h_v\) have
disjoint supports because each consists of matchings on a different labelled
four-site set.  Therefore

\[
       \dim\langle h_1,\ldots,h_5\rangle=5,
\]

and no nonzero constant combination cancels the derivation companions while
retaining the output-lowering terms.

The color-preserving Euler choice
\(L_{x;0\leftarrow0}=D_{x;0\leftarrow0}\) instead gives

\[
 \prod_{x\in F_v}L_{x;0\leftarrow0}\,\delta(d_{v,0})
   =g_vY_0.
\]

These are precisely the five old pure-output denominator faces.  Their
monomials use only color \(00\), while the \(h_v\) use colors 1 and 2, so

\[
 \dim\langle g_1,\ldots,g_5,h_1,\ldots,h_5\rangle=10.
\]

Local covariance therefore recovers the old \(g_v\) rows and realizes each
\(h_v\) only as a locked equality \(L_F=D_F\).  It does not move the
\(h_v\)-classes into the old denominator image.

## Why a Weyl identity is not yet a source chain

In the Weyl algebra of the universal \(q\)-space, the operators
\(L_x-D_x\) annihilate the matching tensor.  This says \(T_F\) is horizontal
for the sitewise color connection.  Horizontality does not imply exactness.

In the ordinary source complex, coefficients act by polynomial
multiplication.  A derivation \(D_F\) is not such a coefficient, and
\(D_Fd_{v,0}\) is not an existing source-chain element.  One can formally
adjoin a jet or Spencer generator whose boundary is
\(D_F\delta(d_{v,0})\), but that added generator is exactly a presentation of
the missing \(\tau_v\); covariance alone supplies no physical lift of it.

This is a bounded no-go.  It excludes the bare fourfold connection cube and
constant cross-face cancellation.  It does not exclude a larger derived
base-change construction, a Spencer contraction proven to descend into the
full-nine source resolution, higher-\(q\)-degree syzygies, or a non-flat
specialization transgression.

## Exact verification

The dependency-free checker
[verify_h3_sitewise_gl3_covariance_face_tau_no_go.py](../computations/verify_h3_sitewise_gl3_covariance_face_tau_no_go.py)
uses sparse universal polynomials and exact rational arithmetic.  It checks
all 180 local covariance identities, all 80 connection-cube corners, the
five target vanishings, the exact face tags, and the ranks \(5,5,10\).
Its frozen ledger digest is

    aaba3b9ff228908041820f6f4dfbc02c970e36c2dc14113fa2c6073f876fcaa4
