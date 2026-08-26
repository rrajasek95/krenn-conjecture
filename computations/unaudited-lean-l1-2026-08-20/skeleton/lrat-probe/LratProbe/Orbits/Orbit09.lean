/- UNAUDITED — lane L1, generated. Orbit 9 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit9Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_9.cnf")

def orbit9CNF : CNF Nat :=
  orbit9Parsed.map (·.cnf) |>.getD []

theorem orbit9Parsed_ok : orbit9Parsed.isSome = true := by
  native_decide

theorem orbit9Unsat : orbit9CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit9CNF
    (include_str "../../artifacts/n8k4_9.lrat")
  native_decide

end LratProbe.Orbits
