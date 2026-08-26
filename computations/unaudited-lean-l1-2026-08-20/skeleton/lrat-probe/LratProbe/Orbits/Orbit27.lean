/- UNAUDITED — lane L1, generated. Orbit 27 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit27Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_27.cnf")

def orbit27CNF : CNF Nat :=
  orbit27Parsed.map (·.cnf) |>.getD []

theorem orbit27Parsed_ok : orbit27Parsed.isSome = true := by
  native_decide

theorem orbit27Unsat : orbit27CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit27CNF
    (include_str "../../artifacts/n8k4_27.lrat")
  native_decide

end LratProbe.Orbits
