use std::{io};
use std::collections::HashMap;
use std::io::Read;
use std::ops::Deref;

#[derive(Debug)]
#[derive(Clone)]
struct Monkey {
    monkey1: String,
    monkey2: String,
    op: char,
    number: i64,
}

fn get_value(monkeys: &HashMap<&str, Monkey>, name: &str) -> i64 {
    let monkey = monkeys.get(name).unwrap();
    if monkey.op == '\0' {
        return monkey.number;
    } else {
        let v1 = get_value(monkeys, &monkey.monkey1);
        let v2 = get_value(monkeys, &monkey.monkey2);
        match monkey.op {
            '+' => v1 + v2,
            '-' => v1 - v2,
            '*' => v1 * v2,
            '/' => v1 / v2,
            _ => unreachable!("Unknown op {}", monkey.op),
        }
    }
}

fn part1(input: &str) -> String {
    let mut monkeys = HashMap::<&str, Monkey>::new();

    for line in input.lines() {
        let (name, job) = line.split_once(":").unwrap();
        // println!("{}: {}", monkey, job);
        let tokens = job.trim().split(" ").collect::<Vec<_>>();
        if tokens.len() == 1 {
            monkeys.insert(name, Monkey {
                monkey1: "".to_string(),
                monkey2: "".to_string(),
                op: '\0',
                number: tokens[0].parse::<i64>().unwrap(),
            });
        } else {
            monkeys.insert(name, Monkey {
                monkey1: tokens[0].to_string(),
                monkey2: tokens[2].to_string(),
                op: tokens[1].chars().next().unwrap(),
                number: 0,
            });
        }

        // println!("{:?}", monkeys[monkey]);
    }

    get_value(&monkeys, "root").to_string()
}

fn part2(input: &str) -> String {
    let mut monkeys = HashMap::<&str, Monkey>::new();

    for line in input.lines() {
        let (name, job) = line.split_once(":").unwrap();
        // println!("{}: {}", monkey, job);
        let tokens = job.trim().split(" ").collect::<Vec<_>>();
        if tokens.len() == 1 {
            monkeys.insert(name, Monkey {
                monkey1: "".to_string(),
                monkey2: "".to_string(),
                op: '\0',
                number: tokens[0].parse::<i64>().unwrap(),
            });
        } else {
            monkeys.insert(name, Monkey {
                monkey1: tokens[0].to_string(),
                monkey2: tokens[2].to_string(),
                op: tokens[1].chars().next().unwrap(),
                number: 0,
            });
        }

        // println!("{:?}", monkeys[monkey]);
    }

    let root = monkeys.get("root").unwrap();
    let monkey1 = root.monkey1.clone();
    let monkey2 = root.monkey2.clone();

    let mut i = 3099532650600;
    loop {
        monkeys.get_mut("humn").unwrap().number = i;
        let m1 = get_value(&monkeys, monkey1.as_str());
        let m2 = get_value(&monkeys, monkey2.as_str());
        if m1 == m2 {
            break;
        }
        i += 1;

        // println!("{} {} {} {}", i, m1, m2, m2 - m1);
    }
    i.to_string()
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

    const DAY_NUM: &str = "21";

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