package main

import (
	"fmt"
	"regexp"
)

type infoBox struct {
	name string
	data map[string]string
}

func (i infoBox) String() string {
	s := i.name
	for key, val := range i.data {
		s += fmt.Sprintf("\n  %s: %s", key, val)
	}
	return s
}

func parseInfo(text string) *infoBox {
	reInfo := regexp.MustCompile(`(?:^|\n){{Infobox *([^\n]*)(\n *|[^\n]*)*\n}}`)
	match := reInfo.FindStringSubmatch(text)
	if len(match) == 0 { return nil }
	name := match[1]

	// get lines in the infobox
	infoText := match[0]
	reLines := regexp.MustCompile(`(?m)^ *\|[^\n]*$`)
	lines := reLines.FindAllString(infoText, -1)
	
	data := make(map[string]string)
	reLine := regexp.MustCompile(`\| ([^ ]+) *= *(.*)`)
	for _, line := range lines {
		m := reLine.FindStringSubmatch(line)
		data[m[1]] = m[2]
	}

	return &infoBox { name, data } // infobox name as first element
}