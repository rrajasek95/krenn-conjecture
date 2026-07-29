# Independent projective closure of every invisible one-cell deformation

## 1. Exact result

Let \(q\) and \(z\) be the sparse eight-site quadratics

\[
\begin{aligned}
q={}&23_{00}+45_{00}+67_{00}
     +01_{11}+36_{11}+57_{11}
     +02_{22}+14_{22}+56_{22},\\
z={}&01_{00}+24_{11}+37_{22}.
\end{aligned}                                                   \tag{1}
\]

Here \(ij_{ab}\) denotes the endpoint-ordered cell having colour \(a\) at
the smaller site \(i\) and colour \(b\) at the larger site \(j\).  Thus

\[
                         zq^{[3]}=\Delta_{8,3}.             \tag{2}
\]

Among all \(28\cdot9=252\) endpoint-colour cells \(e\), exactly \(99\)
satisfy

\[
                         zeq^{[2]}=0.                       \tag{3}
\]

For every such cell and every \(t\in\mathbb C^*\), put
\(q_{e,t}=q+te\).  Then

\[
 zq_{e,t}^{[3]}=\Delta_{8,3},                              \tag{4}
\]

but the same perturbed quadratic has no pair-cap preimage:

\[
 \boxed{\quad
 (a q_{e,t}+4ps)q_{e,t}^{[3]}\ne\Delta_{8,3}
 \quad\text{for every }a\in\mathbb C\text{ and all linear }p,s.
 \quad}                                                     \tag{5}
\]

Thus the fixed-\(q\) obstruction survives every single monomial direction
invisible to the displayed polarized preimage, including endpoint-asymmetric
cells and arbitrary nonzero complex values of \(t\).

The clean-room exact checker is
[verify_polarized_eight_site_single_invisible_cell_projective_closure_independent.py](../computations/verify_polarized_eight_site_single_invisible_cell_projective_closure_independent.py).
It uses no primary exploration or verifier module.

## 2. The \(99\) invisible directions

Every quadratic cell squares to zero in the site-square-zero algebra.  The
divided-power binomial formulas are therefore

\[
\begin{aligned}
q_{e,t}^{[3]}&=q^{[3]}+t\,e q^{[2]},\\
q_{e,t}^{[4]}&=q^{[4]}+t\,e q^{[3]}.
\end{aligned}                                                   \tag{6}
\]

Equation (4) follows from (2), (3), and the first identity in (6), with no
higher powers of \(t\).

The checker scans all \(252\) cells directly.  It expands \(zeq^{[2]}\) by
choosing one of the three \(z\)-cells and two of the nine \(q\)-cells, and
retains only four-edge choices with eight distinct physical endpoints.
Exactly the following eleven physical edges admit no such choice:

\[
 03,04,05,06,07,12,13,15,17,25,34.                       \tag{7}
\]

Physical disjointness is independent of the endpoint colours of \(e\), so
all nine cells on each edge in (7) are invisible.  This gives
\(11\cdot9=99\).  None is already a cell of \(q\).

## 3. Exact coefficient rules

Write

\[
 F_t=q_{e,t}^{[3]},\qquad Q_t=q_{e,t}^{[4]}.
\]

If (5) failed, the identity \(q_{e,t}F_t=4Q_t\) would give

\[
                       aQ_t+psF_t={1\over4}\Delta_{8,3}. \tag{8}
\]

For site-modes \(X,Y\), set

\[
 R_{XY}=p_Xs_Y+s_Xp_Y=\beta(x_X,x_Y),\qquad
 x_X=(p_X,s_X),                                           \tag{9}
\]

with

\[
 \beta((r,u),(s,v))=rv+us.                               \tag{10}
\]

The checker reconstructs every coefficient form of \(psF_t\) and every
coefficient of \(Q_t\) over the exact ring \(\mathbb Z[t]\).  It uses a
mixed top word only when:

1. \(Q_t\) is identically absent on that word;
2. the word has exactly one Gram contributor; and
3. its coefficient is exactly \(1\) or \(t\).

