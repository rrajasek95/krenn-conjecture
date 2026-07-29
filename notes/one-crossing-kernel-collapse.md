# The one-crossing kernel criterion already gives a six-site collapse

> **Superseding audit (2026-07-26).**  The proved arbitrary-complex
> six-site obstruction, applied to the internal four-site cofactors of any
> ternary five-set, implies that this criterion fails for every aggregate
> edge family and every five-set:
> \(\ker F_1\not\subseteq\ker\delta_U\) universally.  See
> [the universal cofactor-annihilator theorem](five-set-universal-cofactor-annihilator.md).
> The factorization and examples below remain correct, but the proposed
> search for a successful ternary cut is retired.  Full GHZ would instead
> have to contradict the universal target-active kernel witnesses through
> their simultaneous three-/five-crossing responses.

## 1. Outcome

Let \(B=C\mathbin{\dot\cup}U\), where both shores are odd and
\(|U|=5\).  Write \(T_1\) for the part of the matching tensor having
exactly one edge across \(C|U\), and regard its flattening as

\[
                 F_1:V_U^*\longrightarrow V_C.             \tag{1}
\]

For the ternary target write

\[
 D(\beta)=\sum_{r=0}^2\beta(e_r^{\otimes U})g_{C,r},
 \qquad g_{C,r}=e_r^{\otimes C}.                            \tag{2}
\]

Then the apparently necessary condition

\[
                         \ker F_1\subseteq\ker D             \tag{3}
\]

is already sufficient for an exact ordinary six-site response.  One does
**not** have to annihilate \(T_3+T_5\), or even mention its Schmidt space.
The reason is elementary but important: (3) says exactly that the desired
three-row target map factors through the total one-crossing flattening.

This strictly improves the high-sector separation criterion in
[`bounded-response-and-principal-minor-gap.md`](bounded-response-and-principal-minor-gap.md).
The improvement is realized by an exact matching source, not just by an
abstract decomposition of tensors: an eight-site rational binary GHZ source
has a cut on which (3) holds and the collapsed source is exact binary GHZ,
although the high-crossing Schmidt space contains a constant left tensor.

The new test is still not automatic.  The same exact binary GHZ source fails
(3) on (44) of its (56) five-set cuts.  Moreover, the ternary
active-anchor model of
[`total-sector-six-reduction.md`](total-sector-six-reduction.md) fails (3)
on all (56) cuts, while retaining all three normalized constant fibres,
an active \(E_{rr}\) anchor at every vertex and color, and invertible
non-anchor matrices.  That model has one surviving mixed coefficient, so it
does not refute a theorem using the full ternary GHZ equations.  It shows
exactly where such a theorem would have to enter.

The exact audit is
`computations/verify_one_crossing_kernel_collapse.py`.

## 2. Factorization through the one-crossing response

It is useful to separate the two copies of the target flattening.  Let

\[
 \delta_U:V_U^*\longrightarrow\mathbb C^3,
 \qquad
 \delta_U(\beta)=\sum_{r=0}^2
       \beta(e_r^{\otimes U})e_r,                          \tag{4}
\]

and let

\[
 \iota_C:\mathbb C^3\hookrightarrow V_C,
 \qquad \iota_C(e_r)=g_{C,r}.                              \tag{5}
\]

Thus \(D=\iota_C\delta_U\).  Since \(\iota_C\) is injective,

\[
                         \ker D=\ker\delta_U.              \tag{6}
\]

**Lemma 2.1 (one-crossing factor criterion).**  The following are
equivalent.

1. \(\ker F_1\subseteq\ker D\).
2. There is a linear map \(\Phi:V_C\to\mathbb C^3\) such that

   \[
                            \Phi F_1=\delta_U.              \tag{7}
   \]
3. There is a linear map \(\Phi:V_C\to\mathbb C^3\) such that

   \[
       (\Phi\otimes\operatorname{id}_{V_U})T_1
          =\sum_{r=0}^2e_r\otimes e_r^{\otimes U}.          \tag{8}
   \]

