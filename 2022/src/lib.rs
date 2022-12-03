use std::fs;

type PartFn = fn(&str) -> String;

pub fn test_part(filename: &str, part_fn: PartFn, expected: &str) {
    let input = fs::read_to_string(filename).unwrap();
    assert_eq!(part_fn(&input), expected);
}