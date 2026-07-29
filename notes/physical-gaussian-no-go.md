# Physical Gaussian states add no constraint to the aggregate model

## Outcome

The physical pure-Gaussian formulation is exactly equivalent, up to one
irrelevant common scalar, to the arbitrary complex aggregate-matrix
formulation.  In particular, covariance positivity cannot supply an extra
hypothesis: every finite collection of arbitrary complex endpoint tables
lies on a ray of valid pure bosonic Gaussian states.  Projecting the Gaussian
annihilator equations onto one photon at every spatial site gives only the
usual hafnian deletion recurrence.  If one sandwiches a linear annihilator
between the postselection projectors, it vanishes identically.

Thus a Gaussian-state proof may still be useful if it discovers a new
algebraic identity for arbitrary complex symmetric Bargmann matrices, but
physicality, normalization, covariance positivity, and the standard linear
nullifiers do not narrow the Krenn problem.  Two exact constructions below
show sharply that pure Gaussian states can produce postselected binary GHZ
states at every even order and a ternary GHZ state at order four.

## 1. From arbitrary endpoint tables to a physical pure Gaussian state

Let `B={1,...,n}` and let `A_uv` be an arbitrary complex `3 by 3` table for
each `u<v`.  Endpoint order is retained: no symmetry is assumed of the
individual table.  On the `3n` bosonic modes `(v,i)`, form the global matrix

\[
 Z_{(u,i),(v,j)}=A_{uv}(i,j),\qquad
 Z_{(v,j),(u,i)}=A_{uv}(i,j)                              \tag{1}
\]

for `u<v`, and put all same-site blocks equal to zero.  This is a complex
symmetric `3n by 3n` matrix.  Notice that global symmetry says that the
reverse block is `A_uv^T`; it does **not** say that `A_uv=A_uv^T`.  Hence (1)
retains completely arbitrary asymmetric endpoint colours.

For every scalar `t` satisfying

\[
                         0<|t|\,\|Z\|_2<1,                \tag{2}
\]

the vector

\[
 |\Psi_t\rangle=
 \det(I-|t|^2ZZ^\dagger)^{1/4}
 \exp\!\left({t\over2}\,a^\dagger Za^\dagger\right)|0\rangle
                                                                  \tag{3}
\]

is a normalized zero-mean pure bosonic Gaussian state.  This can be checked
without invoking any physical convention.  A Takagi factorization
`Z=U diag(s_1,...,s_(3n)) U^T` turns the unnormalized vector into a product
of single-mode vectors

\[
                 \exp\!\left({t s_k\over2}(b_k^\dagger)^2\right)|0\rangle.
\]

The squared norm of the `k`-th factor is
`(1-|t|^2s_k^2)^(-1/2)`.  Their product is
`det(I-|t|^2ZZ^dagger)^(-1/2)`, which proves (3).  Conversely, this is the
usual Bargmann matrix parametrization of a zero-mean pure Gaussian state.

Let `Pi_v` project the three modes at site `v` onto total occupation one and
put `Pi=prod_v Pi_v`.  Write

\[
       |c\rangle=\prod_{v=1}^n a_{v,c(v)}^\dagger|0\rangle.
\]

Expanding the exponential in (3), a term contributing to `|c>` must pair
the `n` selected modes.  The contribution of a pairing `M` is the product
of the corresponding entries of (1).  Therefore, for `n=2m`,

\[
 \Pi|\Psi_t\rangle=
 \det(I-|t|^2ZZ^\dagger)^{1/4}t^m
       \sum_{c:B\to\{0,1,2\}}H_A(c)|c\rangle,              \tag{4}
\]

where

\[
 H_A(c)=\sum_{M\in {\rm PM}(B)}
                    \prod_{uv\in M}A_{uv}(c(u),c(v))       \tag{5}
\]

is exactly the aggregate matching tensor.  There are no hidden factorials:
the factor `1/(2^m m!)` in the exponential is cancelled by the orders and
orientations of the `m` commuting pairs.  Same-site covariance blocks, had
we allowed them, could not occur in a term with one photon per site and are
irrelevant.

Parallel decorated sources are also retained exactly.  For fixed endpoints
and endpoint colours their weights add to one entry of `A_uv`; expanding a
product of aggregate entries in (5) is the sum over all choices of the
original parallel sources.

It follows immediately from (4) that

