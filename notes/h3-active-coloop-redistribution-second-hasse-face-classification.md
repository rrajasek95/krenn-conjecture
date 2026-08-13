# The first nonlinear coloop face is one of four literal lower packets

## Complete matching census

On six residual sites, the pure target coefficient has the fifteen
occurrences of `q^[3]`.  A fixed complete response coefficient has

```text
15 direct occurrences d*q^[3]
+
90 ordered endpoint occurrences p_u*s_v*q^[2]
=
105 literal occurrences.
```

For a scalar direction `xi`, the second Hasse coefficient is the sum over
unordered pairs of varied cells which occur in one of these matchings.  The
checker enumerates all 28 scalar labels

```text
15 q edges + 6 p sites + 6 s sites + d
```

and all 378 unordered pairs of distinct labels.  The 28 repeated-label
second terms vanish by scalar-cell multiaffinity.  There are exactly 45 target pair incidences
and 630 response pair incidences.  Every nonzero pair has one of the
following five forms.

| varied pair | number of pairs | literal base tail |
|---|---:|---|
| disjoint `Q,Q` in target | 45 | one residual `q` cell |
| disjoint `Q,Q` in response | 45 | `d*q_uv+p_u*s_v+p_v*s_u` |
| `D,Q` | 15 | three-match four-site hafnian |
| distinct-site `P,S` | 30 | the same four-site hafnian |
| disjoint `P,Q` or `S,Q` | 60+60 | three-term one-endpoint insertion |

All 168 remaining response pairs are occurrence-incompatible: incident
`Q,Q`, same-row `P,P` or `S,S`, same-site `P,S`, incident endpoint/`Q`,
and the incompatible direct/endpoint pairs.  Their second face is exactly
zero.

Checker:
[`verify_h3_active_coloop_redistribution_second_hasse_face_classification.py`](../computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py).

## Literal formulas

For the representative varied pair `q01,q23`, the target tail is `q45` and
the response tail is

\[
                     d q_{45}+p_4s_5+p_5s_4.          \tag{1}
\]

For `d,q01`, or for `p0,s1`, it is

\[
 q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}.             \tag{2}
\]

For `p0,q12`, it is

\[
 s_3q_{45}+s_4q_{35}+s_5q_{34},                      \tag{3}
\]

with the `p`-reverse for `s0,q12`.  Thus the complete nonlinear face is not
an anonymous obstruction.  The direction pair together with each displayed
tail reconstructs one original source occurrence, retaining its physical
sites, word colours, endpoint heads, fine grade, and matching complement.

The five formulas reduce to four named lower packets:

```text
QQ target       one-edge restricted face,
QQ response     two-site target-normal C2+ packet,
DQ or PS        four-site C4 hafnian packet,
PQ or SQ        one-endpoint P2 insertion packet.
```

This is a strict residual-site reduction from the six-site `h=3` equation.

## Which terms already route

Take a nonzero literal base-tail monomial of a nonzero second-face
coefficient.  If one of its base `q` cells is offdiagonal, the complete
target-augmented private-site identity supplies a nonzero determinant/
cofactor fan; the pinned fan theorem then gives four-good or a literal
pure-colour coloop.  If its physical endpoint/hole lies outside the current
closed Hall shore, it enters the proved finite saturation route.  If all
base factors are pure and trapped, it stays in one of the four lower packets
above.

There is an important variance distinction.  The two varied cells are
tangent directions, not necessarily occupied base-source cells.  Their
being offdiagonal does not itself create an active source carrier.  The
route is unconditional only when the offdiagonal cell occurs in the
nonzero **base tail**.

If every pair in `supp(xi)` is occurrence-incompatible, all higher matching
faces vanish as well: no source occurrence contains two varied cells.
Then the exact affine-line deletion theorem of `f77c2ed` applies, provided
the direction is occupied and anchor-safe.

## The sharp residual

The census does not make every compatible face terminal.  Saturate the Hall
shore to all fifteen holes and use only pure diagonal base `q` cells.  The
assignments

```text
q23=q45=d=s3=1,
all other displayed q/s entries=0
```

make (1), (2), and (3) nonzero while containing neither an offdiagonal base
cell nor an outside Hall hole.  This is an exact full-matching-face quotient
guard.  It is not asserted to be a complete nine-row GHZ source.

The residual is nevertheless much smaller and already named.  The pinned
order-two audits show:

- the `P2` packet still needs an occurrence-local one-endpoint
  principal-parts section; and
- the even `B-4/C2+` packet still needs its common target-bearing physical
  cell.

Their coefficient shadows are exact, but source-labelled placement in the
full protected grade is not yet proved.  Therefore the implication

```text
nonzero H2 face -> active/four-good, outside Hall, or completed coloop
```

is currently conditional on precisely these lower cells.

## Shortest next theorem

Construct a source-natural restriction map carrying the pure trapped
second-Hasse packet to its `C2+/C4/P2` lower cell with the same word, fine,
anchor, and protected rows.  Equivalently, prove that failure of this
restriction forces a nonzero literal mate with an offdiagonal private
cofactor or outside Hall hole.

This replaces the abstract second-order cokernel by a finite physical list.
It does not yet fill the occurrence-local lower cells.

Run normally, optimized, and isolated/no-site.  The frozen ledger digest is
recorded by the checker.
