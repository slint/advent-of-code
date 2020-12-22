use std::collections::HashMap;
pub mod d1;
pub mod d2;
pub mod d3;

pub fn get_solutions() -> HashMap<u8, fn(String) -> ()> {
    let mut solutions: HashMap<u8, fn(String) -> ()> = HashMap::new();
    solutions.insert(1, d1::run);
    solutions.insert(2, d2::run);
    solutions.insert(3, d3::run);
    solutions
}
