// Exhaustive 5^10 search for the sparsest first-lift separating left dual.

const BASIS: [[u8; 30]; 10] = [
 [0,0,1,4,0,0,2,4,3,1,4,0,2,2,1,2,1,2,2,2,1,0,0,0,0,0,0,0,0,0],
 [4,0,3,2,0,1,2,4,3,1,0,4,4,4,0,1,0,1,3,3,0,1,0,0,0,0,0,0,0,0],
 [2,0,4,0,0,3,1,0,1,1,1,3,3,1,0,1,3,2,0,4,0,0,1,0,0,0,0,0,0,0],
 [2,0,2,3,0,4,0,1,4,2,1,3,2,1,2,2,0,3,3,1,0,0,0,1,0,0,0,0,0,0],
 [2,2,2,3,2,3,4,1,2,2,1,2,4,2,2,3,3,0,1,0,0,0,0,0,1,0,0,0,0,0],
 [2,0,3,2,0,4,1,1,3,2,1,3,0,4,4,2,2,3,3,1,0,0,0,0,0,1,0,0,0,0],
 [3,3,1,4,3,2,2,4,0,0,2,1,3,2,4,3,2,2,2,0,0,0,0,0,0,0,1,0,0,0],
 [1,0,0,4,0,4,3,0,4,1,1,3,0,3,1,3,4,4,0,4,0,0,0,0,0,0,0,1,0,0],
 [0,3,4,1,3,0,4,0,0,2,4,3,2,4,4,4,3,2,3,4,0,0,0,0,0,0,0,0,1,0],
 [2,2,1,4,2,3,1,2,2,4,3,4,0,1,4,2,1,3,2,4,0,0,0,0,0,0,0,0,0,1],
];
const RHS: [u8; 30] = [4,3,3,4,3,4,2,4,2,1,4,3,1,4,3,4,2,4,3,3,0,3,3,2,4,3,3,3,4,2];

fn half(start: usize) -> Vec<[u8; 30]> {
    let mut answer = Vec::with_capacity(3125);
    for code in 0..3125usize {
        let mut digits = code;
        let mut vector = [0u8; 30];
        for basis in start..start + 5 {
            let coefficient = (digits % 5) as u8;
            digits /= 5;
            for index in 0..30 {
                vector[index] = (vector[index]
                    + coefficient * BASIS[basis][index]) % 5;
            }
        }
        answer.push(vector);
    }
    answer
}

fn main() {
    let left = half(0);
    let right = half(5);
    let mut best_weight = 31usize;
    let mut best = [0u8; 30];
    let mut best_pairing = 0u8;
    for a in &left {
        for b in &right {
            let mut vector = [0u8; 30];
            let mut weight = 0usize;
            let mut pairing = 0u8;
            for index in 0..30 {
                vector[index] = (a[index] + b[index]) % 5;
                weight += (vector[index] != 0) as usize;
                pairing = (pairing + vector[index] * RHS[index]) % 5;
            }
            if pairing != 0 && weight < best_weight {
                best_weight = weight;
                best = vector;
                best_pairing = pairing;
            }
        }
    }
    assert!(best_weight < 31);
    println!("minimum support: {}", best_weight);
    println!("pairing: {}", best_pairing);
    println!("dual: {:?}", best);
}
