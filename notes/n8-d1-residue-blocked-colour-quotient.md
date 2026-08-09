# N=8 D1: blocked-colour quotient obstruction

This lemma closes a large sparse family without inspecting the opposite
residue edges.

At one residue vertex, suppose one non-target color is absent on all three
incident edge matrices.  Let `u1,u2,u3` be the three row vectors belonging
to the other non-target color.  Assume each `ui` has a non-target nonzero
coordinate, so it is not the target line at the neighboring vertex.

Comparing the blocked matching tensor at the active non-target color gives

```text
u1 tensor F23 + u2 tensor F13 + u3 tensor F12 = 0.       (1)
```

Here `Fjk` is the edge form opposite the remaining star vector.  Let
`qi:Vi -> Vi/<ui>` be the quotient map.  Apply `q2 tensor q3` to (1).  The
second and third terms die because they contain `u2` and `u3`; hence

```text
(q2 tensor q3)(F23)=0.
```

The other two double quotients give the analogous conclusions for `F13`
and `F12`.

Now compare the target-color coefficient.  Each of its three matching terms
contains one of these opposite forms, so the full triple quotient
`q1 tensor q2 tensor q3` kills its left side.  Its right side is the pure
target tensor.  That tensor survives because no target vector lies on a
line `<ui>`.  This is the contradiction.

The proof uses only the nine blocked cells and one non-target witness in
each active incident row.  Every other residue or external cell is
irrelevant, and the argument holds over every field.

The exact checker
[`verify_n8_d1_residue_blocked_colour_quotient.py`](../computations/verify_n8_d1_residue_blocked_colour_quotient.py)
audits a 208-cell representative, all 8,100 matching fibres, the three
isolating double quotients, and the target triple quotient.  Its frozen
ledger is
`a320d6f7513b9c52b8b87f1270fe6bc60421dc86e2809b84c99a5dddc0ce4929`.
