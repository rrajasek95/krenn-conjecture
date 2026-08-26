/- UNAUDITED — lane L1, generated. Orbit 84 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit84Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_84.cnf")

def orbit84CNF : CNF Nat :=
  orbit84Parsed.map (·.cnf) |>.getD []

theorem orbit84Parsed_ok : orbit84Parsed.isSome = true := by
  native_decide

theorem orbit84Unsat : orbit84CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit84CNF
    (include_str "../../artifacts/n8k4_84.lrat")
  native_decide

end LratProbe.Orbits
