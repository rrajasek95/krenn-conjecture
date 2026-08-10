# Curved OO transport requires a global signed matching invariant

## Outcome

The desired arbitrary-packet private-fibre theorem does not follow from the
local curved OO data.  There is an explicit rational eight-site packet with

- two rank-one direct arms with distinct heads;
- four deleted-star ranks `(3,3,3,3)`;
- curvature `-1`;
- both arm cofactors support-active; and
- the complete target-2 right-ruling ledger, with nonzero sites `3` and `2`.

Nevertheless none of its complete (3^8=6561) endpoint-colour fibres has a
unique support-live matching.  Thus curvature, goodness, activity, and
alignment do not force alternative (i), even globally across all words.

The same packet also shows the correct replacement.  Three literal mixed
full-output rows are binomials whose signed exponent differences form an odd
triangle.  An ordinary three-row identity gives a unit after localizing the
active cells.  Therefore physical rows can realize alternative (ii), but
the load-bearing datum is the **global signed matching-circuit module**, not
a selected local fibre or rank ledger.

For an arbitrary active packet the exact missing invariant is now:

\[
 \boxed{
   (I_{\rm mix}:({\textstyle\prod}_{e\in S}x_e)^\infty)=R,
 }
                                                               \tag{1}
\]

or a source-labelled certificate of (1).  Equivalently, after quotienting
by signed binomial characters, the unit-pivot dependency graph must either
peel acyclically or every critical strongly connected component must have a
nonzero coefficient/Fitting determinant.  None of the local OO hypotheses
controls this invariant.

This is a strong negative boundary plus one positive circuit atom.  It is
not a proof that (1) holds for every curved packet and not a Krenn
counterexample.

## 1. A dense aligned packet with no private fibre

Use the same centres and orientations as commits `726deeb` and `89a3a0e`:

\[
                         p=0,\qquad q=2,\qquad r=4.
\]

The checker specifies every one of the 28 physical blocks by a compact
row-major (3 by 3) support mask and gives each supported cell coefficient
one.  There are 177 supported endpoint-coloured cells.  Direct expansion
recovers

\[
 \operatorname {rank}A_{02}=operatorname {rank}A_{04}=1,
 \qquad
 (g_{02},g_{20},g_{04},g_{40})=(3,3,3,3),
 \qquad \kappa=-1.                                      \tag{2}
\]

Both deleted-arm cofactor tensors are nonzero.  The literal target-2 ruling
audit gives exactly the same nonzero sites `(3)` and `(2)` as the sparse
active packet.

Now enumerate all 105 physical perfect matchings in every endpoint-colour
word.  The nonzero fibre sizes range from 2 to 105, with

```text
singleton fibres:       0
two-matching fibres:   18
zero fibres:          816
```

In particular, no choice of a raw source word produces a private matching.
This is not a dimension heuristic: all 6,561 fibres are reconstructed from
the 177 literal cells.

The packet is a structural counterguard, not a ternary source.  Its full
mixed equations are inconsistent by the circuit below.  That distinction
is the point: exact source equations, rather than the local OO packet, carry
the missing transport.

## 2. The source-provenant odd triangle

Among the eighteen binomial mixed fibres, take the words

```text
20120121
22100121
22120101
```

and write their rows as

\[
                         f_0=A+B,
 \qquad                 f_1=C+D,
 \qquad                 f_2=E+F,                       \tag{3}
\]

where each letter is the literal four-cell matching monomial recorded by
the checker.  Coordinatewise exponent comparison gives

\[
                    A D E=B C F=:K.                    \tag{4}
\]

Equivalently,

\[
                  (A-B)-(C-D)+(E-F)=0,                 \tag{5}
\]

an odd dependency among the three plus-binomial characters.  Multiplying
the three physical rows by literal matching monomials gives the ordinary
identity

\[
 \boxed{
        D E f_0-B E f_1+B C f_2=2K.
 }                                                       \tag{6}
\]

Every factor of (K) is an active source cell.  In characteristic zero,
saturating by those cells turns (6) into (1).  This is a source-level unit:
no Ward, Hasse, jet, cap-codomain, finite-field, or support-only inference
enters it.

The pattern is the familiar hafnian triangle.  After common factors are
removed, the three ratios telescope multiplicatively, while each zero row
sets its ratio to (-1).  Their product says (1=-1).

## 3. Exact contamination identity

The triangle also identifies why one finite circuit does not yet prove the
arbitrary-packet theorem.  In a larger packet the same source words can have
alternate matching sums (R_0,R_1,R_2):

\[
 f_0=A+B+R_0,\qquad
 f_1=C+D+R_1,\qquad
 f_2=E+F+R_2.                                           \tag{7}
\]

The same literal multiplication gives

\[
\boxed{
 D E f_0-B E f_1+B C f_2
 =2K+D E R_0-B E R_1+B C R_2.
}                                                       \tag{8}
\]

Thus contamination is not an unspecified error: it is a three-term
source-labelled debt.  A global transport theorem may orient (8) only if
each remainder class is lower in a well-founded source order, or if the
resulting critical cycle has nontrivial coefficient holonomy.  Local
curvature and star ranks give no order on the (R_i).

This precisely subsumes the guard in `89a3a0e`.  A selected two-row factor
can fail while another physical fibre, or a multi-fibre odd circuit, closes
the packet.  Conversely, merely declaring the remainders lower would assume
the missing theorem.

## 4. The global invariant

Let (S) be the active cell set, let

\[
 R=\mathbb Q[x_e:e\in S],
\]

and let (I_mix) be generated by every literal mixed full-output coefficient.
A private matching, or a physical reduction of all its alternates to one
nonzero Laurent class, places a monomial in (I_mix).  After localization
that monomial is a unit, so (1) follows.

Conversely, if (1) holds, Laurent Nullstellensatz gives a finite physical-row
unit certificate.  A source-order proof is a structured way of producing
that certificate:

1. quotient exact binomial fibres by their integral signed character;
2. reduce every remaining fibre to Laurent classes with coefficients;
3. peel a one-class row, or an odd/valuation-holonomy circuit;
4. on an unpeeled strongly connected component, compute its coefficient
   Fitting determinant rather than choosing another raw matching order.

The invariant is global because blocks between residual sites do not enter
the direct-arm ranks, good-star maps, or curvature minor, yet they change
the alternate matching sums and their circuit graph.  Activity is monotone
under adding such support.  Hence no conclusion about (1) can be read from
the local rank ledger alone.

## 5. Verification and scope

The standard-library checker
[`verify_oo_curved_global_private_transport_boundary.py`](../computations/verify_oo_curved_global_private_transport_boundary.py)
pins the minimal-unit and contamination artifacts, reconstructs the 177
physical cells, audits all local OO/ruling/activity hypotheses, enumerates
all 6,561 fibres, and verifies (4)--(6) as exact monomial identities.  It
also records (8), which is the theorem-level interface for any future global
source order.

What remains proof-completing is not another bounded support layer.  It is a
uniform proof of the saturation/Fitting alternative (1) on every active
curved overlap, or a genuine common-source packet on which that invariant is
proper.  The present result supplies neither and claims neither.
