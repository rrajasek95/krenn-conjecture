/- UNAUDITED — lane L1, generated. Orbit 18 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit18Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_18.cnf")

def orbit18CNF : CNF Nat :=
  orbit18Parsed.map (·.cnf) |>.getD []

theorem orbit18Parsed_ok : orbit18Parsed.isSome = true := by
  native_decide

theorem orbit18Unsat : orbit18CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit18CNF
    (include_str "../../artifacts/n8k4_18.lrat")
  native_decide

end LratProbe.Orbits
