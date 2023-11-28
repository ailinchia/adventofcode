use std::{io};
use std::io::Read;
use pathfinding::prelude::dijkstra;

const GRID_SIZE: usize = 25;

#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Coord {
    z: usize,
    y: usize,
    x: usize,
}

// print grid
fn print_grid(grid: &Vec<Vec<Vec<bool>>>) {
    for z in 0..grid.len() {
        println!("z={}", z - grid.len() / 2);
        for y in 0..grid[z].len() {
            for x in 0..grid[z][y].len() {
                print!("{}", if grid[z][y][x] { '#' } else { '.' });
            }
            println!();
        }
        println!();
    }
}

// count exposed
fn check_neighbours(grid: &Vec<Vec<Vec<bool>>>, z: usize, y: usize, x: usize, check_exterior: bool) -> i32 {
    let mut count = 0;

    // up
    if y > 0 && !grid[z][y - 1][x] && (!check_exterior || is_exterior(grid, z, y - 1, x)) {
        count += 1;
    }
    // down
    if y < GRID_SIZE - 1 && !grid[z][y + 1][x] && (!check_exterior || is_exterior(grid, z, y + 1, x)) {
        count += 1;
    }
    // left
    if x > 0 && !grid[z][y][x - 1] && (!check_exterior || is_exterior(grid, z, y, x - 1)) {
        count += 1;
    }
    // right
    if x < GRID_SIZE - 1 && !grid[z][y][x + 1] && (!check_exterior || is_exterior(grid, z, y, x + 1)) {
        count += 1;
    }
    // front
    if z > 0 && !grid[z - 1][y][x] && (!check_exterior || is_exterior(grid, z - 1, y, x)) {
        count += 1;
    }
    // back
    if z < GRID_SIZE - 1 && !grid[z + 1][y][x] && (!check_exterior || is_exterior(grid, z + 1, y, x)) {
        count += 1;
    }

    count
}

fn is_exterior(grid: &Vec<Vec<Vec<bool>>>, z: usize, y: usize, x: usize) -> bool {
    let result = dijkstra(
        &Coord{z, y, x},
        |c| {
            let mut result = Vec::new();
            // up
            if c.y > 0 && !grid[c.z][c.y - 1][c.x] {
                result.push((Coord{z: c.z, y: c.y - 1, x: c.x}, 1));
            }
            // down
            if c.y < GRID_SIZE - 1 && !grid[c.z][c.y + 1][c.x] {
                result.push((Coord{z: c.z, y: c.y + 1, x: c.x}, 1));
            }
            // left
            if c.x > 0 && !grid[c.z][c.y][c.x - 1] {
                result.push((Coord{z: c.z, y: c.y, x: c.x - 1}, 1));
            }
            // right
            if c.x < GRID_SIZE - 1 && !grid[c.z][c.y][c.x + 1] {
                result.push((Coord{z: c.z, y: c.y, x: c.x + 1}, 1));
            }
            // front
            if c.z > 0 && !grid[c.z - 1][c.y][c.x] {
                result.push((Coord{z: c.z - 1, y: c.y, x: c.x}, 1));
            }
            // back
            if c.z < GRID_SIZE - 1 && !grid[c.z + 1][c.y][c.x] {
                result.push((Coord{z: c.z + 1, y: c.y, x: c.x}, 1));
            }
            result
        },
        |c| c.z == 0 && c.y == 0 && c.x == 0,
    ).is_some();
    // println!("{} {} {} {:?}", z, y, x, result);
    result
}

fn parse_input(input: &str) -> Vec<Vec<Vec<bool>>> {
    let mut grid = vec![vec![vec![false; GRID_SIZE]; GRID_SIZE]; GRID_SIZE];

    for line in input.lines() {
        let parts = line.split(",").map(|s| s.parse::<usize>().unwrap()).collect::<Vec<_>>();
        let x = parts[0];
        let y = parts[1];
        let z = parts[2];

        grid[z][y][x] = true;
    }
    grid
}

fn part1(input: &str) -> String {
    let grid = parse_input(input);

    let mut count = 0;
    for z in 0..GRID_SIZE {
        for y in 0..GRID_SIZE {
            for x in 0..GRID_SIZE {
                if !grid[z][y][x] {
                    continue;
                }

                count += check_neighbours(&grid, z, y, x, false);
            }
        }
    }
    count.to_string()
}

fn part2(input: &str) -> String {
    let grid = parse_input(input);
    // print_grid(&grid);

    let mut count = 0;
    for z in 0..GRID_SIZE {
        for y in 0..GRID_SIZE {
            for x in 0..GRID_SIZE {
                if !grid[z][y][x] {
                    continue;
                }
                count += check_neighbours(&grid, z, y, x, true);
            }
        }
    }
    count.to_string()
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();

    println!("{}", part1(&input));
    println!("{}", part2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    const DAY_NUM: &str = "18";

    #[test]
    fn test_input() {
        let filename = format!("day{}/input", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "4460");
        adventofcode::test_part(filename.as_str(), part2, "2498");
    }

    #[test]
    fn test_inputa() {
        let filename = format!("day{}/inputa", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "10");
        adventofcode::test_part(filename.as_str(), part2, "10");
    }

    #[test]
    fn test_inputb() {
        let filename = format!("day{}/inputb", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "64");
        adventofcode::test_part(filename.as_str(), part2, "60");
    }
}