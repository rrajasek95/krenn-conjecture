/- UNAUDITED — lane L1, generated. N=6 orbit 8 of 13 (z=0 encoding). -/
import LratProbe.CnfCheck

namespace LratProbe.N6

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit8Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n6/n6_8.cnf")

def orbit8CNF : CNF Nat :=
  orbit8Parsed.map (·.cnf) |>.getD []

theorem orbit8Parsed_ok : orbit8Parsed.isSome = true := by
  native_decide

theorem orbit8Unsat : orbit8CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit8CNF
    (include_str "../../artifacts/n6/n6_8.lrat")
  native_decide

end LratProbe.N6
