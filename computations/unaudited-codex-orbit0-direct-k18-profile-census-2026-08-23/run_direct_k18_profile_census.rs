mod base {
    #![allow(dead_code)]
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");

    use std::cmp::Reverse;
    use std::collections::BinaryHeap;
    use std::fs::{File,rename,metadata};
    use std::io::{BufReader,BufWriter,Read,Write};

    const U2:i128=400_591_699_200;
    const ODIR:&str="computations/unaudited-codex-orbit0-direct-k18-profile-census-2026-08-23/";
    const HEADER:usize=256;
    const REC:usize=72;
    const STEP:usize=32;

    #[derive(Clone,Copy,Debug,Eq,Hash,Ord,PartialEq,PartialOrd)]
    struct Key { lineage:u8, profile:[u8;29], sig:[u8;12], pivot:u8 }
    #[derive(Clone,Copy,Debug,Eq,Ord,PartialEq,PartialOrd)]
    struct Witness { ri:u16, i0:u8, i1:u8, i2:u8 }
    #[derive(Clone,Copy,Debug)] struct Agg { weight:i128, uses:u64, witness:Witness }
    #[derive(Clone,Copy,Default)] struct Stats { full:[u64;6], piv:[u64;6], uses:[u64;6] }
    impl Stats { fn add(&mut self,x:&Stats){for i in 0..6{self.full[i]+=x.full[i];self.piv[i]+=x.piv[i];self.uses[i]+=x.uses[i]}} }

    fn run_path(start:usize,end:usize)->String{format!("{}run_{:03}_{:03}.bin",ODIR,start,end)}
    fn add(map:&mut HashMap<Key,Agg>,k:Key,v:i128,w:Witness){use std::collections::hash_map::Entry;match map.entry(k){Entry::Vacant(x)=>{x.insert(Agg{weight:v,uses:1,witness:w});}Entry::Occupied(mut x)=>{let a=x.get_mut();a.weight+=v;a.uses+=1;if w<a.witness{a.witness=w}}}}

    fn observe(row:Row,lineage:usize,rho:i128,witness:Witness,e:&E,map:&mut HashMap<Key,Agg>,s:&mut Stats){
        s.full[lineage]+=1;let sg=sig(&row,e);let ps=avail(sg,e);if ps.is_empty(){return}s.piv[lineage]+=1;let m=ps.len()as i128;assert_eq!(rho*U2%m,0);let w20=rho*U2/m;
        for p in ps{s.uses[lineage]+=1;let k=Key{lineage:lineage as u8,profile:profile(&row,p,e),sig:sg,pivot:p as u8};add(map,k,w20,witness)}
    }

    fn put_header(w:&mut BufWriter<File>,magic:&[u8;8],start:usize,end:usize,s:&Stats,count:u64,sum:i128,uses:u64,zero:u64){
        let mut h=[0u8;HEADER];h[..8].copy_from_slice(magic);h[8..24].copy_from_slice(&U2.to_le_bytes());h[24..26].copy_from_slice(&(start as u16).to_le_bytes());h[26..28].copy_from_slice(&(end as u16).to_le_bytes());h[28..30].copy_from_slice(&(REC as u16).to_le_bytes());
        let mut p=32;for x in s.full{h[p..p+8].copy_from_slice(&x.to_le_bytes());p+=8}for x in s.piv{h[p..p+8].copy_from_slice(&x.to_le_bytes());p+=8}for x in s.uses{h[p..p+8].copy_from_slice(&x.to_le_bytes());p+=8}
        h[176..184].copy_from_slice(&count.to_le_bytes());h[184..200].copy_from_slice(&sum.to_le_bytes());h[200..208].copy_from_slice(&uses.to_le_bytes());h[208..216].copy_from_slice(&zero.to_le_bytes());w.write_all(&h).unwrap()
    }
    fn write_rec<W:Write>(w:&mut W,k:Key,a:Agg){w.write_all(&[k.lineage]).unwrap();w.write_all(&k.profile).unwrap();w.write_all(&k.sig).unwrap();w.write_all(&[k.pivot]).unwrap();w.write_all(&a.weight.to_le_bytes()).unwrap();w.write_all(&a.uses.to_le_bytes()).unwrap();w.write_all(&a.witness.ri.to_le_bytes()).unwrap();w.write_all(&[a.witness.i0,a.witness.i1,a.witness.i2]).unwrap()}
    fn read_rec<Rd:Read>(r:&mut Rd)->Option<(Key,Agg)>{let mut b=[0u8;REC];match r.read_exact(&mut b){Ok(())=>{},Err(x)if x.kind()==std::io::ErrorKind::UnexpectedEof=>return None,Err(x)=>panic!("record {x}")}let mut p=[0u8;29];p.copy_from_slice(&b[1..30]);let mut s=[0u8;12];s.copy_from_slice(&b[30..42]);Some((Key{lineage:b[0],profile:p,sig:s,pivot:b[42]},Agg{weight:i128::from_le_bytes(b[43..59].try_into().unwrap()),uses:u64::from_le_bytes(b[59..67].try_into().unwrap()),witness:Witness{ri:u16::from_le_bytes(b[67..69].try_into().unwrap()),i0:b[69],i1:b[70],i2:b[71]}}))}

    fn build_run(e:&E,start:usize,end:usize)->(String,Stats,u64,i128,u64){let mut map=HashMap::new();let mut st=Stats::default();
        for ri in start..end{let r=&e.records[ri];let rho=(r.coefficient as i128)*(r.size as i128);
            for low in 0..3{let o:Vec<_>=(0..3).filter(|&x|x!=low).collect();for(i,&a)in e.factor[low][0].iter().enumerate(){for(j,&b)in e.factor[o[0]][2].iter().enumerate(){for(k,&c)in e.factor[o[1]][2].iter().enumerate(){let row=match low{0=>make(r,&a,&b,&c),1=>make(r,&b,&a,&c),_=>make(r,&b,&c,&a)};let mut ix=[0u8;3];ix[low]=i as u8;ix[o[0]]=j as u8;ix[o[1]]=k as u8;observe(row,low,rho,Witness{ri:ri as u16,i0:ix[0],i1:ix[1],i2:ix[2]},e,&mut map,&mut st)}}}}
            for hi in 0..3{let o:Vec<_>=(0..3).filter(|&x|x!=hi).collect();for(i,&a)in e.factor[o[0]][1].iter().enumerate(){for(j,&b)in e.factor[o[1]][1].iter().enumerate(){for(k,&c)in e.factor[hi][2].iter().enumerate(){let row=match hi{0=>make(r,&c,&a,&b),1=>make(r,&a,&c,&b),_=>make(r,&a,&b,&c)};let mut ix=[0u8;3];ix[o[0]]=i as u8;ix[o[1]]=j as u8;ix[hi]=k as u8;observe(row,3+hi,rho,Witness{ri:ri as u16,i0:ix[0],i1:ix[1],i2:ix[2]},e,&mut map,&mut st)}}}}
        }
        let mut v:Vec<_>=map.into_iter().filter(|(_,a)|a.weight!=0).collect();v.sort_unstable_by_key(|x|x.0);let count=v.len()as u64;let sum=v.iter().map(|x|x.1.weight).sum();let uses=v.iter().map(|x|x.1.uses).sum();let path=run_path(start,end);let tmp=format!("{}.tmp",path);let mut w=BufWriter::with_capacity(8<<20,File::create(&tmp).unwrap());put_header(&mut w,b"D18RUN1\0",start,end,&st,count,sum,uses,0);for(k,a)in v{write_rec(&mut w,k,a)}w.flush().unwrap();drop(w);rename(tmp,&path).unwrap();assert_eq!(metadata(&path).unwrap().len(),HEADER as u64+REC as u64*count);(path,st,count,sum,uses)
    }

    fn parse_header(path:&str,magic:&[u8;8])->(usize,usize,Stats,u64,i128,u64,u64){let mut f=File::open(path).unwrap();let mut h=[0u8;HEADER];f.read_exact(&mut h).unwrap();assert_eq!(&h[..8],magic);assert_eq!(i128::from_le_bytes(h[8..24].try_into().unwrap()),U2);assert_eq!(u16::from_le_bytes(h[28..30].try_into().unwrap())as usize,REC);let mut st=Stats::default();let mut p=32;for x in &mut st.full{*x=u64::from_le_bytes(h[p..p+8].try_into().unwrap());p+=8}for x in &mut st.piv{*x=u64::from_le_bytes(h[p..p+8].try_into().unwrap());p+=8}for x in &mut st.uses{*x=u64::from_le_bytes(h[p..p+8].try_into().unwrap());p+=8}let n=u64::from_le_bytes(h[176..184].try_into().unwrap());assert_eq!(metadata(path).unwrap().len(),HEADER as u64+REC as u64*n);(u16::from_le_bytes(h[24..26].try_into().unwrap())as usize,u16::from_le_bytes(h[26..28].try_into().unwrap())as usize,st,n,i128::from_le_bytes(h[184..200].try_into().unwrap()),u64::from_le_bytes(h[200..208].try_into().unwrap()),u64::from_le_bytes(h[208..216].try_into().unwrap()))}

    struct RR{r:BufReader<File>,cur:Option<(Key,Agg)>,prior:Option<Key>,read:u64,n:u64}
    impl RR{fn open(path:&str,n:u64)->Self{let mut r=BufReader::with_capacity(2<<20,File::open(path).unwrap());let mut h=[0u8;HEADER];r.read_exact(&mut h).unwrap();let mut z=RR{r,cur:None,prior:None,read:0,n};z.next();z}fn next(&mut self){let x=read_rec(&mut self.r);if let Some((k,_))=x{if let Some(p)=self.prior{assert!(p<k)}self.prior=Some(k);self.read+=1}self.cur=x}fn finish(&self){assert!(self.cur.is_none());assert_eq!(self.read,self.n)}}

    fn merge(paths:&[String],total:&Stats)->(u64,u64,i128,u64,String){let mut rs=Vec::new();let mut heap=BinaryHeap::new();let mut expected=0;for(i,path)in paths.iter().enumerate(){let(s,e,_st,n,_sum,_uses,_z)=parse_header(path,b"D18RUN1\0");assert_eq!(s,expected);expected=e;let r=RR::open(path,n);if let Some((k,_))=r.cur{heap.push(Reverse((k,i)))}rs.push(r)}assert_eq!(expected,485);
        let out=format!("{}direct_k18_enriched_profiles.bin",ODIR);let tmp=format!("{}.tmp",out);let mut w=BufWriter::with_capacity(8<<20,File::create(&tmp).unwrap());put_header(&mut w,b"D18MRG1\0",0,485,total,0,0,0,0);let(mut count,mut zero,mut sum,mut uses)=(0u64,0u64,0i128,0u64);
        while let Some(Reverse((key,i)))=heap.pop(){let(_,mut a)=rs[i].cur.unwrap();rs[i].next();if let Some((k,_))=rs[i].cur{heap.push(Reverse((k,i)))}while let Some(Reverse((k,j)))=heap.peek().copied(){if k!=key{break}heap.pop();let(_,b)=rs[j].cur.unwrap();a.weight+=b.weight;a.uses+=b.uses;if b.witness<a.witness{a.witness=b.witness}rs[j].next();if let Some((n,_))=rs[j].cur{heap.push(Reverse((n,j)))}}if a.weight==0{zero+=1}else{write_rec(&mut w,key,a);count+=1;sum+=a.weight;uses+=a.uses}}
        w.flush().unwrap();let mut f=w.into_inner().unwrap();f.flush().unwrap();drop(f);{let mut q=std::fs::OpenOptions::new().write(true).open(&tmp).unwrap();use std::io::{Seek,SeekFrom};q.seek(SeekFrom::Start(176)).unwrap();q.write_all(&count.to_le_bytes()).unwrap();q.write_all(&sum.to_le_bytes()).unwrap();q.write_all(&uses.to_le_bytes()).unwrap();q.write_all(&zero.to_le_bytes()).unwrap();q.sync_all().unwrap()}rename(tmp,&out).unwrap();for r in &rs{r.finish()}assert_eq!(metadata(&out).unwrap().len(),HEADER as u64+REC as u64*count);(count,zero,sum,uses,out)
    }

    fn witness_row(e:&E,k:Key,w:Witness)->Row{let r=&e.records[w.ri as usize];let ix=[w.i0 as usize,w.i1 as usize,w.i2 as usize];if k.lineage<3{let low=k.lineage as usize;let o:Vec<_>=(0..3).filter(|&x|x!=low).collect();let a=e.factor[low][0][ix[low]];let b=e.factor[o[0]][2][ix[o[0]]];let c=e.factor[o[1]][2][ix[o[1]]];match low{0=>make(r,&a,&b,&c),1=>make(r,&b,&a,&c),_=>make(r,&b,&c,&a)}}else{let hi=(k.lineage-3)as usize;let o:Vec<_>=(0..3).filter(|&x|x!=hi).collect();let a=e.factor[o[0]][1][ix[o[0]]];let b=e.factor[o[1]][1][ix[o[1]]];let c=e.factor[hi][2][ix[hi]];match hi{0=>make(r,&c,&a,&b),1=>make(r,&a,&c,&b),_=>make(r,&a,&b,&c)}}}

    pub fn evaluate(){let begun=Instant::now();let e=parse();let path=format!("{}direct_k18_enriched_profiles.bin",ODIR);let(_s,_e,_st,n,_sum,_uses,_z)=parse_header(&path,b"D18MRG1\0");let mut r=BufReader::with_capacity(8<<20,File::open(&path).unwrap());let mut h=[0u8;HEADER];r.read_exact(&mut h).unwrap();let(mut full_q,mut irr_q)=(0i128,0i128);let(mut evals,mut irr_evals,mut retained_occ,mut retained_irr_occ)=(0u64,0u64,0u64,0u64);let mut prior=None;for _ in 0..n{let(k,a)=read_rec(&mut r).unwrap();assert!(a.weight!=0);if let Some(p)=prior{assert!(p<k)}prior=Some(k);let row=witness_row(&e,k,a.witness);assert_eq!(profile(&row,k.pivot as usize,&e),k.profile);assert_eq!(sig(&row,&e),k.sig);assert!(avail(k.sig,&e).contains(&(k.pivot as usize)));for t in &e.tails[k.pivot as usize][0]{let child=replace(&row,&e.anchors[k.pivot as usize],t);let q=charge(&child,&e)as i128;full_q+=a.weight*q;evals+=1;retained_occ+=a.uses;let child_irr=avail(child_sig(k.sig,k.pivot as usize,t,&e),&e).is_empty();if child_irr{irr_q+=a.weight*q;irr_evals+=1;retained_irr_occ+=a.uses}}}assert!(read_rec(&mut r).is_none());let text=format!("{{\n \"status\":\"PASS_TRIVIAL_K2_CHARGE_EVALUATION\",\n \"scale\":{},\n \"profile_keys\":{},\n \"literal_tail_evaluations\":{},\n \"irreducible_tail_evaluations\":{},\n \"retained_profile_occurrence_tails\":{},\n \"retained_irreducible_occurrence_tails\":{},\n \"full_charge_scaled\":\"{}\",\n \"irreducible_charge_scaled\":\"{}\",\n \"scope_guard\":\"charges are exact after signed profile aggregation; retained occurrence counts omit exactly cancelling profile contributions\",\n \"elapsed_seconds\":{:.6}\n}}\n",U2,n,evals,irr_evals,retained_occ,retained_irr_occ,full_q,irr_q,begun.elapsed().as_secs_f64());std::fs::write(format!("{}results_direct_k18_k2_charge.json",ODIR),&text).unwrap();print!("{}",text)}

    pub fn run(){std::fs::create_dir_all(ODIR).unwrap();let begun=Instant::now();let e=std::sync::Arc::new(parse());let mut jobs=Vec::new();for start in(0..485).step_by(STEP){let end=(start+STEP).min(485);let x=e.clone();jobs.push(std::thread::spawn(move||build_run(&x,start,end)))}let mut rows=Vec::new();for j in jobs{rows.push(j.join().unwrap())}rows.sort_by_key(|x|x.0.clone());let mut paths=Vec::new();let mut total=Stats::default();let(mut runkeys,mut runsum,mut runuses)=(0u64,0i128,0u64);for(path,s,n,w,u)in rows{paths.push(path);total.add(&s);runkeys+=n;runsum+=w;runuses+=u}assert_eq!(total.full.iter().sum::<u64>(),152_251_200);assert_eq!(total.piv.iter().sum::<u64>(),137_817_600);let(count,zero,sum,uses,out)=merge(&paths,&total);assert_eq!(sum,runsum);assert!(uses<=runuses);let names=["D18:244|R:2","D18:424|R:2","D18:442|R:2","D18:433|R:2","D18:343|R:2","D18:334|R:2"];let line=(0..6).map(|i|format!("\"{}\":{{\"full_parents\":{},\"pivotable_parents\":{},\"outgoing_pivot_uses\":{}}}",names[i],total.full[i],total.piv[i],total.uses[i])).collect::<Vec<_>>().join(",");let text=format!("{{\n \"status\":\"PASS_FULL_DIRECT6_K18_ENRICHED_PROFILE_CENSUS\",\n \"scale\":{},\n \"atomic_runs\":{},\n \"run_nonzero_key_sum\":{},\n \"merged_nonzero_keys\":{},\n \"cross_run_exact_zero_keys\":{},\n \"merged_weight_sum_scaled\":\"{}\",\n \"total_outgoing_pivot_uses\":{},\n \"atomic_nonzero_key_uses\":{},\n \"merged_nonzero_key_uses\":{},\n \"lineages\":{{{}}},\n \"checkpoint\":\"{}\",\n \"record_schema\":\"lineage1,profile29,signature12,pivot1,weight_i128,uses_u64,witness_ri_u16,witness_tail_indices3\",\n \"elapsed_seconds\":{:.6}\n}}\n",U2,paths.len(),runkeys,count,zero,sum,total.uses.iter().sum::<u64>(),runuses,uses,line,out,begun.elapsed().as_secs_f64());std::fs::write(format!("{}results_direct_k18_profile_census.json",ODIR),&text).unwrap();print!("{}",text)}
}

fn main(){if std::env::args().any(|x|x=="--evaluate-k2"){base::evaluate()}else{base::run()}}
