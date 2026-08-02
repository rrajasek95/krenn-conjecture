# Independent audit of the denominator Tor transgression gate

Audit target: commit `b15d1ad`.  The central Tor, kernel, transgression, and
packet nonmembership calculations are correct.  One local augmented-minor
statement needs a maximal-rank qualification, and the global (I_{11})
condition is insufficient already over fields on lower-rank strata.

This audit does not compute the full source complex, construct a physical
four-face homotopy, prove that the active full-nine quotient is nonzero,
close the overlap theorem, or prove Krenn's conjecture.

## 1. Audited outcome

Independently reconstructing the universal five-site denominator map

\[
 b:R_0^{15}\longrightarrow R_0^{243},\qquad
 d_{v,a}\longmapsto e_a^{(v)}q^{[2]},
 \tag{A1}
\]

and its two rational specializations gives

\[
\begin{array}{c|c|c|c|c|c}
 &\operatorname {rank}b&\operatorname {rank}b_{\rm oth}
 &\dim\ker b&\operatorname {rank}\tau&\dim\operatorname {coker}\tau\\ \hline
\text{direct-free}&7&6&8&4&1\\
\text{tilted}&8&6&7&3&2.
\end{array}
\tag{A2}
\]

Here `oth` denotes the ten columns not indexed by
((v,12112_v)), and (\tau) is projection of the specialized kernel to
the five selected column coordinates.  All five selected coefficients at
the word `12112` vanish on both packets.  Thus the packet conclusion of
`b15d1ad` is exact: scalar vanishing of the five (h_v) does not make the
five-dimensional transgression onto.

The exact field formula

\[
 \operatorname {rank}\tau
 =5-\bigl(\operatorname {rank}b-
              \operatorname {rank}b_{\rm oth}\bigr)
 \tag{A3}
\]

is verified in both cases.  The direct-free and tilted augmented minors are
again (-4) and (8), respectively, on the row and column sets printed in
the primary note.  Those witnesses are valid because the six unselected
columns in each minor already span the complete rank-six unselected image.

The correction is local and precise.  A unit (r\times r) minor of
(b_{\rm oth}) by itself does **not** make membership equivalent to the
vanishing of augmented ((r+1)\)-minors if (b_{\rm oth}) may have rank
larger than (r).  The statement becomes correct if (r) is the local
maximal/constant rank, for example if

\[
 \Delta_r\in S^\times,
 \qquad I_{r+1}(b_{\rm oth})S=0,
 \tag{A4}
\]

or on the universal ten-column open if a (10\times10) minor of
(b_{\rm oth}) is a unit.  No packet conclusion depends on the missing
qualification.

## 2. Independent universal reconstruction

For a word (w\in\{0,1,2\}^5), the audit rebuilds every entry directly as

\[
 [e_w]b(d_{v,a})=
 \delta_{w_v,a}
 \sum_{M\in\operatorname {Match}(D\setminus\{v\})}
        \prod_{ij\in M}q_{ij}^{w_iw_j}.
 \tag{A5}
\]

No matrix, kernel, or rank datum is imported from the primary checker.  At
the independent integral specialization

\[
 q_{ij}^{ab}=2+131i+29j+11a+5b,
 \tag{A6}
\]

the same fifteen word rows selected by exact elimination support a full
minor of value

\[
139281539437818783919164219631300207644007326361143791616000000000
\ne0.
\tag{A7}
\]

The ten unselected columns support an independent minor of value

\[
805044475597749235674596440940876188626217574400000\ne0.
\tag{A8}
\]

These values differ from the primary witnesses because (A6) is a different
specialization.  They independently prove universal ranks fifteen and ten.
Since (R_0) is a domain and the source of (A1) has rank fifteen, the
universal kernel is zero.  Therefore

\[
0\longrightarrow R_0^{15}\mathop{\longrightarrow}^{b}R_0^{243}
 \longrightarrow Q_0\longrightarrow0
\tag{A9}
\]

is a free resolution, and for every (R_0)-algebra (S),

\[
 \operatorname {Tor}_1^{R_0}(Q_0,S)\cong\ker(b\otimes S).
 \tag{A10}
\]

Polynomial extension to the full eight-site cell ring is flat, so the same
resolution argument justifies the full-ring formula in the primary note.

## 3. Exact transgression and kernel calculation

Write (b=[b_{\rm sel}\ b_{\rm oth}]).  A selected vector (y\in S^5)
is in the image of the cap projection on (\ker b_S) exactly when some
(z\in S^{10}) satisfies

\[
 b_{\rm sel}y+b_{\rm oth}z=0.
\tag{A11}
\]

Consequently the exact criterion

\[
 \operatorname {im}\tau_S
 =\ker\left(S^5\longrightarrow
       \operatorname {coker}(b_{\rm oth}\otimes S)\right)
\tag{A12}
\]

and the surjectivity/membership equivalence in `b15d1ad` are correct.  Over a
field, the rank of the induced map in (A12) is

