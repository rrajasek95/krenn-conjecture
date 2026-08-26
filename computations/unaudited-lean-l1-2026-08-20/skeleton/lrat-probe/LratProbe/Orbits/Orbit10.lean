/- UNAUDITED — lane L1, generated. Orbit 10 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit10Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_10.cnf")

def orbit10CNF : CNF Nat :=
  orbit10Parsed.map (·.cnf) |>.getD []

theorem orbit10Parsed_ok : orbit10Parsed.isSome = true := by
  native_decide

theorem orbit10Unsat : orbit10CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit10CNF
    (include_str "../../artifacts/n8k4_10.lrat")
  native_decide

end LratProbe.Orbits
