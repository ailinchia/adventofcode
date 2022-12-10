use std::{io};
use std::cmp::max;
use std::io::Read;

fn parse_input(input: &str) -> Vec<Vec<u32>> {
    input.lines().map(|line| {
        line.chars().map(|c| c.to_digit(10).unwrap()).collect::<Vec<_>>()
    }).collect::<Vec<_>>()
}

fn part1(input: &str) -> String {
    let trees = parse_input(&input);

    let mut count = 0;
    for y in 0..trees.len() {
        for x in 0..trees[y].len() {
            if x == 0 || x == trees[y].len() - 1 || y == 0 || y == trees.len() - 1 {
                count += 1;
                continue;
            }

            let mut visible = true;

            // check top
            for i in 0..y {
                if trees[i][x] >= trees[y][x] {
                    visible = false;
                    break;
                }
            }
            if visible {
                count += 1;
                continue;
            }

            // check bottom
            visible = true;
            for i in y + 1..trees.len() {
                if trees[i][x] >= trees[y][x] {
                    visible = false;
                    break;
                }
            }
            if visible {
                count += 1;
                continue;
            }

            // check left
            visible = true;
            for i in 0..x {
                if trees[y][i] >= trees[y][x] {
                    visible = false;
                    break;
                }
            }
            if visible {
                count += 1;
                continue;
            }

            // check right
            visible = true;
            for i in x + 1..trees[y].len() {
                if trees[y][i] >= trees[y][x] {
                    visible = false;
                    break;
                }
            }
            if visible {
                count += 1;
                continue;
            }
        }
    }
    count.to_string()
}

fn part2(input: &str) -> String {
    let trees = parse_input(&input);

    let mut max_score = 0;
    for y in 0..trees.len() {
        for x in 0..trees[y].len() {
            if x == 0 || x == trees[y].len() - 1 || y == 0 || y == trees.len() - 1 {
                continue;
            }

            let mut score = 1;

            // check top
            let mut count = 0;
            for i in (0..y).rev() {
                count += 1;
                if trees[i][x] >= trees[y][x] {
                    break
                }
            }
            score *= count;

            // check bottom
            count = 0;
            for i in y + 1..trees.len() {
                count += 1;
                if trees[i][x] >= trees[y][x] {
                    break
                }
            }
            score *= count;

            // check left
            count = 0;
            for i in (0..x).rev() {
                count += 1;
                if trees[y][i] >= trees[y][x] {
                    break
                }
            }
            score *= count;

            // check right
            count = 0;
            for i in x + 1..trees[y].len() {
                count += 1;
                if trees[y][i] >= trees[y][x] {
                    break
                }
            }
            score *= count;

            max_score = max(score, max_score);
        }
    }
    max_score.to_string()
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

    const DAY_NUM: &str = "08";

    #[test]
    fn test_input() {
        let filename = format!("day{}/input", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "1695");
        adventofcode::test_part(filename.as_str(), part2, "287040");
    }

    #[test]
    fn test_inputa() {
        let filename = format!("day{}/inputa", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "21");
        adventofcode::test_part(filename.as_str(), part2, "8");
    }
}