**Proof.**  If (7) holds, then \(F_1\beta=0\) implies
\(\delta_U\beta=0\), and (6) gives (3).

Conversely, assume (3).  Define a map on the image of \(F_1\) by

\[
                 \Phi_0(F_1\beta)=\delta_U\beta.           \tag{9}
\]

This is well defined: two preimages differ by an element of \(\ker F_1\),
which lies in \(\ker D=\ker\delta_U\).  Extend \(\Phi_0\) linearly from
\(\operatorname{im}F_1\) to all of \(V_C\).  The extension satisfies (7).
Finally, (7) and (8) are the same equality under the canonical
tensor--flattening correspondence.  \(\square\)

No equality \(T_1+T_3+T_5=\Delta\) was used in this proof.  That equality is
needed only to know which three rows \(\delta_U\) are desired and, in an
application, to derive (3).

## 3. The factor is an ordinary six-site matching tensor

For \(u\in U\), define the complete one-crossing boundary response

\[
 K_u=\sum_{c\in C}\ \sum_{N\in\operatorname{PM}(C\setminus\{c\})}
 \left(\bigotimes_{xy\in N}A_{xy}\right)\otimes A_{cu}
       \in V_C\otimes V_u.                                \tag{10}
\]

Introduce one ordinary vertex \(\star\) with space \(\mathbb C^3\), and put

\[
 Y_{\star u}=(\Phi\otimes\operatorname{id}_{V_u})K_u,
 \qquad
 Y_{uv}=A_{uv}\quad(u,v\in U).                            \tag{11}
\]

**Theorem 3.1 (kernel-only six-site collapse).**  Suppose

\[
                         H_B(A)=\Delta_{B,3}               \tag{12}
\]

and (3) holds for some five-set \(U\).  Then the aggregate tensors (11)
satisfy

\[
                       H_{\{\star\}\cup U}(Y)=\Delta_{6,3}. \tag{13}
\]

**Proof.**  A matching in \(T_1\) has a unique crossing edge \(cu\).  After
removing it, the remaining vertices of \(C\setminus\{c\}\) and
\(U\setminus\{u\}\) are matched independently.  Expanding the left side of
(13) at \(\star\) therefore gives, without dropping any one-crossing term,

\[
 H_{\{\star\}\cup U}(Y)
       =(\Phi\otimes\operatorname{id}_{V_U})T_1.           \tag{14}
\]

Lemma 2.1 turns the right side into the tensor in (8), which is exactly
\(\Delta_{6,3}\).  The sectors \(T_3,T_5\) never enter (14), so no condition
on them is needed.  `QED`

The same proof works for every odd \(|U|=2t-1\), producing an ordinary
\(2t\)-site response.  The five-set case is decisive because the established
six-site obstruction then applies.

## 4. Relation to the older high-sector criterion

Put \(T_h=T_3+T_5\).  The earlier criterion asks for a map satisfying

\[
 (\Phi\otimes\operatorname{id})T_h=0,
 \qquad \Phi(g_{C,r})=e_r.                                \tag{15}
\]

If the full tensor is \(T_1+T_h=\Delta\), (15) implies (8), and hence (3).
Thus high-sector separation is sufficient but stronger than necessary.
The new map is permitted to act nontrivially on \(T_h\); only its action on
\(\operatorname{im}F_1\) matters.

At the level of arbitrary tensor decompositions the strictness is already
visible from \(F_1=2D, F_h=-D\): their sum is \(D\), (3) is an equality of
kernels, but \(\operatorname{im}F_h=\mathcal G_C\).  The next section gives
an exact matching-realizable instance.

## 5. Exact binary strictness and local failure

Use vertices \(1,\ldots,8\) and the following nonzero binary cells:

\[
\begin{array}{c|c}
12&(00)=1,(10)=1\\
34,24&(00)=1\\
13&(10)=-1\\
16,23&(11)=1\\
45&(11)=3/4\\
15,46&(11)=1/2\\
57,68&(00)=1\\
78&(11)=1.
\end{array}                                                \tag{16}
\]

