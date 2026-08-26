/- UNAUDITED — lane L1, generated. Orbit 17 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit17Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_17.cnf")

def orbit17CNF : CNF Nat :=
  orbit17Parsed.map (·.cnf) |>.getD []

theorem orbit17Parsed_ok : orbit17Parsed.isSome = true := by
  native_decide

theorem orbit17Unsat : orbit17CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit17CNF
    (include_str "../../artifacts/n8k4_17.lrat")
  native_decide

end LratProbe.Orbits