\[
 H_A=\Delta_{n,3}\quad\Longrightarrow\quad
 {\Pi|\Psi_t\rangle\over\|\Pi|\Psi_t\rangle\|}
 =e^{i\theta}{1\over\sqrt3}\sum_{i=0}^2|i\rangle^{\otimes n}. \tag{6}
\]

The success probability is

\[
 3|t|^n\det(I-|t|^2ZZ^\dagger)^{1/2}>0.                  \tag{7}
\]

Conversely, if the conditional vector in (4) is a nonzero scalar multiple
of the displayed GHZ vector, then `H_A=lambda Delta_(n,3)` for some
`lambda!=0`.  Replacing every table by `sA_uv`, where `s^m=lambda^(-1)`,
gives `H_(sA)=Delta_(n,3)`.  One may then choose a new sufficiently small
physical scale `t`.  We have proved the following exact equivalence.

**Proposition 1 (physical-ray equivalence).**  There is an arbitrary-complex
aggregate realization of `Delta_(n,3)` if and only if a zero-mean pure
bosonic Gaussian state on three modes per site has a nonzero one-photon per
site projection proportional to `GHZ_(n,3)`.  The covariance may be required
to have zero same-site blocks.  Every algebraic aggregate candidate gives a
whole punctured interval of physical Gaussian states by (2).

In particular, the contraction condition on a physical Bargmann matrix is
not an obstruction.  It can always be imposed by the scalar `t`, while all
ratios inside the degree-`n` postselected sector are unchanged.

## 2. What the Gaussian annihilators say after postselection

Put

\[
 Q={1\over2}a^\dagger(tZ)a^\dagger,
 \qquad |\Psi_t^{(2r)}\rangle={Q^r\over r!}|0\rangle,       \tag{8}
\]

temporarily omitting the common normalization.  The standard Gaussian
nullifiers

\[
 L_\alpha=a_\alpha-\sum_\beta(tZ)_{\alpha\beta}a_\beta^\dagger,
 \qquad L_\alpha|\Psi_t\rangle=0                           \tag{9}
\]

follow directly from `[a_alpha,Q]=sum_beta(tZ)_(alpha beta)
a_beta^dagger`.  In fixed number sectors, (9) is precisely

\[
 a_\alpha|\Psi_t^{(2r)}\rangle
 =\sum_\beta(tZ)_{\alpha\beta}a_\beta^\dagger
                         |\Psi_t^{(2r-2)}\rangle.           \tag{10}
\]

There are two exact reasons that (10) does not close on the postselected
GHZ sector.

First, for every mode `alpha=(v,i)`,

\[
                  \Pi a_\alpha\Pi=0,
          \qquad  \Pi a_\alpha^\dagger\Pi=0.              \tag{11}
\]

Indeed, the first operator changes the occupation at `v` from one to zero
and the second changes it from one to two.  Consequently

\[
                         \Pi L_\alpha\Pi=0                 \tag{12}
\]

is an operator identity, independent of both the state and the covariance.
A linear nullifier sandwiched into the code yields only `0=0`.  Any
nontrivial use of (9) necessarily passes through a sector with a hole or a
collision, on which the desired postselection places no condition.

Second, extracting collision-free coefficients from one application of
(10) gives exactly the ordinary hafnian recurrence.  For an even vertex set
`S`, let `H_S(c)` denote (5) for the covariance induced on `S`, with
`H_empty=1`.  Pairing (10) with the Fock bra selecting one prescribed mode
at every vertex of `S\setminus{v}` gives

\[
 H_S(c)=\sum_{w\in S\setminus\{v\}}
       Z_{(v,c(v)),(w,c(w))}H_{S\setminus\{v,w\}}(c).       \tag{13}
\]

This is just expansion of a perfect matching at `v`.  The top-order
identity `H_B=Delta_(n,3)` prescribes none of the smaller induced tensors on
the right side.  Iterating (10), or using quadratic products of nullifiers,
generates the usual Wick/hafnian recurrences among these same unconstrained
sectors.  Thus it cannot eliminate the auxiliary sectors without proving a
new algebraic statement about arbitrary tables—the original substantive
problem.

