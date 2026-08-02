#!/usr/bin/env python3
"""Exclude all site-5 zero-cell lifts of the transverse incidence boundary.

Every one of the eight lines retains literal R2. Exact polynomial kernel
vectors of degree at most three join the five universal gauge vectors over
Q(t), forcing differential rank at most 54 on every line.

The sparse integer certificates are compressed only to keep this source
readable. Their decoded JSON has a fixed SHA-256 digest and is audited
coefficientwise using the standard library.
"""

from ast import literal_eval
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
site4 = run_path(str(
    HERE
    / "verify_level_two_two_invertible_transverse_column_one_cell_r2_obstruction.py"
))
survivor = site4["survivor"]
guard = site4["guard"]
rank_core = site4["rank_core"]
dense_core = site4["dense_core"]

BASE_BLOCKS = site4["BASE_BLOCKS"]
BASE_D = site4["BASE_D"]
SITES = site4["SITES"]
COLOURS = site4["COLOURS"]
EDGES = site4["EDGES"]
CELLS = site4["CELLS"]
WORDS = site4["WORDS"]

SITE5_ZERO_CELLS = (
    (0, 5, 1, 0),
    (1, 5, 0, 0),
    (1, 5, 1, 1),
    (2, 5, 0, 1),
    (2, 5, 1, 0),
    (2, 5, 1, 1),
    (3, 5, 0, 0),
    (3, 5, 1, 0),
)
EXPECTED_DEGREES = {
    (0, 5, 1, 0): 1,
    (1, 5, 0, 0): 2,
    (1, 5, 1, 1): 2,
    (2, 5, 0, 1): 3,
    (2, 5, 1, 0): 3,
    (2, 5, 1, 1): 3,
    (3, 5, 0, 0): 0,
    (3, 5, 1, 0): 0,
}
EXPECTED_UNIT_SIGNATURES = {
    (0, 5, 1, 0): (54, 52, 54, 54, 54),
    (1, 5, 0, 0): (54, 52, 54, 54, 54),
    (1, 5, 1, 1): (54, 52, 54, 54, 54),
    (2, 5, 0, 1): (54, 52, 54, 54, 54),
    (2, 5, 1, 0): (54, 54, 55, 55, 56),
    (2, 5, 1, 1): (54, 54, 55, 55, 56),
    (3, 5, 0, 0): (54, 52, 54, 54, 54),
    (3, 5, 1, 0): (54, 53, 54, 55, 55),
}

