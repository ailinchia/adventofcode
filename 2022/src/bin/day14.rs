use std::{io};
use std::cmp::{max, min};
use std::io::Read;

const DIFF_X: usize = 400;

fn print_grid(grid: &Vec<Vec<char>>) {
    for row in grid {
        for c in row {
            print!("{}", c);
        }
        println!("");
    }
}

// return true when sand fall off grid
fn simulate_sand(grid: &mut Vec<Vec<char>>, mut sand_y: usize, mut sand_x: usize, most_max_y: usize, check_blocked: bool) -> bool {
    let orig_sand_x = sand_x;
    let orig_sand_y = sand_y;

    // println!("simulate_sand({}, {})", sand_y, sand_x);
    while sand_y < most_max_y {
        // println!("{} {} {}", most_max_y, sand_y, sand_x);
        // sand fall straight down
        if grid[sand_y + 1][sand_x] == '.' {
            // println!("fall down");
            sand_y += 1;
            continue;
        }
        // sand fall left
        if grid[sand_y + 1][sand_x - 1] == '.' {
            // println!("fall left");
            sand_x -= 1;
            sand_y += 1;
            continue;
        }

        // sand fall right
        if grid[sand_y + 1][sand_x + 1] == '.' {
            // println!("fall right");
            sand_x += 1;
            sand_y += 1;
            continue;
        }

        // sand can't fall down, left, or right
        // println!("can't fall");
        grid[sand_y][sand_x] = 'o';
        if check_blocked {
            if sand_y == orig_sand_y && sand_x == orig_sand_x {
                return true;
            }
        }
        return false;
    }

    true
}

fn part1(input: &str) -> String {
    let mut grid = vec![vec!['.'; 200]; 200];

    let mut most_max_y = 0;
    for line in input.lines() {
        let mut path = line.split(" -> ").map(|s| s.split_once(",").unwrap()).collect::<Vec<_>>();
        for i in 0..path.len() - 1 {
            let (x1, y1) = path[i];
            let (x2, y2) = path[i + 1];
            let min_x = min(x1.parse::<usize>().unwrap(), x2.parse::<usize>().unwrap());
            let max_x = max(x1.parse::<usize>().unwrap(), x2.parse::<usize>().unwrap());
            let min_y = min(y1.parse::<usize>().unwrap(), y2.parse::<usize>().unwrap());
            let max_y = max(y1.parse::<usize>().unwrap(), y2.parse::<usize>().unwrap());

            most_max_y = max(most_max_y, max_y);

            for x in min_x..=max_x {
                for y in min_y..=max_y {
                    grid[y][x-DIFF_X] = '#';
                }
            }
        }
    }
    // print_grid(&grid);

    // rock fall
    let sand_x = 500 - DIFF_X;
    let sand_y = 0;
    let mut count = 0;
    loop {
        // print_grid(&grid);
        if simulate_sand(&mut grid, sand_y, sand_x, most_max_y, false) {
            break;
        }
        count += 1;
    }
    // print_grid(&grid);
    count.to_string()
}

fn part2(input: &str) -> String {
    let mut grid = vec![vec!['.'; 1000]; 200];

    let mut most_max_y = 0;
    for line in input.lines() {
        let mut path = line.split(" -> ").map(|s| s.split_once(",").unwrap()).collect::<Vec<_>>();
        for i in 0..path.len() - 1 {
            let (x1, y1) = path[i];
            let (x2, y2) = path[i + 1];
            let min_x = min(x1.parse::<usize>().unwrap(), x2.parse::<usize>().unwrap());
            let max_x = max(x1.parse::<usize>().unwrap(), x2.parse::<usize>().unwrap());
            let min_y = min(y1.parse::<usize>().unwrap(), y2.parse::<usize>().unwrap());
            let max_y = max(y1.parse::<usize>().unwrap(), y2.parse::<usize>().unwrap());

            most_max_y = max(most_max_y, max_y);

            for x in min_x..=max_x {
                for y in min_y..=max_y {
                    grid[y][x] = '#';
                }
            }
        }
    }
    for x in 0..grid[0].len() {
        grid[most_max_y + 2][x] = '#';
    }

    // print_grid(&grid);

    // rock fall
    let mut count = 0;
    let sand_x = 500;
    let sand_y = 0;
    loop {
        // print_grid(&grid);
        count += 1;
        if simulate_sand(&mut grid, sand_y, sand_x, most_max_y + 2, true) {
            break;
        }
    }
    // print_grid(&grid);
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

    const DAY_NUM: &str = "14";

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