\[
 \operatorname {rank}b-\operatorname {rank}b_{\rm oth},
\tag{A13}
\]

which proves (A3).

The independently reduced packet kernels are

\[
\begin{aligned}
\ker b_{\rm df}=\langle{}
 &d_{10},d_{11},d_{12},d_{30},d_{31},d_{32},
 -d_{22}+d_{41},-2d_{22}+d_{52}\rangle,\\
\ker b_{\rm tilt}=\langle{}
 &d_{10},d_{11},d_{12},d_{30},d_{31},d_{32},
 -d_{22}+d_{41}\rangle.
\end{aligned}
\tag{A14}
\]

Projection to the selected coordinates
((d_{11},d_{22},d_{31},d_{41},d_{52})) gives

\[
\begin{aligned}
\operatorname {im}\tau_{\rm df}
 &=\langle\omega_1,\omega_3,-\omega_2+\omega_4,
                         -2\omega_2+\omega_5\rangle,\\
\operatorname {im}\tau_{\rm tilt}
 &=\langle\omega_1,\omega_3,-\omega_2+\omega_4\rangle.
\end{aligned}
\tag{A15}
\]

The annihilating covectors are, up to nonzero scalar,

\[
 (0,1,0,1,2)
\tag{A16}
\]

in the direct-free case and

\[
 (0,1,0,1,0),\qquad(0,0,0,0,1)
\tag{A17}
\]

in the tilted case.  Only (\omega_1) and (\omega_3) occur individually
in either image.  This reproduces every load-bearing numerical statement in
Sections 1 and 5 of the primary note.

## 4. Correct Fitting and augmented-minor scope

If every selected column belongs to the unselected image, then all fifteen
columns of (b) are generated by ten columns.  Therefore

\[
                         I_{11}(b)S=0
\tag{A18}
\]

is a correct necessary condition.  It is not sufficient in general.  The
two packets sharpen the scope: they have (\operatorname {rank}b<11), so
(A18) holds over the reduced field (\mathbb Q), while (\tau) is not
onto.  Thus insufficiency is not confined to nonreduced rings; it already
occurs whenever the unselected block drops below rank ten.

On an open where a (10\times10) unselected minor is a unit, the ten
unselected columns form a direct summand of their row module.  For a selected
column (c), Cramer's rule gives

\[
 c\in\operatorname {im}b_{\rm oth}
 \iff
 \text{all }11\times11\text{ minors of }[b_{\rm oth}\ c]
 \text{ vanish}.
\tag{A19}
\]

More generally, (A19) holds with (10) replaced by (r) on a
constant-rank-(r) stratum satisfying (A4).  The constant-rank hypothesis
is necessary.  A two-dimensional counterexample is

\[
 b_{\rm oth}=\begin{pmatrix}1&0\\0&1\end{pmatrix},
 \qquad c=\binom01,
 \qquad r=1.
\tag{A20}
\]

The upper-left (1\times1) minor is a unit and
(c\in\operatorname {im}b_{\rm oth}), but adjoining (c) to the first
pivot column gives determinant one.  This is the exact flaw in the sentence
that assumes only an arbitrary unit (r\times r) minor.

The packet augmented minors do not suffer from (A20).  In both packets the
six displayed unselected columns have rank six, equal to the complete
unselected rank.  Adding `d22` raises the direct-free rank to seven with
minor (-4); adding `d22,d52` raises the tilted rank to eight with minor
(8).  They are maximal-rank nonmembership witnesses.

## 5. Scope of what was and was not audited

The curvature values (-1/4) and (-5/2) are external metadata of the two
previously certified eight-site packets.  The five-site denominator matrix
contains no endpoint entries and therefore cannot derive (\kappa); both
the primary and independent checker use only the already established fact
that these values are nonzero.  Curvature localization is flat, so the
claim that it cannot create the kernel in (A10) is correct.

Likewise, the five-dimensional map (a:C^1\to W) is a labelled diagnostic
cap-coordinate projection.  The audit proves the Tor gate for that map.  It
does not promote (W) or its basis to physical full-source chains.  A proof
still has to construct source-provenant columns or prove the five module
memberships after imposing the complete simultaneous full-nine ideal.

The guards have six and seven full `pq` EqSystem failures and are not points
of the full source scheme.  Hence (A2) is a counterguard to implications from
the retained scalar denominator data, not evidence that the intended
full-nine quotient has the same transgression ranks.  The primary note
states this limitation correctly.

The dependency-free checker
[`audit_h3_denominator_tor_transgression_fitting_gate_independent.py`](../computations/audit_h3_denominator_tor_transgression_fitting_gate_independent.py)
uses a different universal specialization, reconstructs both sparse packet
matrices from raw q-cells, computes kernels and cokernels by exact rational
elimination, derives maximal augmented minors algorithmically, and freezes
the local-minor counterexample (A20).  It has no imports from the primary
checker.
