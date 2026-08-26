/- UNAUDITED — lane L1, generated. Orbit 47 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit47Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_47.cnf")

def orbit47CNF : CNF Nat :=
  orbit47Parsed.map (·.cnf) |>.getD []

theorem orbit47Parsed_ok : orbit47Parsed.isSome = true := by
  native_decide

theorem orbit47Unsat : orbit47CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit47CNF
    (include_str "../../artifacts/n8k4_47.lrat")
  native_decide

end LratProbe.Orbits
