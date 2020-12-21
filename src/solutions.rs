use std::collections::HashMap;
pub mod d1;

pub fn get_solutions() -> HashMap<u8, fn(String) -> ()> {
    let mut solutions: HashMap<u8, fn(String) -> ()> = HashMap::new();
    solutions.insert(1, d1::run);
    solutions
}
