package main

import (
	"log"
	"github.com/bitly/go-nsq"
	"bufio"
	"encoding/csv"
	"io"
	"os"
	"time"
)

type Flow struct {
	flow string	`json:"flow"`
}

func main() {
	csvFile, _ := os.Open("test.csv")
	reader := csv.NewReader(bufio.NewReader(csvFile))

	var flows []Flow
	for {
		line, error := reader.Read()
		if error == io.EOF {
			break
		} else if error != nil {
			log.Fatal(error)
		}

		flows = append(flows, Flow {
			flow: line[1],
			})
	}

	// Connect to NSQ
	config := nsq.NewConfig()
	w, _ := nsq.NewProducer("127.0.0.1:4150", config)


	// Send the data
	for i:=0; i < len(flows); i++ {
		var message string = flows[i].flow
		err := w.Publish("nsq-spark-in", []byte(message))
		if err != nil {
			log.Panic("Could not connect")
		}	
		time.Sleep(1000*time.Millisecond)
	}
	w.Stop()
}