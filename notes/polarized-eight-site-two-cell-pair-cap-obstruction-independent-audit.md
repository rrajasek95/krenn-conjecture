# Independent audit: every two-cell deformation preserving the sparse polarized model misses the pair-cap locus

## 1. Exact theorem and scope

Work in the ternary eight-site square-zero algebra.  For a cell
\(ij_{cd}\), the colour \(c\) belongs to the smaller endpoint \(i\), and
\(d\) belongs to the larger endpoint \(j\).  Thus endpoint order is retained
for asymmetric cells.  Set

\[
\begin{aligned}
q={}&23_{00}+45_{00}+67_{00}
     +01_{11}+36_{11}+57_{11}\\
   &+02_{22}+14_{22}+56_{22},\\
z={}&01_{00}+24_{11}+37_{22}.
\end{aligned}                                                   \tag{1}
\]

The displayed polarized model satisfies

\[
                         zq^{[3]}=\Delta_{8,3}.                  \tag{2}
\]

Let \(e\ne f\) be two basis cells outside
\(\operatorname{supp}(q)\), and let \(t,u\in\mathbb C^\times\).  Put

\[
                         q_{e,f}=q+te+uf.                        \tag{3}
\]

The clean-room census proves both of the following statements.

1. Exactly \(3960\) unordered pairs \(\{e,f\}\) admit any nonzero
   \(t,u\) for which

   \[
                         zq_{e,f}^{[3]}=\Delta_{8,3}.             \tag{4}
   \]

   In fact, every such pair satisfies (4) for every
   \(t,u\in\mathbb C^\times\).

2. For each of those \(3960\) pairs and all nonzero \(t,u\),

   \[
   \boxed{\quad
   (a q_{e,f}+4ps)q_{e,f}^{[3]}\ne\Delta_{8,3}
   \quad}                                                       \tag{5}
   \]

   for every \(a\in\mathbb C\) and all linear forms \(p,s\).

Consequently, every deformation by exactly two distinct cells that
preserves the displayed \(z\)-polarized identity misses the one-pair-cap
preimage variety.

The independent exact checker is
[verify_polarized_eight_site_two_invisible_cells_pair_cap_obstruction_independent.py](../computations/verify_polarized_eight_site_two_invisible_cells_pair_cap_obstruction_independent.py).
It imports no exploration or primary verification module.

This is a strict fixed-\((q,z)\), exactly-two-cell theorem.  It is not a
statement about arbitrary quadratics, a deformation with three or more new
cells, a simultaneous deformation of \(z\), or compatibility between
multiple shared pair-cap rows.  It does not supply the missing all-even
descent and does not prove Krenn's conjecture.

## 2. Exhausting every possible two-cell cancellation

For any outside cells \(e,f\), define

\[
 D_e=zeq^{[2]},\qquad D_f=zfq^{[2]},\qquad D_{ef}=zefq.          \tag{6}
\]

The site-square-zero relations give the exact divided-power expansion

\[
 q_{e,f}^{[3]}
   =q^{[3]}+teq^{[2]}+ufq^{[2]}+tu\,efq.                        \tag{7}
\]

There are no \(t^2\) or \(u^2\) terms.  If \(e\) and \(f\) share a physical
endpoint, the \(ef\) term simply vanishes.  Combining (2) and (7), equation
(4) is equivalent to

\[
                        tD_e+uD_f+tuD_{ef}=0.                   \tag{8}
\]

Put \(X=1/t\) and \(Y=1/u\).  On the required torus \(tu\ne0\), this becomes
the linear vector equation

\[
                        D_fX+D_eY=-D_{ef}.                      \tag{9}
\]

This reduction is important: it tests all cancellation involving
individually visible cells, rather than assuming at the outset that
\(D_e=D_f=0\).

There are \(252-9=243\) cells outside \(\operatorname{supp}(q)\), hence

\[
                            \binom{243}{2}=29403                 \tag{10}
\]

unordered pairs.  The checker reconstructs every coefficient vector in
(9) and performs exact rational row reduction.  Since coefficient and
augmented ranks are unchanged under extension from \(\mathbb Q\) to
\(\mathbb C\), this decides complex solvability.  In rank one, the checker
also tests whether the affine solution line meets \(XY\ne0\); whenever it
does, a rational torus point exists because \(\mathbb Q\) is infinite.

The exact outcome is

\[
\begin{array}{c|r}
\text{localized linear-system outcome}&\text{pairs}\\ \hline
\text{rank zero, all three debts vanish}&3960\\
\text{nonzero constant contradiction}&3573\\
\text{rank one forces }X=0&11268\\
\text{rank one forces }Y=0&2421\\
\text{rank two solution lies outside }XY\ne0&8181
\end{array}                                                     \tag{11}
\]

