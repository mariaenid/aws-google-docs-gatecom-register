<!--
title: 'Maria\'s project to talk to a spreadsheet'
description: 'register people\'s access to the anti COVID offices'
layout: Doc
framework: v1
platform: AWS
language: Python
authorLink: 'https://github.com/mepineda1992'
authorName: 'Maria and friends'
-->
# Simple HTTP Endpoint for update user access into a a google

## Requirements
- serverless (insall using `npm install`)
- python3 environment (install using `pyenv activate <mytestenvironmentorsomething>`)

## Setup
```bash
$ npm install
$ pip install -r requirements
```

## Local Test?
- 🦗

## Deploy

In order to deploy the you endpoint simply run

```bash
serverless deploy
```

The expected result should be similar to:

```bash
Serverless: Packaging service...
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading service .zip file to S3 (758 B)...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...
..........
Serverless: Stack update finished...

Service Information
service: aws-python-simple-http-endpoint
stage: dev
region: us-east-1
api keys:
  None
endpoints:
  GET - https://f7r5srabr3.execute-api.us-east-1.amazonaws.com/dev/ping
functions:
  aws-python-simple-http-endpoint-dev-currentTime: arn:aws:lambda:us-east-1:377024778620:function:aws-python-simple-http-endpoint-dev-currentTime
```

## Usage

You can now invoke the Lambda directly and even see the resulting log via

```bash
serverless invoke --function registerHim --log
```

```bash
serverless invoke local --function registerHim --data '{"user_id": "123213", "name":"Maria Prueba", "device_id":"gatecom1" }'
```

Finally you can send an HTTP request directly to the endpoint using a tool like curl

```bash
curl https://XXXXXXX.execute-api.us-east-1.amazonaws.com/dev/ping
```

The expected result should be similar to:

```bash
{"message": "Hello, the current time is 15:38:53.668501"}%
```

## Scaling

By default, AWS Lambda limits the total concurrent executions across all functions within a given region to 100. The default limit is a safety limit that protects you from costs due to potential runaway or recursive functions during initial development and testing. To increase this limit above the default, follow the steps in [To request a limit increase for concurrent executions](http://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html#increase-concurrent-executions-limit).
