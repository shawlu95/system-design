## Analytics

- Athena (stored in S3): upload raw data, serverless, SQL, pay for queries
- Elastic Map Reduce (EMR):
  - fully managed Hadoop, transform and cleanse data
  - HBase data store on clusters or S3
  - **EMR Studio** IDE to create data science app
- OpenSearch (previously ElasticSearch)
  - real-time distrubuted search and analytics engine
  - analyze data from S3, Kinesis Stream, DynamoDB Stream, CloudWatch Logs, CloudTrail Logs
- QuickSight BI
- Amazon Machine Learning
- Lambda
- real time: Kinesis
- storage: S3, Redshift (more expensive, pay for Redshift cluster, exabytes), Dynamo, RDS
- serverless ETL: **AWS Glue** (triggered by Lambda)
- QuickSight: BI tools to visualize data, 1/10 of traditional BI software cost

### Kinesis streaming

- Data Stream: capture, process, store data stream
- Data Firehose: load data streams into AWS data store, export output to Redshift
- Data Analytics: using SQL or Flink
- Vidro Stream: capture, process, store video stream
