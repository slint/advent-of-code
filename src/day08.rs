mod grid;
use std::collections::HashMap;
use std::collections::HashSet;
use std::env;
use std::fmt::Display;
use std::fs;

use grid::{ColorChar, Grid, Point};

#[derive(Debug, Default, Clone, Copy, PartialEq, Eq)]
enum Tile {
    Antenna(char),
    Antinode(char),
    #[default]
    Empty,
}

impl Display for Tile {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{}",
            match self {
                Tile::Antenna(c) => ColorChar {
                    // use ascii value of c as color
                    color: Some(*c as u8),
                    underline: false,
                    char: *c,
                },
                Tile::Antinode(c) => ColorChar {
                    // use ascii value of c as color
                    color: Some(*c as u8),
                    underline: true,
                    char: *c,
                },
                Tile::Empty => ColorChar {
                    color: None,
                    underline: false,
                    char: '.',
                },
            }
        )
    }
}

fn main() {
    let val = env::args().last().unwrap();
    println!("File name: {val}");
    let data = fs::read_to_string(val).unwrap();
    let lines: Vec<&str> = data.lines().collect();
    let mut grid: Grid<Tile> = Grid::new(lines.len(), lines.len());

    let mut antenna_positions: HashMap<char, Vec<Point>> = HashMap::new();

    for (y, line) in lines.iter().enumerate() {
        for (x, char) in line.chars().enumerate() {
            let tile = match char {
                '.' => Tile::Empty,
                c => Tile::Antenna(c),
            };
            let cell = &mut grid[(x, y)];
            cell.value = tile;
            if let Tile::Antenna(c) = tile {
                let positions = antenna_positions.entry(c).or_default();
                positions.push((x, y));
            }
        }
    }

    part_one(&grid, &antenna_positions);

    part_two(&grid, &antenna_positions);
}

fn part_one(grid: &Grid<Tile>, antenna_positions: &HashMap<char, Vec<(usize, usize)>>) {
    let grid_max_x = grid.width() - 1;
    let grid_max_y = grid.height() - 1;
    let mut antinode_positions: HashMap<char, HashSet<Point>> = HashMap::new();
    // get each unique pair for each antenna type
    for (antenna_type, positions) in antenna_positions {
        let antenna_pairs = position_pairs(positions);
        // for each pair get their two anti-diametric points
        for (antenna_1, antenna_2) in antenna_pairs {
            let (antinode_1, antinode_2) =
                get_antinodes(antenna_1, antenna_2, grid_max_x, grid_max_y);
            if let Some(antinode_1) = antinode_1 {
                let positions = antinode_positions.entry(*antenna_type).or_default();
                positions.insert(antinode_1);
            }
            if let Some(antinode_2) = antinode_2 {
                let positions = antinode_positions.entry(*antenna_type).or_default();
                positions.insert(antinode_2);
            }
        }
    }

    let total_antinode_positions: HashSet<Point> =
        antinode_positions.values().flatten().cloned().collect();

    println!(
        "Total antinode poistions: {:?}",
        total_antinode_positions.len()
    );
}

fn part_two(grid: &Grid<Tile>, antenna_positions: &HashMap<char, Vec<(usize, usize)>>) {
    let grid_max_x = grid.width() - 1;
    let grid_max_y = grid.height() - 1;
    let mut antinode_positions: HashMap<char, HashSet<Point>> = HashMap::new();
    // get each unique pair for each antenna type
    for (antenna_type, positions) in antenna_positions {
        let antenna_pairs = position_pairs(positions);
        // for each pair get their two anti-diametric points
        for (antenna_1, antenna_2) in antenna_pairs {
            let (antinode_1, antinode_2) =
                get_antinodes(antenna_1, antenna_2, grid_max_x, grid_max_y);
            if let Some(antinode_1) = antinode_1 {
                let positions = antinode_positions.entry(*antenna_type).or_default();
                positions.insert(antinode_1);
            }
            if let Some(antinode_2) = antinode_2 {
                let positions = antinode_positions.entry(*antenna_type).or_default();
                positions.insert(antinode_2);
            }
            // check in one direction for antinodes
            let node_1 = antenna_1;
            if let Some(node_2) = antinode_1 {
                loop {
                    let (antinode_1, antinode_2) =
                        get_antinodes(node_1, node_2, grid_max_x, grid_max_y);
                    if let Some(antinode_1) = antinode_1 {
                        let positions = antinode_positions.entry(*antenna_type).or_default();
                        positions.insert(antinode_1);
                    }
                    if let Some(antinode_2) = antinode_2 {
                        let positions = antinode_positions.entry(*antenna_type).or_default();
                        positions.insert(antinode_2);
                    }
                }
            }
        }
    }

    let total_antinode_positions: HashSet<Point> =
        antinode_positions.values().flatten().cloned().collect();

    println!(
        "Total resonant antinode poistions: {:?}",
        total_antinode_positions.len()
    );
}

fn position_pairs(positions: &[Point]) -> Vec<(Point, Point)> {
    let mut pairs = Vec::new();
    for i in 0..positions.len() {
        for j in i + 1..positions.len() {
            pairs.push((positions[i], positions[j]));
        }
    }
    pairs
}

fn get_antinodes(a: Point, b: Point, max_x: usize, max_y: usize) -> (Option<Point>, Option<Point>) {
    let (x1, y1) = a;
    let (x2, y2) = b;
    let (dx, dy) = (x1 as isize - x2 as isize, y1 as isize - y2 as isize);
    let (x3, y3) = (x2 as isize + (-dx), y2 as isize + (-dy));
    let (x4, y4) = (x1 as isize + dx, y1 as isize + dy);

    let a1 = checked_point(max_x, max_y, x3, y3);
    let a2 = checked_point(max_x, max_y, x4, y4);

    (a1, a2)
}

fn checked_point(max_x: usize, max_y: usize, x: isize, y: isize) -> Option<Point> {
    if (0isize..=max_x as isize).contains(&x) && (0isize..=max_y as isize).contains(&y) {
        Some((x as usize, y as usize))
    } else {
        None
    }
}
