#!/usr/bin/env python3
"""Exact obstruction on a minimal two-cell transverse R2-restoration plane.

The plane moves cells 04(0,0) and 05(0,0) from the rank-54/52 full-R2
base. Its full-R2 locus is exactly s=0 union t=-84. Polynomial kernel
certificates force rank at most 54 on both lines.

Standard library only; checks remain live under python -O and python -I -S.
"""

from base64 import b85decode
from hashlib import sha256
from itertools import product
from json import loads
from pathlib import Path
from runpy import run_path
from zlib import decompress


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
site5 = run_path(str(
    HERE
    / "verify_level_two_two_invertible_transverse_column_site5_one_cell_r2_obstruction.py"
))
site4 = site5["site4"]
survivor = site4["survivor"]
rank_core = site4["rank_core"]
dense_core = site4["dense_core"]

BASE_BLOCKS = site4["BASE_BLOCKS"]
SITES = site4["SITES"]
COLOURS = site4["COLOURS"]
EDGES = site4["EDGES"]
CELLS = site4["CELLS"]
WORDS = site4["WORDS"]

CERTIFICATE_B85 = (
    "c-oDaTdo|t4MpeT?`}X8NlDCK?lcUKB*@&eHdXDw0q!|5j6Ue<Dm}>kQvK`4KY#q==g*(^vMih7HOH^l&-v%q^~!0>=UI99dS0F*"
    "EM|Hb-)+41$#RQvzx(TL+`ZSFzH2RA%a^%%Y@RzqgW7(*_pwoD?6MKM#K>pNZQ(vcQ_aaxV~sOwo?cnJ%6*Tq>P&rSZKZh*|Mk6i"
    ";EbqX$Q`|2x7XW`GiK#Et1mI`Vb)q%*?V*?dNQip91&ZCd%WJceePs;Sz4m!Yt|k<txoiF=k=ar?;W*HaUrOs2ajcr6`{=sV>>gQ"
    "Wy6-9ihP~zUSrM`O9Mx}Y}Yu!e9;BUsb&9Bj%1)er%$F2Kaq3q<(@}lB}G_+1|HipH#2fkJwC-y=jrf&zbq!&=Bu)1_xC+lTIRk>"
    "qrdMxXeCXE+h3!)Ny+`(JN9eYtU;BRt=mZ!dYny`_n@<D$@cc_4$!!F0um2^bsJ}Z#c7eRTYY=YNE?hW?uGva13f#HrfzZdHY_}M"
    "37oZVckJY1+Wty!-ezDE$dpGsz2TWvbnxlS`_H}5hd;MM%_rEQ+)giY{i3`-{(5-yww*qT4pCsLuaPET^c4nSy7an-R@43gAhZyQ"
    "&z44<<cik)GVRef)i49KbbADYz&vd<Ug?$_WX^FGmwA#cQoZoF8>7B!X4r|NZn16pNt?NQz~rt6U9wnAtWNU0Iczi$QUHVQ<Dqj-"
    "Ds-4YwFG6E3(_)~YszjY41b@9Dq~tZKGt3!mA&N{2d3Sw8tW>y$qLw0ZptvVC|gH=Dd$HVJdhM&m_0g-Hb}kJIpf&bF(1Kzw5%O0"
    "FDS?F?1pZgv5cLuvR;}*VLOdjtEe>n&FOGsQ*A!#fgm{N8E%k}O)xYH@=y}whL+mAinQtQ*(?qD)9z^Cu7gNq(#MPSd05aim%MCN"
    ")#X^G2{RtydV88}wjKPKzS!wLTjI4Oqmvr&h?JHxEh-vlP&Ak#*M~DXC|hJ6TMJA=>S}QSf(XN-e{hwe@Dqz-xm0Hcn4T4L4zq_{"
    "-}eQ^!N$d=Ctc-EkhvyYIGZLx)~ktuLr{Cx1UJz+3dB=_@d;a1O(UfA9WgdArqH4oaDfp^OhFfHH-q=fsDHq7O0|;e4TfQ8mN3sl"
    "YN&CL*ENO&4<t8R=`0JPIr9=dBw8f_rFB5n=of!Q4e;<`zccQZc;k5pi<}S4!9BKDap?!3=4QSPo{%81Hh~G20$Qo?of75vKhTM&"
    "e_sY^&Y+=l2v)$Kk0Aj8bFsOHc8x3jlCHIpuqgNsoLBZgR>#8(`?$dy_W?1mA#iG=R|8JaC9r$0PEBvM*y5YHJQtvKRc@cTgAPwG"
    "a2W^^Kt0u_R^YyM3YK9{Cb%$?WRTHxiD|D)31ro?0!n^bacD6;8pE$0(F6+O;usEOo7OwlMj5Z9^g7N|2TYY=8%iiVf+&(VS_9%m"
    "QP?4xim#yr12;+}mdTlRJQBu^#abg!;D-hkhd3DMb@qZKU^ocou;D~08W?RyfsvNAuPsZz)D#5(d{rP~;lLpDz<@r#<qNi>4C!Pc"
    "2E~U=en-K(Rad-d2%MZKNzks8KW)h%%esI>y1;!QRfUIwF}6>$TvV?HP$wxE$^(e_raEMe#Pw`R#I7gPF8WI|Kr3rd$(af@2dUKp"
    "fNX&}q5*DzRxQC9jo{`%zKJVaR3DINF>tTVBE<-Frgt=zSz1xB6*+O!7BtgZ)hFjC$bo5L4~SDl$sXi@oDd8NXapkJtXIB>S%Gg9"
    "j3@xPph<pUYP6opIpI_HrQb=(RN7dt3HAH7sT~oCanMD{O{!bmEsX|wQnx2Fs_a|w6Pe~C<lX>@$_m+!^r4BUJ|s2oIHv@Hxx(Xk"
    "!p!clLR?}6P3bde1*~v2uelL}pump<*+KC(WhVV>IF@a@Pafr&nw~v!$sW*0V8Dl@@`_{1_$UTpVU@@#?6UGbE;*1!S3t%@n6Ksx"
    "bpr|_O0d0qA9VIxmLZ<=Oi3QjvsouvK*<?`yX}HV%K05J(9Lgan7GH5uAt25D`Tcy1dd|_+aGP{5RJYy+;Mzl#b|W4&mI-_qpcY7"
    "Q3=%BDbrWUSvMwH<gE3PR+C6kx+DB5abnvk?6rhQS;1MA(i6a@V|b}4UXG8ho=yWe384|$2CT}c+4+KaLAZp(aGsQ!5S0@Uy0ULj"
    "hNBc<6P-{_@c>R~4obf60q%Xs-YGMMF@RapBt5t~fS^J%*A8he`6PypIGlkv!L*v7rnH|i6waZWwdcV(Z_j_UR9=X!p%i%ErjOVJ"
    "#1ip3ezugR0t@+wj=+A9f^eNal|4c#`l&LQ*%l0B)wCFR)aR%H&`#%RkV^-dGdnZbrGO+fmmrD9AY9rAKp@0NTl*DI%xiY$JYbvA"
    "f(*gJ_D4P;2JQl=!COk#m8n7k5YPFBJ8CNAfo}JE)V(bG997vlZK9Y+E8&l!l;HCw%l#6dfCUc5jwLEb=4y{3$}RRmZmAD;T_jh="
    "5RY_H>2jf(I3DRj?sb?MVhCF5_1#D-rlVG=v*qeE<vLq1)T;S8FY5#(@)Ai<1*DJ=IK@M`_oJ6zcMi4Gp@j4RMd1^_!X&L81!@>e"
    "Dxn=?^HAypN`26nBLVi`84-?A0od6X=8Qs7s(V@MBa?JQdjbY5;V1y6tCzjy(EACkPVt0;9DSWK00xB~pL3z?DZPCOwn3|-_(X~G"
    "9s`j`j#)@OJSX}Rnvj{+uBY}0Bz-6S>0p7-gB*Mn8RRf@k1LYLZ)k%!x(K6}1Il74#3EQ6c^|7s8oz-%!uU<ikVQQ3^dn1eJC+uJ"
    "%@Y@hvL8`QsZZf1rOdh&%zzHdV1ZpXDWW*xuDX=|O<6h&6G@r%w;&R|iG1><U?FT<N%490BF9|PCz${%1&~_&wRmNcGf4unZS)7F"
    "qvEGuYjk{+IDsfeS5Y>rVV?VffYU!&8kLht7Q3VPp?n|bbFc+#K$O#9Nza#J%#>SSkz*i?UT+X&c@VOLZrzs)NF19|GUkw@0~Ndj"
    "3*7Q~DZ;inM0;DIj85rYcVE**xr8ts8ZC8r#}87kCPsWz3tyoa6qF&5n-170*gg25S&FGsBqQ=lvuFZ0#+9^wT|(QH1Zgo8Inng^"
    "9rnKXb?J=`8&~e-3;-0Btk;tQu~p-;NjX3na<eJ_eBN%MREMpssYC((Wg|y<=@AcQJ1}JuyYW~PpdfD4H8_cs;tShi;Hh^KD45P_"
    "p3keHH?`nLYKi{fR2@TxV)}Wa8h9lKZV3*jvr<CPaqYTB$21PjZ7K+ca_mwivHtmqXmr0y7GJt3OFeptdBc0_4vl4*SUh;vN&tU7"
    "juH}D2*`D6Bk?1YY7sm!u3+d*p<Yc%P8hxV_|CELqgz^n&TJeZH7ota>UHk5d$?*t_yVAaNvH-G7YN^a&BHDx{L1He`u+-l=*X89"
    "Kt=k!2ThIavqtEQs&~30pF=Bc1T;!u=sO7xMFdKOiQ5JVh|V&gVTyR{29-g8ce{whqiyf+fvN=jcfbDn_3!@x5R%@|"
)
CERTIFICATE_SHA256 = (
    "3392f3490091d86f0c8d24fcc1173e052c6c763b823fd228c14a8bcf8f30803b"
)
EXPECTED_DEGREES = {"A": 1, "B": 4}


