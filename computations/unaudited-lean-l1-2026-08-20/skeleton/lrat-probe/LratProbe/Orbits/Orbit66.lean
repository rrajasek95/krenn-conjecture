/- UNAUDITED — lane L1, generated. Orbit 66 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit66Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_66.cnf")

def orbit66CNF : CNF Nat :=
  orbit66Parsed.map (·.cnf) |>.getD []

theorem orbit66Parsed_ok : orbit66Parsed.isSome = true := by
  native_decide

theorem orbit66Unsat : orbit66CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit66CNF
    (include_str "../../artifacts/n8k4_66.lrat")
  native_decide

end LratProbe.Orbits
