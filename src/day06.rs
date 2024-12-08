mod grid;
use std::collections::HashSet;
use std::env;
use std::fs;

use grid::{Dir, Grid, Point};

#[derive(Debug, Default, Clone, Copy, PartialEq, Eq)]
enum Tile {
    Box,
    #[default]
    Empty,
    Visited,
}

fn main() {
    let val = env::args().last().unwrap();
    println!("File name: {val}");
    let data = fs::read_to_string(val).unwrap();

    let lines: Vec<&str> = data.lines().collect();
    let mut grid: Grid<Tile> = Grid::new(lines.len(), lines.len());

    let mut guard_pos = (0, 0);

    for (y, line) in lines.iter().enumerate() {
        for (x, char) in line.chars().enumerate() {
            let tile = match char {
                '#' => Tile::Box,
                '^' => Tile::Visited,
                '.' => Tile::Empty,
                _ => panic!("Invalid tile"),
            };
            grid[(x, y)].value = tile;
            if char == '^' {
                guard_pos = (x, y);
            }
        }
    }

    part_one(&grid, guard_pos);
    part_two(grid, guard_pos);
}

fn part_two(grid: Grid<Tile>, guard_pos: (usize, usize)) {
    // Insert obstacles in every valid position
    let mut valid_obstacle_count = 0;
    for x in 0..grid.width() {
        for y in 0..grid.height() {
            if grid[(x, y)].value != Tile::Empty {
                continue;
            }
            let mut grid = grid.clone();
            grid[(x, y)].value = Tile::Box;
            if !walk_guard(&mut grid, guard_pos) {
                println!("Guard is trapped because of ({}, {})", x, y);
                valid_obstacle_count += 1;
            }
        }
    }

    println!("Valid obstacles: {}", valid_obstacle_count);
}

fn part_one(grid: &Grid<Tile>, guard_pos: (usize, usize)) {
    let mut original_grid = grid.clone();
    walk_guard(&mut original_grid, guard_pos);
    let visited_cells = original_grid
        .cells()
        .into_iter()
        .filter(|cell| cell.value == Tile::Visited)
        .count();

    println!("Visited cells: {}", visited_cells);
}

fn walk_guard(grid: &mut Grid<Tile>, mut guard_pos: Point) -> bool {
    let mut guard_dir = Dir::North;

    // Keep encountered boxes from a certain direction to detect cycles
    let mut boxes: HashSet<(Point, Point)> = HashSet::new();

    loop {
        let cur_point = grid[guard_pos].point();
        let next_cell = {
            let cur_cell = &grid[guard_pos];
            grid.get_neighbor(cur_cell, guard_dir)
        };

        if let Some(next_cell) = next_cell {
            match next_cell.value {
                Tile::Box => {
                    // The guard turns right
                    match guard_dir {
                        Dir::North => guard_dir = Dir::East,
                        Dir::East => guard_dir = Dir::South,
                        Dir::South => guard_dir = Dir::West,
                        Dir::West => guard_dir = Dir::North,
                        _ => unreachable!("Guard doesn't move diagonally"),
                    }

                    // Check if the guard has visited this box before
                    let key = (cur_point, next_cell.point());
                    if boxes.contains(&key) {
                        // Guard is trapped
                        return false;
                    } else {
                        boxes.insert(key);
                    }
                }
                Tile::Empty => {
                    let next_pos = (next_cell.x, next_cell.y);
                    grid[next_pos].value = Tile::Visited;
                    guard_pos = next_pos;
                }
                Tile::Visited => {
                    guard_pos = (next_cell.x, next_cell.y);
                }
            }
        } else {
            // Guard is of the grid
            return true;
        }
    }
}
