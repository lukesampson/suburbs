package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
)

func main() {
	res, _ := getURL("http://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Suburbs_in_Australia&cmlimit=500")
	fmt.Println(res)
	//text, _ := fixture("subcats.json")
	//ids := subcatsString(text)
	//fmt.Println(ids)
}

func fixture(name string) (string, error) {
	bindir := filepath.Dir(os.Args[0])
	dir := filepath.Join(bindir, "fixtures")
	path := filepath.Join(dir, name)

	bytes, err := ioutil.ReadFile(path)
	if err != nil { return "", err }

	return string(bytes), nil
}