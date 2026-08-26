# Independent rank-two chart-design referee

Status: **PASS for orientation and chart coverage only.** No Singular job was launched, and this package does not claim any chart ideal is the unit ideal.

The sealed rank-one theorem (manifest `45ab914f...`) correctly closes `rank(A57)<=1` on the canonical support. For rank two, writing `A57=UV^T` gives `A56^T=-A26VU^T` and therefore `A56=-U(A26V)^T`. Because `U` has rank two, the other guard equations reduce exactly to `A06V=0` and `(I-A17A26)V=0`. The three response maps and their reduction to eighteen dual variables have the same orientation as the physical formulas.

The five proposed charts are exhaustive. A rank-two `U` and `V` each have a nonzero row minor; label their omitted rows by `r,s`, and label the failed diagonal coordinate by `i`. Simultaneous color permutation has exactly the five equality-pattern orbits `i=r=s`, `i=r!=s`, `i=s!=r`, `r=s!=i`, and all distinct. The listed charts are representatives after normalizing `i=0`. The inverse-minor equation closes each chart against rank drop.

The remaining obligation is proof-producing characteristic-zero elimination on all five charts. Even after that, the result applies only to the canonical support; the other five full-family support orbits and any transport to all 64 coefficient loci remain separate obligations.