**Proposition 2 (direct nullifier non-closure).**  Sandwiching any standard
linear Gaussian annihilator into the one-photon-per-site code gives the
tautology (12).  Extracting a nonzero equation from one nullifier requires
leaving that code; on collision-free coefficients the resulting equation is
exactly (13), involving unprescribed smaller sectors.  More elaborate
elimination could help only by producing a new algebraic identity among
arbitrary entries of `Z`; (9) itself supplies no extra physical hypothesis.

This also explains why purity gives no extra relation here.  Purity is
already built into (3) for every scaled aggregate matrix; it does not impose
a relation among the tables beyond global symmetry (1).

## 3. There is no positive-distance physical obstruction

The exact border degeneration in `notes/tensor-route.md` has an immediate
physical interpretation.  For every even `n>=6` it supplies a Laurent
family of finite aggregate matrices `Z(epsilon)`, `epsilon!=0`, such that

\[
 H_{Z(\epsilon)}=\Delta_{n,3}+O(\epsilon)                 \tag{14}
\]

coefficientwise as `epsilon -> 0`.  Some entries of `Z(epsilon)` diverge,
which has no physical consequence.  Choose any positive scalar

\[
 0<r(\epsilon)<{1\over 2\|Z(\epsilon)\|_2}.               \tag{15}
\]

Then `r(epsilon)Z(epsilon)` is a valid pure-Gaussian Bargmann matrix by
Section 1, and its normalized postselected vector is exactly the
normalization of (14), because the common factor `r(epsilon)^(n/2)` cancels.
Consequently

\[
 {\Pi|\Psi_{r(\epsilon)Z(\epsilon)}\rangle
       \over\|\Pi|\Psi_{r(\epsilon)Z(\epsilon)}\rangle\|}
 \longrightarrow {1\over\sqrt3}\sum_{i=0}^2|i\rangle^{\otimes n}. \tag{16}
\]

Thus ternary GHZ belongs to the ordinary norm closure of physically valid
conditional pure-Gaussian outputs at every relevant order.  Along this
particular realization the heralding probability can tend to zero; this is
why the conclusion does not assert exact preparation.  It does show that a
compactness argument, a uniform fidelity gap, or any other robust
positive-distance separation cannot prove exact nonattainability.  An
analytic proof would have to identify a non-closed-image equality case.

## 4. Sharp counterexamples to broad Gaussian no-GHZ claims

The failure above is not merely formal.  Pure Gaussian states can have
exact multipartite GHZ states as their one-photon-per-site sectors.

Let `n>=4` be even.  On a cycle with vertices `1,...,n`, let

\[
 P_0=12|34|\cdots|(n-1)n,
 \qquad
 P_1=23|45|\cdots|n1.                                    \tag{17}
\]

Put a unit covariance entry between colour-zero modes on every edge of
`P_0`, a unit entry between colour-one modes on every edge of `P_1`, and no
other entries.  A supported postselected colouring has its set of zero
vertices closed under `P_0` and its set of one vertices closed under `P_1`.
Equivalently, membership in the zero set is constant across every edge of
`P_0 union P_1`.  That union is the connected cycle, so the colouring is
all zero or all one.  Both have coefficient one.  Hence

\[
                         H_A=|0\rangle^{\otimes n}
                              +|1\rangle^{\otimes n}        \tag{18}
\]

for every even `n>=4`.  At `n=2`, put the two colours on the same spatial
pair of vertices; the same conclusion is immediate.  Scaling as in (2)
makes this a valid normalized pure
Gaussian state with an exact postselected `GHZ_(n,2)` sector.

At `n=4`, take the three one-factors

\[
 P_0=12|34,\qquad P_1=13|24,\qquad P_2=14|23               \tag{19}
\]

and put unit covariance entries between colour-`i` modes on the edges of
`P_i`.  Two edges from different one-factors cannot be disjoint, so the only
supported postselected terms are the three constant colourings, each with
coefficient one.  Thus a scaled version of this covariance is a physical
pure Gaussian state whose four-site sector is exactly `GHZ_(4,3)`.

These examples refute any no-go based only on Gaussianity, purity, linear
annihilators, photon-number parity, or the entanglement type of the
postselected state.  A successful Gaussian-language proof for `n>=6` must
instead exploit a genuinely ternary algebraic compatibility identity for
the arbitrary off-diagonal blocks of `Z`.  By Proposition 1, such an
identity would simultaneously be a direct matching-tensor identity; the
physical formulation alone does not strengthen its hypotheses.
