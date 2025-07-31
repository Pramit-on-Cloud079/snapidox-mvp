# AWS CI/CD Pipeline for Lambda

**Author:** Pramit Dasgupta  
**Date:** 2025-07-30  

## Summary
This AWS project is a pipeline that automates the deployment of Lambda functions using CodePipeline and GitHub. 

What it does:
The pipeline takes source code from a GitHub repository, builds the Lambda functions, and deploys them to the AWS Lambda service.

AWS services used:
- AWS CodePipeline: Orchestrates the workflow of the deployment pipeline.
- AWS Lambda: Executes the serverless functions.
- GitHub: Stores the source code of the Lambda functions.

How the automation works:
1. Code changes are made in the GitHub repository.
2. GitHub webhook triggers CodePipeline.
3. CodePipeline fetches the latest code from GitHub, builds the Lambda functions, and packages them.
4. The packaged Lambda functions are deployed to the AWS Lambda service.
5. The deployment status is updated in CodePipeline.

Deployment flow in 4-5 steps:
1. Code changes are pushed to the GitHub repository.
2. GitHub webhook triggers CodePipeline.
3. CodePipeline fetches the latest code, builds and packages the Lambda functions.
4. Packaged Lambda functions are deployed to AWS Lambda.
5. Deployment status is updated in CodePipeline.

## Features
- Automated deployment using CodePipeline & CodeBuild
- Lambda function deployment from GitHub commits
- Artifacts stored in S3

## Folder Structure
snapidox-mvp/
├── src/
├── reports/
├── screenshots/
├── assets/

bash
Copy
Edit

## Output Files
- PDF Report: `/reports/project_report.pdf`
