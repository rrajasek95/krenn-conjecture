# Carrier algebraic-matroid / rigidity-stress screen

Status: **exact bounded negative screen**.  No polynomial solve was used.

For a carrier `C`, let `M_C` be the row-vector matroid on its response rows
`R_C` and four blockers.  A blocker belongs to `cl(R_C)` exactly when a
circuit containing it exists; its coefficients are the corresponding
fundamental stress.  Thus the no-cap condition remains one circuit choice
from four for each of 728 carriers.  Circuit language does not compress the
simultaneous disjunction.

The exact countercontrol is a rational dense source, normalized by a
site-colour torus scaling so all three pure Hafnians are one.  Every one of
168 star and 560 triangle matrices has rank nine.  Consequently every
carrier has zero cap-flex space and all 2,912 blockers have exact fundamental
circuits.  Their detailed ledger has logical SHA
`af9a0926bb4999531ad45a81f236b4addb53dfee2d743a37afe939e7769b28bb`.
All 168 cross-colour tail cells are nonzero.  The witness is deliberately not
an `X5` source: `F_00000001=128308/138113`.  It therefore disproves only a
response-matroid-only implication and identifies the missing datum as the
shared polynomial source coupling.

On the tail side, the frozen `380 x 12` rank-twelve matrix has a free
rank-twelve column matroid and 368 row stresses.  Those stresses see only the
lowest linear layer.  The exact cyclic system
`x-yz=y-xz=z-xy=0` has initial matrix `I_3` but four nonzero remote points,
so initial rigidity still does not imply global zero-tail descent.

The smallest viable upgrade is a source identity carrying tail Fitting
minors to carrier augmented minors, or an algebraic-matroid/Jacobian
calculation on the joint `X5` incidence.  Either restores precisely the
coefficient-level information discarded by the separate matroids.

Standard, optimized, and isolated/no-site modes agree at logical SHA
`758eb4b16fc60e0b0c608a0c59020a6f046f6b0b16b5ae04d73d5933f98a530e`.
