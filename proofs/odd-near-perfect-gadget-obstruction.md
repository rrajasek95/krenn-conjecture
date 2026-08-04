# Three disjoint near-one-factors always create a singleton mixed fiber

This note rules out the most direct finite vertex-expansion gadget for a
three-color diagonal matching construction.

Let `V` have odd cardinality and contain three distinct terminals
`0,1,2`.  For `r in {0,1,2}`, let `P_r` be a near-perfect matching of `V`
whose unique exposed vertex is `r`.  Assume that the three `P_r` are
pairwise edge-disjoint, and color every edge of `P_r` by `r`.

Given a near-perfect matching `Q` in their union which exposes terminal
`r`, extend its edge-coloring to all vertices by assigning color `r` to the
exposed terminal.  Call the set of compatible near-perfect matchings with
the same exposed-terminal color and the same vertex coloring its *fiber*.

## Theorem

If `|V| >= 5`, the union `P_0 union P_1 union P_2` contains a mixed
near-perfect matching whose fiber is a singleton.

## Proof

Adjoin one new vertex `infinity` and, for each `r`, an edge
`infinity-r` of color `r`.  Then

\[
                 M_r=P_r\mathbin\cup\{\mathord\infty r\}
\]

are three pairwise edge-disjoint perfect matchings on the even set
`V union {infinity}`, which has at least six vertices.

We use the standard three-one-factors lemma:

> Three pairwise edge-disjoint perfect matchings on an even vertex set of
> size at least six have a fourth perfect matching in their union.

*Attribution.*  This lemma is **Bogdanov's observation** (Bogdanov 2017),
published as Thm 1 of Chandran-Gajjala, arXiv:2202.05562, and in
multigraph form as Thm 1.7 of Chandran-Gajjala-Illickan,
arXiv:2407.00303; see
[`references/REFERENCES.md`](../references/REFERENCES.md).  **No priority
is claimed**: the self-contained proof below is given only because the
audit discipline of this repository requires every consumed statement to
be either cited to a checked source or proved inside the artifact.

For completeness, here is a proof.  If the union of two of the matchings
has at least two alternating-cycle components, switch on one nonempty
proper collection of components.  Otherwise every pair forms an
alternating Hamilton cycle.  Fix the cycle formed by `M_0,M_1`.  If an
`M_2` chord joins opposite cycle parities, that chord and the alternating
matchings on the two complementary even paths give a fourth matching.
Otherwise `M_2` separately matches the even and odd cycle positions.  An
even-position chord and an odd-position chord must interlace.  Indeed, if
none interlaced, each chord would cut off a set closed under the matching
of the opposite parity, so its endpoint indices would be congruent modulo
two.  Restricting to either parity class repeats the argument and forces
the endpoints to be congruent modulo every power of two, which is
impossible for two distinct indices in a finite matching.  Two interlacing
chords, together with alternating matchings on the four complementary even
paths, again give a fourth matching.  The only exceptional order is four,
where the three matchings can be the one-factorization of `K_4`.

Let `M` be the resulting fourth perfect matching.  Exactly one of its
edges is incident with `infinity`; write it as `infinity-r`.  Then

\[
                         Q=M\setminus\{\mathord\infty r\}
\]

is a near-perfect matching of `V` exposing terminal `r`.  It is mixed:
if all its edges and the exposed terminal had color `s`, then necessarily
`r=s` and the completed matching would be the unique color-`s` matching
`M_s`, contrary to the choice of `M`.

Finally fix the vertex coloring induced by `M`.  At every vertex `v` of
color `s`, the union has exactly one incident edge of color `s`, namely the
edge of `M_s` at `v`.  Hence any compatible perfect matching is forced at
every vertex and equals `M`.  Removing its forced edge at `infinity` shows
that the near-perfect fiber of `Q` is a singleton.  This proves the theorem.

The lower bound is sharp: on three old vertices, adjoining `infinity`
gives the three one-factors of `K_4`, and there need not be a fourth
matching.

The finite smoke audit
[`computations/verify_odd_near_perfect_gadget_obstruction.py`](../computations/verify_odd_near_perfect_gadget_obstruction.py)
enumerates all pairwise edge-disjoint triples at orders five and seven and
checks both the fourth-matching and singleton-fiber conclusions directly.
