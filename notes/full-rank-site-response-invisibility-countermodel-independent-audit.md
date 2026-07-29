# Independent audit of the full-rank-site response countermodel

## Verdict

The one-site and two-separated-site constructions in
[full-rank-site-response-invisibility-countermodel.md](full-rank-site-response-invisibility-countermodel.md)
are correct.  A clean-room square-zero expansion reproduces
\(q^{[2]}\), proves \(q^{[3]}=0\) for arbitrary \(a,b\in V_0\), checks
all nine tensor responses before scalar contraction, and independently
recovers the cofactor matrix, its determinant, the diagonal response
pencil, its adjugate, and the five-vector deformation kernel in the first
model.  A second local-algebra implementation separately checks all nine
responses, the cubic identity, both incident ranks, and the cofactor
determinant of the two-site model.  No sign, endpoint-order, or
factorial-normalization error was found.

Neither construction is a ternary six-site GHZ/Krenn instance.  In the
first, target directions at sites \(1,\ldots,5\) have local rank one.  In
the second, targets are separated at sites zero and one, but sites
\(2,\ldots,5\) still have target rank one and the total incident-rank
budget is only eight.  The first model refutes the isolated one-site
scalar-response package; the second shows that merely retaining one more
target frame still does not propagate endpoint rank.  Neither evades the
global four-cover constraint.

The rank-budget equality classification and its omission-pair flattening
argument are also correct.  There is one notation point that must be kept
explicit: before choosing quotient functionals, \(N_P\) has entries in
\((V_a/W_a)\otimes(V_b/W_b)\).  Simple-tensor uniqueness therefore gives
\[
 N_{B_i}=\theta_i E_{ii}\otimes
          \bar e_i^{(a)}\otimes\bar e_i^{(b)},           \tag{A}
\]
not literally \(N_{B_i}=\theta_iE_{ii}\).  The shorter formula is valid
only after suppressing or scalarizing those quotient target factors.
The important conclusion
\(F_{B_i}=\theta_i^{-1}E_i(B_i)\) is unchanged.

## 1. Divided powers rebuilt by repeated multiplication

Work in

\[
 (\mathbb C\oplus V_0)\otimes
 \bigotimes_{v=1}^5(\mathbb C\oplus\mathbb Cz_v),
 \qquad z_S=\prod_{v\in S}z_v,
\]

with products that repeat a site set equal to zero.  The independent
checker does not choose unordered subsets of the primary edge list.
Instead, it expands \(q\) into coloured site-mask monomials in the
scrambled order

\[
 34,\ 05,\ 24,\ 03,\ 25,\ 02,\ 15,\ 04,\ 01
\]

and recursively computes

\[
 q^{[d]}=\frac1d q^{[d-1]}q.
\]

This independently tests the divided-power normalization.  A complete
support-by-support expansion gives

\[
\begin{aligned}
q^{[2]}={}&(a+2e_2)(z_{124}+z_{134}+z_{234})
       +b(z_{145}+z_{345})\\
 &+2e_2(z_{135}-z_{125}-z_{235})
       +z_{1245}+z_{1345}-z_{2345}.                    \tag{1}
\end{aligned}
\]

In the first line and the first three terms of the second line, the
vector is at site zero.  Thus (1) contains eight vector-valued support
words and three scalar support words; there are no omitted supports.
The cubic coefficient is rebuilt as

\[
 -(2e_2+a)+a+2e_2=0,                                  \tag{2}
\]

so \(q^{[3]}=0\) as a tensor identity for arbitrary vectors \(a,b\), not
only after applying a covector.  Direct multiplication also verifies
\(q^2=2q^{[2]}\) and \(q q^{[2]}=3q^{[3]}=0\).

## 2. All nine responses and the deformation kernel

Using the six rows from the primary construction, direct multiplication
of (1) gives

\[
 \bigl(p_i s_jq^{[2]}\bigr)_{0\leq i,j\leq2}
 =\operatorname{diag}(e_0,e_1,e_2)\,z_{12345}.          \tag{3}
\]

Equation (3) is checked with all components of \(a\) and \(b\)
independent.  The checker also splits every row into local summands and
reassembles each entry from explicitly ordered
\((p\text{-site},s\text{-site})\) pairs.  Hence the two physical endpoint
orders have not been identified or silently halved.

For a further adversarial check, add arbitrary vectors \(t_v\in V_0\) to
the five star blocks.  Re-expansion from scratch yields

\[
 \Delta q^{[3]}=(-t_1+t_2+t_3)z_{12345}                \tag{4}
\]

and

\[
 \Delta M=
 \begin{pmatrix}
 0&0&0\\
 (t_4-t_5)/2&0&0\\
 (-t_1+t_2+t_3)/2&0&(t_1-t_2+t_3)/4
 \end{pmatrix}z_{12345}.                               \tag{5}
\]

