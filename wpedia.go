package main

import (
	"encoding/json"
	"fmt"
	"net/http"
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

func getURL(url string) (*http.Response, error) {
	req := http.NewRequest("GET", url, nil)
	return http.Do(req)
}

func parseSubcats(text string) []int {
	var d interface{}
	json.Unmarshal([]byte(text), &d)

	query := d.(map[string]interface{})["query"]
	members := query.(map[string]interface{})["categorymembers"].([]interface{})
	
	pageids := make([]int, len(members))

	for i, page := range members {
		pagemap := page.(map[string]interface{})
		pageid := pagemap["pageid"].(float64)
		pageids[i] = int(pageid)
	}

	return pageids
}