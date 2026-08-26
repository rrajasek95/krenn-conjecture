/- UNAUDITED — lane L1, generated. Orbit 82 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit82Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_82.cnf")

def orbit82CNF : CNF Nat :=
  orbit82Parsed.map (·.cnf) |>.getD []

theorem orbit82Parsed_ok : orbit82Parsed.isSome = true := by
  native_decide

theorem orbit82Unsat : orbit82CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit82CNF
    (include_str "../../artifacts/n8k4_82.lrat")
  native_decide

end LratProbe.Orbits
