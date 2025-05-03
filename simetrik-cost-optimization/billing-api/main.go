package main

import (
    "context"
    "database/sql"
    "fmt"
    "log"
    "time"

    _ "github.com/lib/pq"
    "github.com/aws/aws-sdk-go-v2/config"
    "github.com/aws/aws-sdk-go-v2/service/costexplorer"
)

func main() {
    cfg, err := config.LoadDefaultConfig(context.TODO())
    if err != nil {
        log.Fatalf("unable to load SDK config, %v", err)
    }

    ce := costexplorer.NewFromConfig(cfg)

    end := time.Now()
    start := end.AddDate(0, -1, 0)
    res, err := ce.GetCostAndUsage(context.TODO(), &costexplorer.GetCostAndUsageInput{
        TimePeriod: &costexplorer.DateInterval{
            Start: &start.Format("2006-01-02"),
            End:   &end.Format("2006-01-02"),
        },
        Granularity: "DAILY",
        Metrics:     []string{"UnblendedCost"},
    })
    if err != nil {
        log.Fatalf("could not get cost: %v", err)
    }

    db, err := sql.Open("postgres", "host=localhost port=5432 user=user password=pass dbname=billing sslmode=disable")
    if err != nil {
        log.Fatalf("DB connection error: %v", err)
    }
    defer db.Close()

    for _, r := range res.ResultsByTime {
        date := *r.TimePeriod.Start
        cost := *r.Total["UnblendedCost"].Amount
        _, err := db.Exec(`INSERT INTO aws_billing (date, cost) VALUES ($1, $2)`, date, cost)
        if err != nil {
            log.Printf("insert error on %s: %v", date, err)
        }
    }

    fmt.Println("Data ingested successfully")
}