The five counts sum to \(29403\).  In particular, no pair involving an
individually visible debt has a solution of (9).  Every solution belongs
to the first row, so it has

\[
                         D_e=D_f=D_{ef}=0.                      \tag{12}
\]

This proves the first part of the theorem and rules out hidden
complex-parameter cancellation.

## 3. The \(99\) invisible cells and the mixed-debt test

Exactly \(99\) cells satisfy \(D_e=0\).  They are all nine endpoint-colour
cells on each of the eleven physical pairs

\[
       03,04,05,06,07,12,13,15,17,25,34.                       \tag{13}
\]

Among their \(\binom{99}{2}=4851\) unordered pairs, exactly \(3960\) also
satisfy \(D_{ef}=0\).  For each of the other \(891\) pairs,
\(D_{ef}\) consists of exactly one word with coefficient one.  Thus no
sign or multiplicity cancellation is being hidden in the mixed term.

The compatible-pair geometry has the exact census

\[
\begin{array}{c|rrr}
\#\text{ shared physical endpoints}&0&1&2\\ \hline
\#\text{ pairs}&1539&2025&396
\end{array}                                                     \tag{14}
\]

The \(396\) pairs sharing two endpoints are pairs of distinct
endpoint-colour cells on the same physical pair.  Hence the theorem
includes both same-pair and different-pair additions.

## 4. Complete pair-cap coordinate equations

For one of the \(3960\) pairs, write

\[
 F_{t,u}=q_{e,f}^{[3]},\qquad Q_{t,u}=q_{e,f}^{[4]}.             \tag{15}
\]

For site-modes \(A=(i,c)\) and \(B=(j,d)\), set

\[
\begin{aligned}
R_{AB}
 &=p_As_B+s_Ap_B\\
 &=\beta(x_A,x_B),\qquad
x_A=(p_A,s_A),\\
\beta((r,v),(r',v'))&=rv'+vr'.
\end{aligned}                                                   \tag{16}
\]

If (5) failed, the divided-power Euler identity
\(q_{e,f}F_{t,u}=4Q_{t,u}\) would give

\[
                  aQ_{t,u}+psF_{t,u}
                     ={1\over4}\Delta_{8,3}.                    \tag{17}
\]

The checker builds \(F_{t,u}\) and \(Q_{t,u}\) by choosing pairwise
site-disjoint cells from the eleven labelled summands of \(q+te+uf\).
Every incidence is tagged by one of

\[
                              1,\ t,\ u,\ tu.                   \tag{18}
\]

For all \(3960\) pairs, a second support construction verifies:

- the full Gram filling of \(psF_{t,u}\);
- every direct \(aQ_{t,u}\) coordinate, including its tag and
  multiplicity; and
- the coefficientwise identity
  \(q_{e,f}F_{t,u}=4Q_{t,u}\).

Thus the scalar direct term in (17) is never silently discarded.

## 5. Projective singleton closure of \(3944\) pairs

A non-target top coordinate gives a safe Gram zero only when

1. its entire \(Q_{t,u}\) coefficient is identically zero;
2. exactly one tagged Gram entry occurs; and
3. its coefficient is a positive integer times one monomial in (18).

Because \(t,u\ne0\), such an equation forces that Gram entry to vanish.
Coordinates containing two tagged terms are not used: expressions such as
\(1+t\), \(t+u\), or \(1+tu\) may vanish at exceptional complex
parameters.

On a pure target word with no direct \(Q_{t,u}\) term, equation (17)
implies that at least one displayed Gram entry is nonzero.  The checker
branches over every such entry; it does not assume that any coefficient
sum is nonzero.

For the nonzero modes in a branch, let \(L_A=\mathbb Cx_A\).  A safe zero
\(R_{AB}=0\) says

\[
                              L_B=L_A^\perp.                    \tag{19}
\]

Orthogonal complement is an involution on the projective line of the
nondegenerate two-space in (16).  Therefore:

- an odd zero path joining the endpoints of a required-nonzero edge
  contradicts that edge; and
- an odd zero cycle makes its component an isotropic line, so every
  required-nonzero edge internal to that component is impossible.

The checker implements this exact bipartite-parity criterion only on
modes already known nonzero.  It closes every pure-word branch for
\(3944\) of the \(3960\) pairs.  The number of branches examined per pair
is

\[
\begin{array}{c|rrrrr}
\#\text{ branches}&0&1&2&3&4\\ \hline
\#\text{ pairs}&4&2641&1171&50&94.
\end{array}                                                     \tag{20}
\]

Here zero branches means that a pure target coordinate has a direct
\(aQ_{t,u}\) term, so the deliberately conservative projective test makes
no inference there.

## 6. The sixteen residual localized ideals

