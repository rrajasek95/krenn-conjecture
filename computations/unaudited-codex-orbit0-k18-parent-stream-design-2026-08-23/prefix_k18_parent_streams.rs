mod base {
    #![allow(dead_code)]
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");

    use std::collections::BTreeMap;

    const U2: i128 = 400_591_699_200;
    const CAP: u64 = 50_000;
    const OUT: &str = "computations/unaudited-codex-orbit0-k18-parent-stream-design-2026-08-23/results_parent_stream_prefix.json";

    #[derive(Default)]
    struct PStat { generated:u64, pivotable:u64, outgoing_uses:u64, denominator:BTreeMap<(usize,usize),u64>, keys:HashMap<RKey,i128> }

    fn add_key(m:&mut HashMap<RKey,i128>,k:RKey,v:i128){let x=m.entry(k).or_default();*x+=v;if *x==0{m.remove(&k);}}

    fn observe(row:Row,w18:i128,m1:usize,e:&E,z:&mut PStat){
        z.generated+=1;let s=sig(&row,e);let ps=avail(s,e);if ps.is_empty(){return}z.pivotable+=1;let m2=ps.len();
        assert_eq!(w18%(m2 as i128),0);assert_eq!(U2%((m1*m2)as i128),0);let w20=-w18/(m2 as i128);
        *z.denominator.entry((m1,m2)).or_default()+=1;
        for p in ps{z.outgoing_uses+=1;let k=RKey{profile:profile(&row,p,e),sig:s,pivot:p as u8,degree:2};add_key(&mut z.keys,k,w20)}
    }

    fn direct(e:&E)->PStat{
        let mut z=PStat::default();
        'outer:for r in &e.records{let positive=(r.coefficient as i128)*(r.size as i128);let w=-positive*U2;
            for low in 0..3{let o:Vec<_>=(0..3).filter(|&x|x!=low).collect();for a in &e.factor[low][0]{for b in &e.factor[o[0]][2]{for c in &e.factor[o[1]][2]{let row=match low{0=>make(r,a,b,c),1=>make(r,b,a,c),_=>make(r,b,c,a)};observe(row,w,1,e,&mut z);if z.pivotable>=CAP{break 'outer}}}}}
            for hi in 0..3{let o:Vec<_>=(0..3).filter(|&x|x!=hi).collect();for a in &e.factor[o[0]][1]{for b in &e.factor[o[1]][1]{for c in &e.factor[hi][2]{let row=match hi{0=>make(r,c,a,b),1=>make(r,a,c,b),_=>make(r,a,b,c)};observe(row,w,1,e,&mut z);if z.pivotable>=CAP{break 'outer}}}}}
        }z
    }

    fn k14(e:&E)->PStat{
        let mut z=PStat::default();
        'outer:for r in &e.records{let positive=(r.coefficient as i128)*(r.size as i128);
            for a in &e.factor[0][0]{for b in &e.factor[1][0]{for c in &e.factor[2][0]{let head=make(r,a,b,c);let s=sig(&head,e);let ps=valid(s,e);let m1=ps.len();assert_eq!(positive*U2%(m1 as i128),0);let w=positive*U2/(m1 as i128);for p in ps{for t in &e.tails[p][2]{let row=replace(&head,&e.anchors[p],t);observe(row,w,m1,e,&mut z);if z.pivotable>=CAP{break 'outer}}}}}}
        }z
    }

    fn k15(e:&E)->PStat{
        let mut z=PStat::default();
        'outer:for r in &e.records{let positive=(r.coefficient as i128)*(r.size as i128);
            for hi in 0..3{let o:Vec<_>=(0..3).filter(|&x|x!=hi).collect();for a in &e.factor[o[0]][0]{for b in &e.factor[o[1]][0]{for c in &e.factor[hi][1]{let head=match hi{0=>make(r,c,a,b),1=>make(r,a,c,b),_=>make(r,a,b,c)};let s=sig(&head,e);let ps=avail(s,e);let m1=ps.len();assert!(m1>0);assert_eq!(positive*U2%(m1 as i128),0);let w=positive*U2/(m1 as i128);for p in ps{for t in &e.tails[p][1]{let row=replace(&head,&e.anchors[p],t);observe(row,w,m1,e,&mut z);if z.pivotable>=CAP{break 'outer}}}}}}}
        }z
    }

    fn k16(e:&E)->PStat{
        let d=read(format!("{}checkpoint_direct_k16.bin",DIR)).unwrap();assert_eq!(&d[..8],b"K16DIR1\0");let mut z=PStat::default();
        'outer:for i in 0..nrec(&d){let(row,v)=rec(&d,i);let s=sig(&row,e);let ps=avail(s,e);if ps.is_empty(){continue}let m1=ps.len();assert_ne!(v,0);assert_eq!(-(v as i128)*U2%(m1 as i128),0);let w=-(v as i128)*U2/(m1 as i128);for p in ps{for t in &e.tails[p][0]{let child=replace(&row,&e.anchors[p],t);observe(child,w,m1,e,&mut z);if z.pivotable>=CAP{break 'outer}}}}
        z
    }

    fn object(name:&str,z:&PStat)->String{
        let hist=z.denominator.iter().map(|(&(a,b),&n)|format!("\"{}_{}\":{}",a,b,n)).collect::<Vec<_>>().join(",");
        let nonzero=z.keys.values().filter(|&&x|x!=0).count();let weight:i128=z.keys.values().sum();
        format!("\"{}\":{{\"generated_until_cap\":{},\"pivotable_parents\":{},\"outgoing_pivot_uses\":{},\"distinct_nonzero_profile_keys\":{},\"profile_weight_sum_scaled\":\"{}\",\"m1_m2_hist\":{{{}}}}}",name,z.generated,z.pivotable,z.outgoing_uses,nonzero,weight,hist)
    }

    pub fn run(){let begun=Instant::now();let e=parse();let a=direct(&e);let b=k14(&e);let c=k15(&e);let d=k16(&e);let text=format!("{{\n  \"status\":\"PASS_BOUNDED_FOUR_K18_PARENT_STREAM_PREFIXES\",\n  \"cap_pivotable_parents_per_component\":{},\n  \"components\":{{{},{},{},{}}},\n  \"elapsed_seconds\":{:.6}\n}}\n",CAP,object("direct_K18",&a),object("K14_K4",&b),object("K15_K3",&c),object("K16_K2",&d),begun.elapsed().as_secs_f64());std::fs::write(OUT,&text).unwrap();print!("{}",text)}
}

fn main(){base::run()}
