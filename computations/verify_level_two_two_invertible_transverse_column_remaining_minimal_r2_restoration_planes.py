#!/usr/bin/env python3
"""Exclude the three remaining sharp minimal transverse R2-repair planes.

Together with the earlier 04(0,0)/05(0,0) plane, these cover the four
rank-raising zero-cell lifts on 04 and 14, each paired with the unique
one-cell cancellation that makes the alternate site-5 spoke pure.

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
first = run_path(str(
    HERE
    / "verify_level_two_two_invertible_transverse_column_minimal_r2_restoration_plane.py"
))
site4 = first["site4"]
survivor = first["survivor"]
rank_core = first["rank_core"]
dense_core = first["dense_core"]

BASE_BLOCKS = first["BASE_BLOCKS"]
SITES = first["SITES"]
COLOURS = first["COLOURS"]
EDGES = first["EDGES"]
CELLS = first["CELLS"]
WORDS = first["WORDS"]

# label: (rank-raising cell, alternate-witness cancellation cell, constant)
PLANES = {
    "R0b": ((0, 4, 1, 0), (0, 5, 0, 0), 84),
    "R1a": ((1, 4, 0, 0), (1, 5, 1, 0), 37),
    "R1b": ((1, 4, 1, 0), (1, 5, 1, 0), 37),
}

CERTIFICATE_B85 = (
    "c-n=TOOhP95k&7Y>nbxK@Yhar4caWEYshqWy$2wB*reDb$2i@YRY)Mh-NPgDKY#o)|M8D+-@fJ7JGYgimKEu**SGlL_x{Q$#^|Y+"
    "RQY{!f3-U5N@XlA<n(%v*;dIl)$E1xieB5OeWW!?_fmW1$h}8h(dTlV%)%vQmT9HWG`%!lkz=KiYNWCDB_3BM8_2bksQc1-@$=-n"
    "W3Ih=xaZ2noLZmZmHK+~>5^8>tNOU;uXkHLqD=nt!g}>K%UrXwyeBP$qI2rrN1bfdOYxd3r`6kPI~t|DR>X>2IoQ6?c+wiFL|(J*"
    "EAz$f2La-w{9cW4As(f*)N6IewY&;z&Yn}=%T$(`qm-3`*ma*>7vCEzO&%3B`KcDKAA-?{^{1z|NpxmyrmU1UU8!-@L`r8K(a7Xq"
    "TqEzqkG##&cEmpaO0@FK0D)z8(nlsMv+dBCaaXG``pFWzNI5UEou7Qqk$M|>rhUF__-BpEf3Y`8vfqOhR&L;^Ke-k*tF{#<(_js#"
    "0T2G(OcU2KfYv;Dj>fK7XFge8BXS;X$B-nyXYZ!H$CKldm*`$6f<^G8lq01+MvjwYE|tC-tJd64noB7psI|3eK$ZdF0B$vIk~_Iv"
    "wUC{8Qv9x&WjSQp=Of2#tO~JF_5n#TaRc*pfYK+!--m$wzCS;h1iyjODz&h+voZ;O_bFpDN2smu4D-R55i^Z;lNNJ=-ri2i+&_m*"
    "8(K27z&*~pZo)`0xN0Zzr0etj`T8Cpk`l;4%l_mkgF!NtE*;C7Egu-0B><b};awPoIp-J<<b;+l&OF-<?5DdeK0}jufV>fCQkP2{"
    "{f|G>zpu9O$<k^aDZ~9fTFu61iqw%0>?hymP`!Z?qA>>ig8pr!qY7e>bRb`4fN6+Skq6?R+s-P$t_$8yvIc)viJo(x<bxkKN;{$M"
    "Ltdkt+!#?nLFS1BWk;7Y@X^xwN>j(y0{8MQ6%f@Pj?I+WRPStet;T_8X3Hq0@VLC|if46g(8p;@=O2RC(X11GQ%gKjBcPyDqLSzl"
    "kb=jxBm3l=gO*I-Q>invJ3a~*5z!H8vr7z+V<2C~<Vawhnt;$vo(|jdMFy}W(@|R@vXqWqQxphFAnN8yq!%17)|52C4W$M#3Le9D"
    "j)ooPlbBwkahv0;1VLdBxmo?fEVm&>yXfgXw^kNfK@8RwDv(!t351TY1<^%U_%=C*linXMVu1#dP$SL%gYA&4Ls<2M<bs1twot$d"
    "GA3H09=X-L6TVeu$sP(&_q<E0)xmu@*xQkrtvtU=gkm%Vrj;sq(&~AdVxFA@(%et9;DJ$5)C@6qfDXVMY*&T3#j2ts4TVA47BFsb"
    "a47ohtd_m2vBi&Xwk_$CgOcJdV&mvoenF!d<eP1)4+y<*<|IqN)(`n3+uTI|2!#|T=7<WVh{AUiu?Tu%5Nje<$@*M_xRJD055bU!"
    "IW0BFB(xwutstyjdqH6K<F+dN7K^IsZv&vfhQ@*VkfXsv64C;5VX4Z>#F1*S09_3gK!aO3SJ+05p&+{2#rCPRARnP-$wsvr@D+M4"
    "V1`U=4XO=sA>4!Sb<vFYfNk8&RiJ7zVri7JWfx*onNFS2T?j1}Fk<kivnPyJC^@&5M|0zd4g1J?D{?p3`Kf_87EO-gxHuAfB&!HC"
    "`>7jV+3;#JEUmDnR8yUXRi8-rD^LJu)KvIh+hl+toysf;$72JDHQP@KH!1y5S<I2bSli<i012T+X~`!M>zxf-@>)LC1#QB#Rga6M"
    "VMWLV!4!Aue7(LAuTmk+QJblzFDYbNj|?tk5F3T8t04q~a=scK42izWAWU!|$avqTi;aOL?F5@1@l-lggeRZ{)h`PuXpg*X54npU"
    "Y~jQ}7AD~QEH+6jZ&;#A3-3@=957K76Ds+<cd5LnRi6493V63DLwmNmZzICL$;?qL>!(h{$ZaH1s?eeu=P?C;P&-<Lgd#|YOsJw%"
    "A*g;xrmUfe6IIPoHjGK+M4AZmxN;R+h`!9<_E+eHm4#zjb6cXKrHUv6?2TF#jmu4jH8PNGF-D*$xTkY;<cv)~sMHkntP|$QC{eh>"
    "bk&R<kbXXr_=nRbaj@DBP1VZMguq<lMyXhp>LXqz?0e+SvaXO*4mmzu1(-lqAW+KJ&a0W=2TUe~g!({2ita8>iPzz0Z6-3sMK4dQ"
    "I8_?mK2WLCW~&|CaxC`1GbVwgsC&StEx<$Xo&f8D!Qnu_*5Yw{Hr4QV@K+0e7rmxYtM+3&3a-kuxl1oTp2q0(M2#4W2E@yUf+(A@"
    "=~?->s^33kHQ{BkNBUhWGmq|DL3jUhTNQMUr&v}%=(4U*4%qer9{nmRIB5zf8-_N>IjQTXm5SFWiFm?5k`S7$?IzOI(&<@Po2ssJ"
    "TE-|HA=Ponj;5fdOq0dpv~i~oew$mpAfC8M#>Ov=jrFH5hVzt)DK{*-Rws6yH+huMrus#(DFx}M7Epj_C~iCg%8?O5JRdqu?aHLj"
    "O53kEQZS+4lvTu!s!7^+J-Bj&dh!J@!IL>WIsiolLOJKx#<LbVL6nIC{IbEdN~7FYIXk{n32fBsq^9YAi&}7X6F5n2!iy0{kk~MP"
    "BF;$_&E=jjA<c~-Ayu!?>+KC-u;8a&b9muLonb3!*L(GnRjDFj3o$5j8*gY|%xmJZ?KCEt#Nv|K9`bRf7lXwS>LOU!I{|DuzI2rG"
    ">ja>auyNaPzsb$2qLM<yVtt6@9#4Qjl^A(K3fnFa^J?U<^aI?=e(@uiR$@!lJ1|oqzf2M8sP}Q)g5{YmrdK8jBI+n(w*KgrOr?5_"
    "o+13CBjyptW-SCH#FPUM7>>&LocYM2ZiFgNQmILy-KlpL!6CQhSC+f24jK$p=x@vMcG_ENpgXW5K(mV8D7OBjM-UNHp01g<gmxq8"
    "fF?a^2wtwAVTomp17skdGTyHk0@dy;NXtc>tjsn$U_CujICmCw`f4g?(8`tdof3WxXLa!FU~LsFWE|J26;2+Un6Iq`{g}qBfm{ox"
    "HF^77WCY++L~&&EDB!S;4I44j5BJ)38XCtf?pywHwZT(qkq+z}4JBfQtDnbDI^)P_9Q8<z48!VZEuBshJK7zx*&(90dGGp&!=97j"
    "R_yB88A6D{C>>|+p#W)gc@#GZo86CI(JWm1=E#FT7&at4*-aDdJM@8jdQgOm?S+NO*~@5mbzCM!*(P9zkXD8mtvzM9!yZkN?cZ*e"
    "vwvf!_0f%AA5GEt;x177;@t4wZ2=xMs7wD2u<;2;kjnN5bdwa%<PZSq#XKuv*M~Uavu(F8E5blhc<l6HcWCGA!vPWBM_8cGila;L"
    "nTHc;>aY8oDhzIE_4y1K{k)ER>Ero%^25B_ldia#ZKr66ims0M%~O`(Dy~DNK&r`UrJQm=y46GFwx=m=3%0YO;&hEtPqB|fLWoRl"
    "X1$6KP?`aAw@EwWV7oIoMHz?hlx{MHXeYhTy!`tr>&`E~Ivm_{(o4p=47aCFo0@ALm4JAxMPrD(4BINZX#XVXK5w4}6zyOgS&|z*"
    "Z%51lILD^c*7aY)r~aB$d)k!$b*D}EdO9`w8`AlVRe!!_Kc>JCO<Vbo39B6t>ZcDojoaocm_>hwMn*P0G+nzB4m(_;zf+OrK*ZYf"
    "RIEEBy`)81mxC2zNTTPR$I_%}Wh5E(>C7aY%3@&D)arzZ&irg;?biY@-^CEESmTb~v#BSL+)D@W&S9!ZD>`~-^7D`oX<J%RdxKP;"
    "flATESO%s8<~Ri^y;fEf#YF`#<LN(8c&a}ApA)!`IZ81dIv9l0sn;{crQuLZs-1?-?wx`x@r`$*hOOK7L!(`WvhxY22oHPq7>qq9"
    "z0!%&E^nAjgutQx_8)h`yX`NYh<e5M=J+5Hwo|FLQNr}DL!EAWOq-$B!v2R6@BgzunBagCR5zP@+x2U{ZM3y;%LzUTd~1yb-Ub0m"
    "6J5Yi#xpAp#~SJni@^iddwlg<-tU>|72Th%z=h8jHcIV{?D@b&v<IZvUx%Si8cx**q0W;ml8&zGwX|=FO!!V`x6IG$f^dGPwNa0r"
    "HwFlEQhDa?Np2TUXsHqL_k<Hvc68WRCs$*4efZ&MDA$i0R0n(orH~ap-@Gpkd{3dOwd)$d+)w-4I*-G^x6!fH^nmT>{ed-dLs6w%"
    "P7BTLGv8cX0(s2i_W>GraYe(P>9kwb8Sf8KP@x?CA@u%x8yYeVb~+TMO}gf;m4n648`9$7sT-dgb^D_e4{Z&|8O=pF>hm57Dr>{C"
    "#tCj6+Jh``fF<dBRuT4@M;||?@y!>7V_8A(=<BCTntR<2t2^zE(^_#@iUT4~yZE3kTetw7(-7hv&#TAe#IEhRL_b)p`ucFHnVm?a"
    "ad9`aPO+%j{jo^>RjdldxuCt{6-B^6MoBry{ZPb}Y(CT-ZS?$j6G^~|uR3qYeMzO)ZN4O!hs|+@j2Ni3oQEN|7m^lHibb(f9WxIm"
    ")jMPcMZ}Knx30yyj;BG8h3UBO9>dS#%V<hTMV$8!0MoZ*Q)dP%`l*~E(+LBe%kbUo2Q&fADt#OA{YvNWw=mAVhXbT>hVpeQY_U=B"
    "1!q2GYkP`jKVo%Sar-{~ymLi}ze^up?}F6Vj!w8BT{<n~M(NL+6Q;JTz8=HSWe4UDOs%usa5gJrTX*IV=8L?gyz5`RLk8=G@8xu4"
    "DL&>3b*Jw$`q;OoADL(l73$eX*teqHZ1~Rk*n|`EaCA$i$PVcL@BaX`#<!^"
)
CERTIFICATE_SHA256 = "0dfae109373d00a9ffb5c64afce3983d9e44fb2bc83516533a31652780eae732"
EXPECTED_NEW_DEGREES = {"A1": 2, "B0b": 4, "B1a": 1, "B1b": 1}


def decode_certificates():
    raw = decompress(b85decode(CERTIFICATE_B85))
    require(sha256(raw).hexdigest() == CERTIFICATE_SHA256,
            "remaining-plane certificate digest changed")
    decoded = loads(raw)
    require(frozenset(decoded) == frozenset(EXPECTED_NEW_DEGREES),
            ("remaining-plane certificate labels changed", decoded.keys()))
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
    } == EXPECTED_NEW_DEGREES, "remaining-plane degrees changed")
    return certificates, len(raw)


NEW_CERTIFICATES, CERTIFICATE_BYTES = decode_certificates()
CERTIFICATES = dict(NEW_CERTIFICATES)
CERTIFICATES["A0"] = first["CERTIFICATES"]["A"]


def plane_blocks(label, s_value, t_value):
    lift, repair, _constant = PLANES[label]
    blocks = dict(BASE_BLOCKS)
    for (u, v, a, b), increment in (
        (lift, s_value),
        (repair, t_value),
    ):
        changed = [list(row) for row in blocks[u, v]]
        changed[a][b] += increment
        blocks[u, v] = tuple(tuple(row) for row in changed)
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


def audit_plane_definitions_and_r2():
    require(BASE_BLOCKS[0, 4] == ((0, 85), (0, 87)),
            ("base 04 block changed", BASE_BLOCKS[0, 4]))
    require(BASE_BLOCKS[0, 5] == ((84, 87), (0, 28)),
            ("base 05 block changed", BASE_BLOCKS[0, 5]))
    require(BASE_BLOCKS[1, 4] == ((0, 74), (0, 66)),
            ("base 14 block changed", BASE_BLOCKS[1, 4]))
    require(BASE_BLOCKS[1, 5] == ((0, 76), (37, 0)),
            ("base 15 block changed", BASE_BLOCKS[1, 5]))

    results = {}
    for label, (lift, _repair, constant) in PLANES.items():
        root = lift[0]
        expected = {
            (0, 0): (),
            (0, -constant): (),
            (1, 0): (root,),
            (1, -constant): (),
        }
        tables = {}
        for point, expected_failing in expected.items():
            table, failing = site4["r2_tables"](
                plane_blocks(label, *point)
            )
            require(failing == expected_failing,
                    ("remaining-plane R2 stratum changed",
                     label, point, failing, table))
            tables[point] = table
        require(not tables[1, 0][root][1],
                ("off-locus output-one witness survived",
                 label, tables[1, 0][root]))
        require(tables[1, -constant][root][1] == (5,),
                ("alternate site-5 witness was not restored",
                 label, tables[1, -constant][root]))
        results[label] = expected

    # In each literal block, the original site-4 spoke is pure in output
    # one iff s=0; the alternate site-5 spoke is pure iff t=-constant.
    # Every other witness is fixed. Thus these four support representatives
    # prove the exact R2 locus s=0 union t=-constant over C.
    return results


def audit_generic_kernel_and_selected_rows():
    moved_edges = {
        (u, v)
        for lift, repair, _constant in PLANES.values()
        for u, v, _a, _b in (lift, repair)
    }
    require(all(
        edge in site4["old"]["FREE_EDGES"]
        and survivor["POTENTIAL"][edge[0]]
        + survivor["POTENTIAL"][edge[1]] == 0
        for edge in moved_edges
    ), ("a remaining-plane edge left the zero cut", moved_edges))

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
    for label in PLANES:
        for s_value, t_value in product((0, 1), repeat=2):
            blocks = plane_blocks(label, s_value, t_value)
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
                        ("remaining-plane generic corner failed",
                         label, s_value, t_value, u, v, a, b),
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
            ), ("remaining-plane selected corner failed",
                label, s_value, t_value))
            selected_checks += len(WORDS)
    return scalar_checks, selected_checks


# family label: (plane label, A/B line, certificate label)
LINE_FAMILIES = {
    "R0b-A": ("R0b", "A", "A0"),
    "R0b-B": ("R0b", "B", "B0b"),
    "R1a-A": ("R1a", "A", "A1"),
    "R1a-B": ("R1a", "B", "B1a"),
    "R1b-A": ("R1b", "A", "A1"),
    "R1b-B": ("R1b", "B", "B1b"),
}


def family_data(plane_label, line):
    constant = PLANES[plane_label][2]
    if line == "A":
        base = plane_blocks(plane_label, 0, 0)
        unit = plane_blocks(plane_label, 0, 1)
        evaluation = plane_blocks(plane_label, 0, 2)
    else:
        require(line == "B", ("unknown line label", line))
        base = plane_blocks(plane_label, 0, -constant)
        unit = plane_blocks(plane_label, 1, -constant)
        evaluation = plane_blocks(plane_label, 2, -constant)
    d0 = differential(base)
    d_unit = differential(unit)
    d1 = [
        [entry - base_entry for entry, base_entry in zip(row, base_row)]
        for row, base_row in zip(d_unit, d0)
    ]
    return evaluation, d0, d1


def evaluate_polynomial(vectors, value):
    answer = [0] * len(CELLS)
    power = 1
    for vector in vectors:
        answer = add_vectors(answer, [power * entry for entry in vector])
        power *= value
    return answer


def audit_polynomial_kernels():
    results = {}
    for family, (plane_label, line, certificate_label) in LINE_FAMILIES.items():
        vectors = CERTIFICATES[certificate_label]
        evaluation, d0, d1 = family_data(plane_label, line)
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
                    ("remaining-plane kernel coefficient failed",
                     family, coefficient))
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
                ("remaining-plane kernel lost independence",
                 family, independent_rank))
        results[family] = (degree, independent_rank)
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


EXPECTED_CALIBRATIONS = {
    "R0b": {
        "base": (54, 52, 54, 54, 54),
        "intersection": (53, 51, 53, 53, 53),
        "restored": (54, 52, 54, 54, 54),
        "off": (55, 53, 55, 55, 55),
    },
    "R1a": {
        "base": (54, 52, 54, 54, 54),
        "intersection": (51, 49, 51, 51, 51),
        "restored": (52, 50, 52, 52, 52),
        "off": (55, 53, 55, 55, 55),
    },
    "R1b": {
        "base": (54, 52, 54, 54, 54),
        "intersection": (51, 49, 51, 51, 51),
        "restored": (52, 51, 52, 53, 53),
        "off": (55, 53, 55, 55, 55),
    },
}


def audit_calibrations():
    results = {}
    for label, (_lift, _repair, constant) in PLANES.items():
        signatures = {
            "base": incidence_signature(plane_blocks(label, 0, 0)),
            "intersection": incidence_signature(
                plane_blocks(label, 0, -constant)
            ),
            "restored": incidence_signature(
                plane_blocks(label, 1, -constant)
            ),
            "off": incidence_signature(plane_blocks(label, 1, 0)),
        }
        require(signatures == EXPECTED_CALIBRATIONS[label],
                ("remaining-plane calibrations changed", label, signatures))
        results[label] = signatures
    return results


def main():
    r2 = audit_plane_definitions_and_r2()
    generic, selected = audit_generic_kernel_and_selected_rows()
    kernels = audit_polynomial_kernels()
    calibrations = audit_calibrations()
    print("remaining minimal transverse R2-restoration planes: all checks passed")
    print(f"  exact R2 loci              : {r2}")
    print(f"  generic/selected checks    : {generic}/{selected}")
    print(f"  full-R2 kernel degrees     : {kernels}")
    print(f"  incidence calibrations     : {calibrations}")
    print(f"  certificate bytes/SHA-256  : {CERTIFICATE_BYTES}/{CERTIFICATE_SHA256}")


if __name__ == "__main__":
    main()