def decode_certificates():
    raw = decompress(b85decode(CERTIFICATE_B85))
    require(sha256(raw).hexdigest() == CERTIFICATE_SHA256,
            "restoration-plane certificate digest changed")
    decoded = loads(raw)
    require(frozenset(decoded) == frozenset(EXPECTED_DEGREES),
            ("restoration-plane certificate labels changed", decoded.keys()))
    certificates = {}
    for label, coefficient_lists in decoded.items():
        vectors = []
        for sparse in coefficient_lists:
            vector = [0] * len(CELLS)
            for index, value in sparse:
                require(0 <= index < len(CELLS),
                        ("certificate index escaped", label, index))
                require(vector[index] == 0,
                        ("duplicate certificate index", label, index))
                vector[index] = value
            vectors.append(vector)
        certificates[label] = tuple(vectors)
    require({
        label: len(vectors) - 1
        for label, vectors in certificates.items()
    } == EXPECTED_DEGREES, "restoration-plane degrees changed")
    return certificates, len(raw)


CERTIFICATES, CERTIFICATE_BYTES = decode_certificates()


def plane_blocks(s_value, t_value):
    blocks = dict(BASE_BLOCKS)
    for edge, row, column, increment in (
        ((0, 4), 0, 0, s_value),
        ((0, 5), 0, 0, t_value),
    ):
        changed = [list(entries) for entries in blocks[edge]]
        changed[row][column] += increment
        blocks[edge] = tuple(tuple(entries) for entries in changed)
    return blocks


