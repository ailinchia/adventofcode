use std::{io};
use std::io::Read;

fn part1(input: &str) -> String {
    input.lines().fold(0, |acc, line| {
        let mut chars = line.chars().map(|c| c as i32).filter(|c| *c != ' ' as i32);
        let op_move = chars.next().unwrap() - 'A' as i32;
        let my_move = chars.next().unwrap() - 'X' as i32;
        acc + match op_move - my_move {
            -1 | 2 => 6,    // win
            0 => 3,         // tie
            1 | -2 => 0,    // lose
            _ => unreachable!("invalid move"),
        } + my_move + 1
    }).to_string()
}

fn part2(input: &str) -> String {
    input.lines().fold(0, |acc, line| {
        let mut chars = line.chars().map(|x| x as i32).filter(|c| *c != ' ' as i32);
        let op_move = chars.next().unwrap() - 'A' as i32;
        let result = chars.next().unwrap() - 'X' as i32;
        let my_move = match result {
            // rock 0, paper 1, scissors 2
            // lose 0, draw 1, win 2
            0 => if op_move == 0 { 2 } else { op_move - 1 },
            1 => op_move,
            2 => (op_move + 1) % 3,
            _ => unreachable!("invalid result"),
        };
        acc + (result * 3) + my_move + 1
    }).to_string()
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

    const DAY_NUM: &str = "02";

    #[test]
    fn test_input() {
        let filename = format!("day{}/input", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "17189");
        adventofcode::test_part(filename.as_str(), part2, "13490");
    }

    #[test]
    fn test_inputa() {
        let filename = format!("day{}/inputa", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "15");
        adventofcode::test_part(filename.as_str(), part2, "12");
    }
}
