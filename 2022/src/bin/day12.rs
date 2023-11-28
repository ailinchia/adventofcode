use std::{io};
use std::cmp::min;
use std::io::Read;
use pathfinding::prelude::dijkstra;

#[derive(PartialEq)]
#[derive(Copy, Clone)]
#[derive(Eq, Hash, Debug)]
struct Coord {
    y: usize,
    x: usize,
}

fn print_grid(grid: &Vec<Vec<char>>) {
    for row in grid {
        for c in row {
            print!("{}", c);
        }
        println!();
    }
    println!();
}

fn find_char(map: &Vec<Vec<char>>, c: char) -> Coord {
    for (y, row) in map.iter().enumerate() {
        for (x, c2) in row.iter().enumerate() {
            if *c2 == c {
                return Coord{y, x};
            }
        }
    }
    panic!("Could not find char");
}

fn get_valid_path(map: &Vec<Vec<char>>, current: Coord) -> Vec<Coord> {
    let y = current.y;
    let x = current.x;
    let c = map[y][x] as u8;
    let mut result = Vec::new();

    // up
    if y > 0 && (map[y-1][x] as u8 <= c + 1) {
        result.push(Coord{y: y-1, x});
    }

    // down
    if y < map.len() - 1 && (map[y+1][x] as u8 <= c + 1) {
        result.push(Coord{y: y+1, x});
    }
    // left
    if x > 0 && (map[y][x-1] as u8 <= c + 1) {
        result.push(Coord{y, x: x-1});
    }
    // right
    if x < map[0].len() - 1 && (map[y][x+1] as u8 <= c + 1) {
        result.push(Coord{y, x: x+1});
    }

    result
}

fn part1(input: &str) -> String {
    let mut map = input.lines().map(|line| line.chars().collect::<Vec<_>>()).collect::<Vec<Vec<_>>>();
    let start = find_char(&map, 'S');
    map[start.y][start.x] = 'a';
    let end = find_char(&map, 'E');
    map[end.y][end.x] = 'z';

    let result = dijkstra(&start, |c| get_valid_path(&map, *c).into_iter().map(|c2| (c2, 1)), |c| *c == end).unwrap();
    // let s = result.0.iter().map(|c| map[c.y][c.x]).collect::<String>();

    result.1.to_string()
}

fn find_all_chars(map: &Vec<Vec<char>>, c: char) -> Vec<Coord> {
    let mut result = Vec::new();
    for (y, row) in map.iter().enumerate() {
        for (x, c2) in row.iter().enumerate() {
            if *c2 == c {
                result.push(Coord{y, x});
            }
        }
    }
    result
}

fn part2(input: &str) -> String {
    let mut map = input.lines().map(|line| line.chars().collect::<Vec<_>>()).collect::<Vec<Vec<_>>>();
    let start = find_char(&map, 'S');
    map[start.y][start.x] = 'a';
    let end = find_char(&map, 'E');
    map[end.y][end.x] = 'z';

    let mut keys = find_all_chars(&map, 'a');
    let mut min_steps = i32::MAX;
    for key in keys {
        let result = dijkstra(&key, |c| get_valid_path(&map, *c).into_iter().map(|c2| (c2, 1)), |c| *c == end);
        if let Some((_, steps)) = result {
            min_steps = min(min_steps, steps);
        }
        // min_steps = min(min_steps, result.1);
    }

    min_steps.to_string()
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

    const DAY_NUM: &str = "12";

    #[test]
    fn test_input() {
        let filename = format!("day{}/input", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "");
        adventofcode::test_part(filename.as_str(), part2, "");
    }

    #[test]
    fn test_inputa() {
        let filename = format!("day{}/inputa", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "");
        adventofcode::test_part(filename.as_str(), part2, "");
    }
}