def differential(blocks):
    return site4["differential"](blocks)


def matrix_vector(matrix, vector):
    return [
        sum(entry * value for entry, value in zip(row, vector))
        for row in matrix
    ]


def add_vectors(*vectors):
    return [
        sum(vector[index] for vector in vectors)
        for index in range(len(vectors[0]))
    ]


def audit_plane_and_r2_locus():
    require(BASE_BLOCKS[0, 4] == ((0, 85), (0, 87)),
            ("base 04 block changed", BASE_BLOCKS[0, 4]))
    require(BASE_BLOCKS[0, 5] == ((84, 87), (0, 28)),
            ("base 05 block changed", BASE_BLOCKS[0, 5]))

    # These four representatives cover the zero/nonzero support strata
    # s=0 versus s!=0 and 84+t=0 versus 84+t!=0.
    expected = {
        (0, 0): (),
        (0, -84): (),
        (1, 0): (0,),
        (1, -84): (),
    }
    tables = {}
    for point, failing_expected in expected.items():
        table, failing = site4["r2_tables"](plane_blocks(*point))
        require(failing == failing_expected,
                ("restoration-plane R2 stratum changed",
                 point, failing, table))
        tables[point] = table

    require(tables[0, 0][0][1] == (4,),
            ("root-0 base output-one witness changed", tables[0, 0][0]))
    require(tables[1, -84][0][1] == (5,),
            ("root-0 restored output-one witness changed",
             tables[1, -84][0]))
    require(not tables[1, 0][0][1],
            ("off-locus point retained output one", tables[1, 0][0]))

    # From the two literal blocks above:
    # M04 is pure in output one iff s=0, while M05 is pure in output one
    # iff 84+t=0. All output-zero and other-root witnesses are fixed.
    return expected, tables