CERTIFICATE_B85 = (
    "c-rlnS&n2!k_4|p@T&)i0DNEODg;k5=)1RwFE5wM0_JxxWEYzmQ4!DG&D2!Y%=3T#{8xDWQD1+=*B{}({`~L1{`xDvVx2LSJX84l"
    "^;i1(vc2+XJ&sXkX}lh<#*b}|*wW;646i=w%&~+LeVzG!<P#y3#t*(#Uzxw0Ba9eF^(nEv(ug6o*7@&DzSUnTrde~%vCq2R8Y~`C"
    "k0s|+hVRVR%&pg2dkf8nr}TQ~Qe(@b*5+qYdA(C{r80AHwbWj9wv_VVkFV$JUD61xCYJ2obLPmmIC!43^*p-Y%RGC`7-p+%XniWP"
    "+8{bL7arEud#o2ZS<Er^mg;)1zS8U=Cr(|~8-vG(-aC;Q#;p)`_T6)>9At&I_;8jQErz%rUFvJ}oM%X>m37=QUqmO2(uqj$Gt~fm"
    "jZ)=7Uze{eU-BrG)3%)J@L82Gv_P&$?8$)s&6_0rU5sW4W2}7hs7dzvjBV%p-AAushTKlRiE8OFhBn(yWE(vaF%n!(LK=w4te$o{"
    "-gWkpIQU6Nti>2}fG~D4QZIu537Q@E7+BC{dQ3a&WzIy(+E}X)VZIEOLMc1G?{6C;n(wbWBX&9ES$gVWtwWr0=CFB?&>70#gyheE"
    "#Z@ukQ^mZ$mCXBF&G7s#Lc#rxA&VArA99~h5WiLp8Lqvw9%kQxtpql<mdZ>(rtGSTIZ#}o=C%WKswVV6IQtyCYTmz=4L=XQ+s9l_"
    "w`^kJ%^0Yf^pp*sG1)7GJ5OKhrqz)L2<7p&Y8t1ej>~8}59#$w&5);=BA9KbINrZh$M@oR|4<#j6vzA5>UjTJ9=}${FU9dwZTwmq"
    "?n)Gowmy@-z9c!RlJVTyNjh8rZ?;(T$$2!mq`04)XGn+x<Qe--IRPh4p@e)h&iUCaFnwsURvr|A{gZEwKS1(fK+;`f?u5UN`DA-Y"
    "S)+d>djh0H!pF%qKZZ&cPO2$*V3lHhGCdL;0AN1~ZjgGm^W?1MCJPejv{P1KSkA;dCu7zDa2-2gWasPF%|$CY!4?I?lpFU%aS?$N"
    "_D`?Imsjyy64p6C{#w!vITGT&j=%;hyBiVgelB(XKmPB;af(^qNGIpW3BXE;ME9T75mBrm1sJB5qmIL@lc}5#q<xCs*T*c!MIoe}"
    "E%T>D^f->+sbjJ}30;Ts#>xDI(gMXfMmr%Pk$hyFiv39*2bBOJQMfszTj*3(Cy<RVmfy<bSeve(oXR-zm?wfN)~((D+wvG+lt?Bp"
    "5cLAYmzPvg5=`h=+3Fc%LTm6V_25D2<JCR^cz8qlDD14GucC>v<A9ne&z27y-eo}W1zt$;XzY8iw-R~sTzLf!7%yZ22-Hm{vLPG+"
    "+8YFO;1CBzjo@9c6e+*lLjy5~2QW8;YK-t$rCLjEA(HD21+*AmAoAnlfC?s@e4;P73WQ?R(UQ19Ee>ElV2<SrC+Uz2#-gnxka8Zu"
    "Hx_G-lku2Shh%tu=sV@68t{_QMNFg|Z&3_6NgpTW-$G%^afAU{L^+oWG3R+w%?+P{=I^g^Tx^{bjm3$C{3Kn&KuL!~0-s)uFRx5!"
    "MVg`Yu-`D98B)b&u49@_aJ}%iKhebm80VP#4a)d4h)5Fbk44JirsT^Kx~0!6n2#?jn2j$hEFPR$5bW1hMCLmkQ+_Jz>lfzNC5$J4"
    "ShlH*8%=1Nl;iMs<xz{p1n08eS^S!=mHOaU{Ct5%du8po!~6X$y9LOBqJ=%v4mw=|^*c#0(LbdH?}mmAf^Wx8M#shm^`>)@aheg>"
    "kluhM1D!Yp2H6#KtA-plDUuaPk#+!>!Hb)!HFD4qTo9s0sqAb;y$wZ<Zg2l8>&p140kAL+?eZ0c0+2({x7cuaa4~>8g2mHD!S})s"
    "xa@YNSK}u0vZb=%OOiQv)%dk`K9{9`<e9|q?Q6A0j%@~r;&AkM5mu@lW?POz;cgTKEAWveU6*Ymj99dT*#h)kix|I%iL8JlY&KHY"
    "`CQeh65MT6^kS9}Qp+yWCF5V>2b8|;uqvZqvyt*l0`qDHg%g@m>lj0c9gipLwq2YWENpx5^$mgyKS1@ZZpB46K{h&3o)&hXa|9N1"
    "a%vbw;p6Oy@8x*vxDi|G1}Z-IGJi#oWG!>Nj@)kp{MJXq4&|fOe4FMLPTEu>I~Tf<Y(z%5uH4RngUeDEHm+wL;QkGorc|@J-AyS|"
    "Hb!)<xnj09VgPQo7>UCNDd2Q?ij8@?EZyi#*Z`Ha6$->qRrI*UgzV-^apv(e*Vfvhk50g{aundtjhEOejS1SE2;Bw?Y(lD&aoZ+Y"
    "fu_l~1ru@)Uw@CzBJ6MbkYjkwhcI!~dbl#p^9OI>d0{CCV)wCXIjvvZV~h9amv*hFHpYR{$#dry_G;`O2C0t;!;(RY^*C=c4dV^!"
    "wI4o!n2<hDx!w74U{c9U<BlgjFRc5rAMIN6!{)>X4#2g}daFHYmnvP}+^M6Jr6MS~ryKtIiE0c2e92SVt!XN}scx&~v~s^b#R8oT"
    "KaZHhtUD23k3$x|JXUwELt9OBSqC!wa3oCvV3<(y3O?@wX)_10#n06LF?YhMTU^xL#DWkI82>tY#0kbB!*s2{f}<RUpSBoy1nLIu"
    "qHb;{r4AK6oZc4dyu*m92w}B@O%`<pAz{&PuTY~+IWcHj&((z7u9^q&MckkrQPr>Yr`vK{NvsTx4jSvNXbJ%Ln>;u>Ej51Xzo5;r"
    "sLv28?oT6zccg-0UKSIC?RMYDN2HA#bS&fmD|K5l+*-8_0Ek3^y+1u#$Gz$Hh$dY+c}dr+Q#5w&tcz+=nE0@8M=NX#z*eULQGh&s"
    "I!uYFB4CJn7bs7^&VF$r)iK&~$R9l*EQ?=}uzI3Hq<Y!~;Llr7KM?w%3rqGlDh&SXw)BYVUWFvnN$3}kn*1gc;P&T@17Ij}`39oN"
    "$FUE##D_>a?5nguY&7by)XX1KF?P*T&}v8METXoFg@;Y~h;`uFUiW}y*^!{s2M?@3#N$aY)Dv2CwBx`Ep(}e%6jvPR1cr$txco#E"
    "^0kf0mLGNv>VuDjj}9}v9f3mR8gu?mtDEwfp&Ci3pY5+sP!&8}^``AWW+O#KNAAhncKx6QS5gdlZgdN9Q#<s9`(|H34?l^9`gN@g"
    "l0a%mBb=!+T(=sd9hiE-68w+lZYM#>H<~N_RbIrIHwUOzutV1N6Dg@ZICePf$5NC-uq-)Cb8br^Z^#k|-JZiH<d1CaCJM+Bb|-|O"
    "8<nJ|IZl|v4clS#U=n#4GHwS{UccJ{fE5c>#&E8k>?7m6P8kZdMdmz1`0JByD@w4*-iT|4tQj2T_9wsDxT;6Ma7)yvTX4ESfb*k%"
    "xUPb^p@Y|*FH&%u8@2^oH&h@Lmy&EfT#AirJ)2#1Z;gcjEzf7IzNlM^ag8)hH)%&Mhs;Lo!^do&K9qVG%D;ZRhhwU-Ng6^ri79^4"
    "NAs$^hfe_oD#GS{#5LHsf>evH5jX<lK2K9*D;SImKGiFUzKea`07&A?eNNe+ZfPy6mu1^dugx)adWKy%WCUvNDL(4_G`rNVBT=VT"
    "nHT_uc5eq9*g%dn#}pVkQs*(^Ffr9fR(T%=X9sQLR0uek9czMnhf-_)=~Ft^(zXUY4Uf~pJRrU`*nM))+Zw-Ztat<>GJ{2&_7Fx|"
    "{ds*^6*F$*RH!$49lNFR%t;HqgUyZ(3k8HoACL~Gc(4VC0*v*+=+C>>uhV+t=bZc?+9W)miyrU^0&xMoEIF)-@rOl2Y;;D@5+YAA"
    "Z*XSZQ&sxlpBVP+aE(v#w@&vgFVNE-vyN)5dBD^zaQbneY2f*^-9#Q;pK+M9J71(s0l23-6ZbCZklJ9MDPe)iadC;o?hacpm<~eX"
    "IH*KAhw#H#!Civ#3cl2t0e;tvgmhYY^?>}r*3CZmYCXzRsRG<VUIr{Z!xw@e7tmv9M$2~Y0HWH1LG2Mkp_#7f5@%bf&~+jgrS6NI"
    "b#=u*u~PI=J5+9eDNx*_Y}S#4HI6)R%vBL@V-3$jJ?4@IFeyaDeQ46c#p2Iv%a<sVr33vgKeGp@OWpZ6yQd=M7DN8Dir6IxNLOMu"
    "VmtlfkDHYz9g>40#U6(NhR(ENzA#Y83_?BD^wQc+-)w2TwiH5_Uhy$Hm3RgYZ!ew*gEDD@bFL`8$?-lEl~%~d2$wMv3fv90tPGRo"
    "a0d{a1YX1844Yy4p=Zu#tEBN%yopmgqjvphSfgNy3!d}s`ivyh3mT=dd-raSckX=9UGLG#LUao48BT~OH9;;%^u`@g(7D<%u&+4v"
    "mY*){nxoc6-$6jm0NDGWb%Q}Ik#C+BJ|-6Mai1tDe$9!7Gl0XEavSwxo7nApjtd<&!E7G#NshXn0ftexA4V_H<M@m*q9%?405()d"
    "euf#)1j|jY3MC!>ev7tD`P16#A_-)!`^e_Rf^$4GjMxKVpzDB3$jHYe<L9u;l0WU&)+s7B(+dxRKOBwS$%cb2+o!>{CHZ>C8%+yd"
    "_#+z^4l2a<H9Qzag@_kSJ=Q#A!BO&PP3O3^_!&#ChS?6y8wjVRt>3{01?BvO(=_LvlI1gamXi2px3_9uP~2u1FXO$2{Xb;vEo&+D"
    "45C3D&$n*LkU_7{KpIwsQoNq$u#n@tjuV5@-3Pqre0iS}Om?s2Y3lR^!O8iNaJ=}`J{aSt9@1(TqN6Q(f^N>H6TvekEz)U`{k5Wc"
    "rsFnI3a8{a4A$}Xq8wBfeFy<*Uh#}2a0ixgUB%dnCYzZv;E*%zkDVjv)$WiMU|JwFMRI16y4ZO<xcqr}X_L=52JwnR*+atT0VbWE"
    "17Z;4uP}HG(eCj3=kNo~=n%ZiH`p;?u=gx=PA8CF7~1i|qdh%c5w9p30g6mFM~>|E3OEkRdw7n|&cm6t2rlc!+xsHpp9|0i_Nv;-"
    "+sR)CxzLRE{~WN3OSk{DL&ht5*??Fsr~fb|yl+4eWyrK`2PZ616N*_A@3o>EY`1UM1Zv3OrbZ8UM>hIvA-^U<3plyoE{GDd^Y80Q"
    "@!p+U-&Aw)>OAb*3pvt$F3S<Y-nZ29cuEJu#1sbAR*{oC=&^Ksh<Ex0!df@F3y%oaSi>gg>HP@u9m<k!<kY)ae-q%0?eKa{iPhw>"
    "Twgbid9@FyVb_@{`J<dx-C4R%qkxU3V}u8eKdrvt$b*aB2t<ZGjP)7y+6l26P%q|Sq1&SW6m+2oIF%E$$6x8;!F@x~2}$r5j$B?)"
    ">_LD)O#b4HwLmR$JlcwMX;KyrUUdzdq@&qBR+F>rKisxaXgfxl7klGX`vGCZ#z`owS?aRj2ZORJk^=wnZ@kS7x`KJEHt$1tURGSj"
    "DlE$h)uczIsrlm7Gm95#`)ahiMjN4ir#&-Vg^qO%HO=TK_vSX*XE_yL<n{cPhJ3D?E8I|8yWWv4TDs0+c-WRfVF!AtSqQb-%ADTA"
    "I}7$mSKS;0#J;au7UmG+(T#c0|LiVG4z$!T{@N9t^l7xQrpg9ZoepNK0l1zKwFZ^A`d|ljv=>AC!=gaVS*v{}srEMa43VUFtPC9r"
    "KyyTbIXu5e@Kb=nS#=IRU2$F0rqh)~$I^HcAWZ2+FSXAVRsQF<eg64vpAR6!e}M4+8VLXX4~u3{i~"
)
CERTIFICATE_SHA256 = (
    "562be43160fb5d54393a0d8725496ac5447892114b0ec6bde206d2a5af70d84a"
)