These are vector identities at site zero.  Substitution
\((t_1,t_2,t_3,t_4,t_5)=(a,a,0,b,b)\) kills every entry of (4)--(5),
confirming the claimed two-vector invisible deformation without selecting
a cancelling scalar term.

## 3. Cofactor matrix in an independent site order

Let \(x_i=x(e_i)\), \(A=x(a)\), \(B=x(b)\), and put
\(D=A+2x_2\).  Rather than generate deleted-pair matchings, the checker
extracts each complementary four-site coefficient directly from (1).
In the nonstandard site order

\[
                         \pi=(5,2,0,4,1,3),
\]

the resulting matrix is

\[
C_\pi=
\begin{pmatrix}
0&D&0&0&D&D\\
D&0&1&2x_2&B&B\\
0&1&0&0&-1&1\\
0&2x_2&0&0&-2x_2&-2x_2\\
D&B&-1&-2x_2&0&0\\
D&B&1&-2x_2&0&0
\end{pmatrix}.                                         \tag{6}
\]

Returning (6) to ordinary site order gives exactly the matrix displayed
in the primary note.  Symbolic elimination, with \(A=\sum a_ix_i\) and
\(B=\sum b_ix_i\) rather than fresh unrelated symbols, gives

\[
                         \det C=-64x_2^2(A+2x_2)^2.     \tag{7}
\]

The row coefficients are also extracted from the tensor rows, permuted by
\(\pi\), and multiplied only then.  They give

\[
 P_\pi C_\pi S_\pi^{\mathsf T}
   =\operatorname{diag}(x_0,x_1,x_2),                  \tag{8}
\]

with determinant \(x_0x_1x_2\) and adjugate

\[
 \operatorname{diag}(x_1x_2,x_0x_2,x_0x_1).           \tag{9}
\]

Thus the full cofactor form is generically nonsingular, and none of
\(A,B\) contaminates the reduced diagonal pencil.

## 4. Rank and exact scope

At \(a=e_0,\ b=e_1\), the site-zero star vectors are

\[
 e_0+2e_2,\quad e_0,\quad2e_2,\quad e_1,\quad e_1.
\]

Their \(3\times5\) matrix has rank three, proving \(W_0=V_0\).  At every
other site the ambient degree-one space is only
\(\mathbb Cz_v\), and each such site is incident with a nonzero internal
edge.  Consequently

\[
             (\dim W_0,\ldots,\dim W_5)=(3,1,1,1,1,1). \tag{10}
\]

Likewise, the three right-hand targets in (3) have local target rank
three at site zero but local target rank one at each of sites
\(1,\ldots,5\): all use the same \(z_v\).  Krenn's ternary target instead
requires three independent local axes at every site.  This is the precise
reason the construction is a countermodel to the isolated local
invariant and not to the conjecture.

## 5. Independent reconstruction of the two-site model

For the stronger model, the checker switches to a second algebra whose
monomials are literal six-tuples of local labels.  Sites zero and one each
have three labels, sites \(2,\ldots,5\) have one label, and no code from
the first implementation is reused for multiplication or contraction.
It enters the edge terms in reverse-scrambled order and reconstructs
\[
\begin{aligned}
q'={}&(2e_2+e_1)f_2+e_1z_2+2e_2z_3+e_0z_5+f_2z_5\\
    &-z_2z_5+z_2z_4+z_3z_4.                            \tag{11}
\end{aligned}
\]

