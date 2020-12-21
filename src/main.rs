use std::error::Error;
use std::path::Path;

mod solutions;

static LAST_DAY: u8 = 1;

fn parse_args() -> Result<(u8, String), Box<dyn Error>> {
    let mut args = std::env::args();

    // Parse day
    let day = match args.next() {
        Some(day_or_input_path) => match day_or_input_path.parse::<u8>() {
            Ok(day_input) => day_input,
            Err(_) => LAST_DAY,
        },
        None => LAST_DAY,
    };

    // Parse input path
    let input_path = match args.next() {
        Some(input_path) => {
            if Path::new(&input_path).exists() {
                input_path
            } else {
                "input.txt".to_string()
            }
        }
        None => "input.txt".to_string(),
    };
    let input = std::fs::read_to_string(input_path).unwrap();
    Ok((day, input))
}

fn main() {
    let (day, input) = parse_args().unwrap();
    println!("Running day {}...", day);
    let solutions = solutions::get_solutions();
    solutions.get(&day).expect("No solution for this day")(input);
}
