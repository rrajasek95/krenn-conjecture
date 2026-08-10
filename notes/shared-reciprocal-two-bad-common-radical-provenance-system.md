# The common-radical branch has a localized target chord

## 1. Complete normalized provenance system

This note imposes one literal five-site quadratic `q_C` on the
nondegenerate branch of the bright-pairing radical dichotomy.  After row
operations among zero odd-star equations, normalize

\[
 \pi_t(Q_a)=\pi_t(R_c)=e_0,
 \qquad
 \pi_t(Q_t)=\pi_t(R_t)=e_1.                            \tag{1}
\]

All non-target entries of these four rows remain arbitrary.  Every entry
of the two affine bright rows `Q_c,R_a`, the controller row `P`, the
internal quadratic `q_C`, and the direct block `D` also remains arbitrary.

The exact polynomial system consists of

```text
variables                 184
odd-star coefficient rows 1458
full common-hafnian rows  2187
total rows                3645
sparse terms            139404
```

Its source SHA-256 is

```text
8089db4d27fb6babb25badd2081cc5fd80768d6e3f99f54ac90a5a26f5b3d214
```

The checker builds every polynomial from literal perfect matchings.  It
can emit a deterministic Singular input with `--emit-singular PATH`.

This system is only trichotomy branch (iii).  It does not include the
separate branches `[X_t] in R_nt`, `pi_t(Q_a)=0`, or `pi_t(R_c)=0`.

## 2. Exact pure-target theorem

Let

\[
 K_x^{t}=K_x(t,t,t,t),qquad
 R=\sum_xP_{x,t}K_x^t.                                 \tag{2}
\]

The pure-target coefficients of the four normalized kernel rows give

\[
                         K_0^t=K_1^t=0.                \tag{3}
\]

Because `Q_t` and `R_t` both have target projection `e_1`, their target
insertions cannot occupy two distinct kernel-product holes.  Hence
`P Q_t R_t q_C` has zero raw all-target coefficient.  The `(t,t)` full row
is therefore

\[
                         D_{tt}R=1.                    \tag{4}
\]

In particular both `D_tt` and `R` are nonzero at every field-valued point.
The pure target is supplied by a literal direct target chord, not by the
tilted product term.

The same-radical `(a,c)` row and the two crossed rows give

\[
 D_{ac}R=0,
 \qquad D_{at}R+S=0,
 \qquad D_{tc}R+S=0,                                   \tag{5}
\]

where

\[
 S=\sum_{x=2}^4P_{x,t}
 q_{\{2,3,4\}\setminus\{x\}}^{tt}.                    \tag{6}
\]

Combining (4)--(5) gives the exact consequences

\[
                 \boxed{D_{ac}=0},
 \qquad           \boxed{D_{at}=D_{tc}}.               \tag{7}
\]

The checker verifies ordinary polynomial certificates:

\[
\begin{aligned}
D_{ac}&=D_{tt}(D_{ac}R)-D_{ac}(D_{tt}R-1),\\
D_{at}-D_{tc}
 &=D_{tt}\big((D_{at}R+S)-(D_{tc}R+S)\big)\\
 &\quad -(D_{at}-D_{tc})(D_{tt}R-1).
\end{aligned}                                          \tag{8}
\]

Thus (4) and (7) are source-ideal consequences, not divisions performed
only at a hypothetical point.

## 3. The proposed `dim W<=1` shortcut is false

The two bright equations alone do not force a one-dimensional target
projection.  There is a literal rational seven-cell counterguard.  In
zero-based site labels its nonzero cells are

```text
12:00=3/5, 02:00=4/5, 34:00=1,
01:11=1,   23:11=1,
02:10=1,   02:20=1.
```

Its common-cofactor map satisfies

```text
rank Phi = 11,       dim ker Phi = 4,
X_a,X_c in im Phi,   X_t not in im Phi,
dim pi_t(ker Phi) = 2.
```

Explicit bright preimages are

\[
                 X_a=\Phi((5/3)e_a@0),
 \qquad          X_c=\Phi(e_c@4).                      \tag{9}
\]

An exact kernel basis is

\[
\begin{aligned}
&-(4/3)e_a@0-(5/3)e_c@0-(5/3)e_t@0+e_a@1,\\
&e_a@3,\qquad e_c@3,\qquad e_t@3.
\end{aligned}                                          \tag{10}
\]

The target projections in (10) span the coordinate pair `{0,3}`.  This
counterguard does not satisfy the nine full equations and is not a
two-bad source.  It proves only that the bright-image/odd-star subsystem
cannot eliminate branch (iii); the full common-hafnian rows are essential.

## 4. Current exact frontier

The full normalized ideal has not been decided.  Direct modular standard-
basis attempts on all rows and on the near-monochrome subideal did not
return a certified verdict within the bounded runs, so no solver outcome is
promoted here.

The exact next reduction should first use (4) to work on the chart

\[
                         D_{tt}=R=1                    \tag{11}

by the corresponding torus normalization, eliminate `D_ac` and one of
`D_at,D_tc` using (7), and only then search a small resultant/minor among
the remaining eight full-row families.  A full 184-variable Gröbner basis
is not the intended next step.

## 5. Reproduction

```sh
python3 computations/verify_shared_reciprocal_two_bad_common_radical_provenance_system.py
python3 -O computations/verify_shared_reciprocal_two_bad_common_radical_provenance_system.py
python3 computations/verify_shared_reciprocal_two_bad_common_radical_provenance_system.py \
  --emit-singular /tmp/common-radical.sing
```

Normal and optimized ledgers have SHA-256

```text
19bcdab49338f25ae6b28e3407994c288f7acfb54de9f1a77d6c35193254d1cc
```
