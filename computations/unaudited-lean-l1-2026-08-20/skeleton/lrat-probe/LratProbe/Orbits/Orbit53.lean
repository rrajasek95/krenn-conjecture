/- UNAUDITED — lane L1, generated. Orbit 53 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit53Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_53.cnf")

def orbit53CNF : CNF Nat :=
  orbit53Parsed.map (·.cnf) |>.getD []

theorem orbit53Parsed_ok : orbit53Parsed.isSome = true := by
  native_decide

theorem orbit53Unsat : orbit53CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit53CNF
    (include_str "../../artifacts/n8k4_53.lrat")
  native_decide

end LratProbe.Orbits
