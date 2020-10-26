import json
import pytest

from aws_cdk import core
from jupyter_service.jupyter_service_stack import JupyterServiceStack


def get_template():
    app = core.App()
    JupyterServiceStack(app, "jupyter-service")
    return json.dumps(app.synth().get_stack("jupyter-service").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
