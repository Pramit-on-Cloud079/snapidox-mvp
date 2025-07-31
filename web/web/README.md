# Ci/cd pipeline using codepipeline, codebuild and lambda

**Author:** Pramit Dasgupta  
**Date:** 2025-07-31  

## Summary
This AWS project is a CI/CD pipeline that leverages CodePipeline, CodeBuild, and Lambda to automate the deployment process of an application. 

What it does:
The CI/CD pipeline automates the process of building, testing, and deploying code changes to production, ensuring a streamlined and efficient deployment process.

AWS services used:
- CodePipeline: orchestrates the workflow of the CI/CD pipeline, managing the different stages of the deployment process.
- CodeBuild: compiles the code, runs tests, and packages the application for deployment.
- Lambda: used for custom actions within the pipeline, such as triggering notifications or running additional scripts.

How the automation works:
The automation process begins with a code commit to the repository, which triggers the CodePipeline. CodePipeline then initiates the build process using CodeBuild, running tests and packaging the application. Custom Lambda functions can be integrated at various stages of the pipeline to perform additional actions, such as sending notifications or updating configuration files.

Deployment flow in 4-5 steps:
1. Code commit triggers CodePipeline.
2. CodePipeline initiates the build process using CodeBuild.
3. CodeBuild compiles the code, runs tests, and packages the application.
4. Lambda functions can be triggered at various stages for custom actions.
5. Once the build is successful, the application is deployed to the production environment.

## Features
- Automated deployment using AWS tools
- Based on prompt: “Ci/cd pipeline using codepipeline, codebuild and lambda”

## Output Files
- PDF Report: `project_report.pdf`
