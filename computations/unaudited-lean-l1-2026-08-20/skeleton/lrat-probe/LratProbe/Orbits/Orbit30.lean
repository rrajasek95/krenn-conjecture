/- UNAUDITED — lane L1, generated. Orbit 30 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit30Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_30.cnf")

def orbit30CNF : CNF Nat :=
  orbit30Parsed.map (·.cnf) |>.getD []

theorem orbit30Parsed_ok : orbit30Parsed.isSome = true := by
  native_decide

theorem orbit30Unsat : orbit30CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit30CNF
    (include_str "../../artifacts/n8k4_30.lrat")
  native_decide

end LratProbe.Orbits