def audit_generic_kernel_and_selected_rows():
    require(
        (0, 4) in site4["old"]["FREE_EDGES"]
        and (0, 5) in site4["old"]["FREE_EDGES"],
        "a restoration-plane edge left the free cut",
    )
    require(
        survivor["POTENTIAL"][0] + survivor["POTENTIAL"][4] == 0
        and survivor["POTENTIAL"][0] + survivor["POTENTIAL"][5] == 0,
        "a restoration-plane multiplier became nonzero",
    )
    numerator_vector = []
    for u, v, a, b in CELLS:
        numerator = dense_core["matrix_product"](
            dense_core["matrix_product"](
                survivor["X"][u], survivor["J"]
            ),
            dense_core["transpose"](survivor["X"][v]),
        )
        numerator_vector.append(numerator[a][b])

    scalar_checks = 0
    selected_checks = 0
    for s_value, t_value in product((0, 1), repeat=2):
        blocks = plane_blocks(s_value, t_value)
        for u, v in EDGES:
            numerator = dense_core["matrix_product"](
                dense_core["matrix_product"](
                    survivor["X"][u], survivor["J"]
                ),
                dense_core["transpose"](survivor["X"][v]),
            )
            multiplier = survivor["POTENTIAL"][u] + survivor["POTENTIAL"][v]
            for a, b in product(COLOURS, repeat=2):
                require(
                    numerator[a][b] == multiplier * blocks[u, v][a][b],
                    ("restoration-plane generic-kernel corner failed",
                     s_value, t_value, u, v, a, b),
                )
                scalar_checks += 1
        derivative = differential(blocks)
        tangent = matrix_vector(derivative, numerator_vector)
        values = site4["packet"](blocks)
        slope = [
            rank_core["hafnian"](values, SITES, word)
            for word in WORDS
        ]
        require(all(
            -slope_value + tangent_value == 0
            for slope_value, tangent_value in zip(slope, tangent)
        ), ("restoration-plane selected corner failed", s_value, t_value))
        selected_checks += len(WORDS)
    return scalar_checks, selected_checks