This is the subdivided rational source from
`verify_n8_pair_cap_obstruction.py`; exact enumeration gives

\[
                           H_8=0^{\otimes8}+1^{\otimes8}.  \tag{17}
\]

Take

\[
 C=\{1,2,5\},\qquad U=\{3,4,6,7,8\}.                     \tag{18}
\]

In lexicographic order on the eight binary words of \(C\), one exact factor
map is

\[
 \Phi(e_{000})=e_0,\qquad \Phi(e_{111})=4e_1,
 \qquad \Phi(e_w)=0\quad(w\ne000,111).                   \tag{19}
\]

Direct row reduction gives

\[
 \operatorname{rank}F_1=2,
 \qquad \Phi F_1=\delta_U.                               \tag{20}
\]

The collapsed star has only two nonzero incident matrices,

\[
                     Y_{\star7}=E_{00},
 \qquad             Y_{\star3}=2E_{11}.                 \tag{21}
\]

Together with the old edges internal to \(U\), these give exactly
\(\Delta_{6,2}\).  On the same cut, however,

\[
 \dim\left(\operatorname{span}\{e_{000},e_{111}\}
        \cap\operatorname{LS}_C(T_3)\right)=1,            \tag{22}
\]

and the surviving direction is \(e_{111}\).  Thus the old high-sector
criterion fails while the kernel-only collapse succeeds.

Across all \(\binom83=56\) cuts, exact rational ranks give

\[
\begin{array}{c|c|c}
 \operatorname{rank}F_1&
 \operatorname{rank}\binom{F_1}{\delta_U}-\operatorname{rank}F_1&
 \text{number of cuts}\\ \hline
2&0&12\\
1&1&28\\
0&2&8\\
2&1&4\\
1&2&4.
\end{array}                                                \tag{23}
\]

Hence exact GHZ does not force (3) on a prescribed five-set, even in the
binary case: it fails on (44) of the (56) cuts.  This example still has
twelve successful cuts, so it does not disprove a specifically binary
existence theorem asserting that *some* five-set works.

## 6. A ternary all-cut near-target obstruction

The eight-vertex integer source of
[`total-sector-six-reduction.md`](total-sector-six-reduction.md) has three
edge-disjoint coordinate one-factors \(Q_0,Q_1,Q_2\), with \(E_{rr}\) on
\(Q_r\), and two further one-factors carrying the invertible cyclic
permutation matrices \(S,S^2\).  It has all of the following exact
properties:

* every vertex and color has an active coordinate \(E_{rr}\) anchor;
* all three constant coefficients are exactly one;
* the two non-anchor matrix types are invertible;
* one mixed coefficient, at (00000122), is one, so the source is not
  ternary GHZ.

For this source, exact rational row reduction of the one-crossing flattening
on every three-versus-five cut gives

\[
\begin{array}{c|c|c}
 \operatorname{rank}F_1&
 \operatorname{rank}\binom{F_1}{\delta_U}-\operatorname{rank}F_1&
 \text{number of cuts}\\ \hline
6&3&32\\
9&3&15\\
3&3&8\\
8&3&1.
\end{array}                                                \tag{24}
\]

Thus (3) fails maximally on every one of the (56) cuts: none of the three
constant right rows lies in the row space of \(F_1\).

This leaves a sharply stated all-order bottleneck.  Proving that the
vanishing of every ternary mixed coefficient forces (3) for at least one
five-set would, by Theorem 3.1 and the arbitrary-complex six-site theorem,
prove the whole all-even conjecture.  The anchor model shows that constants,
activity, invertible auxiliary blocks, and freedom to choose \(U\) do not
approach that implication by themselves.  The missing statement must use
the simultaneous mixed equations in a genuinely global way.

## 7. Exact audit

Run

```text
python3.13 computations/verify_one_crossing_kernel_collapse.py
```

The checker reconstructs both sources, verifies the exact binary GHZ
identity, performs all rational row-rank tests, constructs (19)--(21),
enumerates the collapsed six-site tensor, checks the strict high-sector
failure (22), and audits all (56) ternary near-target cuts.
