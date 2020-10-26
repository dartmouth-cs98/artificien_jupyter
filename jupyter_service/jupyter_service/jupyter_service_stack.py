from aws_cdk import (
    aws_ec2 as ec2,
    core
)


class JupyterServiceStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        jupyter_ec2 = True
        vpc = ec2.Vpc(self,
                    "VPC", 
                    subnet_configuration=[ec2.SubnetConfiguration(
                        cidr_mask=24,
                        name="Ingress",
                        subnet_type=ec2.SubnetType.PUBLIC
                    )]
                    )
        jupyter_security_group = ec2.SecurityGroup(self, "jupyter_security_group", allow_all_outbound=True, vpc=vpc)

        jupyter_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80))
        jupyter_security_group.add_ingress_rule(ec2.Peer.any_ipv6(), ec2.Port.tcp(80))
        jupyter_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(443))
        jupyter_security_group.add_ingress_rule(ec2.Peer.any_ipv6(), ec2.Port.tcp(443))
        jupyter_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22))
        jupyter_security_group.add_ingress_rule(ec2.Peer.any_ipv6(), ec2.Port.tcp(22))
    
        
        if jupyter_ec2:
            #create instance
            jupyter_instance = ec2.Instance(
                    self,
                    "jupyter_client",
                    instance_type=ec2.InstanceType("t2.medium"),
                    machine_image=ec2.MachineImage.generic_linux({'us-east-1': 'ami-0817d428a6fb68645'}),
                    security_group=jupyter_security_group,
                    vpc=vpc,
                    key_name="littlest-jupyter"
            )
            core.Tag.add(jupyter_instance, "Name", "Little Jupyter Service")

            jupyter_userdata = ec2.UserData.for_linux(shebang="#!/bin/bash -xe")
            jupyter_userdata.add_commands(
                    #updata packages
                    "apt update -y",
#                    "apt install -y software-properties-common",
#                    "add-apt-repository -y ppa:deadsnakes/ppa",
                    "apt upgrade -y",
                    # install littlest jupyter hub
                    "curl -L https://tljh.jupyter.org/bootstrap.py | python3 - --admin artificien",
            )
            jupyter_userdata.add_signal_on_exit_command(resource=jupyter_instance)

            jupyter_instance.instance.cfn_options.creation_policy = core.CfnCreationPolicy(
                resource_signal=core.CfnResourceSignal(count=1, timeout="PT10M")
            )

