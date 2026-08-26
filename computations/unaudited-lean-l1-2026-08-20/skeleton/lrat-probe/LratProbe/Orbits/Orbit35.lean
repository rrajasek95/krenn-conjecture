/- UNAUDITED — lane L1, generated. Orbit 35 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit35Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_35.cnf")

def orbit35CNF : CNF Nat :=
  orbit35Parsed.map (·.cnf) |>.getD []

theorem orbit35Parsed_ok : orbit35Parsed.isSome = true := by
  native_decide

theorem orbit35Unsat : orbit35CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit35CNF
    (include_str "../../artifacts/n8k4_35.lrat")
  native_decide

end LratProbe.Orbits
