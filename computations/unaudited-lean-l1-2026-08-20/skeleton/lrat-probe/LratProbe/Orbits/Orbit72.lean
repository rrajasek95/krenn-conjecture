/- UNAUDITED — lane L1, generated. Orbit 72 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit72Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_72.cnf")

def orbit72CNF : CNF Nat :=
  orbit72Parsed.map (·.cnf) |>.getD []

theorem orbit72Parsed_ok : orbit72Parsed.isSome = true := by
  native_decide

theorem orbit72Unsat : orbit72CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit72CNF
    (include_str "../../artifacts/n8k4_72.lrat")
  native_decide

end LratProbe.Orbits
