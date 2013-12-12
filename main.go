package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
)

func main() {
	text, _ := fixture("cannon_hill.txt")
	info := parseInfo(text)
	fmt.Println(info)
}

func fixture(name string) (string, error) {
	bindir := filepath.Dir(os.Args[0])
	dir := filepath.Join(bindir, "fixtures")
	path := filepath.Join(dir, name)

	bytes, err := ioutil.ReadFile(path)
	if err != nil { return "", err }

	return string(bytes), nil
}