# The coordinate-diagonal one-bridge incidence is impossible

## 1. Result

The remaining product incidence for a minimal target-axis bridge also
closes.

> **One-bridge-site product lemma.**  Work over an integral domain in the
> coordinate-diagonal two-bad packet.  Suppose a nonzero minimal target-axis
> kernel row is supported at sites `0,1`, the two bright pure tensors have
> arbitrary preimages, and a nonzero pure target product uses exactly one
> bridge centre.  If the other kernel and product centres lie outside the
> bridge, then the source equations are inconsistent.

Together with the same-pair coupling theorem in
[`shared-reciprocal-two-bad-three-coordinate-bright-coupling.md`](shared-reciprocal-two-bad-three-coordinate-bright-coupling.md),
this closes both ways a pure product can meet a minimal two-centre
coordinate-diagonal bridge: it selects both bridge sites, or exactly one.
The remaining coordinate-diagonal kernel geometry begins with a minimal
kernel circuit on at least three centres.  Mixed-colour internal cells are
still a separate branch.

## 2. Literal bridge equations

Put the bridge at sites `0,1` and the residual sites at `2,3,4`.  Let `a,c`
be the bright colours and `t` the target colour.  As in the preceding
three-coordinate theorem, write

```text
u_d,i = q_0i(d,d),       v_d,i = q_1i(d,d),
r_d,i = q_jk(d,d),       {i,j,k}={2,3,4}.
```

The target bridge factorization is

\[
 K_0=e_t^{(1)}Z,\qquad K_1=e_t^{(0)}Z.                 \tag{1}
\]

For a word with colour `t` on the surviving bridge endpoint and residual
site `i`, and colour `d` on the other two residual sites, literal matching
expansion gives

\[
 [K_0]=v_{t,i}r_{d,i},\qquad [K_1]=u_{t,i}r_{d,i}.
\]

After identifying the two copies of `Z`, therefore,

\[
 (v_{t,i}-u_{t,i})r_{d,i}=0\qquad(d=a,c).              \tag{2}
\]

The one-bridge pure product has, after removing its other localized
factors, a selected coefficient

\[
 \delta_z=v_{t,z}-u_{t,z}\ne0.                         \tag{3}
\]

Normalize `z=0`.  Equations (2)--(3) give

\[
 r_{a,0}=r_{c,0}=0.                                    \tag{4}
\]

Two further literal row families will be used.  The all-`d` coefficient
of each bridge cofactor is

\[
 \sum_i u_{d,i}r_{d,i}=0,\qquad
 \sum_i v_{d,i}r_{d,i}=0.                              \tag{5}
\]

The mixed `2+2` coefficients give, for `d!=e`,

\[
 u_{d,i}r_{e,i}=v_{d,i}r_{e,i}=0.                      \tag{6}
\]

Here `e` may be the other bright colour or the target colour.  The target,
wrong-bridge, and foreign-pure rows are exactly the pinned equations
(4)--(7) of the preceding coupling theorem.

## 3. Fifteen support patterns

Let

\[
 R_d=\{i\in\{1,2\}:r_{d,i}\ne0\}.
\]

There are four possible supports for each bright colour and hence sixteen
ordered pairs `(R_a,R_c)`.  For the crossed permanent

\[
 p_{d,i}=u_{d,j}v_{d,k}+u_{d,k}v_{d,j},\qquad
 \{i,j,k\}=\{0,1,2\},                                  \tag{7}
\]

a nonzero term uses star entries at both coordinates complementary to `i`.
Equation (6) then forces

\[
 p_{d,i}\ne0\quad\Longrightarrow\quad R_e\subseteq\{i\}
 \quad(e\ne d).                                        \tag{8}

The fifteen pairs other than `(empty,empty)` fall into six exact cases.

- `full/full`: opposite annihilators leave only coordinate-zero stars, so
  all crosses vanish.  Both targets are direct, and the two wrong-bridge
  rows contradict them.

- `full/singleton`: the singleton response is direct and forces its bridge
  scalar nonzero.  Its wrong-bridge row kills the full support's direct
  sum, while its foreign-pure row kills the sole full-support weight that
  can see a cross.

- `singleton/singleton`, distinct coordinates: the one-term equations (5)
  and the opposite equations (6) leave only coordinate-zero stars.  Both
  targets are direct and contradict the wrong-bridge rows.

- `singleton/singleton`, the same coordinate: both complete responses are
  supported on that coordinate.  Their target weights and entries are
  nonzero, contradicting a foreign-pure zero row.

- `empty/full`: the full opposite support leaves the empty colour only one
  possible star coordinate, so its crossed response vanishes.

- `empty/singleton`: both complete responses are supported on the singleton
  coordinate.  The two target equations make the relevant weight-entry
  products nonzero, contradicting the foreign-pure row.

This accounts respectively for `1,4,2,2,2,4` ordered pairs, or fifteen in
all.  The checker computes the maximal star and cross envelopes for every
pair; no generic value is assigned to a surviving cell.

## 4. The empty/empty target coupling

Suppose now `r_a=r_c=0`.  Both bright responses consist only of crossed
permanents.  The two target equations select coordinates `i,j` with

\[
 w_{a,i}p_{a,i}\ne0,\qquad w_{c,j}p_{c,j}\ne0.          \tag{9}
\]

The foreign-pure zero rows imply `p_c,i=0` and `p_a,j=0`; hence `i!=j`.
Choose a nonzero monomial from each selected permanent.  The first uses
both star coordinates complementary to `i`, and the second uses both
coordinates complementary to `j`.  Applying (6) with `e=t` kills `r_t` on
both complements.  Since distinct coordinate complements cover all three
coordinates,

\[
 r_t=0.                                                 \tag{10}
\]

Thus every residual-residual diagonal cell is zero in all three colours.
Every perfect matching in either four-site bridge cofactor contains one
residual-residual edge, so `K_0=K_1=0`, contrary to the nonzero minimal
bridge (1).  The checker audits all six ordered choices `i!=j`, both
monomial orientations for each permanent, and all three matchings in each
bridge cofactor.

The target-colour step is essential.  If it is deleted, the exact rational
packet

```text
colour a: edges 03,14,
colour c: edges 02,14
```

has `K_0=K_1=0`, `K_2=X_a`, and `K_3=X_c`.  This packet is retained in the
checker as a mutation guard against silently treating the two-bright
projection as sufficient.

## 5. Scope and uniformity

The proof is independent of the sizes of the bright preimages: parity
purification reduces them to their bright coordinate weights before this
argument starts.  It is division-free except for removing the named
nonzero factors that define (3), and every zero-product inference is over
an integral domain.  It is therefore valid over fraction fields in a
uniform descent argument.

The proof does rely on colour-diagonal internal cells.  A mixed-colour
internal edge can survive after all three diagonal residual vectors vanish,
so the last `K_0=K_1=0` step does not cover that branch.

## 6. Reproduction

```sh
python3 computations/verify_shared_reciprocal_two_bad_one_bridge_incidence.py
python3 -O computations/verify_shared_reciprocal_two_bad_one_bridge_incidence.py
```

The checker pins the earlier coupling theorem, reconstructs six delta rows,
two own-colour rows, and twelve opposite-colour annihilators from literal
matchings, closes all sixteen support patterns, and retains the exact
target-coupling-deleted counterguard.
