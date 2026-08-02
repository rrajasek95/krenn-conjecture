#!/usr/bin/env python3
"""Exact characteristic-zero chart-25 lift through off-carrier degree three."""

import base64
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path
import zlib


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "analyze_n8_chart25_degree2_lift.py"
SPEC = importlib.util.spec_from_file_location("n8_chart25_degree2", BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
QQ = Fraction

EXPECTED_CERTIFICATE_SHA256 = (
    "84795646e62301243d4fb0ecf28e3c07e41ffcbda2d646c62337a9bfa81c08fa"
)
EXPECTED_LEDGER_SHA256 = (
    "d91352a729a204f67e551c44f9128c439a21d69c880da8dbb98a216277a08ef4"
)
CERTIFICATE_B85 = """c-obnYm&ye2}SoZzq_l9<mXzZX8+q5zb(P#LQkraRB}H03Ly-#E&u!PKg02l$nek4zfyl>`B~<lb@(YV{gkr*XW9RAEdTw;&;D;3FZ0hL$1eab8ejJR_h(*`)^~QdzT^8JVAf^-M`@RB-O=%<)Lr3NJL@0*YR}+}_5|K)C%6o)_TBV4?f>N-?pV@zX#E;$+Io)%)|a0uk7p9rHO{T?N-q3xWNh8wp7rt!b*w-0`e`rMPqO$CmGa;M@gu|*i~mCNN6@T4+mckH@JP)yt=pJWGoFK8oWWvz8NR_b;(s%IFGnnYttdR&0`cAaJK9i=;sZJJ&p3FYfb5@q8w-4H4bJCw&%f0R1+1pjE*2s+3g>E;(>DuTRY;BD1K*##6FSg*sa@oRaugrRDb)*|-h6R$PKD-+n{);!zrd{1*oQbsI#dqGI#iBIJ6w**I=vjs>$Fo*Xcjl?3`C7eI-wenb(k8EbbK`?=WtiTltX3~<{UD!Ch0_SK+d6ZK++*{VAk<{50j4Xdy{j5NPtO)sR22MsZlA%Ra0=`B3%lUkRQG4Nx_wlIM<Vc%iW_&+n9M<?-t6d92E{%@!@b)K^^M16?IAQ@APtanw%-#1+L)It1~YlK04R8f(x}!jY@)%8ijK;CTDV2nj9EJj^TsIF*!4mqjF#<NAZCilLWc%4bFXUa%K<-CJ9Dr6dtKjIWttF`r2TTqsEpja@*N*`>?fj>=!rZqsy~{kL?vmAg%*{U}`{0W@<o2W@=Qz4Ahv6IXaiyQrv`D1M@m#4shAxGBc6`GA5M+QYMjOa%SL7m^A&lg*nroTaz+FH6Uj)H6UgBYGB4BzK1E3_}=799ttpJQaK=JQaLJVA~_=Ww&!@)X|l(g*{%Cc@Nm1X!LL=GH?Mft{5e>w{<u0w8bADAp_-f5>I3syyl4LE39uY6RS%BLBfN;`o9Alv#!Z8Ru>!mlCl2Hj(~kA!wRo3zX7=FMJb&JL*a)wO8`;<Tk$t)T)n4CZSo`9oHvT;6=046ofNg8+GyJ}MZmRn%O;%|5H!DE%pZYQsSN-uf>YC)AyFZ(9&;Gx%;oiJhUXAzh=GwUD;D@H=*e*T$e|<}@+D+H@gY#z55kJol&H-%wtt+`k-13K>*8V7sf26;;bjTk*>-wGu!TT)uiYc!6XK|H&w8c^X27l?~c=#LppKnCoJ37O&6f3;F6yjj89ezhzgcoIf^S6>I5BB9d{*jZluX*2oarO5XM2g#8sSZc#YaaKk7aRzEza$Z_`X!&=+}51pw)^aG6=<P)5SS&yC)I1*ReuM<g)f7DePcYjzV-a_bFyjsJ&*05|6F{X-s|~PuHTHJmN~}f`%jpx(BR|PUd?4)&0a6Vw<m==_*6f9(Ao>aAMIoPYC8{~#aOQ#*VaGn7T@P-Tl1b#c;uNKmto1f=HPdG>A~*Yy5*y$!81{FaF6=TOdZ^#p8CGnn3rDtZ>OjDL0<^3qkggXa~OY4?nwCE<zC$XqVZ0}4SdL>$S<5Xp+6G-2;_<PZw-HR{!?3bH9y*aP>h52A53FYNcsFzEPy0vFF}}}?*OU;;X$IRC@DYuY$sSZaUGAAJN*OadY}LB7r=t29%@%S_t3k<^o8QN%=L00eyo@}P~6P#YV%Ja7rDX5(d-iK&1I;Lu^6-%$xxfM_*y60(NbjdbkufRex4K_%@d4cZr)zDh<y~r#P#U1HBkIjpPAYAvK7x2PJ_>8!LJ=I$(w`o2W;AG?5B8WzKD0(RXblE{-lsXaBxxltQUiW6k7<c)(N^L)$wN}&v`j0Au~N~Bqw|c(y{MLC(_O#>qsC!c=nkf4<e1)2a)!gZ@uFdcumtJjGvYBA&+8hh0);V@UjseM$a1jKqo@_7f}2#4}nyOJXD_Rzg{l|#%KASTLb}Du7D_r2l0dOQ~mZlBqO#bZhZ67_aiA{J8l8Cd%Cx+={?eHYk(%!<Btm{n%9;mkx%)V#Ldf()wU|ad99}mgl|^Xye0IvEAg<u#`fP<r6lw;EBDbu{nM`WTMzY5TdviFeZ8)5f#l(BbXI^rJ9qm}_UmJ4UEzFPz4(!<wl&6|jku(k8-J_|j~plE$W`ssB>&!efj<B_>b5`SaAJN(#_7Ekr0wG$OyhHFhw!D{>RZA+9*FyUJRiP?<@yKf4Nk3pwd0~LZ|2qr#@}w0;H~zA^;SEzUR>>VcM9@kck1JjddczBezQ5U#9IZBCtC#{uP#CBWS{(F{5F1@gOHc&A&@kWrWfmX*Ojd=AnrGzACA0J)A&}=zH(_B?$$Svb?wT)I>-skGbk{TXZ)OCOHzpYEz^f<zmMh#O@^OAMsV%-z&Z+Hf`g2}JOctAd&bRYpw)mpX*E6`h44st6qJB3EZ<0;Kb>C)kJgmrd1Bws2zHqimJy1NBlSZXcde6EC29P04Z+c>%Hz;_=~L?v<Vqihxw64!jx({3yVe^=4ne;0ahPu!Tx$=kYwg(jyFQMV`OY8X=G7mVpH}bsUHbJsMC-MDA&>N|NWQ_R#ks1Lez^|8`txzP{u&%b*^tH~>&Jy;&3mT7J<pW$38wE!h-VLNdv>zZc>mO=#dk6D8sXh@6U&0zo!@}h{SM^E@spz-C&=*a^8}DTa^Lg^{@5>^Gy0oqYr!p5#Ot04^4dQOXc}5xjo0OiKfk8Park*~l1@>#qUJx?NB)QQegB)J>F~M+gnX+%W53l;>=zdQL!Lk5xe#8*Lu4PV7igcvr{wuP>$dxhmPhgY2i~#Ycd2oFLY~BDR~>c!nP7f%`L^DH{BaL|#<y-EKa1s={==W+AM_m8y1)46*yY^=EFq{_!102FJXw%kN!U%m2)eAITGo;C!+i$Q^`QE7XJol<c-@a-n^T8eyqepwJ^sD&H_zVLIxg-UfrRj7c8}fgd3@|f&)=_+Y4xuChHvFZyw>C5*YQ(h^^R2W@zDC23XhukyxS5xv*%-Hevz{#<TU4m-KTlg#UA|S;E(I;663pNIV#UJXMMYGnXmoJE*d}Xlg?KhglkIS(VDtnMHy{W));St65>}uj{J_ppyyl1hrIH9$Sc=Ve*MCXui2iD*X+d~?b*EL?LU0l{+eBeiVv4zId69zMM-KIma{-T_9<)Cp)4UDg>spm$k*1L!M^Wor!FTw9$rqGH^Nhw6UE1_|IX-`Oz4EX3LT%%rX7WcbM?IdpSf6FZ?rj6D<NOuSp_dY9)-wpR>20>xkP;A%#(lKlAhvquK8%4U;L$~>O4|ozOxVc>->R(2YE^&KK9RdzCmIsYCKqq-RTLld)i#j-`)q6nnZkRw9o9$Vd-UXc$%HU@3|c^vDWi(tc_-^aBm(jSDn1A0j8MmYJiB>H9*Ac8o=eZD{-cBL(j+2aPenJwdL(Ud~E-?rZ3(#y+D2$;CK^wxE3!QjW&U2txvYz$>7n-x(kdQuM!s+9iJR)gU4f??{$c3Yl(POTXWvl)||JswacHi@&sR$W;l8)9N@{~PUA`6JH;C27u;oK_&6swC+1|XC<+hb{>^A0?qfczz8ZeZdS`<R1@Z0qKpF3A{x9|u#q5rYx7Pvj<0Nm~lX-aCk_CN-;e)<ozK=sdrFaJCeZg~h5=v?byx*wdxY?-TxY?+2ah%XXJV-g+u~L~J`;Li9<UfsP#I)^O9AwpN_fU{6Kee<4e$adxoCjHZ#+CJrM0jxJ=}yp!bFsmBF7Ccb5btDaJlM(9UpxqQGCMrp$$arOb$7tv(X3uL+Uv^T3BNm~;x9H|z4{}=N7tP0V6;q>DLfo)eT(`jslMS;>YV}v@Vo2p{T9hYj>T!@yax{D>U4wiT=^Ym^jN1eWpOvp7x#`E_GEEyxvfbaKd-}Z@BmJagL`f@kHb@^d%V3PhEJVVyt*a!7apJZ-SYOP7#*#>Cq_rx-x7<}kB|CV^~{DiJb$mn@0(m}HZBz(#wEBbCV$}nVE@d3#k>i_@G^KcLNWJ=)T;VT@aRAQ#CO-iSWb5>WOEB{<51s&`#8~Pb<e;e6WnQ`gS9tW25x<sJ@GDon9n5<#fM4c=GWx1?eTEgf*UQ8$1A-$n2mV&1%@8i`{dP+8@N$UTxoW)Lpj$?8Ju7x<U={v#`F<sI^|&dJ>TXW%&U#yXt?*PU7KAWVe%Cpta7uP%2)Zj|Cjbo&nLVyn}WJ>IrsGnjMm}R9-0K^H^(_fyxD;Yl8)Je3i+e^!5Q4c^&XJ~=ADH93x`{3my@|O4IVl3z&B5gF%LH@<PZEG>?cYQjR&O&+^!(&1nyT1O#L{#b)#tYA>OM;xOgetQ7`7^C08%6oGo4`h7axE3u{d!!RIVmltq3se6X<Ivu?-aWc7GBSvNjqovHZPnYGKwL!`cXDIEKzdMUY6^PYh{miL35(|3rpxqsI2SLjSzhM$MG-&?Z$-K|Q7{~l8uo|o#5c-Uh8Jk9l(-6giarTufi3v?7dxdDG)d(91?`8sTB0C#CUXD969&jDm+pxs^t11O9K18{j~23+2o0sVuW9?Sbx*(uLEO91fm@b2?1dEQw9fd9Veo0x$93&8ONyu1@ZF7HK9`$^*G#>nQ~>B#WzK5olDEzU;vaqpwur_=s=orS!S`#|64akpoJ6Z#Dw>2GuNvFmhR?@FF8651cToa=1ns!u|1X*oR~%ekN4uDNi~eC*D9A8Afa@Avp{{R@A!A){pc)AL1~9#HHP#G1$E=SP0dojsp$=ezX;<h%UQ;HRSP+q}`<OyEUuUm@+YRd;2(#?H~a`&gTRr=`eqXVN}1GJED7etXS(_k<kWyGJbTLl-zOf%UdO&cwauqquJy<U}NBJcxw0pU#AFTb5+9pyvN%fAjB!in{Y#5ss}paqQtu7{^!Wo{yGE*W|=;tnna@yPhasRrihAYo97HTEhpUz4-f%U+nw?pSpUmgmOAQSXUQ+Z%D_>yepRzfp7RA@OwTC`~x35@6f>iirLiFr__6D&&SRaq0`=3jsw}?Jdh83diI49IqKr?!Z*&C2Im>`D3gm9XSk{^ZJ0%IqxmR|r}Immcokyv(k{Yik!wC$<n!&FC3Uqjc;Nf_aZc`Pb${mci{l_JH6Fy}{P<=LSIND1eKchEV5@&~Q{KJe?cEL?%uN-SfBVDgMMC-7y#+oX0dUyuNgC&3aIYt6+}qnkxZSH1%+E>J+&G@sU&w<_k_}chlF?v6A1P@(oG8#0Qdfem5MI_G9**_Gw>j(izK4vK)WaX6O$7qzIVFw9uAfaK5Lw^6u}Z|Nd$Ptp>>>S`H7z6`tnMIN>yDb)l+wb?+YXXA$Fz_&O7(pY83o$Iqd@j>Cys%7({l1v1v^gS9Mf_Rp>wJinee)%T1c*5_jpm{z$VZ4rRni%q^3UNbxQd4cqfj3v7Ejq3<6U(g~4SU_Jpo;Y)i;X5Zw_5&cQ7qRnvEbL!@Rhl{!@eIzr}3)ev$ux&;d+3U*+A+}IY3$BpU1g2BQTjLYeJupyE&etkoH;lKFDeq8L<=iSrPb>FmvQRKj$(2rx&5)M&eFW#E{^>}9$Vl{n7$k#Y*2uUQEjxdM>-4X_Y2|GeAr*8>sC`Y_?*x^NBODN8}T2ch|gyOaDm@k69`|j|Y{_?AM_<IX;bo%S!-@y#<_68;uWA9%k@Ml%UuD1;^9V@=u>5tVkz(PG~I@%y^%)QQ#S1oEJ2i)rn@U}%AW9#}(C&Sf^P9DQuN1Iq8rUMrI%20<loq*u?867<Iq-tn`d|*1%$n)T)XoSzsSY7<xln#SZb+qEV>hAE-%$kmNq*DcNiu$899qq`c%5=1Rs!T^aa_7LCqC}4AXoE;IEh>+DcvrNL>!xZ^gHV8XMY;Owg&M)%dNI6=s~&ZXF5{|4<&g>RL$d3v>N$hZf%hS~`s#%yxN@4FlMWW&h77E?)h>6v?Kve<WA8#zHGR)1ks8%=O5jRx6Ecb0ssapF-GmHED03Gw;7t$A1IP5hJdW{g$U^1xJ+MS_`W{$9Ircszm7{uET8P*tH3&7+r1HRr_bm%kBi<ta^>}C5Vm0=*B`wyAH?wG};BCu7dxzqM0>;IQdq<AFZ^`9|w@`Y#xJ{>|@w0=Et#>^n+^#78ZO-EIxNnm@AK1s8o8<Y{J(ORp{si92hd5~TsCsZSvIM+t^(4>7-UscK<awoEAg^zoFn6k_LPPg}mPP{eo1?~vhYbyJ4!lQ4oMRsI<gsQR^9<$|wlor$-yAhYym`!%&n)a`h%eziH{wg!(Fl`My+CuVZ=M>EWYvR`HOS$hKas$^6FA5@utQ;2AaGO6caC{bGPt6^21W9GFk1VdBy~RSP`Dg>Ta3$@%<Tsz2ec?u4!AEyyl<XOtO;HhJ8taY8)I(l*k==C^|mRXYV3V6UyXS-kxvyY@yS%d8&M>3%(IC#l4EOpE=Rm|g5<y|-}gPd6XpBfJexR#b*U}#sT%RZ9;*>Aj9WE=Ud|$iig~>E>|@8@ddilx-|&I`uBx8b(7xew_V0JcOV<9!$M%~SdYAj;nDKsju*Up*cHr1W55mv01CR1#GKXtI{NDFJaCNw*sCTE%mwC1L@&%`eJ(|#p*LeS?r#Aob$Cn0&@22XN7glKwb(19j-0klUR>XK|_FXdO%eByx=C`4LjWojV!3t5+w$FO7A+JW8!N<ILJ=&00!v%QT4QJ-c@O-XXJTX@to|vm^8BXsz<7eO#=V<<2S5tz&wbYq7v&YY@ki^IDNsc<l_#Kp|bvD?0ryvt)EuV?Bj?YBeodc(=?;Aej`yLN{-{2YFH+aJLV{;Zj#`i6s@a6jzh}HV$H^H~g33=t6kXP;@_<3|gVwt~(^QYxEd`f=9$MTO|x;smy<aB&&{-D}pjQv;>(HFS6dhhVKIDQ{W;GqiDt?OLgsq4fXN{~~p@j!i>GY5&)Yd%)r?8erl{f5ulm*M^Z>T|BOIx~a(;Oz~9AISX$P8r~-9Q+6TFMPQ(HwQf*`{?5T;3NHmEjNNc_z3)f{e?FFXW~fnk&oI0t>++t2dk{j=ZQ6}@uYPbCOf|=zL{Re%V=je%TxQ`)g|To9uK{9pQ@Agj^?+N`n-1lPwdY><N6+R9m_ZP7FeH_4(H+#POX0z_QcF;JiPMmLw(LFOr$l#2U%@72HWyMQbRnq|J5;>ysvqZ(@KA-yCZFw;X4kZUnfleU?1_&jyT|V>(h6l7v+n(l-BPDBJ2mxbtU<OeFU2x0pX7kY<dKcFVBT;dN;6_W+zE~^0w#O1=jFwY3t$lsSN!WavFRdkeaf3YVJb_7t2F63cuA{IIw;l)%|7K&^h-H-qacD*M&^vPEaXPf9f(Oa**b^hsHB{7B6}v<Qw_Fp8e-YZQ~w*&jXTkyI(@S8SSrUAINdNqp#GVdq63`{iCnd;fVDQ!XaPZYI7pg=W)at{wxQa`~&nGoX5W@Hi89wmJd$;foc@aSBoi5g6!~oa|^}~l%x5`J2#J_huKHL<JtGJ+b{b83Lf+WQ!(-2JaH$Tpw(jdU^$usi^u+nJLv?=QGBp=pEt9e`0;rh5199I10I0>LFmx?2Tnjp`~%-d1=c^$k>$ok#Vvm-96)jFp8<NPzyj#mK3p9+p#G_Bw4eYQpga2tUG51Ro*TneXNZC;rpTSTV2Z|z>Lu!bR4~yAKot{pDJq$$PoE#;d<tu<>bew`SOdCd6j)*P{sHDeiB;VRgB8|*t}q1_SiLWSc~oIB=b!?Mc?Z>3Y`CbrV&m1-Rp@?QUIiY4^%Yq#u)reg1?~Qj1rH0X%H)Fzi!3fvV)1-}D=g|BRAN#8pc;#g7!_G`$hyjkra%{2+(&2^i-jmGviv0pYb<|7ni4CBe^_HxGFVVz`RjMbJKqGU+!kb^FLgy04i}YV%=@S!W9~-<8S^Kq$6SXV+gEG1edRf{;N7dyX?P0WjS{aParm(-SAiT=y^T(PRPc6`c-@Y}k6mpG<UISU_4B4ZC!pbV^%l8PS8vgHbukwDU;iMSfaeE)7;%>i!zs`|2<E_)W8$=64&KcGw%(?z(d(xQ-tZEq!E^9#eg)z{jps~TjYZDUeB>QnjYY%Nd^BENy@l@A)mz{pQ;h`+#_+*<G1VJi@TM9IR*T_-#bT;Ao=<Es7P?3OAoPze#=;TnAB02J)mt<Lx_aY2GSyoUqNW_<OVZ$cMeg{f>m`z&O|cg&7gN3Q^=@#!+->z1`chYKp?+PBMc&tZ<bGX^MGn$D_0XQ&#!XjmczW^Pn|RGvDQ@{z(P)cXy`jFS;H@|D8nsf~>a8N*6t{RoT~~2-(n9CxVl32;sxjtHRE#lyqS}f%2$fd8hhSw@VJ<IjX*Ku`HMNyEom44qX;oq3FK%r$_|s*ID{&gHQvBMAx(5|k)IX@Yq9aD-6&<p!uc9f?<rVi4tgie80E;U>{!MKaEMQn%`O5{?Rs$KUDy@R-fNLw}98_8{@1V+x4Hp$wY`nUz3f->@tH491vf{xB3oEi7VP!>@qp6j6?88!tEM8bE4a_^bSc=@EYo$m(DwU`|QLRKBii#!bB2+B_AIbZ)%~;zdJZ!LB^6>L<Li4fS9&c8BYaOe(3W#k<s_F4i&3(?|m{T*JgIyfoV7v)WWnLn_RgdK~pJ&g=xvoUcXeHt!Io$`>6W%;|Cl-JljR$l4<mPS3s<~1v@(xtf<AIv)3*iahYd-S*^@;Go@g>0T<MEfQoSu*6Tv-P@v&D;>b1F1n+@!NW`2}U2mWSp+(xGxd)}eCxv=hkDSx1@2ypDy+&FieQpujIE>BMS4)?sQu((%>koD;YbrW`V}Fz1k&)k!Cm19A?P1CkDr1GA3rdzf^5-|L(cMFLDZOby66OiiD1d^H8vIjeVl!2A)ZO$rpqtF0Ayfhf4p3FWAq6UtFJhs!ZJXY>+&!KKdXBz%nbYQ*9y=Y(oh&WY5hoWs?aoWosda!xR_Cg%h*YjRE`N9CMQj><WK9Fudn?@i9(zBf51hy;^!A~h=KL~2yd@zoSJ=Tv0AxG4u+O$w}XTI*O1NI6Um$T&=m>a7Abrng$1t3xSn!l^JUi<@y4CP(#FksOe5s2q@Th#b>f1>S^7$Ddo6bNsnAy;Z0N<Q%33q#R!j%s9mNFy#>6o8F3t0!%qn4#+uFj_R$joWk~VB#obkXxI!`oc){@|App3YsJ*4oD->0MNXi`R5=A+It$y+k-)rq%nw~Ui?g2-$^o4fm7{V_Aji}>fj41u<<G6jIeczSnG>o3y%kfVat>DmJ1gRQlXC*!n>vSw0&K0Q9F=oIIjYcc<@ozK12kXUq_aTz#oa|7h#Zh~s2q@Ws2s43?8||>$b)Ylrkw$WW^uF5LezjwWU2;a9i|2(9bXOHLmoKp1Ol2_m~+U?!cAl*2jm<o2P7RL2WB1L_b}=BzK46r15*Q%4pRei4pRfRkf9o~pCick&VG(~*Au*-)7pnPXs)Onm2*NlpuO_t!0t+X^RT@VFt^TrjyTr`yq^=R0o@f-qjC;c1A8msxDyCyW=+lsW)?PAOb+O+s2r7Z0y(g|@_lb|4);Cmt%Ruo%@tFla!#ZMv{qP+zn_CH56*s$z#Z-4?B}#NRs&KFQv)&%Q=@vTK#l3G#7XyLKW7Nc>x{F&u*bKpA~_)AP&pvw5ILr|3cLxEjz70B=lFALdaF<k$T>_6NIAY5m~n{jVag%CH@y`P1(<TE9FTLU9MxMPIU@I|+;uungSsN8%-2uM>0lkcY22I+_TuAsSib}3!Oebohi@AH-i*`uaf)Yo&(_l7f7uU?*T%Gb@Pp%FZ+Q>n(gUDBX#c`9g!Tvbbk*^EoLo87w9YL*t(reh)_3?ltBuB`wufl>X*E+IE`Po4uwLP&?L&N8H7?@e<w-o}yKb@hk3Y^G@a)U=ukU&I$-aBk&KBdJvpt%V`ZRtxbA;xBoa12E(w`JQ_Gj=Cygh&)t8e(}``%sqwE>MEpZ6(W+@FhOCgu<RelPL;oZd#wZ^!A=8$NYCz`s)uV?3Iv=QUDxE+PDZe4{<Sap3-e`@Gl!=Bgn57w<UV=W7%6xATGi<9i~f{Ar6Kxj=V5uUr>n9`o-3*G7I{4mS3i!?sJvyY^-HUc;HpsYTYl!}s4;2>CL2E4|^{%m6-C(c#U?E#H?seEDjn58sDET)tWA?<tsLj(?+b^oHA~hGPupS8^t9|D4_-GhK>Lxbs}R8#z@J{Xp8iugU~9%Uw-CfIp%0eW^t}98DL&k#|arm%+)jJr12|`71OpH_AGPOY1d1E}5nBCAQp3w|ubD-**<qEPvPI>hK9K^uH(U^;sll00qbX{r=+hRR(~oV7Q<7xB4CaZ{~}97m5}y&Sm;ZZu+w2@z2YkgEn7a0ro7#&A~y@@Zw@|u*f%CPbvJZk8XV2D2~KbAO9*Ca750>cgt{_BG<gur#a=x_f?uPiQkJvouD$#6pzPBE+<D&nkXZeld~~vKI7H#YK^$|3%>e4m(W#RK1;u-+T!kP5~rT;Km2vIy4#A6{3dvR<Tti{duJ}%dWdJOH-)LpCf$qql*D@Pr!4Slr9X0(7T@Ec_#21fi-*VJ+s`&P69vA+DD8^@HVo>T#!u^dXG+><fR*_}_y)`uH_Dowi<keNzES4OXTIUfbK$(cc(B1L2l3aJgK>%0@psbc>~CI5Yw&V@^D~J<HTqg|etk!t?EP#3ZO>0O_4%ETzw>c@ev{yjZ~N8$OM{RvL-#4*qfi^0$(1%^O7rc&<NH3n9<y^tcy;W)D8BR0GKTgIAK354TPG*OTKvch&v2V>AHIBP-G7^(>K*$<Ur?^_(el^Yloo2b$~#?05!<*E@}>PW<m3%E!((?^{_zjq$+G;JINx|yi&x}*gKT&lR5$<iJ;tLq)H?o7<Z1hgC-#f0zu$LfICycW!;$)$#$D?L``$h@&v5VpLWgVZfpx9jwO(B970nao(bKmbkJQ&Z@7XUb?j_Ho$09o(MULcoV&9MZ!AzHjgNK4T9H}4DxNDuny`*vQa6yNo$dNSeTleFBK=b6py?Aj+;(o~U*uK1#@?I~@%?0J%D`<8t5dK_G-kpwi*Qo!&I6Y0xV_$7^^!PM(I5&TMH~Z})V)HMam4DnPo1V5NcF%EQ>Db|(`D>wUP8U?y-nw42(^t5ExETBig%l1W;p%LV7#s-?{|kSxyYi}(6N7yN=dSGDpSbuHICov$;lG6MX6ojv!JWXFJZHkV@tq0dhWPR*<d!FJtaHS}Pxah8&jVQ?7SwKI&x2Jyc0Jrh_et=OvZGhmDn>rT)ox>lKl|WG>i}=9|Mx$MNpvg"""


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def decode_certificate():
    compressed = base64.b85decode(CERTIFICATE_B85.encode("ascii"))
    raw = zlib.decompress(compressed)
    require(sha256(raw).hexdigest() == EXPECTED_CERTIFICATE_SHA256,
            "chart25 degree-three certificate digest changed")
    return json.loads(raw), len(raw), len(compressed)


def exact_actual_replay(certificate):
    actual2, _ = BASE.averaged_degree2_residual()
    actual3, _ = BASE.corrected_residual_at_degree(3, {})
    residuals = {2: dict(actual2), 3: dict(actual3)}
    columns = []
    seen = set()
    minimum_degrees = Counter()
    coefficient_values = Counter()
    orbit_sizes = Counter()

    for word_text, multiplier_list, numerator, denominator in certificate:
        require(len(word_text) == 8 and set(word_text) <= set("012"),
                "invalid certificate word")
        word = tuple(map(int, word_text))
        require(len(set(word)) > 1, "certificate uses a pure generator")
        require(len(multiplier_list) == 8
                and multiplier_list == sorted(multiplier_list)
                and all(0 <= value < len(BASE.COORDINATES)
                        for value in multiplier_list),
                "invalid certificate multiplier")
        column = (word, bytes(multiplier_list))
        require(column not in seen, "duplicate certificate column")
        seen.add(column)
        require(BASE.canonical_column(column) == column,
                "certificate column is not a stabilizer representative")
        minimum_degree = BASE.column_minimum_degree(column)
        require(minimum_degree in (2, 3),
                "certificate column starts outside the coupled layers")
        scalar = QQ(numerator, denominator)
        require(scalar and denominator in (1, 2),
                "unexpected certificate coefficient")
        columns.append((column, scalar))
        minimum_degrees[minimum_degree] += 1
        coefficient_values[scalar] += 1
        orbit = BASE.column_orbit(column)
        orbit_sizes[len(orbit)] += 1
        for actual_column in orbit:
            for row in BASE.column_rows(actual_column):
                degree = BASE.row_degree(row)
                if degree not in residuals:
                    continue
                value = residuals[degree].get(row, QQ(0)) + scalar
                if value:
                    residuals[degree][row] = value
                else:
                    residuals[degree].pop(row, None)

    require(not residuals[2] and not residuals[3],
            "chart25 degree-three exact actual replay failed")
    return {
        "certificate_columns": len(columns),
        "minimum_degree_counts": dict(sorted(minimum_degrees.items())),
        "coefficient_denominator_lcm": math.lcm(*(
            value.denominator for value in coefficient_values
        )),
        "coefficient_histogram": sorted(
            (value.numerator, value.denominator, count)
            for value, count in coefficient_values.items()
        ),
        "column_orbit_size_histogram": dict(sorted(orbit_sizes.items())),
        "initial_degree2_actual_rows": len(actual2),
        "initial_degree3_actual_rows": len(actual3),
        "remaining_degree2_actual_rows": len(residuals[2]),
        "remaining_degree3_actual_rows": len(residuals[3]),
    }


def audit():
    certificate, raw_size, compressed_size = decode_certificate()
    require(len(certificate) == 1634, "certificate support changed")
    ledger = exact_actual_replay(certificate)
    ledger.update({
        "certificate_raw_bytes": raw_size,
        "certificate_compressed_bytes": compressed_size,
        "degree2_row_orbits": 2264,
        "degree2_column_orbits": 3690,
        "degree2_rank": 2052,
        "degree2_kernel_dimension": 1638,
        "degree3_bockstein_rank": 1430,
        "coupled_degree3_row_orbits": 27440,
        "new_degree3_column_orbits": 55798,
        "coupled_block_rank": 27904,
    })
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "chart25 degree-three ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("chart 25 degree-three characteristic-zero lift: PASS")
    print("certificate orbit-columns:", ledger["certificate_columns"])
    print("minimum-degree counts:", ledger["minimum_degree_counts"])
    print("coefficient denominator lcm:",
          ledger["coefficient_denominator_lcm"])
    print("degree-three Bockstein rank:",
          ledger["degree3_bockstein_rank"])
    print("remaining actual rows:",
          ledger["remaining_degree2_actual_rows"],
          ledger["remaining_degree3_actual_rows"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