def family_data(label):
    if label == "A":
        base = plane_blocks(0, 0)
        unit = plane_blocks(0, 1)
        evaluation = plane_blocks(0, 2)
    else:
        require(label == "B", ("unknown family label", label))
        base = plane_blocks(0, -84)
        unit = plane_blocks(1, -84)
        evaluation = plane_blocks(2, -84)
    d0 = differential(base)
    d_unit = differential(unit)
    d1 = [
        [entry - base_entry for entry, base_entry in zip(row, base_row)]
        for row, base_row in zip(d_unit, d0)
    ]
    return base, evaluation, d0, d1


def evaluate_polynomial(vectors, value):
    answer = [0] * len(CELLS)
    power = 1
    for vector in vectors:
        answer = add_vectors(answer, [power * entry for entry in vector])
        power *= value
    return answer


def audit_polynomial_kernels():
    results = {}
    for label, vectors in CERTIFICATES.items():
        _base, evaluation, d0, d1 = family_data(label)
        degree = len(vectors) - 1
        zero = [0] * len(CELLS)
        for coefficient in range(degree + 2):
            x_now = vectors[coefficient] if coefficient <= degree else zero
            x_before = vectors[coefficient - 1] if coefficient else zero
            image = add_vectors(
                matrix_vector(d0, x_now),
                matrix_vector(d1, x_before),
            )
            require(not any(image),
                    ("restoration-plane kernel coefficient failed",
                     label, coefficient))

        gauges = []
        for basis in range(5):
            mu = [0] * 6
            mu[basis] = 1
            mu[5] = -1
            gauges.append(site4["gauge_tangent"](evaluation, mu))
        extra = evaluate_polynomial(vectors, 2)
        columns = gauges + [extra]
        independent_rank = dense_core["rational_rank"]([
            [column[row] for column in columns]
            for row in range(len(CELLS))
        ])
        require(independent_rank == 6,
                ("restoration-plane kernel lost independence",
                 label, independent_rank))
        results[label] = (degree, independent_rank)
    return results


def append_columns(matrix, *columns):
    return [
        row[:] + [column[index] for column in columns]
        for index, row in enumerate(matrix)
    ]


def incidence_signature(blocks):
    derivative = differential(blocks)
    pure_zero = [int(word == (0,) * 6) for word in WORDS]
    pure_one = [int(word == (1,) * 6) for word in WORDS]
    mixed = [
        row
        for row, word in zip(derivative, WORDS)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    return tuple(
        dense_core["rational_rank"](matrix)
        for matrix in (
            derivative,
            mixed,
            append_columns(derivative, pure_zero),
            append_columns(derivative, pure_one),
            append_columns(derivative, pure_zero, pure_one),
        )
    )


def audit_calibrations():
    signatures = {
        (0, 0): incidence_signature(plane_blocks(0, 0)),
        (0, -84): incidence_signature(plane_blocks(0, -84)),
        (1, -84): incidence_signature(plane_blocks(1, -84)),
        (1, 0): incidence_signature(plane_blocks(1, 0)),
    }
    require(signatures == {
        (0, 0): (54, 52, 54, 54, 54),
        (0, -84): (53, 51, 53, 53, 53),
        (1, -84): (54, 52, 54, 54, 54),
        (1, 0): (55, 53, 55, 55, 55),
    }, ("restoration-plane calibrations changed", signatures))
    return signatures


def main():
    r2, _tables = audit_plane_and_r2_locus()
    generic, selected = audit_generic_kernel_and_selected_rows()
    kernels = audit_polynomial_kernels()
    signatures = audit_calibrations()
    print("dense transverse minimal R2-restoration plane: all checks passed")
    print(f"  R2 support strata           : {r2}")
    print(f"  generic/selected checks     : {generic}/{selected}")
    print(f"  full-R2 kernel degrees      : {kernels}")
    print(f"  incidence calibrations      : {signatures}")
    print(f"  certificate bytes/SHA-256   : {CERTIFICATE_BYTES}/{CERTIFICATE_SHA256}")


if __name__ == "__main__":
    main()
