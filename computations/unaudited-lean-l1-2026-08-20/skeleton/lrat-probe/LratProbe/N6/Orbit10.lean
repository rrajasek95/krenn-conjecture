/- UNAUDITED — lane L1, generated. N=6 orbit 10 of 13 (z=0 encoding). -/
import LratProbe.CnfCheck

namespace LratProbe.N6

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit10Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n6/n6_10.cnf")

def orbit10CNF : CNF Nat :=
  orbit10Parsed.map (·.cnf) |>.getD []

theorem orbit10Parsed_ok : orbit10Parsed.isSome = true := by
  native_decide

theorem orbit10Unsat : orbit10CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit10CNF
    (include_str "../../artifacts/n6/n6_10.lrat")
  native_decide

end LratProbe.N6
