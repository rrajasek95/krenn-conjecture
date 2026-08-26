//! Independent literal replay of the 257 distributed K22 direct-family samples.
#![allow(dead_code)]
mod provider {
include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");

const U:i128=400_591_699_200;

fn row(s:&str)->Row {
    assert_eq!(s.len(),48);
    let mut x=[0u8;24];
    for i in 0..24 { x[i]=u8::from_str_radix(&s[2*i..2*i+2],16).unwrap(); }
    assert!(x.windows(2).all(|w|w[0]<=w[1]));
    Row(x)
}

fn belongs(r:&R8,want:&Row,g:usize,e:&E)->bool {
    match g {
        0|1 => {
            let specs=[(0usize,1usize,2usize),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)];
            for &(d2,d3,d4) in &specs {
                for a in &e.factor[d2][0] { for b in &e.factor[d3][1] { for c in &e.factor[d4][2] {
                    let mut f:[Option<&[u8;4]>;3]=[None,None,None]; f[d2]=Some(a);f[d3]=Some(b);f[d4]=Some(c);
                    if make(r,f[0].unwrap(),f[1].unwrap(),f[2].unwrap())==*want{return true}
                }}}
            }
            for a in &e.factor[0][1] { for b in &e.factor[1][1] { for c in &e.factor[2][1] {
                if make(r,a,b,c)==*want{return true}
            }}}
            false
        }
        2 => {
            for low in 0..3 { let o:Vec<_>=(0..3).filter(|&x|x!=low).collect();
                for a in &e.factor[low][0] { for b in &e.factor[o[0]][2] { for c in &e.factor[o[1]][2] {
                    let x=match low{0=>make(r,a,b,c),1=>make(r,b,a,c),_=>make(r,b,c,a)};
                    if x==*want{return true}
                }}}
            }
            for high in 0..3 { let o:Vec<_>=(0..3).filter(|&x|x!=high).collect();
                for a in &e.factor[o[0]][1] { for b in &e.factor[o[1]][1] { for c in &e.factor[high][2] {
                    let x=match high{0=>make(r,c,a,b),1=>make(r,a,c,b),_=>make(r,a,b,c)};
                    if x==*want{return true}
                }}}
            }
            false
        }
        3 => {
            for low in 0..3 { let o:Vec<_>=(0..3).filter(|&x|x!=low).collect();
                for a in &e.factor[low][1] { for b in &e.factor[o[0]][2] { for c in &e.factor[o[1]][2] {
                    let x=match low{0=>make(r,a,b,c),1=>make(r,b,a,c),_=>make(r,b,c,a)};
                    if x==*want{return true}
                }}}
            }
            false
        }
        _=>false
    }
}

pub fn run(){
    let path=std::env::args().nth(1).expect("sample TSV");
    let text=std::fs::read_to_string(path).unwrap();
    let e=parse();
    let mut n=0usize;
    for (ln,line) in text.lines().enumerate(){
        if ln==0 { assert_eq!(line,"group_index\tsample_ordinal\tr8_index\tsource_mass\tsource_row\tintermediate_row\tp1\tt1\tp2\tm1\tm2\tfirst_degree\tfinal_degree\tterminal_q\tunit_scaled_U\tnonzero_contribution_scaled_U");continue }
        let f:Vec<_>=line.split('\t').collect(); assert_eq!(f.len(),16);
        let g=f[0].parse::<usize>().unwrap(); let j=f[1].parse::<usize>().unwrap(); let ri=f[2].parse::<usize>().unwrap();
        assert_eq!(g,j%4); assert_eq!(ri,j*484/256); assert!(ri<485);
        let mass=f[3].parse::<i128>().unwrap(); let source=row(f[4]); let mid=row(f[5]);
        let p1=f[6].parse::<usize>().unwrap(); let ti=f[7].parse::<usize>().unwrap(); let p2=f[8].parse::<usize>().unwrap();
        let m1=f[9].parse::<usize>().unwrap(); let m2=f[10].parse::<usize>().unwrap(); let first=f[11].parse::<usize>().unwrap(); let finald=f[12].parse::<usize>().unwrap();
        let q=f[13].parse::<i64>().unwrap(); let unit=f[14].parse::<i128>().unwrap(); let contribution=f[15].parse::<i128>().unwrap();
        let r=&e.records[ri]; assert_eq!(mass,(r.size as i128)*(r.coefficient as i128)); assert!(belongs(r,&source,g,&e));
        let s1=sig(&source,&e); let ps1=avail(s1,&e); assert_eq!(m1,ps1.len()); assert!(ps1.contains(&p1));
        if g==3 { assert_eq!((first,finald,m2,ti,p2),(0,3,1,0,p1)); assert!(source==mid); }
        else {
            assert_eq!(first,if g==1{3}else{2}); assert_eq!(finald,if g==0{3}else{2});
            let t1=&e.tails[p1][first-2][ti]; assert!(replace(&source,&e.anchors[p1],t1)==mid);
            let s2=sig(&mid,&e); assert_eq!(s2,child_sig(s1,p1,t1,&e)); let ps2=avail(s2,&e); assert_eq!(m2,ps2.len()); assert!(ps2.contains(&p2));
        }
        let sf=sig(&mid,&e); let mut literal_q=0i64;
        for t in &e.tails[p2][finald-2] {
            let child=replace(&mid,&e.anchors[p2],t); literal_q+=charge(&child,&e);
            assert!(avail(child_sig(sf,p2,t,&e),&e).is_empty());
        }
        assert_ne!(q,0); assert_eq!(q,literal_q);
        let expected_unit=if g==3 { U/(m1 as i128) } else { -U/((m1*m2)as i128) };
        assert_eq!(unit,expected_unit); assert_eq!(contribution,mass*unit*(q as i128));
        n+=1;
    }
    assert_eq!(n,257);
    println!("{{\"status\":\"PASS_INDEPENDENT_257_LITERAL_REPLAYS\",\"samples\":{},\"distributed_r8_interval\":[0,484],\"all_nonzero\":true,\"all_terminal\":true,\"all_source_family_members\":true,\"all_sign_U_contributions_exact\":true}}",n);
}
}
fn main(){provider::run()}
