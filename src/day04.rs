mod grid;
use std::env;
use std::fs;

use grid::{Dir, Grid};

fn main() {
    let val = env::args().last().unwrap();
    println!("File name: {val}");
    let data = fs::read_to_string(val).unwrap();

    let lines: Vec<&str> = data.lines().collect();
    let mut grid: Grid<char> = Grid::new(lines.len(), lines.len());

    for (y, line) in lines.iter().enumerate() {
        for (x, char) in line.chars().enumerate() {
            grid[(x, y)].value = char;
        }
    }

    part_one(&grid);
    part_two(&grid);
}

fn part_two(grid: &Grid<char>) {
    let mut x_mas_count = 0;
    for y in 0..grid.data.len() {
        for x in 0..grid.data[y].len() {
            let cell = &grid[(x, y)];
            if cell.value == 'A' {
                let neighbors = grid.get_neighbors_map(cell);
                let nw = neighbors.get(&Dir::NorthWest);
                let ne = neighbors.get(&Dir::NorthEast);
                let sw = neighbors.get(&Dir::SouthWest);
                let se = neighbors.get(&Dir::SouthEast);

                if let (Some(nw), Some(ne), Some(sw), Some(se)) = (nw, ne, sw, se) {
                    let one_match = matches!((nw.value, se.value), ('M', 'S') | ('S', 'M'));
                    let two_match = matches!((ne.value, sw.value), ('M', 'S') | ('S', 'M'));
                    if one_match && two_match {
                        x_mas_count += 1;
                    }
                }
            }
        }
    }
    println!("X-MAS count: {x_mas_count}");
}

fn part_one(grid: &Grid<char>) {
    // find all the XMAS in the grid
    let mut xmas_count = 0;
    for y in 0..grid.data.len() {
        for x in 0..grid.data[y].len() {
            let cell = &grid[(x, y)];
            if cell.value == 'X' {
                let found_m = grid.find_in_neighbors(cell, 'M');
                for (dir, cell) in found_m {
                    if let Some(cell) = grid.get_neighbor(cell, *dir) {
                        if cell.value == 'A' {
                            if let Some(cell) = grid.get_neighbor(cell, *dir) {
                                if cell.value == 'S' {
                                    xmas_count += 1;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    println!("XMAS count: {xmas_count}");
}
