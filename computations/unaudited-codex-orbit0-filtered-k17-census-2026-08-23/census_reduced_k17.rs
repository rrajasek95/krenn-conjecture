//! Read-only structural census of the frozen reduced K17 checkpoint.
use std::collections::BTreeMap;
use std::fs::File;
use std::io::{BufReader,BufWriter,Read,Write};
use std::time::{Duration,Instant};

const INPUT:&str="computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_reduced_k17.bin";
const OUTPUT:&str="computations/unaudited-codex-orbit0-filtered-k17-census-2026-08-23/results_reduced_k17_census.json";
const EXPECTED:u64=55_191_349;
const SCALE:i128=281_801_520;
const CAP:Duration=Duration::from_secs(180);
const COLOUR_PERMS:[[usize;3];6]=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];

#[derive(Clone,Copy,Default)]struct EdgeOption{cycle:u8,a:u8,b:u8}
#[derive(Clone,Copy,Eq,Ord,PartialEq,PartialOrd)]struct PartitionKey([u8;13]);
#[derive(Clone,Copy,Eq,Ord,PartialEq,PartialOrd)]struct ContentKey([u8;37]);
#[derive(Clone,Default)]struct Stats{orbits:u64,pivotable:u64,signed:i128,l1:i128,signed_pivotable:i128,l1_pivotable:i128}
impl Stats{fn add(&mut self,value:i128,pivotable:bool){self.orbits+=1;self.signed+=value;self.l1+=value.abs();if pivotable{self.pivotable+=1;self.signed_pivotable+=value;self.l1_pivotable+=value.abs();}}}
fn gcd(mut a:i128,mut b:i128)->i128{a=a.abs();b=b.abs();while b!=0{let r=a%b;a=b;b=r}if a==0{1}else{a}}
fn rat_text(x:i128)->String{let g=gcd(x,SCALE);format!("[{},{ }]",x/g,SCALE/g)}
fn key_text(k:&PartitionKey)->String{(0..k.0[0]as usize).map(|i|k.0[i+1].to_string()).collect::<Vec<_>>().join(",")}
fn content_text(k:&ContentKey)->String{(0..k.0[0]as usize).map(|i|format!("{}:{}:{}",k.0[1+3*i],k.0[2+3*i],k.0[3+3*i])).collect::<Vec<_>>().join(";")}
fn stats_text(s:&Stats)->String{format!("{{\"orbits\":{},\"pivotable\":{},\"unpivotable\":{},\"signed_mass\":{},\"l1_mass\":{},\"signed_pivotable_mass\":{},\"l1_pivotable_mass\":{}}}",s.orbits,s.pivotable,s.orbits-s.pivotable,rat_text(s.signed),rat_text(s.l1),rat_text(s.signed_pivotable),rat_text(s.l1_pivotable))}
fn cell_decode(mut id:u8)->(u8,u8,u8,u8){let colour=id%9;id/=9;let a=colour/3;let b=colour%3;let mut u=0u8;while id>=7-u{id-=7-u;u+=1}(u,u+1+id,a,b)}

fn matching_flags(options:&[[EdgeOption;9];28],counts:&[u8;28],site_mask:u16,cycle_mask:u16,first:u8,mixed:bool)->u8{
    if site_mask==0xff{return 1|if mixed{2}else{0}}
    let u=(0..8usize).find(|&i|site_mask&(1<<i)==0).unwrap();let mut flags=0u8;
    for v in u+1..8{if site_mask&(1<<v)!=0{continue}let edge=u*(15-u)/2+(v-u-1);
        for oi in 0..counts[edge]as usize{let op=options[edge][oi];if cycle_mask&(1<<op.cycle)!=0{continue}let mut nf=first;let mut nm=mixed;if nf==3{nf=op.a}else if op.a!=nf{nm=true}if op.b!=nf{nm=true}
            flags|=matching_flags(options,counts,site_mask|(1<<u)|(1<<v),cycle_mask|(1<<op.cycle),nf,nm);if flags&2!=0{return flags}}
    }flags
}

