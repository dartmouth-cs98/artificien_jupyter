# Jupyter Deployment

This repository contains code relating to deploying a multi-user juypter notebook service that integrates with the Artificien platform.

## Requirements

Core Needs
- More than one user has to be able to use
- Different users must have different file spaces
- Different users must have different accounts
- Users must me able to save files
- Users must be able to send completed Pysyft models to Pygrid engine for deployment
- Integration with Artificien website on the frontend

Stretch
- Scalable/inexpensive infrastructure to accomodate many users at one

## General Information

Directory `jupyter_service` contains deployable multiuser JupyterHub application (Using AWS EC2 CDK script). This is what will be used in MVP production

Directory `jupyter_service_kubernetes` contains various methonds to deployAWS EKS kubernetes cluster and VPC using cloudformation & terraform. This approach is more scalable than the AWS EC2 approach being deployed, but much more challenging & error prone. This has been tabled until Phase 2 of the project, and can be used as research to re-evaluate this architecture next term.

### Using jupyter_service

This is an AWS CDK service. Dependancies are `aws-cli`, `aws-cli-ec2`.

cd into `jupyter_service` directory.

To compile: `cdk synth`
To deploy: `cdk deploy`
To deprovision cloud resources: `cdk destroy`

When run, the script will deploy a multiuser jupyterhub at a public IP, accessable via HTTP (one issue for sprint 2 is HTTPS). It is automatically configured with an admin account `artificien` with password `artificien`. Admins can add other users via CLI or GUI. Another issue for sprint 2 is integrating access with Oauth (AWS cognito).

When deployed, cloud resource is accessable at: http://ec2-54-145-15-160.compute-1.amazonaws.com/hub/login  
