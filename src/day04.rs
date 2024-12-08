use std::collections::HashMap;
use std::env;
use std::fs;
use std::ops::Index;
use std::ops::IndexMut;

#[derive(Debug, Copy, Clone, Hash, Eq, PartialEq)]
enum Dir {
    North,
    NorthEast,
    East,
    SouthEast,
    South,
    SouthWest,
    West,
    NorthWest,
}

#[derive(Debug)]
struct Cell<T> {
    x: usize,
    y: usize,
    value: T,
}

#[derive(Debug, Default)]
struct Grid<T> {
    data: Vec<Vec<Cell<T>>>,
}

impl<T> Grid<T> {
    fn new(height: usize, width: usize) -> Self
    where
        T: Default,
    {
        let mut data = Vec::with_capacity(height);
        for y in 0..height {
            let mut row = Vec::with_capacity(width);
            for x in 0..width {
                row.push(Cell {
                    x,
                    y,
                    value: T::default(),
                });
            }
            data.push(row);
        }
        Grid { data }
    }

    fn get_neighbor(&self, cell: &Cell<T>, dir: Dir) -> Option<&Cell<T>> {
        let (x, y) = match dir {
            Dir::North => (cell.x, cell.y.checked_sub(1)?),
            Dir::NorthEast => (cell.x + 1, cell.y.checked_sub(1)?),
            Dir::East => (cell.x + 1, cell.y),
            Dir::SouthEast => (cell.x + 1, cell.y + 1),
            Dir::South => (cell.x, cell.y + 1),
            Dir::SouthWest => (cell.x.checked_sub(1)?, cell.y + 1),
            Dir::West => (cell.x.checked_sub(1)?, cell.y),
            Dir::NorthWest => (cell.x.checked_sub(1)?, cell.y.checked_sub(1)?),
        };

        self.data.get(y).and_then(|row| row.get(x))
    }

    fn get_neighbors(&self, cell: &Cell<T>) -> Vec<(&Dir, Option<&Cell<T>>)> {
        let mut neighbors = Vec::with_capacity(8);
        for dir in &[
            Dir::North,
            Dir::NorthEast,
            Dir::East,
            Dir::SouthEast,
            Dir::South,
            Dir::SouthWest,
            Dir::West,
            Dir::NorthWest,
        ] {
            neighbors.push((dir, self.get_neighbor(cell, *dir)));
        }
        neighbors
    }

    fn get_neighbors_map(&self, cell: &Cell<T>) -> HashMap<Dir, &Cell<T>> {
        let mut neighbors: HashMap<Dir, &Cell<T>> = HashMap::new();
        for dir in &[
            Dir::North,
            Dir::NorthEast,
            Dir::East,
            Dir::SouthEast,
            Dir::South,
            Dir::SouthWest,
            Dir::West,
            Dir::NorthWest,
        ] {
            if let Some(neighbor) = self.get_neighbor(cell, *dir) {
                neighbors.insert(*dir, neighbor);
            }
        }
        neighbors
    }

    fn find_in_neighbors(&self, cell: &Cell<T>, val: T) -> Vec<(&Dir, &Cell<T>)>
    where
        T: PartialEq,
    {
        let mut cells = Vec::new();
        for (dir, neighbor) in self.get_neighbors(cell) {
            if let Some(neighbor) = neighbor {
                if neighbor.value == val {
                    cells.push((dir, neighbor));
                }
            }
        }
        cells
    }
}

impl<T> Index<(usize, usize)> for Grid<T> {
    type Output = Cell<T>;

    fn index(&self, index: (usize, usize)) -> &Self::Output {
        &self.data[index.1][index.0]
    }
}

impl<T> IndexMut<(usize, usize)> for Grid<T> {
    fn index_mut(&mut self, index: (usize, usize)) -> &mut Self::Output {
        &mut self.data[index.1][index.0]
    }
}

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
