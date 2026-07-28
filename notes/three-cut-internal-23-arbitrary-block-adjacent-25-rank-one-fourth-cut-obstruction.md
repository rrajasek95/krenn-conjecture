# The adjacent rank-one lines \(E_{10},E_{20}\) have a uniform fourth-cut obstruction

## 1. Status and scope

Keep the seven internal cells

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
01&E_{00}&45&E_{00}&02&E_{11}\\
14&E_{11}&04&E_{22}&13&E_{22}\\
35&E_{10},
\end{array}
\]

let \(A_{23}=X\in\operatorname{Mat}_{3\times3}(\mathbb C)\) be arbitrary,
and take, for one moved colour \(c\in\{1,2\}\),

\[
        A_{25}=E_{00}+tE_{c0}=(e_0+t\,e_c)\otimes e_0.      \tag{1}
\]

The exact verifier excludes a fourth complete cut \(z\in\{0,1,5\}\)
simultaneously for both directions, for **every** \(X\in
\operatorname{Mat}_{3\times3}(\mathbb C)\) and **every** \(t\in\mathbb C\)
including \(t=0\), with both boundary stars and \(A_{67}\) arbitrary.
Unlike every earlier one-cell theorem on this interior, the proof uses no
torus normalization, no first-nonzero charts, and no case split on
\(t\): all certificates are polynomial identities and characteristic-zero
unit ideals in \(\mathbb Q[x_{00},\dots,x_{22},t]\) (or in the linear
parameters of one explicit degenerate locus).  The \(t=0\) fibre agrees
with the previously audited arbitrary-\(A_{23}\) theorem but is proved
here directly.

This remains a local statement for the displayed fixed six-site interior.
It does not allow arbitrary \(A_{25}\), and it does not prove the global
Krenn conjecture.  With it, the entire nine-cell one-parameter frontier
\(A_{25}=E_{00}+tE_{cd}\) is closed: \(E_{11}\), the four off-diagonal
lines, \(E_{22}\), and now \(E_{10},E_{20}\).

The consolidated primary verifier is

- [the rank-one exact verifier](../computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_rank_one_fourth_cut_obstruction.py).

Its supporting modules are

- [the direction machinery](../computations/explore_three_cut_internal_23_adjacent_25_rank_one_directions.py);
- [the \(W\)-structure certificates](../computations/derive_three_cut_internal_23_adjacent_25_rank_one_w_structure.py);
- [the shared-star unit ideals](../computations/test_three_cut_internal_23_adjacent_25_rank_one_star_ideals.py).

## 2. Rank-one geometry and the dependent torus weight

The moving block (1) is rank one: site \(5\) always receives colour
\(0\).  Two consequences shape the whole proof.

First, the torus weight of \(t\) is dependent,
\(\operatorname{wt}(t)=\operatorname{wt}(x_{c0})-\operatorname{wt}(x_{00})\),
so the \(E_{22}\)-style scheme "normalize \(t=1\), then chart the
supports of \(X\)" is unavailable; the cross-ratio moduli
\(tx_{00}/x_{c0}\) predicted by the previous audit are real.  The proof
below simply never normalizes anything.

Second, every cylinder whose cut keeps sites \(2\) and \(5\) inherits
three exact column relations from the factorization (1): inserting
\(v=e_0+te_c\) at site \(2\) equals a fixed-cell expansion.  For the cut-3
cylinder the relation in each cut-colour block reads

\[
   C(2,0)+t\,C(2,c)=C(4,0),                              \tag{2}
\]

and cuts \(0,1,4\) have four-term analogues.  The three relations live in
disjoint cut-colour blocks, so their independence is witnessed by an
identity minor: \(\dim\ker M_3\ge3\) and \(\dim\ker M_4\ge3\) for every
\(X,t\), including \(t=0\).  Edges \(23\) and \(25\) share site \(2\), so
no matching term mixes \(X\) and \(t\); the literal eight-site
endpoint-order audit from the \(E_{22}\) verifier is repeated verbatim
for both directions.

## 3. The two-cylinder space \(W=C_2\cap C_3\)

Neither \(C_2\) nor \(C_3\) involves \(A_{23}\) (their cofactors never
use edge \(23\)), and \(C_2\) does not involve \(t\); the verifier
asserts this \(X\)-freeness literally.  Over \(\mathbb Q[t]\):

* the \(87\)-column simultaneous representation matrix of
  \(C_2,C_3\) (three duplicate \(C_2\) columns omitted) has a constant
  \(72\times72\) minor of determinant \(-1\) for both directions, so its
  kernel is at most \(15\)-dimensional for every \(t\);
* the \(C_2\) map is injective (a constant rank-\(42\) matrix), and
  \(\ker M_3\ge3\) by (2); hence \(\dim W\le15-3=12\);
