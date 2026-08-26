/- UNAUDITED — lane L1, generated. Orbit 44 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit44Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_44.cnf")

def orbit44CNF : CNF Nat :=
  orbit44Parsed.map (·.cnf) |>.getD []

theorem orbit44Parsed_ok : orbit44Parsed.isSome = true := by
  native_decide

theorem orbit44Unsat : orbit44CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit44CNF
    (include_str "../../artifacts/n8k4_44.lrat")
  native_decide

end LratProbe.Orbits
