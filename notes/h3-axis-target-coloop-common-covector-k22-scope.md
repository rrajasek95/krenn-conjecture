# Common-covector synchronization does not supply strict K2,2 factors

## Result

In the 50 no-cross residuals, suppose the P-side and S-side complete column
pairs are nonproportional. Fix the selected mixed word d. On the vector
space of mixed target-zero coefficient rows, the two minors

\[
 \Delta_P(d,-),\qquad \Delta_S(d,-)
\]

are nonzero linear forms unless that endpoint already uses a nonzero target
coordinate and enters the alternate-target/affine-line branch. Over the
rationals, two proper hyperplanes cannot cover the whole vector space.
Therefore there is a rational mixed coefficient combination ell such that

\[
 \Delta_P(d,\ell)\ne0,\qquad\Delta_S(d,\ell)\ne0.
\]

Thus the two endpoint minors always synchronize on the common two-dimensional
output quotient spanned by d and ell. A literal fine word common to both is
not needed for this Fitting statement; a source-valid linear combination of
zero coefficient rows suffices.

Checker:
computations/verify_h3_axis_target_coloop_common_covector_k22_scope.py.

## Why this does not invoke the strict bistar unit

The endpoint-support-complete strict K2,2 chart in 79907d3 localizes two
pure target matchings in each bright colour. Normalize the selected target
matching to

    Q_left = P0 | S1 | 23 | 45.

The second strict matching of the same colour is

    Q_right = P3 | S2 | 01 | 45.

It avoids both selected endpoint arms. If its literal monomial is localized,
it is already an alternate pure target matching and the target-coloop gate
has closed before the bistar source-unit certificate is used. Consequently
the 79907d3 identities are a downstream closure after endpoint-support
completion; they cannot manufacture that missing completion in the 50
no-cross coloop residuals.

An extra endpoint component is still controlled: zero complete column means
exact deletion, while a nonzero outside column enters 7114577. Missing
strict factors are different from extra factors and cannot be supplied by
that theorem.

## The canonical smallest union is itself impossible as full support

The canonical three-base residual from 6dc3bd5 is

    M = P0 | S1 | 23 | 45,
    N = 01 | P2 | S3 | 45,
    K = PS | 01 | 23 | 45.

These are the only perfect matchings in their physical edge union, and all
three contain edge 45. If the full source support had no further matching,
its entire H8 tensor would factor across the cut 45 | complement:

\[
                       H_8=Q_{45}\otimes G_6.
\]

Write q00,q11 for two edge-45 coefficients and g0,g1 for the complementary
pure coefficients. The pure 0, pure 1, and mixed zero output rows are

    F0 = q00*g0-1,
    F1 = q11*g1-1,
    Fmix = q00*g1.

They have the integral unit identity

\[
 g_0q_{11}F_{\rm mix}-g_0q_{00}F_1-F_0=1.
\]

Hence this canonical three-base union cannot be the whole physical support.
At a support-minimal full source another nonzero cell must participate in a
fourth perfect matching, introducing an edge outside the displayed union.
An endpoint edge routes by the existing complete-column theorem. An internal
q-only fourth base is the remaining physical routing gate.

## Scope

This removes separated literal word pairs as an abstract synchronization
obstruction, identifies exactly why the strict K2,2 unit is not yet
available, and kills the canonical smallest three-base packet if it is
support-complete. It does not prove that every one of the 50 unions shares a
common physical edge, nor classify every possible fourth internal matching.

Run:

    python3 computations/verify_h3_axis_target_coloop_common_covector_k22_scope.py
    python3 -O computations/verify_h3_axis_target_coloop_common_covector_k22_scope.py
    python3 -I -S computations/verify_h3_axis_target_coloop_common_covector_k22_scope.py

Frozen ledger SHA-256:

    e77f24f4ea7ee6a5199947dec2fe5a77d9e12756123b33916a90de637eee7bc0
