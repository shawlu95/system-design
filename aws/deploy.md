## Infra as Code

- defined infra in text file (JSON, YAML)
- version control

Workflow

1. write code using **CLoudFormation** template landuage

- CloudFormation Designer IDE available, simple drag and drop
- format template version
- descriotion, metadata, params, resources (required), conditions

2. upload to s3
3. create a cloud stack from console, CLI or API
4. tear down the stack, do not delete individual instances

### AWS OpsWorks

- Configuration management fully managed by AWS
  1. Chef Automate
  2. Puppet Enterprise
  3. Stacks

### CodePipeline (CI/CD)

Automate the entire process:

- commit code via git
- compile and build
- run test
- deploy, provision, monitor (OpsWorks, Beanstalk manage this three parts)

### Elastic Container Service

- orchastration service for docker container
- provision EC2, confiture compute resource, deploy containers, scale automatically, monitor with CloudWatch
- Amazon Elastic COntainer Registry stores images
- AWS Fargate deploy in serverless manner

### Elastic K8s Service (EKS)

- automate deplooyment, scaling, maangement of docker container cluster
- clusters are built using EKS Distro open source distribution

### Deploy Strategies

- all-at-once: have downtime
  - temporarily double capacity
  - setup another cluster and change Route53 to redirect traffic
- in-place: each instance is stopped and updated incrementally, no new resource is created
  - can have new instance to sub the temporarily unavailable instance
- blue/green: two identical architecture, update one, switch traffic via Route53
- canary: two-stage blue/green; redirect half traffic, and then the other half (if OK)
- linear: incremental blue/green; start with 10% traffic, slowly increase
