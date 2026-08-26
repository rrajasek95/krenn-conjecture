/- UNAUDITED — lane L1, generated. Orbit 32 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit32Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_32.cnf")

def orbit32CNF : CNF Nat :=
  orbit32Parsed.map (·.cnf) |>.getD []

theorem orbit32Parsed_ok : orbit32Parsed.isSome = true := by
  native_decide

theorem orbit32Unsat : orbit32CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit32CNF
    (include_str "../../artifacts/n8k4_32.lrat")
  native_decide

end LratProbe.Orbits