def decode_certificates():
    raw = decompress(b85decode(CERTIFICATE_B85))
    require(sha256(raw).hexdigest() == CERTIFICATE_SHA256,
            "site-5 certificate digest changed")
    decoded = loads(raw)
    certificates = {}
    for direction_text, coefficient_lists in decoded.items():
        direction = literal_eval(direction_text)
        vectors = []
        for sparse in coefficient_lists:
            vector = [0] * len(CELLS)
            for index, value in sparse:
                require(0 <= index < len(CELLS),
                        ("certificate index escaped", direction, index))
                require(vector[index] == 0,
                        ("duplicate certificate index", direction, index))
                vector[index] = value
            vectors.append(vector)
        certificates[direction] = tuple(vectors)
    require(frozenset(certificates) == frozenset(SITE5_ZERO_CELLS),
            ("site-5 certificate directions changed", certificates.keys()))
    require({
        direction: len(vectors) - 1
        for direction, vectors in certificates.items()
    } == EXPECTED_DEGREES, "site-5 certificate degrees changed")
    return certificates, len(raw)


CERTIFICATES, CERTIFICATE_BYTES = decode_certificates()


def moved_blocks(direction, value):
    return site4["moved_blocks"](direction, value)


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


def derivative_increment(direction):
    moved = differential(moved_blocks(direction, 1))
    return [
        [entry - base for entry, base in zip(row, base_row)]
        for row, base_row in zip(moved, BASE_D)
    ]


