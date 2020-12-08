package main

import (
	"bufio"
	"fmt"
	"os"
)

type operation string

const (
	opAcc = "acc"
	opJmp = "jmp"
	opNop = "nop"
)

type instruction struct {
	op operation
	arg int
}

func execute(ins instruction, pos *int, acc *int) {
	switch ins.op {
	case opAcc:
		*acc += ins.arg
		*pos += 1
		break
	case opJmp:
		*pos += ins.arg
		break
	case opNop:
		*pos += 1
		break
	}
}

func validate(instructions []instruction) (bool, int) {
	visited := make(map[int]bool)

	pos := 0
	acc := 0
	for {
		_, ok := visited[pos]
		if ok {
			return false, acc
		}
		visited[pos] = true

		execute(instructions[pos], &pos, &acc)

		if pos >= len(instructions) {
			return true, acc
		}
	}
}

func part1(instructions []instruction) {
	_, acc := validate(instructions)
	fmt.Println(acc)
}

func part2(instructions []instruction) {
	for i := 0; i < len(instructions); i++ {
		instruction := instructions[i]
		oriInstruction := instruction

		// fix instruction
		switch instruction.op {
		case opAcc:
			continue
		case opJmp:
			instruction.op = opNop
			break
		case opNop:
			instruction.op = opJmp
			break
		}
		instructions[i] = instruction

		if valid, acc := validate(instructions); valid {
			fmt.Println(acc)
			break
		}

		// revert instruction
		instructions[i] = oriInstruction
	}
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var instructions []instruction
	for scanner.Scan() {
		var ins instruction
		n, err := fmt.Sscanf(scanner.Text(), "%s %d", &ins.op, &ins.arg)
		if n != 2 || err != nil {
			fmt.Printf("Invalid input. n=%d err=%v\n", n, err)
		}

		instructions = append(instructions, ins)
	}

	part1(instructions)
	part2(instructions)
}