fn analyze(row:&[u8;24])->(PartitionKey,ContentKey,bool,&'static str){
    let mut adjacency=[[0u8;2];24];let mut degree=[0usize;24];let mut decoded=[(0u8,0u8,0u8,0u8);24];
    for(i,&cell)in row.iter().enumerate(){let(u,v,a,b)=cell_decode(cell);decoded[i]=(u,v,a,b);let x=(3*u+a)as usize;let y=(3*v+b)as usize;assert!(degree[x]<2&&degree[y]<2);adjacency[x][degree[x]]=y as u8;degree[x]+=1;adjacency[y][degree[y]]=x as u8;degree[y]+=1}assert!(degree.iter().all(|&d|d==2));
    let mut label=[u8::MAX;24];let mut sizes=[0u8;12];let mut contents=[[0u8;3];12];let mut nc=0usize;
    for start in 0..24{if label[start]!=u8::MAX{continue}let mut stack=[0u8;24];let mut top=1usize;stack[0]=start as u8;label[start]=nc as u8;while top>0{top-=1;let x=stack[top]as usize;sizes[nc]+=1;contents[nc][x%3]+=1;for &yy in &adjacency[x]{let y=yy as usize;if label[y]==u8::MAX{label[y]=nc as u8;stack[top]=yy;top+=1}}}nc+=1}
    let mut sorted=sizes[..nc].to_vec();sorted.sort_unstable();let mut pk=[0u8;13];pk[0]=nc as u8;pk[1..1+nc].copy_from_slice(&sorted);
    let mut best:Option<[u8;37]>=None;for perm in COLOUR_PERMS{let mut comps=Vec::with_capacity(nc);for source in &contents[..nc]{let mut target=[0u8;3];for old in 0..3{target[perm[old]]=source[old]}comps.push(target)}comps.sort_unstable();let mut key=[0u8;37];key[0]=nc as u8;for(i,c)in comps.iter().enumerate(){key[1+3*i..4+3*i].copy_from_slice(c)}if best.map_or(true,|old|key<old){best=Some(key)}}
    let mut options=[[EdgeOption::default();9];28];let mut counts=[0u8;28];for &(u,v,a,b)in &decoded{let edge=(u as usize)*(15-u as usize)/2+(v-u-1)as usize;let op=EdgeOption{cycle:label[(3*u+a)as usize],a,b};let mut duplicate=false;for i in 0..counts[edge]as usize{let old=options[edge][i];if old.cycle==op.cycle&&old.a==a&&old.b==b{duplicate=true;break}}if !duplicate{let n=counts[edge]as usize;options[edge][n]=op;counts[edge]+=1}}
    let flags=if nc>=4{matching_flags(&options,&counts,0,0,3,false)}else{0};let pivotable=flags&2!=0;let reason=if pivotable{"pivotable"}else if nc<4{"fewer_than_four_cycles"}else if flags&1==0{"no_physical_pm_across_four_cycles"}else{"only_pure_pm_across_four_cycles"};
    (PartitionKey(pk),ContentKey(best.unwrap()),pivotable,reason)
}

