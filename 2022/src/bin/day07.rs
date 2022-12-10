use std::{io};
use std::cell::RefCell;
use std::collections::LinkedList;
use std::io::Read;
use std::rc::Rc;

#[derive(Debug)]
struct Node {
    parent: Option<Rc<Node>>,
    is_dir: bool,
    name: String,
    size: RefCell<u64>,
    children: RefCell<LinkedList<Rc<Node>>>,
}

fn print_node(node: &Rc<Node>, indent: usize) {
    let mut s = String::new();
    for _ in 0..indent {
        s.push_str("  ");
    }
    s.push_str(&node.name);
    println!("{} {} {}", s, node.size.borrow(), node.is_dir);
    for child in node.children.borrow().iter() {
        print_node(child, indent + 1);
    }
}

fn calculate_size(node: Rc<Node>) -> u64 {
    if !node.is_dir {
        return node.size.borrow().clone();
    }

    let mut size = 0;
    for child in node.children.borrow().iter() {
        size += calculate_size(child.clone());
    }

    node.size.replace(size);
    return size;
}

fn get_total_size(node: &Rc<Node>, total_size: &mut u64) -> u64 {
    if node.is_dir {
        let current_size = node.size.clone().take();
        if current_size <= 100000 {
            *total_size += current_size;
        }

        for child in node.children.borrow().iter() {
            get_total_size(child, total_size);
        }
    }
    *total_size
}

fn parse_input(input: &str) -> Rc<Node> {
    let root = Rc::new(Node {
        parent: None,
        is_dir: true,
        name: "/".to_string(),
        size: RefCell::new(0),
        children: RefCell::new(LinkedList::new()),
    });

    let mut current = root.clone();
    for line in input.lines() {
        let mut tokens = line.split_ascii_whitespace();
        let first = tokens.next().unwrap();
        match first {
            "$" => {
                let second = tokens.next().unwrap();
                match second {
                    "cd" => {
                        let third = tokens.next().unwrap();
                        match third {
                            "/" => {
                                // $ cd /
                            }
                            ".." => {
                                // $ cd ..
                                current = current.parent.as_ref().unwrap().clone();
                            }
                            _ => {
                                // $ cd <dir>
                                for child in current.children.clone().take().iter() {
                                    if child.name == third {
                                        current = child.clone();
                                        break;
                                    }
                                }
                            }
                        }
                    }
                    _ => {
                        // $ ls
                    }
                }
            }
            _ => {
                let mut size = 0;
                if first == "dir" {
                    // dir <dir>
                } else {
                    // <size> <file>
                    size = first.parse::<u64>().unwrap();
                }
                let node = Node {
                    parent: Some(current.clone()),
                    is_dir: first == "dir",
                    name: tokens.next().unwrap().to_string(),
                    size: RefCell::new(size),
                    children: RefCell::new(LinkedList::new()),
                };

                current.children.borrow_mut().push_back(Rc::new(node));
            }
        }
    }
    calculate_size(root.clone());

    root
}

fn part1(input: &str) -> String {
    let root = parse_input(input);
    let mut total_size = 0;
    get_total_size(&root, &mut total_size).to_string()
}

fn get_min_size(node: &Rc<Node>, min_size: u64, current_min_size: &mut u64) -> u64 {
    if node.is_dir {
        let current_size = node.size.clone().take();
        if current_size >= min_size && current_size < *current_min_size {
            *current_min_size = current_size;
        }

        for child in node.children.borrow().iter() {
            get_min_size(child, min_size, current_min_size);
        }
    }
    *current_min_size
}

fn part2(input: &str) -> String {
    let root = parse_input(input);
    let total_used = root.size.clone().take();
    let needed = 30000000 - (70000000 - total_used);
    let mut current_min_size = u64::MAX;
    get_min_size(&root, needed, &mut current_min_size).to_string()
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

    const DAY_NUM: &str = "07";

    #[test]
    fn test_input() {
        let filename = format!("day{}/input", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "1648397");
        adventofcode::test_part(filename.as_str(), part2, "1815525");
    }

    #[test]
    fn test_inputa() {
        let filename = format!("day{}/inputa", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "95437");
        adventofcode::test_part(filename.as_str(), part2, "24933642");
    }
}