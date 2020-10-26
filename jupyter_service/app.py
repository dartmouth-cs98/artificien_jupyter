#!/usr/bin/env python3

from aws_cdk import core

from jupyter_service.jupyter_service_stack import JupyterServiceStack

app = core.App()
JupyterServiceStack(app, "jupyter-service", env={'region': 'us-east-1'})

app.synth()