For \(t\ne0\), (8) then forces the corresponding Gram entry to zero.  A
pure word satisfying the same singleton conditions forces its Gram entry
to be nonzero.  No coefficient \(1+t\), cancellation among contributors,
or converse inference from an absent word is used.

## 4. The \(66+33\) exact split

Use the six old distinguished modes

\[
 A=(0,0),\quad B=(1,0),\quad C=(2,1),\quad D=(4,1),\quad
 E=(3,2),\quad F=(7,2).                                  \tag{11}
\]

For \(66\) of the \(99\) cells, the seven old coefficient forms remain
literally unchanged:

\[
 R_{AB},R_{CD},R_{EF}\ne0,\qquad
 R_{AF}=R_{BF}=R_{AC}=R_{CF}=0,                           \tag{12}
\]

and \(Q_t\) remains absent on all seven words.  Hence the old contradiction
applies without modification.

The other \(33\) cells are listed compactly below.  In the second and third
columns, \(ab\) means the cell \(ij_{ab}\) on the physical edge in the first
column.

| edge \(ij\) | all changed endpoint colours \(ab\) | monochromatic subset |
|---|---|---|
| 03 | 00, 01, 22 | 00, 22 |
| 04 | 00, 02, 11 | 00, 11 |
| 05 | 00, 01, 02 | 00 |
| 06 | 00, 01, 02 | 00 |
| 07 | 00, 01, 02, 12, 22 | 00, 22 |
| 12 | 00, 02, 11, 21 | 00, 11 |
| 13 | 00, 01, 22 | 00, 22 |
| 15 | 00 | 00 |
| 17 | 00, 02, 12, 22 | 00, 22 |
| 25 | 10, 11 | 11 |
| 34 | 11, 22 | 11, 22 |

Thus the hard set consists of fifteen endpoint-asymmetric cells and
eighteen monochromatic cells.

## 5. Projective-line closure

Every endpoint of a known nonzero Gram pair in (9) is a nonzero vector.
For such a vector let \(L_X=\mathbb Cx_X\) and define the orthogonality
involution

\[
                           \tau(L)=L^\perp.               \tag{13}
\]

Because \(\beta\) is symmetric and nondegenerate on a two-dimensional
space, \(\tau^2=1\).  A forced zero \(R_{XY}=0\) says exactly
\(L_Y=\tau(L_X)\).  Hence an odd zero cycle forces
\(L=\tau(L)\): its line is isotropic.  Every vertex connected to that cycle
by zero edges then lies on the same isotropic line.  A required-nonzero pair
inside the component is therefore impossible.

The checker implements this statement through graph bipartiteness, not
through union--find closure.  For every contradiction it records and
replays:

- an actual simple odd cycle;
- zero paths from that cycle to both endpoints of a required-nonzero pair;
- the literal singleton coefficient word supporting every zero edge.

It never runs the projective rule through a mode not already known nonzero.
Thus zero vectors cannot create a spurious proportionality inference.

### 5.1 The fifteen asymmetric cells

For every endpoint-asymmetric cell in the table, all three pure words still
have one contributor, so \(R_{AB},R_{CD},R_{EF}\) remain nonzero.  Although
one or more of the four selected mixed coordinates in (12) changes, the
complete mixed-singleton graph supplies another contradiction.  All fifteen
graphs contain a zero triangle and connect one required pair to its
isotropic component.

### 5.2 The eighteen monochromatic cells

If \(e=ij_{cc}\), the two unaffected pure colours still give their old
singleton nonzero pairs.  The affected pure word has exactly two
contributors and \(Q_t\) is absent:

\[
                       R_{U_cV_c}+tR_{X_eY_e}={1\over4}.  \tag{14}
\]

Here \(U_cV_c\) is \(AB,CD,\) or \(EF\), according as \(c=0,1,\) or \(2\).
The new pair in each case is:

