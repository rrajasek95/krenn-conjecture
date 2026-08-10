# A reduced ternary bar kills augmentation but not the source-labelled companion

## Outcome

The natural reduced ternary comparison does remove the coarse obstruction
seen by the normalized bar augmentation.  It does **not** furnish the
missing physical attaching chain.

Use the selected input word

\[
                 m=01211222
\]

and, at each site, compare output changes with different target colours.
For example, on the two endpoint-2 sites the tensor product of the
differences `2->0 - 2->1` has four endpoints

\[
 e_{00}-e_{01}-e_{10}+e_{11}.                         \tag{1}
\]

Its coefficient sum is zero.  Thus the normalized bar augmentation, and
hence the most favourable coarse ordinary-residue augmentation, vanishes.
Every endpoint also has zero direct action on the ternary GHZ tensor,
because the complete input word (m) is mixed.

The obstruction is source provenance.  The contragredient endpoint of the
local-covariance bar retains the complete output word.  Across the three
possible exposed-site colours there are

\[
                  3\cdot3^7=6561                     \tag{2}
\]

distinct source-labelled companion words.  Cancelling them with the
complete full-nine rows is coefficientwise: the companion matrix is the
(6561) by (6561) identity.  Of those rows, (6558) are mixed target-zero
rows and the remaining three are the separately labelled diagonal anchors
(X_0,X_1,X_2).

The coefficient of the desired all-zero endpoint in (1) is one.  Its
companion can therefore be cancelled only with the (X_0) anchor row.  The
three other words in (1) are mixed and cannot absorb this coefficient.
After the companion cancellation the target is exactly (X_0), even though
the original reduced output operator had target zero.  Cancelling that
target with the old split-cap target gives

\[
                       (-1,Y,0,0)                     \tag{3}
\]

in `(u*Eq,w,target,ores)` coordinates: the desired (Yw) is accompanied by
the same `-u*Eq` defect as before.

Consequently neither a difference `2->0` versus `2->1`, nor any cyclic
three-colour sum, supplies a source-labelled companion word with
`target=ores=0` while retaining the desired `22->00` face.  A cyclic sum

\[
        (e_0-e_1)+(e_1-e_2)+(e_2-e_0)
\]

is literally the zero chain.  A nonzero pure-colour contrast has target
(X_0-X_1), not zero, because the three diagonal anchors occupy independent
target grades.

This is an exact no-go for the standard reduced local-(GL_3) bar together
with every full-nine word row and the old split cap.  It does not exclude a
new source-resolution generator with a genuinely different, source-labelled
ordinary-residue map.

## 1. The exact word module

Let (W) be the set of all ternary eight-site words.  A reduced endpoint
combination is a vector

\[
                       c\in\mathbb Q^W,
             \qquad \epsilon(c)=\sum_{w\in W}c_w=0.   \tag{4}
\]

The standard bar has boundary

\[
                         L(c)-D(c).                    \tag{5}
\]

Local covariance identifies the polynomial values of the two endpoints,
but it does not erase the word label on (D(c)).  A full-nine row with word
(w) cancels precisely the (w)-component of that companion.  Hence the
cancelling coefficient vector is uniquely (c).

Let

\[
 P:\mathbb Q^W\longrightarrow
       \mathbb Q\langle X_0,X_1,X_2\rangle             \tag{6}
\]

be diagonal target projection.  It keeps the coefficients of
`00000000`, `11111111`, and `22222222` and kills all other words.  After
the unique companion cancellation, the target is (P(c)).  Therefore

\[
 \epsilon(c)=0,\quad P(c)=0
       \quad\Longrightarrow\quad c_{00000000}=0.       \tag{7}
\]

The conclusion is almost tautological, but it is load-bearing: the desired
face functional is exactly the (X_0)-target coordinate.  The normalized
augmentation kernel has dimension (6560); imposing all three labelled
target coordinates leaves dimension (6557).  The desired all-zero
coefficient vanishes on this entire invisible subspace.

Retaining source labels is essential.  If the three pure anchors were
collapsed to one unlabelled scalar, the contrast (X_0-X_1) would appear to
cancel.  The actual complete tensor has three distinct pure output words,
and the full mixed rows do not identify them.

## 2. The physical cokernel after target cancellation

In the (X_0) summand, the relevant old physical columns are

\[
\begin{array}{c|rrrr}
 &u e_{\rm Eq}&w&\operatorname {tgt}&\operatorname {ores}\\ \hline
 C_0&-1&0&1&0\\
 T_0&0&-Y&1&0\\
 \rho_0&0&1&0&1.
\end{array}                                             \tag{8}
\]

The companion cancellation contributes (C_0).  Removing its target by
subtracting (T_0) produces (3).  The covector

\[
                         \Lambda=(Y,1,Y,-1)             \tag{9}
\]

kills all three columns in (8), but evaluates to (Y) on the desired
invisible column

\[
                         (0,Y,0,0).                    \tag{10}
\]

Thus the old rank is three and (10) raises it to four.  The (X_1) and
(X_2) blocks are direct source-labelled summands and cannot change this
certificate.

## 3. What the reduced comparison did achieve

The reduction is not vacuous.  It proves that the coarse ordinary-residue
augmentation alone is no longer the problem: (1) has coefficient sum zero.
The failure occurs one step later, when the derivation companion is removed
using honest source rows.  At that point the pure-word coefficient is read
by the target anchor, and target cancellation recreates the Eq defect.

Accordingly, the required new datum is sharper than a reduced bar
augmentation.  It must cancel the pure source-labelled companion without
using the corresponding diagonal target row, or provide an independent
lower face cancelling its Eq defect.  Either datum is precisely outside the
standard local-covariance bar and the old split cap.

## 4. Verification and scope

The standard-library checker
[`verify_h3_reduced_ternary_bar_companion_cokernel.py`](../computations/verify_h3_reduced_ternary_bar_companion_cokernel.py)
enumerates all (6561) word labels as three exposed-site sectors of (2187)
residual words, verifies that all word-changing endpoints act trivially on
the mixed-input GHZ target, checks both reduced endpoint-pair comparisons,
and audits the full companion, mixed-row, anchor, augmentation, and
invisible-subspace ranks.  It also replays the physical rank/cokernel at
three nonzero rational values of (Y).  It pins the certified sitewise
covariance and complete 6,561-row output-cascade artifacts on which the
source-labelled interpretation depends.

The result is a source-labelled finite-module no-go.  It is not a proof
that no larger Spencer/Bianchi resolution exists, not a Krenn
counterexample, and not a proof of the conjecture.