Exactly sixteen pairs survive the safe projective test.  For each one, the
checker reconstructs every nonzero top-coordinate equation

\[
 4\sum_{A,B}F_w^{A,B}(t,u)R_{AB}
 +4aQ_w(t,u)-\delta_w=0,                                     \tag{21}
\]

in the \(48\) variables \(p_{i,c},s_{i,c}\) and the parameters \(a,t,u\).
It adjoins a fifty-second variable \(\rho\) and

\[
                              \rho tu-1=0,                     \tag{22}
\]

so the affine scheme is exactly localized to \(t,u\ne0\).

The sixteen cases and equation counts, including (22), are:

| \(e\) | \(f\) | projective residue | equations |
|---|---|---|---:|
| \(03_{00}\) | \(12_{00}\) | pure direct term | 248 |
| \(03_{01}\) | \(13_{01}\) | open branch | 232 |
| \(03_{12}\) | \(07_{12}\) | open branch | 238 |
| \(04_{00}\) | \(15_{00}\) | pure direct term | 242 |
| \(04_{11}\) | \(25_{10}\) | open branch | 232 |
| \(04_{21}\) | \(25_{11}\) | open branch | 244 |
| \(05_{01}\) | \(15_{01}\) | open branch | 214 |
| \(05_{02}\) | \(15_{00}\) | open branch | 214 |
| \(06_{00}\) | \(17_{00}\) | pure direct term | 254 |
| \(06_{02}\) | \(15_{00}\) | open branch | 220 |
| \(07_{01}\) | \(17_{01}\) | open branch | 250 |
| \(12_{11}\) | \(34_{01}\) | open branch | 247 |
| \(12_{21}\) | \(34_{11}\) | open branch | 262 |
| \(13_{12}\) | \(17_{12}\) | open branch | 241 |
| \(15_{00}\) | \(17_{22}\) | open branch | 226 |
| \(17_{22}\) | \(34_{22}\) | pure direct term | 269 |

This is \(3833\) exact equations in total.  Singular works over
\(\mathbb Q\) and returns the reduced unit basis \([1]\) for every one of
the sixteen localized ideals.  Hence the ideals have no zero over
\(\overline{\mathbb Q}\); because the certificate \(1\in I\) remains valid
after base change, they also have no zero over \(\mathbb C\).

As an independence check, this replay does not use the discovery ordering.
It uses a degree-compatible global order with variables

\[
 \rho,u,t,a,s_{7,2},p_{7,2},s_{7,1},p_{7,1},\ldots,
 s_{0,0},p_{0,0},                                            \tag{23}
\]

and supplies top-word generators in reverse lexicographic order.  All
sixteen computations again reduce to \([1]\).

## 7. Reproducibility checksums

The clean-room checker fixes four canonical SHA-256 ledgers:

\[
\begin{array}{c|l}
\text{ledger}&\text{SHA-256}\\ \hline
3960\text{ compatible unordered pairs}
&\mathtt{e10f1c380c47a6d0990c734b94c95dbc122c97863cc28d25972957d9f24faf3c}\\
3960\text{ projective classifications and certificates}
&\mathtt{f93db512df4c43f054d4a49cb4f16efb459416dc0265f07aab87acf27fe1e1f5}\\
29403\text{ localized cancellation classifications}
&\mathtt{f4fe508e4b81010d52c472f8196addff297c9c5c6cf68c93942e6360a5997948}\\
16\text{ full localized ideal inputs}
&\mathtt{5cf3203fb376cfe14fc553dad5f9c975438a94979201fe878f6b8754a1d6ecb7}
\end{array}                                                     \tag{24}
\]

From the repository root, the complete audit is

    .venv/bin/python computations/verify_polarized_eight_site_two_invisible_cells_pair_cap_obstruction_independent.py

The finite census, projective closure, all checksums, and all
\(q^{[3]}/q^{[4]}\) consistency checks can be run without Singular as

    .venv/bin/python computations/verify_polarized_eight_site_two_invisible_cells_pair_cap_obstruction_independent.py --support-only

## 8. Consequence and remaining boundary

The one-cell result did not exclude cancellation between two newly
activated cells.  The exact rank census now shows that no such cancellation
occurs anywhere among the \(29403\) two-cell supports: preserving this
displayed \(z\) forces both individual debts and the mixed debt to vanish.
The pair-cap calculation then excludes every one of the resulting \(3960\)
families.

The next sparse frontier for this particular model must therefore use at
least three simultaneous new cells, alter \(z\), or leave this displayed
\((q,z)\) support altogether.  A global proof still needs information that
links actual shared rows or overlapping physical-pair identities; the bare
polarized equation and this fixed-support neighborhood do not provide the
uniform descent by themselves.