Repeated multiplication divided successively by \(2\) and \(3\) gives
the three full-support packets
\[
 \bigl(-(2e_2+e_1)+e_1+2e_2\bigr)f_2z_{2345}=0,        \tag{12}
\]
so \(q'^{[3]}=0\) with the correct factorial convention.  Direct
six-tuple multiplication with the displayed \(p\)- and \(s\)-rows gives
all nine tensor identities
\[
 p_i s_jq'^{[2]}
  =\delta_{ij}e_i f_i z_2z_3z_4z_5.                   \tag{13}
\]
This check is performed before applying any covectors.

For a separate scalar audit, write \(x_i=x(e_i)\),
\(y_i=y(f_i)\), \(d=x_1+2x_2\), and \(D=dy_2\).  Extracting
complementary supports from the independently computed \(q'^{[2]}\)
gives, in site order \(\pi=(4,1,5,0,3,2)\),
\[
C'_\pi=
\begin{pmatrix}
0&-2x_2&0&0&-2x_2y_2&2x_2y_2\\
-2x_2&0&d&-1&x_0&x_0\\
0&d&0&0&D&D\\
0&-1&0&0&y_2&y_2\\
-2x_2y_2&x_0&D&y_2&0&0\\
2x_2y_2&x_0&D&y_2&0&0
\end{pmatrix}.                                         \tag{14}
\]
Consequently
\[
 \det C'=-64x_2^2y_2^4(x_1+2x_2)^2,                   \tag{15}
\]
and row extraction in the same nonstandard order yields
\[
 P'_\pi C'_\pi S_\pi'^{\mathsf T}
   =\operatorname{diag}(x_0y_0,x_1y_1,x_2y_2).         \tag{16}
\]

The incident vectors at site zero include
\[
 e_1+2e_2,\quad e_1,\quad2e_2,\quad e_0,
\]
and span dimension three.  Every block at site one has endpoint factor
\(f_2\), so its incident span has dimension one.  The four remaining
sites are lines.  Thus
\[
                  (\dim W_0,\ldots,\dim W_5)=(3,1,1,1,1,1), \tag{17}
\]
while the target frames have local ranks \(3,3,1,1,1,1\).  This verifies
both the strength and the limitation of the example: two target frames
are genuinely retained, but the global target-separation hypotheses are
not.

## 6. Rank budget, pair types, and the quotient flattening

Put \(r_u=\#\{i:e_i^{(u)}\in W_u\}\).  The four-cover and site-cover
theorems give
\[
 \sum_u r_u=\sum_i|D_i|\geq12,\qquad
 1\leq r_u\leq\dim W_u.                                \tag{18}
\]
Hence \(\sum_u\dim W_u\geq12\).  If equality holds, all inequalities in
(18) are equalities: every colour occurs at four sites, and every
\(W_u\) is exactly the span of its \(r_u\) contained target axes.  Each
omission set \(B_i\) is therefore a pair.

If \(n_j\) is the number of rank-\(j\) sites, equality and site cover give
\[
 n_1+n_2+n_3=6,\qquad n_1+2n_2+3n_3=12,\qquad n_1=n_3. \tag{19}
\]
With at least one rank-three site, the only triples
\((n_3,n_2,n_1)\) are
\[
                    (1,4,1),\qquad(2,2,2),\qquad(3,0,3). \tag{20}
\]
Viewing \(B_0,B_1,B_2\) as three labelled two-edges, the degree of a site
in this three-edge multigraph is \(3-\dim W_u\).  Its degree sequence
immediately gives the stated pair-overlap types:

| rank counts | omission-pair shape | labelled census |
|---|---|---:|
| \((1,4,1)\) | two pairs meet once; the third is disjoint | 1080 |
| \((2,2,2)\) | two coincident pairs plus a disjoint pair | 270 |
| \((2,2,2)\) | a three-edge path | 1080 |
| \((3,0,3)\) | a triangle | 120 |

The independent checker exhausts all \(15^3\) ordered triples of pairs,
filters to the site-cover cases having at least one rank-three site, and
obtains the four counts above.  Thus the list has neither a missing
multigraph type nor an unjustified simplicity assumption.

Finally decompose \(F=q^{[2]}=\sum_PF_P\) by missing pair.  Under equality
one may first project every local space to the three-dimensional target
span: this fixes \(W_u\), \(q\), \(F\), and all targets because
\(W_u\) is already a coordinate span.  For \(P=\{a,b\}\), quotienting
the two sites by \(W_a,W_b\) kills every \(F_Q\) except \(F_P\).  With
\[
 (\mathcal N_P)_{rs}=
 \bar p_{r,a}\otimes\bar s_{s,b}
 +\bar s_{s,a}\otimes\bar p_{r,b},                     \tag{21}
\]
the exact nine-response identity is
\[
 \mathcal N_P\otimes F_P
 =\sum_{i:B_i=P}E_{ii}\otimes
   \bar e_i^{(a)}\otimes\bar e_i^{(b)}\otimes E_i(P).  \tag{22}
\]

If two colours share \(P\), the two left factors in (22) are independent
because their response factors are \(E_{ii}\) and \(E_{jj}\), and their
four-site target words on the right are also independent.  The right side
therefore has flattening rank two across
\[
 \bigl(\operatorname{Mat}_3\otimes(V_a/W_a)\otimes(V_b/W_b)\bigr)
 \ \big|\ \bigotimes_{u\notin P}W_u.
\]
The left side of (22) has rank at most one, a contradiction.  The checker
reconstructs this coordinate flattening in all 270 labelled coincident
cases and obtains rank two every time.

Thus \(B_0,B_1,B_2\) are pairwise distinct.  For \(P=B_i\), (22) is a
single nonzero simple tensor, so factor uniqueness gives (A) and
\[
                       F_{B_i}=\theta_i^{-1}E_i(B_i).  \tag{23}
\]
This does force the entire missing-pair slice to be pure; it does not
select one term from a cancelling sum.

The standalone checker
[`audit_full_rank_site_response_invisibility_countermodel_independent.py`](../computations/audit_full_rank_site_response_invisibility_countermodel_independent.py)
imports nothing from the primary verifier.  It verifies (1)--(23)
symbolically or by complete finite census, including arbitrary vector
components for \(a,b,t_1,\ldots,t_5\).