| extra cell \(e\) | old pair | new pair \(X_eY_e\) |
|---|---|---|
| \(03_{00}\) | \(01_0\) | \(12_0\) |
| \(03_{22}\) | \(37_2\) | \(27_2\) |
| \(04_{00}\) | \(01_0\) | \(15_0\) |
| \(04_{11}\) | \(24_1\) | \(12_1\) |
| \(05_{00}\) | \(01_0\) | \(14_0\) |
| \(06_{00}\) | \(01_0\) | \(17_0\) |
| \(07_{00}\) | \(01_0\) | \(16_0\) |
| \(07_{22}\) | \(37_2\) | \(23_2\) |
| \(12_{00}\) | \(01_0\) | \(03_0\) |
| \(12_{11}\) | \(24_1\) | \(04_1\) |
| \(13_{00}\) | \(01_0\) | \(02_0\) |
| \(13_{22}\) | \(37_2\) | \(47_2\) |
| \(15_{00}\) | \(01_0\) | \(04_0\) |
| \(17_{00}\) | \(01_0\) | \(06_0\) |
| \(17_{22}\) | \(37_2\) | \(34_2\) |
| \(25_{11}\) | \(24_1\) | \(47_1\) |
| \(34_{11}\) | \(24_1\) | \(26_1\) |
| \(34_{22}\) | \(37_2\) | \(17_2\) |

Equation (14) implies that at least one of its two Gram entries is nonzero.
The checker branches on those two possibilities.  In each branch it uses
the two unaffected pure pairs together with the chosen affected pair, then
restricts the singleton zero graph to their known-nonzero endpoints.  All
\(18\cdot2=36\) branches contain a zero triangle whose isotropic component
contains a required pair.  Thus both alternatives in (14) are impossible.

Together with the fifteen asymmetric cases, this gives \(51\) exact
hard-case certificates.  Every selected odd cycle is a triangle.  The
locked certificate-ledger SHA-256 is

    e1bb9beff9587f2e437f5af2092b6efe64d5d89607051400570a2aed70cac80e

The independent classification ledger has SHA-256

    05561ea470967c3dbff78bb88b4c7038c2102d356f26cb7f53356b14ad6157b7

## 6. Orbit and scope boundaries

The checker searches the full literal \(S_8\times S_3\) action on the
nine-cell support of \(q\).  Its stabilizer is trivial.  Consequently there
is no nontrivial site/colour orbit reduction compatible with this labelled
seed; all \(99\) cells and all \(51\) hard certificates are retained in the
exact ledgers.

This result permits one added cell only.  A sum of two invisible directions
can create cross terms in the polarized cubic and new Gram incidences, so it
is not covered.  Nor does the theorem treat cells outside (7), an arbitrary
ten-cell quadratic unrelated to (1), or an arbitrary eight-site quadratic.
It is a strict local strengthening of the fixed-\(q\) pair-cap obstruction,
not an eight-site Krenn obstruction and not the missing all-even descent.

## 7. Reproduction

Run

    .venv/bin/python computations/verify_polarized_eight_site_single_invisible_cell_projective_closure_independent.py

The exact output is

    independent one-cell invisible-direction closure: PASS
    literal S_8 x S_3 stabilizer of the nine-cell seed is trivial: PASS
    252 endpoint-colour cells scanned; exactly 99 invisible: PASS
    11 invisible physical edges, each with all 9 endpoint colours: PASS
    66 additions retain the old seven coordinates literally: PASS
    15 off-diagonal changed cases close projectively: PASS
    18 diagonal cases and all 36 nonzero branches close projectively: PASS
    hard-case certificate kinds: {'isotropic_component': 51}
    odd-cycle sizes: {3: 51}
    classification SHA-256: 05561ea470967c3dbff78bb88b4c7038c2102d356f26cb7f53356b14ad6157b7
    certificate SHA-256: e1bb9beff9587f2e437f5af2092b6efe64d5d89607051400570a2aed70cac80e
    all 99 families exclude the pair-cap equation for every t != 0: PASS
