## AWS Alphabet Soup

- Region: contains multiple availabiity zones (AZ)
- local zones: close to large population, extension of region
- edge location: over 100, used by **AWS CloudFront** which cache popular content, low-latency distribute, DDOS protection
- **AWS WaveLength** use compute and storage ervices embedded within communication service provider (CSP) data centers at the edge of the 5G network (live-broadcast, gaming)
- **AWS Groundstation** command, control, download from satellites
- **Project Kuiper** low-earch-orbit satellites, low latency, high speed access to AWS cloud
- IAAS: basic building blocks for cloud IT infra (VPC, EC2, EBS)
- PAAS: AWS manages underlying infra (RDS, EMR, ElasticSearch)
- SAAS: complete products ran in browser (email, Office365)
- FAAS (serverless): function-as-a-service (S3, Lambda, DynamoDB, SNS)

### Storage

- S3: theoretically unlimited
- glacier: cheap to store long time archives, can set archive rule
- Elastic Block Store: low-latency block-device, attached to EC2 (attaching hard drive)
- Elastic File System: network-attached storage. Multiple servers access same data source (like a network-attached storage device)
- **AWS Storage Gateway** hybrid storage between on-premise & cloud
  - frequent data stored on-premise. infrequent data on cloud
  - manages syncing between on-premise storage and S3 bucket
- Snowball: migrate large amount of data from on-premise to cloud
  - download petabytes of data to Snowball device and mail it to AWS by courier
  - Amazon will upload data to S3
- virtual private cloud: an "impenetrable fortress" against attack. Services can be launched in VPC
  - S3, Glaciers, EFS are not in VPC
  - **VPC endpoint** controls traffic in & out of VPC

### Networking

- AWS Elastic Load Balancer: distirbute across multiple EC2 and AZ
- Auto Scaling Group, if health check fails
- CloudFront: content delivery
- Virtual Private Cloud: own personal private space
- AWS Direct Connect: highspeed private connection from on-premises hardware to AWS cloud if standard Internet connection is not enough
- **Route 53** domain name service
- **API Gateways**: hundreds of thousands of concurrent calls, serverless
- example pathway: API call -> Route 53 -> CloudFront -> Load Balancer -> EC2

### Management Tools

- **CloudFormation**: define infra in text file
- **AWS Service Catalog**:
- **AWS Cloud Watch**: trigger scaling, monitor resource
- **AWS System Manager**: view operational data from multiple services, automate tasks
- **CloudTrail** monitor activities of AWS accounts (employee activities)
- **AWS Config**: simplifies compliance, security analysis
- **OpsWork**:
- **Trusted Advisor** better achieve security and performance

### Application Services

- **SQS Queue** decouple requests from server
- **CloudWatch Alarm** monitors queue length and trigger auto-scaling, send SNS notification
- reduce instances if queue empty most of the time

### Customer Engagement Services

- **Amazon Connect** define customer interaction
- **Amazon Pinpoint** send SNS message, email to customer (e.g. marketing campaign)
- **Simple Email Service** send email in bulk

### Analytics

- **EMR**: integrate with Hadoop, Spark, Hive, Presto, Flink; data store S3, Dynamo
- **Atheta**: SQL access S3 bucket data
- **FinSpace**: petabyte scale, for financial analysis
- **Kinesis**: real-time streaming data
- **QuickSight**: simialr to Tableau
- **CloudSearch**: fully managed search engine service
- **Amazon Open Search**: previously Elasticsearch

### Machine Learning

- **DeepLens**: deep learning enabled video camera
- **SageMaker**: flapship machine learning product, build, train, deploy on AWS cloud and serve backend
- **Rekognition**: deep learning analysis on video, images
- **Amazon Lex**: build conversational checkbox (customer support)
- **Amazon Polly**: natural-sounding text-to-speech
- **Comprehend** analyze text, relationship
- **Translate**
- **Transcribe**: S3 audio to text

### Security, Identity, Compliance

