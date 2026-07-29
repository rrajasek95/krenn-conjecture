# Uncapped coefficient vanishing on 35 residual witness assignments

## 1. Outcome

Combine the uncapped pair-fibre identity with the thirteen residual
five-witness masks.  A site supplies an **erasing colour** in either of two
exact situations:

* at an exact-double witness, use its missing colour;
* at a triple-zero site hard for colour `c`, use either colour different
  from `c`.

At an erasing colour `d`, both deleted-star columns vanish:

\[
                         A_{pu}e_d=A_{qu}e_d=0.           \tag{1}
\]

This simple observation has a strong uncapped consequence.  In 35 of the
36 hard assignments left by the two-hole audit, four or five outside sites
can be erased with a nonconstant colour pattern.

* In eleven assignments, four erased sites leave exactly the unique
  nonwitness site and one exact-singleton site.  The full `p,q` coefficient
  matrix is an invertible term plus one rank-at-most-two correction.
  Therefore a whole nine-word coordinate slice of the internal six-site
  matching tensor vanishes.  The common four-site cofactor on the erased
  sites also vanishes; otherwise the two surviving sites would form a zero
  product block, which is incompatible with both being nontriple.
* In twenty-four assignments, five erased sites leave only the unique
  nonwitness.  No avoiding-`pq` correction can occur at all, so the whole
  three-word fibre of the internal matching tensor vanishes.

This includes two of the three no-triple residual rows.  For

\[
 (0,1,3,5,6,6)                                           \tag{2}
\]

the nine coefficients with site colours

\[
                    (*,*,2,1,0,0)                        \tag{3}
\]

vanish, and the four-site coefficient on the last four sites at
`(2,1,0,0)` vanishes.  For