def audit_family_and_r2():
    zero_cells = tuple(
        (u, 5, a, b)
        for u in range(4)
        for a, b in product(COLOURS, repeat=2)
        if BASE_BLOCKS[u, 5][a][b] == 0
    )
    require(zero_cells == SITE5_ZERO_CELLS,
            ("site-5 zero-cell census changed", zero_cells))
    base_tables, base_failing = site4["r2_tables"](BASE_BLOCKS)
    require(not base_failing, ("base packet lost R2", base_failing))
    results = {}
    for direction in SITE5_ZERO_CELLS:
        # Pure-column support is identical for every nonzero parameter, so
        # the two signs audit the unique nonzero support pattern.
        for value in (1, -1):
            tables, failing = site4["r2_tables"](
                moved_blocks(direction, value)
            )
            require(not failing,
                    ("site-5 lift lost R2", direction, value, tables))
        results[direction] = ()
    return base_tables, results


def audit_generic_kernel_and_selected_rows():
    require(all(
        (u, v) in site4["old"]["FREE_EDGES"]
        and survivor["POTENTIAL"][u] + survivor["POTENTIAL"][v] == 0
        for u, v, _a, _b in SITE5_ZERO_CELLS
    ), "a site-5 direction left the zero-multiplier cut")

    numerator_vector = []
    for u, v, a, b in CELLS:
        numerator = dense_core["matrix_product"](
            dense_core["matrix_product"](
                survivor["X"][u], survivor["J"]
            ),
            dense_core["transpose"](survivor["X"][v]),
        )
        numerator_vector.append(numerator[a][b])
    require(-sum(survivor["POTENTIAL"]) == -1,
            "direct selected value changed")

    scalar_checks = 0
    selected_checks = 0
    for direction in SITE5_ZERO_CELLS:
        # Both identities are affine along a one-cell edge direction.
        for value in (0, 1):
            blocks = moved_blocks(direction, value)
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
                        ("site-5 generic-kernel coefficient failed",
                         direction, value, u, v, a, b),
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
            ), ("site-5 selected-row coefficient failed", direction, value))
            selected_checks += len(WORDS)
    return scalar_checks, selected_checks


