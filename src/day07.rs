use std::env;
use std::fs;

#[derive(Clone, Debug)]
struct Equation {
    result: u64,
    nums: Vec<u64>,
}

#[derive(Clone, Copy, Debug)]
enum Operation {
    Add,
    Multiply,
    Concatenate,
}

fn main() {
    let val = env::args().last().unwrap();
    println!("File name: {val}");
    let data = fs::read_to_string(val).unwrap();

    let mut equations: Vec<Equation> = Vec::new();

    for line in data.lines().filter(|x| !x.is_empty()) {
        let (result, nums_str) = line.split_once(": ").unwrap();
        equations.push(Equation {
            result: result.parse().unwrap(),
            nums: nums_str.split(" ").map(|x| x.parse().unwrap()).collect(),
        });
    }

    find_solvable_sum(equations.clone(), vec![Operation::Add, Operation::Multiply]);
    find_solvable_sum(
        equations,
        vec![Operation::Add, Operation::Multiply, Operation::Concatenate],
    );
}

fn find_solvable_sum(equations: Vec<Equation>, operations: Vec<Operation>) {
    let mut solvable_sum = 0;

    for eq in equations {
        let available_op_positions = eq.nums.len() - 1;

        // Go through all possible combinations of operations
        for ops in gen_ops(available_op_positions, operations.clone()) {
            if apply_ops(eq.nums.clone(), ops.clone()) == eq.result {
                solvable_sum += eq.result;
                break;
            }
        }
    }

    println!("Sum of solvable equations: {}", solvable_sum);
}

fn apply_ops(nums: Vec<u64>, ops: Vec<Operation>) -> u64 {
    let mut result = nums[0];
    for i in 1..nums.len() {
        result = {
            let b = nums[i];
            let op = ops[i - 1];
            match op {
                Operation::Add => result + b,
                Operation::Multiply => result * b,
                Operation::Concatenate => (result.to_string() + &b.to_string()).parse().unwrap(),
            }
        };
    }
    result
}

fn gen_ops(size: usize, possible_ops: Vec<Operation>) -> Vec<Vec<Operation>> {
    if size == 0 {
        return vec![vec![]];
    }
    let mut result = Vec::new();
    for op in &possible_ops {
        for mut sub_ops in gen_ops(size - 1, possible_ops.clone()) {
            sub_ops.insert(0, *op);
            result.push(sub_ops);
        }
    }
    result
}
