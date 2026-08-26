/- UNAUDITED — lane L1, generated. Orbit 2 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit2Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_2.cnf")

def orbit2CNF : CNF Nat :=
  orbit2Parsed.map (·.cnf) |>.getD []

theorem orbit2Parsed_ok : orbit2Parsed.isSome = true := by
  native_decide

theorem orbit2Unsat : orbit2CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit2CNF
    (include_str "../../artifacts/n8k4_2.lrat")
  native_decide

end LratProbe.Orbits