- **AWS Artifact** provides access to AWS security and compliance documentation
- **AWS Certificate Manager** issues SSL certificate for HTTPS communication, integrate with Route53, CloudFront, free to use
- **Amazon Cloud Directory** can have hierarchy of data in multiple dimension
- **AWS Directory Service**
- **CloudHSM** hard-ware security module
- **Cognito** sign-in, sign-out for mobile app, can integrate with Google
  - continuously monitor and record changes
  - assess, audit, evaluate the config of AWS resources
  - integrated with **AWS Organization**
- **IAM** manages user access to AWS services and resources using _users_ and _groups_
  - takes some time to propagate globally, eventually consistent
  - credential could be 1) password or 2) access key, max 2 per user
  - users can be added to multiple groups, each with different roles
  - group cannot contain groups
  - by default, IAM user can access nothing
  - max 5000 IAM users per account, need more? Federated users!
- **resource-based policies** availablt to S3, Glacier, SBS, SQS, Key Management Service
  - attached to resources,not users (IAM is attached to user group or role)
- **AWS Organization** provide policy based management for multiple AWS accounts
  - large company manages multiple AWS accounts
  - **Service Control Policy** can whitelisting/blacklisting services in an Organizational Unit, even if IAM user/group policy allows it
- **Amazon Inspector** identifies vulnerability in AWS account
- **Key Management Services** create/control encryption keys for encrypted data; uses hardware security module to secure keys (for S3, Redshift, EBS etc)
- **AWS Shield** auto-enabled, DDOS protection
- **Web Aplication Firewall** protect against common attack, SQL inject, cross site scripting
- **AWS Artifact** compliance related information

### Shared Responsibility Model

- AWS is responsible for low-level architecture (software, hardware, infra)
- customers are responsible for what's put into AWS (e.g. server encryption, sensitive data)
- Create users, groups, roles
- **Identity Federation** verify user via 3rd party service (e.g. Google)
- AWS takes more responsibility in managed services

### AWS Developer Tools

- **Cloud9**
- **CodeStar** managed CI, JIRA
- **X-Ray**
- **CodeCommit**
- **CodePipeline**: CI/CD
- **CodeBuild**
- **CodeDeploy**

### AWS Media Services

- Elemental Media Convert
- Elemental Media Package
- Elemental Media Tailor
- Elemental Media Live
- Elemental Media Store
- Kinesis Video Stream

### AWS Mobile Services

- AWS Mobile Hub: one-place, cloud config file
- AWS Device Farm: testing app against large collection of physical devices
- AWS AppSync: **GraphQL** backend for mobile and web app

### AWS Migration Services

- AWS Application Discovery Service: gather information form on-premise data center to help plan migration to AWS
- AWS Database Migration Service: e.g. Oracle -> Aurora
- AWS Server Migration Service: migrate on-premise workflow, minimize cost, down time
- AWS Snowball: petabyte storage device to store on-premise data and mail to AWS by courier

### Business Productivity & App Streaming

- Amazon WorkDocs: just like Office365
- Amazon WorkMail: business email, calender service
- Amazon Chime: online meeting, call, chat
- Amazon WorkSpaces: desktop as a service
- Amazon AppStream: stream Desktop app to HTML5, can access application from anywhere

### Internet of Things

- AWS IOT: embed microcontroller, Rasberry PI to interact with cloud application and other devices
- Amazon FreeRTOS: OS for micro-controller, to connect to AWS IOT
- AWS Greengrass: local AWS lambda funciton, extends AWS services to devices

### Game Dev

- Amazon Gamelift: dedicated game servers
- Amazon Lumberyard: game development env in the cloud

### Elastic Beanstalk

- ElasticBeanstalk: auto-handle capacity privisioning, load balancer, health monitoring
  - app can be docker container, nodejs, python, ruby, go, java, nodejs etc.
  - process: create application -> upload version -> launch environment -> manage environment -> update environment
- highly available and fault tolerant

### Deployment Options

- all at once. Bad down time.
- rolling deploy: e.g. 20 EC2, deploy to 2 EC at a time
- immutable: deploy all 20 new EC2, shutdown old. Temporarily double capacity. Zero downtime.
- blue-green: one for dev, one for prod. Switch between environment.

### References

- aws.amazon.com/certification
- docs.aws.amazon.com
- aws.amazon.com/whitepapers
- aws.amazon.com/products
- static website template: https://html5up.net/
- check dns propagation: https://www.whatsmydns.net/