* twelve explicit members with exact representations in both cylinders
  span \(W\): the nine coordinate tensors \(e_{ab}=[00ab00]\) (literal
  columns of both cylinders), the two sigma tails

  \[
  \sigma_1=[001{,}1{,}1{,}0]\text{-pair}:\;
  [000110]+t[00c110],\qquad
  \sigma_2=[000120]+t[00c120],                            \tag{3}
  \]

  and the plane tensor

  \[
  D=[111110]+[121200]+[220220]+t\,[22c220].               \tag{4}
  \]

  Their restriction to the twelve words
  \(e_{ab},[000110],[000120],[121200]\) is the identity matrix, so
  \(W=\operatorname{span}\{e_{ab},\sigma_1,\sigma_2,D\}\) with exact
  coefficient readout, uniformly in \(t\).

The direct tensor obeys the tail identity

\[
        H(X,t)=\sum_{a,b}x_{ab}\,e_{ab}+D,                \tag{5}
\]

and \(H\) has an exact direct representation in all six cylinders.  Note
\(D\) is precisely the \(A_{23}=0\) matching tail, the analogue of the
\(E_{22}\) ten-space tail \(T\).

## 4. Probe identities: the normals through every rank jump

All probe computations keep the nine \(x_{ab}\) and \(t\) symbolic.

**Cut 5.**  Restrict the \(45\) raw \(C_5\) columns to the probe words
\(e_{ab}\), \([000110]\), \([00c110]\), \([000120]\), \([00c120]\),
\([121200]\), \([121210]\), \([121220]\).  Exactly three columns
survive:

\[
\begin{array}{c|l}
\text{column}&\text{restriction}\\ \hline
12&(x_{00},\dots,x_{22};\,0,0,0,0;\,1;\,0,0)\\
13&[000110]\mapsto x_{01},\;[00c110]\mapsto x_{c1},\;[121210]\mapsto1\\
14&[000120]\mapsto x_{01},\;[00c120]\mapsto x_{c1},\;[121220]\mapsto1.
\end{array}                                               \tag{6}
\]

No member of \(W\) meets \([121210]\) or \([121220]\), so a vector of
\(W\cap C_5\) forces \(y_{13}=y_{14}=0\); the sigma coordinates then
vanish, the \(e\)-coordinates equal \(y_{12}x_{ab}\), and the
\([121200]\)-coordinate equals \(y_{12}\).  With (5),

\[
        C_2\cap C_3\cap C_5=\langle H\rangle
        \qquad\text{for all }X,t.                         \tag{7}
\]

Intersecting further with \(C_4\) cannot enlarge this line, so the cut-5
normal claim holds with no chart and no rank-jump caveat.

**Cuts 0 and 1.**  For \(z\in\{0,1\}\), no raw \(C_z\) column meets any
of the four sigma words at all, and the nine \(e\)-words are met only by
column \(0\), whose restriction is exactly \((x_{ab})\).  Hence for
\(\omega\in W\cap C_z\) the sigma components vanish and the \(e\)-part is
proportional to \(x\); by (5), \(\omega\in\langle H,D\rangle\).
Conversely \(H\) lies in every cylinder and \(D\) has the two-column
exact representations

\[
 D=\text{col}_{19}+\text{col}_{41}\in C_0,\qquad
 D=\text{col}_{25}+\text{col}_{38}\in C_1,                \tag{8}
\]

so

\[
   C_2\cap C_3\cap C_z=\langle H,D\rangle\qquad(z=0,1),
   \qquad\text{for all }X,t.                              \tag{9}
\]

## 5. The degenerate locus: \(D\in C_4\) exactly on \(D_{\mathrm{full}}\)

Because the four-cylinder intersection for a final cut \(z\) is literally
\((C_2\cap C_3\cap C_z)\cap C_4\) and \(H\in C_4\), equation (9) reduces
cuts \(0,1\) to one question: when does \(D\) lie in \(C_4\)?

Define, for direction \(c\) (writing \(\bar c\) for the other nonzero
colour),

\[
 D_{\mathrm{full}}
 =V\bigl(t x_{00}-x_{c0},\;t x_{02}-x_{c2},\;
        x_{\bar c0},\;x_{\bar c2}\bigr)
 =\bigl\{\,X=v\otimes r_0+m\otimes e_1\,\bigr\},          \tag{10}
\]

with \(v=e_0+te_c\), \(r_0\in\mathbb C^3\),
\(m\in0\oplus\mathbb C^2\); the second description is an exact linear
parameterization by \((r_0,w,u)\), verified both ways.

* **On \(D_{\mathrm{full}}\):** an explicit eight-column combination of
  raw \(C_4\) columns with coefficients polynomial in
  \((r_0,w,u,t)\) equals \(D\); e.g. for \(E_{10}\)
  \(\{6\mapsto-a_1,\,7\mapsto-a_1t-w,\,8\mapsto-u,\,9\mapsto-a_0,\,
  11\mapsto-a_2,\,12,19,32\mapsto1\}\).
