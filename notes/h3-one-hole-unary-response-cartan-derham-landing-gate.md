# The response and universal Cartan inventories leave the one-hole anti-diagonal

## Verdict

The two formal unary cofactors left by the first `E01` collision residual
are **not** supplied by the four physical response heads or by the physical
six-site unary row.  This remains true even after granting every termwise,
presentation-safe Cartan graph between each source PP flag and its rooted
target flag.

Write

```text
A_s : remove p0,   remainder on S,1,2,3,4,5,
B_s : remove q01,  remainder on P,S,2,3,4,5,
A_t : p0 -> D and dp0 -> dD,
B_t : q01 -> -s1 and dq01 -> -ds1.
```

Each row has 15 terms.  Three terms in each target row belong to the
already completed lower packets `K_A,K_B`; the other twelve form the live
class

\[
 J_{E01}=A_t^{\rm live}-B_t^{\rm live}
          =(A_t-B_t)-K_A+K_B.                         \tag{1}
\]

On the exact 60-coordinate source/target cofactor model, all four response
heads and their differences have rank-one projection `A_s+B_s`.  The
physical unary row is supported on `0,1,2,3,4,5`, so it has empty
intersection with either augmented cofactor.  Adding the 30 relative
Cartan graphs, the two lower companions, and the complete collision gives
rank 33 and leaves `H0=27`.  The class (1) is not in this span.

Adjoining either the absolute source split `A_s-B_s` or the absolute target
landing `A_t-B_t` raises the rank from 33 to 34 and fills (1).  Thus the
missing datum is exactly one absolute one-hole cofactor split.  Universal
Cartan/de Rham identities describe it, but do not authorize it in the
physical word/fine/root/reinsertion complex.

Exact checker:
[`verify_h3_one_hole_unary_response_cartan_derham_landing_gate.py`](../computations/verify_h3_one_hole_unary_response_cartan_derham_landing_gate.py).

## 1. The two complete cofactor fibres

For the root

\[
 E_{01}:p_0\mapsto D,\qquad q_{01}\mapsto-s_1,
\]

there are exactly 15 response matchings containing `p0` and exactly 15
containing `q01`.  Removing the varied edge gives the two perfect-matching
rows

\[
 A_s=\operatorname{Haf}(S,1,2,3,4,5),\qquad
 B_s=\operatorname{Haf}(P,S,2,3,4,5).                \tag{2}
\]

Transporting both the retained matching and the Kähler label is a termwise
bijection

\[
 (M,dp_0)\longmapsto(E_{01}M,dD),\qquad
 (M,dq_{01})\longmapsto-(E_{01}M,ds_1).              \tag{3}
\]

In each branch, twelve target coefficients survive in the signed
24-term residual and three cancel against the adjacent root parent.  Those
three are precisely the two lower companion packets in (1).  This recovers
the previously computed 24 same-cell reinsertion flags without discarding
their complete 15-term parents.

## 2. Full response-head and unary projection

Restrict the complete response first-PP row to the two source fibres in
(2).  The result is exactly

\[
                         A_s+B_s.                    \tag{4}
\]

There are four response heads.  In the selected head/word block, their
projections are `(A_s+B_s,0,0,0)`; the three head differences project to
`-(A_s+B_s)`.  Therefore their total projected rank is one.  In particular,
head changes do not produce `A_s-B_s`.

The actual unary equation is the 15-term hafnian on the six physical sites

\[
                         0,1,2,3,4,5.                \tag{5}
\]

Its matching support is disjoint from both rows in (2), even before the
root, response-head, word, and reinsertion tags are retained.  Calling
either row in (2) an “existing unary equation” would identify the operation
roles `P,S` with physical GHZ sites.  The full unsigned-shear authorization
audit already excludes exactly that identification.

## 3. The strongest relative Cartan grant still leaves the class

Grant a presentation-safe graph for every term of both rows.  With the root
sign included, their boundaries are

\[
 g_{A,m}=A_{t,m}-A_{s,m},\qquad
 g_{B,m}=-B_{t,m}+B_{s,m}.                            \tag{6}
\]

All 30 columns are independent, and

\[
 \sum_m(g_{A,m}+g_{B,m})
       =(A_t-B_t)-(A_s-B_s).                          \tag{7}
\]

Define a covector on the 60 source/target coordinates by

```text
+1/24 on the twelve live A_s and twelve live A_t terms,
-1/24 on the twelve live B_s and twelve live B_t terms,
0 on the six cancelled companion terms at either side.
```

It kills:

- `A_s+B_s`, hence every response head and head difference;
- the physical unary projections;
- both three-term lower companions;
- the complete collision `2(A_t+B_t)`; and
- every graph in (6).

It reads one on `J_E01`.  Therefore a mapping cylinder for each Cartan
transport preserves the obstruction rather than killing it.

## 4. What Cartan and de Rham contraction really prove

The polynomial identities themselves are exact.  If `R` is the complete
105-matching response, direct calculation gives

\[
             \iota_{E_{01}}(dR)=E_{01}R,
       \qquad L_{E_{01}}(dR)=d(E_{01}R).              \tag{8}
\]

On the two relevant one-forms,

\[
 \iota_E(dp_0)=D,\quad d\iota_E(dp_0)=dD,
 \qquad
 \iota_E(dq_{01})=-s_1,\quad d\iota_E(dq_{01})=-ds_1. \tag{9}
\]

The universal Euler homotopy also satisfies

\[
                         dH+Hd=1                     \tag{10}
\]

in positive Spencer degree.  The exhaustive pinned checker verifies (10)
through polynomial degree six and every exterior degree on five symbols.

Equations (8)--(10) live in the polynomial de Rham/principal-parts
resolution.  A contraction is an operator identity, not automatically a
boundary column of the physical correction presentation.  After retaining
the physical tags, the already authorized realization is (6), and the
anti-diagonal extends across it.  Treating `A_t-B_t` as an absolute boundary
would add a new rank-raising comparison cell; it cannot be inferred merely
from (8).

## 5. Sharp terminal fork

The reduced lane has an exact necessary-and-sufficient repair:

```text
same-word/fine/root/reinsertion absolute source split A_s-B_s exists
    -> (7) and the old K_A,K_B packets fill J_E01;

equivalently, an absolute target landing A_t-B_t exists
    -> (1) fills J_E01;

only response sums, physical unary rows, and relative Cartan graphs exist
    -> the extended anti-diagonal is a normalized terminal detector.
```

This is a local terminal theorem for the completed first-PP one-hole
quotient.  Promoting it to the global proof still requires extending the
same covector through the target, `Eq`, `q`, anchor, `W`, ordinary-residue,
and ridge grades, or constructing the absolute comparison in those grades.

## Verification

Run

```text
python3 computations/verify_h3_one_hole_unary_response_cartan_derham_landing_gate.py
python3 -O computations/verify_h3_one_hole_unary_response_cartan_derham_landing_gate.py
python3 -I -S computations/verify_h3_one_hole_unary_response_cartan_derham_landing_gate.py
```

The checker reconstructs the two 15-term fibres from the complete K8
response, tracks their root signs and removed-edge labels, verifies the
response-head/unary support statements, proves the exact 60-coordinate rank
and dual claims, and checks both Cartan identities in (8) term by term.
