use std::collections::HashMap;
use std::ops::{Index, IndexMut};

#[derive(Debug, Copy, Clone, Hash, Eq, PartialEq)]
pub enum Dir {
    North,
    NorthEast,
    East,
    SouthEast,
    South,
    SouthWest,
    West,
    NorthWest,
}

pub type Point = (usize, usize);

#[derive(Debug)]
pub struct Cell<T> {
    pub x: usize,
    pub y: usize,
    pub value: T,
}

impl<T> Cell<T> {
    pub fn point(&self) -> Point {
        (self.x, self.y)
    }
}

#[derive(Debug, Default)]
pub struct Grid<T>
where
    T: Clone + Default + PartialEq + Eq,
{
    pub data: Vec<Vec<Cell<T>>>,
}

impl<T> Grid<T>
where
    T: Clone + Default + PartialEq + Eq,
{
    pub fn new(height: usize, width: usize) -> Self {
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

    pub fn cells(&self) -> Vec<&Cell<T>> {
        self.data.iter().flatten().collect()
    }

    pub fn get_neighbor(&self, cell: &Cell<T>, dir: Dir) -> Option<&Cell<T>> {
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

    pub fn get_neighbors(&self, cell: &Cell<T>) -> Vec<(&Dir, Option<&Cell<T>>)> {
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

    pub fn get_neighbors_map(&self, cell: &Cell<T>) -> HashMap<Dir, &Cell<T>> {
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

    pub fn find_in_neighbors(&self, cell: &Cell<T>, val: T) -> Vec<(&Dir, &Cell<T>)> {
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

    pub fn width(&self) -> usize {
        self.data[0].len()
    }

    pub fn height(&self) -> usize {
        self.data.len()
    }
}

impl<T> Index<Point> for Grid<T>
where
    T: Clone + Default + PartialEq + Eq,
{
    type Output = Cell<T>;

    fn index(&self, index: Point) -> &Self::Output {
        &self.data[index.1][index.0]
    }
}

impl<T> IndexMut<Point> for Grid<T>
where
    T: Clone + Default + PartialEq + Eq,
{
    fn index_mut(&mut self, index: Point) -> &mut Self::Output {
        &mut self.data[index.1][index.0]
    }
}

impl<T> Clone for Grid<T>
where
    T: Clone + Default + PartialEq + Eq,
{
    fn clone(&self) -> Self {
        let mut data = Vec::with_capacity(self.data.len());
        for row in &self.data {
            let mut new_row = Vec::with_capacity(row.len());
            for cell in row {
                new_row.push(Cell {
                    x: cell.x,
                    y: cell.y,
                    value: cell.value.clone(),
                });
            }
            data.push(new_row);
        }
        Grid { data }
    }
}
