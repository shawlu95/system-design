## Creating Static Website

This is suitable for presentation website with no backend or database interaction.

1. download a package (index.html, assets, css etc)
2. create a new s3 bucket and upload the entire site package
3. make the s3 bucket public. Add the policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AddPerm",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::{{s3_bucket}}/*"
    }
  ]
}
```

4. register a domain in Route53
5. setup domain email using Workmail
6. request SSL certificate (by email) using AWS Certificate Manager
7. Create a CloudFront distribution that points to the s3 bucket (index.html entry)
8. disable public access to s3 bucket
9. create a A record **alias** in Route53 that points to the CloudFront distribution domain name
10. create a CNAME record that directs `www.` to domain name
11. check domain propagation in https://www.whatsmydns.net/
12. create CodePipeline to integrate with GitHub repo

![alt](/aws/exercises/assets/propagation.png)