def evaluate_polynomial(vectors, value):
    result = [0] * len(CELLS)
    power = 1
    for vector in vectors:
        result = add_vectors(result, [power * entry for entry in vector])
        power *= value
    return result


def audit_polynomial_kernels():
    results = {}
    for direction, vectors in CERTIFICATES.items():
        d1 = derivative_increment(direction)
        degree = len(vectors) - 1
        zero = [0] * len(CELLS)
        for coefficient in range(degree + 2):
            x_now = vectors[coefficient] if coefficient <= degree else zero
            x_before = vectors[coefficient - 1] if coefficient else zero
            image = add_vectors(
                matrix_vector(BASE_D, x_now),
                matrix_vector(d1, x_before),
            )
            require(not any(image),
                    ("site-5 polynomial kernel coefficient failed",
                     direction, coefficient))

        value = 2
        blocks = moved_blocks(direction, value)
        gauges = []
        for basis in range(5):
            mu = [0] * 6
            mu[basis] = 1
            mu[5] = -1
            gauges.append(site4["gauge_tangent"](blocks, mu))
        extra = evaluate_polynomial(vectors, value)
        columns = gauges + [extra]
        independent_rank = dense_core["rational_rank"]([
            [column[row] for column in columns]
            for row in range(len(CELLS))
        ])
        require(independent_rank == 6,
                ("site-5 kernel lost independence",
                 direction, independent_rank))
        results[direction] = (degree, independent_rank)
    return results