* **Off \(D_{\mathrm{full}}\):** \(\operatorname{rank}C_4\le42\)
  everywhere by the three relations (2), while six \(43\times43\) minors
  of \([C_4\,|\,D]\) have the factored determinants (direction
  \(E_{10}\))

  \[
  \begin{array}{ll}
  x_{10}^6\,(tx_{00}-x_{10})^3,&
  -x_{12}^6\,(tx_{02}-x_{12})^3,\\
  x_{20}^9,\;-x_{22}^9,&
  x_{00}^6\,(tx_{00}-x_{10})^3,\;
  -x_{02}^6\,(tx_{02}-x_{12})^3,
  \end{array}                                             \tag{11}
  \]

  and mirror-image forms for \(E_{20}\).  Eight Rabinowitsch
  certificates (one per direction and per generator \(g\) of (10)),
  each a unit Gröbner basis of
  \((\text{the six determinants},\,1-y\,g)\) over
  \(\mathbb Q[x_{00},\dots,x_{22},t,y]\), prove that the common zero set
  of the minors lies inside \(D_{\mathrm{full}}\).  A nonvanishing
  \(43\)-minor forces \(\operatorname{rank}[C_4|D]=43>42\ge
  \operatorname{rank}C_4\), so \(D\notin C_4\) at every point off
  \(D_{\mathrm{full}}\).

Combining (7), (9), and this characterization: for every \(X,t\),

\[
 C_2\cap C_3\cap C_4\cap C_z=
 \begin{cases}
 \langle H\rangle,& z=5,\ \text{always};\\
 \langle H\rangle,& z\in\{0,1\},\ (X,t)\notin D_{\mathrm{full}};\\
 \operatorname{span}\{H,D\},& z\in\{0,1\},\ (X,t)\in D_{\mathrm{full}}.
 \end{cases}                                              \tag{12}
\]

By (5) the span in the third case is a plane exactly when \(X\ne0\); at
\(X=0\) it degenerates to the line \(\langle H\rangle=\langle D\rangle\),
consistent with the exact zero-support normals.  The star packet below
covers the span case uniformly, so the distinction never needs a case
split.

## 6. Exact shared-star ideals

Retain target colours \(0,1\), both ordered off-diagonal fibres, and the
same \(72\) endpoint-ordered star variables as the earlier one-cell
theorems.  The arbitrary \(A_{67}\) term in each fibre is a multiple of
\(H\), hence absorbed by every normal in (12).  A solution of the full
three-colour system restricts to this two-colour packet.

Two program shapes close both cases of (12):

* **Line packet** (all normals \(\langle H\rangle\)): all nine
  \(x_{ab}\) and \(t\) remain polynomial variables.  To bound Gröbner
  time the packet is run twice, once with \(x_{00}\) inverted by a
  Rabinowitsch variable and once with \(x_{00}=0\) substituted; the two
  runs still cover every complex point with no normalization.
* **Plane packet** (normals \(\langle H,D\rangle\) on
  \(D_{\mathrm{full}}\)): blocks on the parameterization (10) with
  \((a_0,a_1,a_2,w,u,t)\) polynomial variables and two scalar families,
  one for \(H\) and one for \(D\).

All six programs (three per direction) have reduced Gröbner basis
\([1]\) over characteristic zero.  A unit ideal over
\(\mathbb Q[\text{parameters},\text{scalars},\text{stars}]\) specializes
to every complex parameter point, so every special complex cancellation
- including the cross-ratio locus, all coordinate vanishing, and
\(t=0\) - is covered.

The frozen rank-certificate ledger is

    72a5c3f2af1fe08fae615009be255eb02f1217b88a2f8edf1a8c1d885b85fde0

and the frozen ideal ledger over the \(14\) Singular jobs (eight radical
certificates, four line-packet halves, two plane packets) is

    f5e5f91e56d29c86d4e0db85eb9a70a36b5f65488b0c8feb20cf25edd0385154

The measured line-packet times are \(994/434\) seconds for \(E_{10}\) and
\(878/424\) seconds for \(E_{20}\) (invertible/zero halves).

## 7. Reproduction and audit status

From the repository root, run

    uv run python computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_rank_one_fourth_cut_obstruction.py

The default run re-verifies, for both directions: the endpoint-order
audit, the kernel relations, the \(W\)-basis with its unit minors and
memberships, the tail identity (5), the three probe tables, the
parameterization (10), the six \(C_4\) minors with their factored
determinants, the on-locus representation of \(D\), and then reruns all
\(14\) characteristic-zero Singular jobs (eight radical certificates and
six star packets).

An independent clean-room audit with different orderings is required
before this note is promoted to audited-theorem status; see the route
registry entry for the current status.