fn main(){let start=Instant::now();let f=File::open(INPUT).unwrap();let mut reader=BufReader::with_capacity(1<<22,f);let mut magic=[0u8;8];reader.read_exact(&mut magic).unwrap();assert_eq!(&magic,b"K17RED2\0");let mut nb=[0u8;8];reader.read_exact(&mut nb).unwrap();let n=u64::from_le_bytes(nb);assert_eq!(n,EXPECTED);
    let mut total=Stats::default();let mut partitions=BTreeMap::<PartitionKey,Stats>::new();let mut contents=BTreeMap::<ContentKey,Stats>::new();let mut denominators=BTreeMap::<i128,u64>::new();let mut reasons=BTreeMap::<&str,u64>::new();let mut first_unpivotable=None;
    for index in 0..n{let mut row=[0u8;24];let mut vb=[0u8;16];reader.read_exact(&mut row).unwrap();reader.read_exact(&mut vb).unwrap();let value=i128::from_le_bytes(vb);let(pk,ck,pivotable,reason)=analyze(&row);total.add(value,pivotable);partitions.entry(pk).or_default().add(value,pivotable);contents.entry(ck).or_default().add(value,pivotable);let denominator=SCALE/gcd(value,SCALE);*denominators.entry(denominator).or_default()+=1;*reasons.entry(reason).or_default()+=1;if !pivotable&&first_unpivotable.is_none(){first_unpivotable=Some((row,pk,ck,reason,value))}if(index+1)%500_000==0{eprintln!("ROWS {} pivotable={} partitions={} contents={} elapsed={:.1}",index+1,total.pivotable,partitions.len(),contents.len(),start.elapsed().as_secs_f64());assert!(start.elapsed()<CAP,"180-second cap reached")}}
    let mut end=[0u8;1];assert_eq!(reader.read(&mut end).unwrap(),0);let mut out=BufWriter::new(File::create(OUTPUT).unwrap());writeln!(out,"{{").unwrap();writeln!(out,"  \"status\":\"PASS exact exhaustive read-only K17 structural census\",").unwrap();writeln!(out,"  \"input_rows\":{},",n).unwrap();writeln!(out,"  \"global_scale\":{},",SCALE).unwrap();writeln!(out,"  \"total\":{},",stats_text(&total)).unwrap();writeln!(out,"  \"reason_counts\":{{").unwrap();for(i,(k,v))in reasons.iter().enumerate(){writeln!(out,"    \"{}\":{}{}",k,v,if i+1==reasons.len(){""}else{","}).unwrap()}writeln!(out,"  }},").unwrap();writeln!(out,"  \"coefficient_denominator_histogram\":{{").unwrap();for(i,(k,v))in denominators.iter().enumerate(){writeln!(out,"    \"{}\":{}{}",k,v,if i+1==denominators.len(){""}else{","}).unwrap()}writeln!(out,"  }},").unwrap();writeln!(out,"  \"by_cycle_partition\":{{").unwrap();for(i,(k,v))in partitions.iter().enumerate(){writeln!(out,"    \"{}\":{}{}",key_text(k),stats_text(v),if i+1==partitions.len(){""}else{","}).unwrap()}writeln!(out,"  }},").unwrap();writeln!(out,"  \"by_colour_content_type\":{{").unwrap();for(i,(k,v))in contents.iter().enumerate(){writeln!(out,"    \"{}\":{}{}",content_text(k),stats_text(v),if i+1==contents.len(){""}else{","}).unwrap()}writeln!(out,"  }},").unwrap();let(row,pk,ck,reason,value)=first_unpivotable.unwrap();let hex=row.iter().map(|x|format!("{:02x}",x)).collect::<String>();writeln!(out,"  \"first_unpivotable\":{{\"row\":\"{}\",\"cycle_partition\":\"{}\",\"colour_content\":\"{}\",\"reason\":\"{}\",\"coefficient\":{}}},",hex,key_text(&pk),content_text(&ck),reason,rat_text(value)).unwrap();writeln!(out,"  \"cycle_partitions\":{},",partitions.len()).unwrap();writeln!(out,"  \"colour_content_types\":{},",contents.len()).unwrap();writeln!(out,"  \"elapsed_seconds\":{:.3},",start.elapsed().as_secs_f64()).unwrap();writeln!(out,"  \"scope\":\"Read-only census of checkpoint_reduced_k17.bin; no tails, closure, or rank computation.\"").unwrap();writeln!(out,"}}").unwrap();out.flush().unwrap();println!("PASS rows={} pivotable={} unpivotable={} partitions={} contents={} denominators={} elapsed={:.3}",n,total.pivotable,n-total.pivotable,partitions.len(),contents.len(),denominators.len(),start.elapsed().as_secs_f64())}
