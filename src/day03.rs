use std::env;
use std::fs;
use std::str::Chars;

fn main() {
    let val = env::args().last().unwrap();
    println!("File name: {val}");
    let data = fs::read_to_string(val).unwrap();

    let mut mul_sum = 0;
    let mut mul_enabled = true;

    // read until we have "mul(", "do()" and "don't()"
    let mut chars = data.chars();
    loop {
        match chars.next() {
            Some('m') => match chars.next() {
                Some('u') => match chars.next() {
                    Some('l') => match chars.next() {
                        Some('(') => {
                            // read the two numbers "(x, y)"
                            match read_nums(&mut chars) {
                                Ok(Some((x, y))) => {
                                    if mul_enabled {
                                        mul_sum += x * y;
                                    }
                                }
                                Ok(None) => {
                                    continue;
                                }
                                Err(_) => {
                                    break;
                                }
                            }
                        }
                        _ => continue,
                    },
                    _ => continue,
                },
                _ => continue,
            },
            Some('d') => match chars.next() {
                Some('o') => match chars.next() {
                    Some('(') => match chars.next() {
                        Some(')') => {
                            mul_enabled = true;
                        }
                        _ => continue,
                    },
                    Some('n') => match chars.next() {
                        Some('\'') => match chars.next() {
                            Some('t') => match chars.next() {
                                Some('(') => match chars.next() {
                                    Some(')') => {
                                        mul_enabled = false;
                                    }
                                    _ => continue,
                                },
                                _ => continue,
                            },
                            _ => continue,
                        },
                        _ => continue,
                    },
                    _ => continue,
                },
                _ => continue,
            },
            None => break,
            _ => continue,
        }
    }

    println!("Sum: {}", mul_sum);
}

fn read_nums(chars: &mut Chars<'_>) -> Result<Option<(i32, i32)>, &'static str> {
    let mut x = String::new();
    let mut y = String::new();
    let mut reading_y = false;

    loop {
        match chars.next() {
            Some(c) if c.is_ascii_digit() => {
                if reading_y {
                    y.push(c);
                } else {
                    x.push(c);
                }
            }
            Some(',') => reading_y = true,
            Some(')') => {
                if x.is_empty() || y.is_empty() {
                    return Ok(None);
                }
                return Ok(Some((x.parse().unwrap(), y.parse().unwrap())));
            }
            None => return Err("Ran out of chars"),
            _ => return Ok(None),
        }
    }
}
