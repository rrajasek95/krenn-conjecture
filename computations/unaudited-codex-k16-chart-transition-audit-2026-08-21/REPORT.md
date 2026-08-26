# Literal K16 chart-transition audit

The 25 relaxed anchor-signature orbits do not determine chart transitions.
For example, the same signature orbit

`(0,0,0,0,0,0,1,1,2,1,1,2)`

has one literal completion supporting only chart type 1 and another supporting
types 1 and 2.  Both exact degree-24 rows are frozen in the result.

To obtain a provenance-safe packet, the checker chooses for each of the 216
K14 anchor signatures the lex-first literal singleton pivot constrained to
the exact 25-orbit minimum single-pivot cover.  This reconstructs 2,467,680
literal K16 occurrences and 2,052,084 distinct rows without collecting
polynomial coefficients.

Of these occurrences, 2,345,240 have no dividing pure matching-triple chart
product at all.  The remaining occurrences reach every one of the 31 chart
types.  There are 6,810 transitions back to source chart type 1, so no strict
potential on chart types exists.  These self-type transitions are not
identity Laurent ratios: every one replaces six source anchors by six new
pure cells, and the literal identity-ratio count is zero.

Thus maximal-modulus descent is not supplied by this packet.  The Laurent
ratio `P_dest/P_source` has positive exponent on destination-only cells and
negative exponent on source-only anchors, but support data gives no analytic
sign.  Moreover, the observed graph is only two-level; transitions cannot be
composed at destination nodes without independently recentering and replaying
the K16 construction there.  The smallest observed equality obstruction is
the singleton chart-type SCC `{1}` with a self-loop.

This packet is source-faithful for a minimum single-pivot cover.  It is not
the 25-orbit affine relaxation, the earlier locally-minimal 50-orbit packet,
or a collected K16 residual.

Standard, optimized, and isolated runs agree on logical digest
`4271578ebdb20ba52741dd4c2cbe3034bd9b5a3f876f4b8f9745d49561f14305`.

