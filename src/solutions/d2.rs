enum InstrType {
    FORWARD,
    UP,
    DOWN,
}

struct Instruction {
    op: InstrType,
    value: u32,
}

fn parse_instruction(instr_txt: &str) -> Instruction {
    let (op, value) = instr_txt.split_once(" ").unwrap();
    Instruction {
        op: match op {
            "forward" => InstrType::FORWARD,
            "up" => InstrType::UP,
            "down" => InstrType::DOWN,
            _ => unreachable!(),
        },
        value: value.parse().unwrap(),
    }
}

pub fn run(input: String) {
    let instructions: Vec<Instruction> = input.lines().map(parse_instruction).collect();
    let mut horizontal = 0;
    let mut depth = 0;
    let mut aim = 0;

    for instr in instructions.iter() {
        match instr.op {
            InstrType::FORWARD => {
                horizontal += instr.value;
                depth += aim * instr.value;
            }
            InstrType::UP => aim -= instr.value,
            InstrType::DOWN => aim += instr.value,
        }
    }

    println!(
        "Horizontal: {:#?}, Depth: {:#?}, Horizontal * Depth: {:#?}",
        horizontal,
        depth,
        horizontal * depth
    )
}
