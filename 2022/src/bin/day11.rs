use std::io;
use std::borrow::{Borrow, BorrowMut};
use std::io::Read;

const J_MAX: i32 = 20;
const J_PRINT: i32 = 4;

fn part1(input: &str) -> String {
    #[derive(Debug)]
    #[derive(Clone)]
    struct Item {
        original: u64,
        value: u64,
    }

    #[derive(Debug)]
    struct Monkey {
        items: Vec<Item>,
        operation: Vec<String>,
        test: u64,
        action_true: usize,
        action_false: usize,
        inspected: u64,
    }

    let mut monkeys = Vec::new();
    let mut lines = input.lines();
    loop {
        let inputs = lines.borrow_mut().take(7).map(|line| line.trim().parse::<String>().unwrap()).collect::<Vec<_>>();
        let monkey = Monkey {
            items: inputs[1].split_once(": ").unwrap().1.split(", ").map(|s| {
                let original = s.parse::<u64>().unwrap();
                Item {
                    original,
                    value: original,
                }
            }).collect::<Vec<_>>(),
            operation: inputs[2].split_once(": ").unwrap().1.split_once(" = ").unwrap().1.split_ascii_whitespace().map(|token| token.to_string()).collect::<Vec<_>>(),
            test: inputs[3].split_ascii_whitespace().last().unwrap().parse::<u64>().unwrap(),
            action_true: inputs[4].split_ascii_whitespace().last().unwrap().parse::<usize>().unwrap(),
            action_false: inputs[5].split_ascii_whitespace().last().unwrap().parse::<usize>().unwrap(),
            inspected: 0,
        };
        monkeys.push(monkey);

        if inputs.len() < 7 {
            break;
        }
    }

    for j in 0..J_MAX {
        // if j == J_PRINT {
        //     for i in 0..monkeys.len() {
        //         println!("{}: Monkey {}: {:?} total={}", j, i, monkeys[i].borrow().items.clone(), monkeys[i].borrow_mut().inspected);
        //     }
        // }
        for i in 0..monkeys.len() {
            for item in monkeys[i].items.clone() {
                let first = item.value;
                let second = if monkeys[i].operation[2] == "old" { item.value } else { monkeys[i].operation[2].parse::<u64>().unwrap() };
                let mut new = match monkeys[i].operation[1].as_str() {
                    "+" => {
                        first + second
                    }
                    "*" => {
                        first * second
                    }
                    _ => {
                        unreachable!("Unknown operation");
                    }
                };

                new = new / 3;

                let dest = if new % monkeys[i].test == 0 { monkeys[i].action_true } else { monkeys[i].action_false };
                // if j == J_PRINT {
                //     println!("{}: Monkey {}: item={:?} original={} test={} op={:?} dest={}", j, i, new.clone(), item.original, monkeys[i].test, monkeys[i].operation, dest);
                // }
                monkeys[dest].borrow_mut().items.push(Item{original: item.original, value: new.clone()});
            }
            monkeys[i].borrow_mut().inspected += monkeys[i].borrow().items.len() as u64;
            monkeys[i].borrow_mut().items.clear();
        }
        // println!();
    }

    let mut inspected = Vec::new();
    for i in 0..monkeys.len() {
        inspected.push(monkeys[i].inspected);
    }
    inspected.sort();
    inspected.reverse();
    (inspected[0] * inspected[1]).to_string()
}

// 13393620680 too low
fn part2(input: &str) -> String {
    #[derive(Debug)]
    #[derive(Clone)]
    struct Item {
        original: u64,
        value: u64,
    }

    #[derive(Debug)]
    struct Monkey {
        items: Vec<Item>,
        operation: Vec<String>,
        test: u64,
        action_true: usize,
        action_false: usize,
        inspected: u64,
    }

    let mut monkeys = Vec::new();
    let mut lines = input.lines();
    let mut divisor = 1;
    loop {
        let inputs = lines.borrow_mut().take(7).map(|line| line.trim().parse::<String>().unwrap()).collect::<Vec<_>>();
        let monkey = Monkey {
            items: inputs[1].split_once(": ").unwrap().1.split(", ").map(|s| {
                let original = s.parse::<u64>().unwrap();
                Item {
                    original,
                    value: original,
                }
            }).collect::<Vec<_>>(),
            operation: inputs[2].split_once(": ").unwrap().1.split_once(" = ").unwrap().1.split_ascii_whitespace().map(|token| token.to_string()).collect::<Vec<_>>(),
            test: inputs[3].split_ascii_whitespace().last().unwrap().parse::<u64>().unwrap(),
            action_true: inputs[4].split_ascii_whitespace().last().unwrap().parse::<usize>().unwrap(),
            action_false: inputs[5].split_ascii_whitespace().last().unwrap().parse::<usize>().unwrap(),
            inspected: 0,
        };
        divisor *= monkey.test;
        monkeys.push(monkey);

        if inputs.len() < 7 {
            break;
        }
    }

    for j in 0..10000 {
        // if j == J_PRINT {
        //     for i in 0..monkeys.len() {
        //         println!("{}: Monkey {}: {:?} total={}", j, i, monkeys[i].borrow().items.clone(), monkeys[i].borrow_mut().inspected);
        //     }
        // }
        for i in 0..monkeys.len() {
            for item in monkeys[i].items.clone() {
                let first = item.value;
                let second = if monkeys[i].operation[2] == "old" { item.value } else { monkeys[i].operation[2].parse::<u64>().unwrap() };
                let mut new = match monkeys[i].operation[1].as_str() {
                    "+" => {
                        first + second
                    }
                    "*" => {
                        first * second
                    }
                    _ => {
                        unreachable!("Unknown operation");
                    }
                };

                new = new % divisor;

                let dest = if new % monkeys[i].test == 0 { monkeys[i].action_true } else { monkeys[i].action_false };
                // if j == J_PRINT {
                //     println!("{}: Monkey {}: item={:?} original={} test={} op={:?} dest={}", j, i, new.clone(), item.original, monkeys[i].test, monkeys[i].operation, dest);
                // }
                monkeys[dest].borrow_mut().items.push(Item{original: item.original, value: new.clone()});
            }
            monkeys[i].borrow_mut().inspected += monkeys[i].borrow().items.len() as u64;
            monkeys[i].borrow_mut().items.clear();
        }
        // println!();
    }

    let mut inspected = Vec::new();
    for i in 0..monkeys.len() {
        inspected.push(monkeys[i].inspected);
    }
    inspected.sort();
    inspected.reverse();
    (inspected[0] * inspected[1]).to_string()
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

    const DAY_NUM: &str = "11";

    #[test]
    fn test_input() {
        let filename = format!("day{}/input", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "57838");
        adventofcode::test_part(filename.as_str(), part2, "");
    }

    #[test]
    fn test_inputa() {
        let filename = format!("day{}/inputa", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "10605");
        adventofcode::test_part(filename.as_str(), part2, "2713310158");
    }
}