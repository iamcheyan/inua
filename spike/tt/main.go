package main

import (
	"fmt"
	"github.com/lyricat/inua/internal/appmenu"
	"os"
	"strconv"
)

func main() {
	pid, _ := strconv.Atoi(os.Args[1])
	a := appmenu.NewA11y()
	e, err := a.Menu(pid)
	fmt.Println("a11y err:", err, "count:", len(e))
	for _, x := range e {
		fmt.Printf("  %q children=%d action=%+v\n", x.Label, len(x.Children), x.Action)
	}
}
