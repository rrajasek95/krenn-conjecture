/-
Copyright 2026 Rishi.
Released under Apache 2.0 license.
-/

import MatchingModel

/-! Axiom audit of every public declaration in the matching-model bridge. -/

#print axioms KrennAllOrders.MatchingModel.V
#print axioms KrennAllOrders.MatchingModel.EdgeN
#print axioms KrennAllOrders.MatchingModel.WeightsN
#print axioms KrennAllOrders.MatchingModel.mkEdge
#print axioms KrennAllOrders.MatchingModel.vertices
#print axioms KrennAllOrders.MatchingModel.pmSumListAux
#print axioms KrennAllOrders.MatchingModel.pmSumList
#print axioms KrennAllOrders.MatchingModel.pmSumN
#print axioms KrennAllOrders.MatchingModel.allEqualList
#print axioms KrennAllOrders.MatchingModel.allEqual
#print axioms KrennAllOrders.MatchingModel.EqSystemN
#print axioms KrennAllOrders.MatchingModel.SiteVariable
#print axioms KrennAllOrders.MatchingModel.MatchingPolynomial
#print axioms KrennAllOrders.MatchingModel.edgePolynomial
#print axioms KrennAllOrders.MatchingModel.matchingPolynomialAux
#print axioms KrennAllOrders.MatchingModel.matchingPolynomialList
#print axioms KrennAllOrders.MatchingModel.matchingPolynomialN
#print axioms KrennAllOrders.MatchingModel.selector
#print axioms KrennAllOrders.MatchingModel.eval_edgePolynomial
#print axioms KrennAllOrders.MatchingModel.eval_matchingPolynomialAux
#print axioms KrennAllOrders.MatchingModel.eval_matchingPolynomialN
#print axioms KrennAllOrders.MatchingModel.matchingPolynomialList_nil
#print axioms KrennAllOrders.MatchingModel.matchingPolynomialList_singleton
#print axioms KrennAllOrders.MatchingModel.wordExponent
#print axioms KrennAllOrders.MatchingModel.wordExponent_wrong_color
#print axioms KrennAllOrders.MatchingModel.wordExponent_erase
#print axioms KrennAllOrders.MatchingModel.coeff_edgePolynomial_mul
#print axioms KrennAllOrders.MatchingModel.coeff_matchingPolynomialAux
#print axioms KrennAllOrders.MatchingModel.coeff_matchingPolynomialList
#print axioms KrennAllOrders.MatchingModel.coeff_matchingPolynomialN
#print axioms KrennAllOrders.MatchingModel.coeff_matchingPolynomialList_eq_selector
#print axioms KrennAllOrders.MatchingModel.siteWeight
#print axioms KrennAllOrders.MatchingModel.siteProfile
#print axioms KrennAllOrders.MatchingModel.siteWeight_apply
#print axioms KrennAllOrders.MatchingModel.siteProfile_erase
#print axioms KrennAllOrders.MatchingModel.siteProfile_apply
#print axioms KrennAllOrders.MatchingModel.siteProfile_nodup
#print axioms KrennAllOrders.MatchingModel.edgePolynomial_siteHomogeneous
#print axioms KrennAllOrders.MatchingModel.matchingPolynomialAux_siteHomogeneous
#print axioms KrennAllOrders.MatchingModel.matchingPolynomialList_siteHomogeneous
#print axioms KrennAllOrders.MatchingModel.vertices_eq_finRange
#print axioms KrennAllOrders.MatchingModel.vertices_nodup
#print axioms KrennAllOrders.MatchingModel.vertices_pairwise_lt
#print axioms KrennAllOrders.MatchingModel.mem_vertices
#print axioms KrennAllOrders.MatchingModel.matchingPolynomialN_siteHomogeneous
#print axioms KrennAllOrders.MatchingModel.matchingPolynomialN_siteDegree
#print axioms KrennAllOrders.MatchingModel.matchingPolynomialN_localDegree
#print axioms KrennAllOrders.MatchingModel.eqSystemN_iff_coefficients
#print axioms KrennAllOrders.MatchingModel.edgePolynomial_add
#print axioms KrennAllOrders.MatchingModel.reverseEdge
#print axioms KrennAllOrders.MatchingModel.edgePolynomial_reverse
#print axioms KrennAllOrders.MatchingModel.pmSumListAux_congr_ordered
#print axioms KrennAllOrders.MatchingModel.pmSumN_congr_ordered
