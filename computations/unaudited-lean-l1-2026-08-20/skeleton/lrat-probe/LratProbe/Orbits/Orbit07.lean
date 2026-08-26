/- UNAUDITED — lane L1, generated. Orbit 7 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit7Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_7.cnf")

def orbit7CNF : CNF Nat :=
  orbit7Parsed.map (·.cnf) |>.getD []

theorem orbit7Parsed_ok : orbit7Parsed.isSome = true := by
  native_decide

theorem orbit7Unsat : orbit7CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit7CNF
    (include_str "../../artifacts/n8k4_7.lrat")
  native_decide

end LratProbe.Orbits
