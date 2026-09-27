/-
Copyright (c) 2026 Rishi. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/

import WickCovariance

/-! # Axiom audit for explicit finite Wick moments and covariance identities -/

#print axioms KrennAllOrders.WickCovariance.covariancePair
#print axioms KrennAllOrders.WickCovariance.covariancePair_apply
#print axioms KrennAllOrders.WickCovariance.pairingProduct
#print axioms KrennAllOrders.WickCovariance.pairingProduct_apply
#print axioms KrennAllOrders.WickCovariance.wickMoment
#print axioms KrennAllOrders.WickCovariance.wickMoment_apply
#print axioms KrennAllOrders.WickCovariance.wickMoment_zero
#print axioms KrennAllOrders.WickCovariance.wickMoment_permute
#print axioms KrennAllOrders.WickCovariance.wickMoment_const
#print axioms KrennAllOrders.WickCovariance.slots_one_cases
#print axioms KrennAllOrders.WickCovariance.wickMoment_one
#print axioms KrennAllOrders.WickCovariance.wickMoment_update_add
#print axioms KrennAllOrders.WickCovariance.wickMoment_update_smul
#print axioms KrennAllOrders.WickCovariance.wickMoment_linear_expansion
#print axioms KrennAllOrders.WickCovariance.wickMoment_naturality
#print axioms KrennAllOrders.WickCovariance.wickMoment_invariant
#print axioms KrennAllOrders.WickCovariance.evenSlotsEquiv
#print axioms KrennAllOrders.WickCovariance.centeredMoment
#print axioms KrennAllOrders.WickCovariance.centeredMoment_of_even
#print axioms KrennAllOrders.WickCovariance.centeredMoment_of_not_even
#print axioms KrennAllOrders.WickCovariance.centeredMoment_naturality
#print axioms KrennAllOrders.WickCovariance.centeredMoment_permute
#print axioms KrennAllOrders.WickCovariance.meanProduct
#print axioms KrennAllOrders.WickCovariance.meanProduct_apply
#print axioms KrennAllOrders.WickCovariance.shiftedTerm
#print axioms KrennAllOrders.WickCovariance.shiftedTerm_apply
#print axioms KrennAllOrders.WickCovariance.shiftedMoment
#print axioms KrennAllOrders.WickCovariance.shiftedMoment_apply
#print axioms KrennAllOrders.WickCovariance.shiftedMoment_linear_expansion
#print axioms KrennAllOrders.WickCovariance.shiftedMoment_naturality
#print axioms KrennAllOrders.WickCovariance.shiftedMoment_invariant
#print axioms KrennAllOrders.WickCovariance.replicaCovariance
#print axioms KrennAllOrders.WickCovariance.replicaCovariance_apply
#print axioms KrennAllOrders.WickCovariance.replicaLinear
#print axioms KrennAllOrders.WickCovariance.replicaLinear_apply
#print axioms KrennAllOrders.WickCovariance.replicaLinear_covariance
#print axioms KrennAllOrders.WickCovariance.alternatingProduct
#print axioms KrennAllOrders.WickCovariance.alternatingProduct_replicaLinear
#print axioms KrennAllOrders.WickCovariance.replicaRotation
#print axioms KrennAllOrders.WickCovariance.replicaRotation_apply
#print axioms KrennAllOrders.WickCovariance.replicaRotation_covariance
#print axioms KrennAllOrders.WickCovariance.wickMoment_replicaRotation
#print axioms KrennAllOrders.WickCovariance.shiftedMoment_replicaRotation
#print axioms KrennAllOrders.WickCovariance.shiftedMoment_replicaLinear
