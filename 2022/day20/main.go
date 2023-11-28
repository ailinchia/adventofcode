package main

import (
	"bufio"
	"container/ring"
	"fmt"
	"os"
	"strconv"
)

func printBuffer(cups *ring.Ring) {
	cups.Do(func(p interface{}) {
		fmt.Print(p.(int64), ", ")
	})
	fmt.Println("")
}

type key struct {
	index int
	value int
}

func part1(e []int) {
	values := map[key]*ring.Ring{}

	r := ring.New(len(e))
	for idx, entry := range e {
		values[key{idx, entry}] = r
		r.Value = entry
		r = r.Next()
	}

	//printBuffer(buffer)
	for idx, entry := range e {
		buffer := values[key{idx, entry}].Prev()
		current := buffer.Unlink(1)
		buffer.Move(entry % buffer.Len()).Link(current)
	}
	for r.Value.(int) != 0 {
		r = r.Next()
	}

	sum := r.Move(1000).Value.(int) + r.Move(2000).Value.(int) + r.Move(3000).Value.(int)
	fmt.Println(sum)
}

func part2(e []int) {
	values := map[key]*ring.Ring{}

	r := ring.New(len(e))
	for idx, entry := range e {
		values[key{idx, entry}] = r
		r.Value = entry
		r = r.Next()
	}

	for i := 0; i < 10; i++ {
		for idx, entry := range e {
			buffer := values[key{idx, entry}].Prev()
			current := buffer.Unlink(1)
			buffer.Move(entry % buffer.Len()).Link(current)
		}
	}
	for r.Value.(int) != 0 {
		r = r.Next()
	}
	sum := r.Move(1000).Value.(int) + r.Move(2000).Value.(int) + r.Move(3000).Value.(int)
	fmt.Println(sum)
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var entries []string
	for scanner.Scan() {
		line := scanner.Text()
		entries = append(entries, line)
	}

	var e1 []int
	var e2 []int

	for _, entry := range entries {
		n, _ := strconv.ParseInt(entry, 10, 64)
		e1 = append(e1, int(n))
		e2 = append(e2, int(n*811589153))
	}

	part1(e1)
	part2(e2)
}
