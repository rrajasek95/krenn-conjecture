# Two bright lifts cannot share the target-bridge quotient

## 1. Result

The one-bright packet in
[`the cross-star guard`](shared-reciprocal-two-bad-bridge-projection-cross-star-guard.md)
shows that quotienting a target-line bridge does not kill a crossed
permanent.  Coupling both bright colours does kill it.

> **Three-coordinate bright-coupling lemma.**  Let the five-site internal
> quadratic be colour-diagonal.  Suppose a minimal target-line bridge uses
> sites `0,1`, a nonzero pure target product selects both bridge sites and a
> residual `P` centre, and the two known bright pure tensors have arbitrary
> (possibly multi-centre) preimages.  Then the equations are inconsistent
> over every integral domain.

The theorem is coefficient-complete and uses literal matching cofactors.
It closes the multi-centre bright-lift branch for the same-pair target
bridge product.  Other bridge/product incidence types and mixed-colour
internal cells remain separate.

## 2. Parity purification and projection

Put the bridge at sites `0,1` and the three residual sites at `2,3,4`.
Every four-site word of a colour-diagonal matching has even multiplicity in
each colour.  Inserting a local colour `d` therefore puts the five-site word
in parity sector `e_d`.  The three endpoint-colour components of any
preimage cannot cancel each other.  A preimage of `X_d` can consequently be
replaced by its `d`-coordinate component.

The target-line bridge has

\[
 K_0=e_t^{(1)}Z,\qquad K_1=e_t^{(0)}Z.                 \tag{1}
\]

After quotienting sites `0,1` modulo `e_t`, the bright columns centred at
the bridge die.  Write the remaining bright weights as
`w_d=(w_d0,w_d1,w_d2)`.

For each colour `d`, define

```text
s_d       = q_01(d,d),
u_d,i     = q_0i(d,d),       v_d,i = q_1i(d,d),
r_d,i     = q_jk(d,d),       {i,j,k}={2,3,4}.
```

The pure coefficient of the residual cofactor centred at `i` is

\[
 g_{d,i}=s_dr_{d,i}
   +u_{d,j}v_{d,k}+u_{d,k}v_{d,j}.                    \tag{2}
\]

## 3. Exact coupled rows

Let `a,c` be the two bright colours and put

\[
 A_d=\sum_i w_{d,i}r_{d,i}.                            \tag{3}
\]

Literal expansion gives three families of required equations:

\[
 \sum_iw_{d,i}g_{d,i}=1,                              \tag{4}
\]

\[
 s_eA_d=0\quad(d\ne e),                               \tag{5}
\]

and, coordinatewise,

\[
 w_{d,i}g_{e,i}=0\quad(d\ne e).                      \tag{6}

Equation (5) is the word whose two bridge sites have colour `e` and whose
three residual sites have colour `d`.  Equation (6) is the word with colour
`d` only at residual centre `i` and colour `e` at the other four sites.
The latter is the coupled row absent from a one-bright analysis.

The bridge factorization (1) also gives, for every `i` and `d!=e`,

\[
 u_{d,i}r_{e,i}=v_{d,i}r_{e,i}=0.                     \tag{7}

This includes `e=t`.

## 4. Three-coordinate contradiction

Normalize the selected pure target term so that its residual target edge
is `r_t,0!=0`.  Equation (7) gives

\[
 u_{a,0}=v_{a,0}=u_{c,0}=v_{c,0}=0.                  \tag{8}

Thus the crossed part of (2) can occur only at coordinate zero:

\[
 h_d=u_{d,1}v_{d,2}+u_{d,2}v_{d,1},\qquad
 g_d=(s_dr_{d,0}+h_d,s_dr_{d,1},s_dr_{d,2}).          \tag{9}

If `h_d!=0`, one of its two products is nonzero.  Either product uses one
star entry at coordinate `1` and one at coordinate `2`; (7) therefore
forces

\[
 r_{e,1}=r_{e,2}=0\quad(e\ne d).                      \tag{10}

Now split only on whether `s_a,s_c` vanish.

- If both are nonzero, (5) gives `A_a=A_c=0`, so (4) gives
  `w_a0 h_a=w_c0 h_c=1`.  By (10), `r_c` is supported at coordinate zero;
  `A_c=0` then gives `r_c0=0`.  Hence `g_c0=h_c!=0`, contradicting
  `w_a0 g_c0=0` from (6).
- If only `s_a` is nonzero, the `c` target gives `w_c0h_c=1`.  Equation
  (10) kills `r_a1,r_a2`, while (6) gives `w_a0=0`; then both terms in the
  `a` target equation vanish.  The other asymmetric case is identical.
- If both vanish, (4) gives `w_a0h_a=w_c0h_c=1`, immediately contradicting
  `w_a0g_c0=w_a0h_c=0`.

This proves the lemma.  No genericity, positivity, or division by an
unlisted cell is used.

## 5. Remaining boundary

In the coordinate-diagonal branch, the same-pair two-centre target bridge
is now closed even with arbitrary multi-centre bright lifts.  The remaining
kernel geometry starts with a bridge whose pure product selects a centre
outside its pair, or a minimal kernel circuit on at least three centres.
Mixed-colour internal cells remain the named later branch.

## 6. Reproduction

```sh
python3 computations/verify_shared_reciprocal_two_bad_three_coordinate_bright_coupling.py
python3 -O computations/verify_shared_reciprocal_two_bad_three_coordinate_bright_coupling.py
```

The checker pins the one-bright guard and parity straightening, reconstructs
the displayed coefficient rows from literal matchings, and audits the four
direct-channel support cases.
