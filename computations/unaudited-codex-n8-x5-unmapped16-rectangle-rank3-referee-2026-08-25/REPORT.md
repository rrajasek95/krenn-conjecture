# Independent rectangle-rank-three reduction referee

Status: **PASS exact reduction; no closure and no ideal run.**

The cap-67 guards give `A46=-A47*A26^T`; invertibility of `A47` then gives `A17*A26=I`, and square-matrix algebra gives `A26*A17=I`.  Thus `A17,A26,A46,A47` are all invertible.

All enumerated carriers were reclassified.  Forced zero-kernel counts are 10/24 with `A12` present and 22/40 without it.  The specialization taking every supported block to `I` and `A46=-I` satisfies the rank-three guard and makes every enumerated carrier injective, while failing full X5.  Therefore no guard-only universal carrier exists; this is not a full-X5 countermodel.

Independent signed-monomial expansion on all 6,561 words verifies `Phi=X*Q+R*S`.  The eight supported matchings use neither `A12` nor `A23`, so those matrices are free and amplitude-inactive.  Dropping them and reconstructing `A46` gives the exact established 64-variable/6,571-generator projection.

The smallest additional safe reduction found is held and unmaterialized: set `A17=u26*adj(A26)` with `det(A26)*u26=1`.  Together with `det(A47)*sat47=1`, this gives six matrices plus two inverse variables—56 variables and 6,563 generators.  It uses no unproved gauge normalization.  It must not launch without new clearance, and no run was made while the rep1 exact-Q lane was active.
