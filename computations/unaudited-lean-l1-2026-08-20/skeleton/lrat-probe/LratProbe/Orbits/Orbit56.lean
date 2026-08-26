/- UNAUDITED — lane L1, generated. Orbit 56 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit56Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_56.cnf")

def orbit56CNF : CNF Nat :=
  orbit56Parsed.map (·.cnf) |>.getD []

theorem orbit56Parsed_ok : orbit56Parsed.isSome = true := by
  native_decide

theorem orbit56Unsat : orbit56CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit56CNF
    (include_str "../../artifacts/n8k4_56.lrat")
  native_decide

end LratProbe.Orbits
