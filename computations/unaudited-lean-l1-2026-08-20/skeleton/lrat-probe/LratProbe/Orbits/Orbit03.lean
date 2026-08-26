/- UNAUDITED — lane L1, generated. Orbit 3 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit3Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_3.cnf")

def orbit3CNF : CNF Nat :=
  orbit3Parsed.map (·.cnf) |>.getD []

theorem orbit3Parsed_ok : orbit3Parsed.isSome = true := by
  native_decide

theorem orbit3Unsat : orbit3CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit3CNF
    (include_str "../../artifacts/n8k4_3.lrat")
  native_decide

end LratProbe.Orbits
