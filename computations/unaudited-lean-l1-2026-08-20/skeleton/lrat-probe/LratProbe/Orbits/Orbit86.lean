/- UNAUDITED — lane L1, generated. Orbit 86 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit86Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_86.cnf")

def orbit86CNF : CNF Nat :=
  orbit86Parsed.map (·.cnf) |>.getD []

theorem orbit86Parsed_ok : orbit86Parsed.isSome = true := by
  native_decide

theorem orbit86Unsat : orbit86CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit86CNF
    (include_str "../../artifacts/n8k4_86.lrat")
  native_decide

end LratProbe.Orbits