\[
 (0,3,3,5,5,6)                                           \tag{4}

the three coefficients

\[
                    (*,2,2,1,1,0)                        \tag{5}

vanish.  Here a star is a freely varying colour.

The sole untouched assignment is

\[
                         (0,1,1,1,6,6).                  \tag{6}

It has only two erasing sites.  An exact integer local model realizes its
six witness masks and an actual nonconstant internal matching coefficient
whose avoiding-`pq` correction is invertible and cancels an invertible
`A_pq`.  Thus the failure of this last row is genuine for mask geometry and
the one-word pair equation; a further identity is required there.

That further identity is now supplied in
[`n8-011166-full-row-square-obstruction.md`](n8-011166-full-row-square-obstruction.md):
the arbitrary full row forces a four-factor permanent whose common-core
square relations contradict the unique nonzero four-site hafnian.  Thus
the row (6) is excluded, although the 35 erasure-bearing assignments remain
open at the stronger full-row level.

## 2. Erasing columns

Continue to write

\[
 P_u(d)=A_{pu}e_d,\qquad Q_u(d)=A_{qu}e_d.               \tag{7}
\]

**Lemma 2.1 (erasing-colour lemma).**

1. If `u` is an exact-double witness with zero set `{r,s}` and missing
   colour `d`, then `P_u(d)=Q_u(d)=0`.
2. If `u` is triple-zero and hard for colour `c`, then
   `P_u(d)=Q_u(d)=0` for both `d ne c`.

**Proof.**  At an exact-double site, the row spaces of both `A_pu` and
`A_qu` lie in `e_d^perp`; equivalently their `d` columns vanish.

At a triple-zero site, either one star block is zero or the two nonzero row
spaces are a common line.  Hardness for `c` says that the common
annihilator is contained in `e_c^perp`.  In the one-sided case this forces
the nonzero row space to be `C e_c`; in the two-sided case it forces the
common line to be `C e_c`.  Hence both blocks have only their `c` column.
`QED`

The one-sided possibility in the second part is included; no unjustified
nonzero-block assumption is being made.

## 3. The erased pair-fibre lemma

For a word `x` on the six outside sites, recall

\[
\begin{aligned}
 D_x={}&h_xA_{pq}+X_x,\\
 X_x={}&\sum_{\{u,v\}\subset R}h_{uv,x}
       \big(P_u(x_u)Q_v(x_v)^T+P_v(x_v)Q_u(x_u)^T\big). \tag{8}
\end{aligned}
\]

For a nonconstant word, exactness says `D_x=0`.

**Lemma 3.1 (four/five erasures).**  Let `K subset R` carry a fixed
nonconstant erasing pattern, and let `A=R\setminus K`.

1. If `|A|<=1`, then
   \[
                         h_x=0                            \tag{9}
   \]
   for every extension `x` of the pattern on `K`.
2. Suppose `A={a,b}` and both `a,b` are nontriple sites.  Then, for every
   extension `x`,
   \[
                         h_x=0,                           \tag{10}
   \]
   and the common four-site coefficient
   \[
       c_K=[e_{x|K}]H_K(A)                               \tag{11}
   \]
   also vanishes.

**Proof.**  Every term of `X_x` needs two distinct nonerased partners.  If
`|A|<=1`, then `X_x=0`.  Since the erasing pattern is already nonconstant,
the target coefficient is zero, so (8) gives `h_xA_pq=0`.  Invertibility
of `A_pq` proves (9).

If `A={a,b}`, the only possible correction is

\[
 X_x=c_K\big(P_a(x_a)Q_b(x_b)^T
                    +P_b(x_b)Q_a(x_a)^T\big),            \tag{12}
\]

which has rank at most two.  Equation (8) cannot cancel a nonzero multiple
of the rank-three matrix `A_pq`, proving (10).  It then says that (12)
vanishes for all nine choices of `(x_a,x_b)`.

If `c_K ne0`, define

\[
 U_a=\operatorname{span}\{(P_a(i),Q_a(i)):0\le i\le2\}
       \subset V_p\oplus V_q                             \tag{13}
\]

and similarly `U_b`.  The nine equations (12) say

\[
 \Phi(U_a,U_b)=0,
 \qquad
 \Phi((P,Q),(P',Q'))=PQ'^T+P'Q^T.                       \tag{14}
\]

The two-vertex zero-block classification has only three possibilities:
both subspaces are pure toward `p`, both are pure toward `q`, or both are
one-dimensional mixed antipodal lines.  In each case the two star blocks
at each site have zero cross product in all three colours.  Thus both sites
would be triple-zero, contrary to the hypothesis.  Hence `c_K=0`. `QED`

This use of the zero-block classification is exact and site-graded.  It
does not infer termwise vanishing from a sum of matching weights.

## 4. Exhaustion of the residual masks

Use the mask convention

\[
 0=\varnothing,\quad1=\{0\},\quad3=\{0,1\},
 \quad5=\{0,2\},\quad6=\{1,2\},\quad7=\{0,1,2\}.       \tag{15}
\]

For every exact-double mask use its unique missing colour.  At a triple
site use an off-hard colour, chosen so that the erased pattern contains at
least two colours.  Such a choice exists in every row below.  The exact
enumeration is

\[
\begin{array}{c|c|c|c}
\text{masks}&\text{hard assignments}&|K|&
          \text{forced zero coefficients of }H_R\\ \hline
(0,1,1,1,6,6)&1&2&\text{none by Lemma 3.1}\\
(0,1,3,3,6,7)&1&4&9\text{-word slice and }c_K\\
(0,1,3,5,6,6)&1&4&9\text{-word slice and }c_K\\
(0,1,3,5,7,7)&2&4&9\text{-word slice and }c_K\\
(0,1,6,6,6,7)&1&4&9\text{-word slice and }c_K\\
(0,1,6,7,7,7)&6&4&9\text{-word slice and }c_K\\
(0,3,3,3,5,7)&1&5&3\text{-word fibre}\\
(0,3,3,3,7,7)&1&5&3\text{-word fibre}\\
(0,3,3,5,5,6)&1&5&3\text{-word fibre}\\
(0,3,3,5,6,7)&1&5&3\text{-word fibre}\\
(0,3,3,5,7,7)&2&5&3\text{-word fibre}\\
(0,3,5,7,7,7)&6&5&3\text{-word fibre}\\
(0,3,7,7,7,7)&12&5&3\text{-word fibre}.
\end{array}                                               \tag{16}
\]

The counts are `11` four-erasure assignments and `24` five-erasure
assignments, totaling `35`.  In a four-erasure row the two surviving masks
are always `0` and `1`, hence both sites are nontriple and Lemma 3.1(2)
applies.  In a five-erasure row only the unique mask-zero site survives.

For example, (2) has erasing sites `2,3,4,5` and forced colours
`(2,1,0,0)`, proving (3) and the asserted four-site cofactor vanishing.
Row (4) erases sites `1,...,5` with colours `(2,2,1,1,0)`, proving (5).

## 5. Exact local boundary for the last row

The first row of (16) cannot be disposed of by a hidden rank argument.
Let `R={0,...,5}` and write

\[
 A_{pu}=a_u\ell_u^T,\qquad A_{qu}=b_um_u^T.              \tag{17}
\]

Use row-factor pairs

\[
\begin{array}{c|c|c}
u&\ell_u&m_u\\ \hline
0&(1,1,1)&(1,2,4)\\
1,2,3&(1,1,1)&(2,1,1)\\
4,5&e_1&e_2.
\end{array}                                               \tag{18}
\]

Their cross products have zero sets respectively

\[
                         \varnothing,\quad\{0\},\quad\{1,2\}, \tag{19}
\]

so they realize exactly `(0,1,1,1,6,6)` whenever the displayed left
factors are nonzero.  Choose

\[
\begin{array}{c|cccc}
u&0&1&2&3\\ \hline
a_u&e_0&e_1&e_2&e_0\\
b_u&e_0&e_1&e_2&e_2,
\end{array}                                               \tag{20}
\]

and take arbitrary nonzero left factors at `4,5`.

For the nonconstant word

\[
                         x=(0,0,0,1,0,0),                 \tag{21}
\]

the two erased sites are `4,5`, while

\[
\begin{aligned}
 (P_0,Q_0)&=(e_0,e_0),&(P_1,Q_1)&=(e_1,2e_1),\\
 (P_2,Q_2)&=(e_2,2e_2),&(P_3,Q_3)&=(e_0,e_2).            \tag{22}
\end{aligned}
\]

Put one internal scalar cell of weight one on each of

\[
                         (01;00),\qquad(23;01),\qquad(45;00). \tag{23}
\]

At the word (21), this is one perfect matching, so `h_x=1`; its only
nonzero pair cofactors occur at `01,23,45`.  The last pair is erased, and
the correction is

\[
 X_x=2E_{01}+E_{10}+E_{22}+2E_{02}
     =\begin{pmatrix}0&2&2\\1&0&0\\0&0&1\end{pmatrix}, \tag{24}
\]

which is invertible.  Set `A_pq=-X_x`.  Then `A_pq` is invertible and the
exact nonconstant pair-fibre equation is

\[
                         h_xA_{pq}+X_x=0.                 \tag{25}
\]

Thus mask geometry, actual internal hafnian/cofactor compatibility at the
chosen word, and the uncapped pair equation all coexist on the last row.
This is a local coefficient model, not a full realization of the target.

## 6. Exact audit

Run

```text
.venv/bin/python computations/verify_n8_residual_mask_uncapped_vanishing.py
```

The checker regenerates all 36 residual hard assignments, constructs a
nonconstant erasing pattern for exactly 35 of them, verifies the `11+24`
split in (16), and audits (18)--(25) over the integers.