def append_columns(matrix, *columns):
    return [
        row[:] + [column[index] for column in columns]
        for index, row in enumerate(matrix)
    ]


def incidence_signature(derivative):
    pure_zero = [int(word == (0,) * 6) for word in WORDS]
    pure_one = [int(word == (1,) * 6) for word in WORDS]
    mixed = [
        row
        for row, word in zip(derivative, WORDS)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    return (
        dense_core["rational_rank"](derivative),
        dense_core["rational_rank"](mixed),
        dense_core["rational_rank"](
            append_columns(derivative, pure_zero)
        ),
        dense_core["rational_rank"](
            append_columns(derivative, pure_one)
        ),
        dense_core["rational_rank"](
            append_columns(derivative, pure_zero, pure_one)
        ),
    )


def audit_unit_calibrations():
    signatures = {
        direction: incidence_signature(
            differential(moved_blocks(direction, 1))
        )
        for direction in SITE5_ZERO_CELLS
    }
    require(signatures == EXPECTED_UNIT_SIGNATURES,
            ("site-5 unit signatures changed", signatures))
    return signatures


def main():
    _base_tables, r2 = audit_family_and_r2()
    generic, selected = audit_generic_kernel_and_selected_rows()
    kernels = audit_polynomial_kernels()
    signatures = audit_unit_calibrations()
    print("dense transverse site-5 one-cell R2 obstruction: all checks passed")
    print(f"  zero-cell affine lines       : {len(SITE5_ZERO_CELLS)}")
    print(f"  full-R2 lines               : {len(r2)}/8")
    print(f"  generic/selected checks     : {generic}/{selected}")
    print(f"  polynomial kernel degrees   : {kernels}")
    print(f"  unit incidence signatures  : {signatures}")
    print(f"  certificate bytes/SHA-256  : {CERTIFICATE_BYTES}/{CERTIFICATE_SHA256}")


if __name__ == "__main__":
    main()
