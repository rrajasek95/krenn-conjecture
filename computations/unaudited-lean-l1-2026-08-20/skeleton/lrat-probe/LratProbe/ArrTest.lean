import Std.Tactic.BVDecide.Reflect
set_option maxRecDepth 1000000
open Std.Sat Std.Tactic.BVDecide
def tinyCNF : CNF Nat := [[(0, true)], [(0, false)]]
def tinyProof : Array LRAT.IntAction := #[.addEmpty 3 #[1, 2]]
#eval LRAT.check tinyProof tinyCNF
example : LRAT.check tinyProof tinyCNF = true := by decide
