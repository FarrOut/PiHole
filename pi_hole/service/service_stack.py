from aws_cdk import (
    # Duration,
    Stack, aws_efs as efs,aws_ec2 as ec2,
    aws_ecs as ecs, RemovalPolicy, CfnOutput,
)
from aws_cdk.aws_logs import LogGroup, RetentionDays
from constructs import Construct


class ServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, file_system: efs.FileSystem, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        volume_pihole = {
            # Use an Elastic FileSystem
            "name": "pihole",
            "efs_volume_configuration": {
                "file_system_id": file_system.file_system_id,
                "root_directory": '/etc/pihole'
            }
        }
        volume_dnsmasq = {
            # Use an Elastic FileSystem
            "name": "dnsmasq",
            "efs_volume_configuration": {
                "file_system_id": file_system.file_system_id,
                "root_directory": '/etc/dnsmasq.d'
            }
        }

        task_def = ecs.FargateTaskDefinition(self, "TaskDef",
                                             memory_limit_mib=512,
                                             cpu=256,
                                             volumes=[volume_pihole, volume_dnsmasq],
                                             )

        log_group = LogGroup(self, "LogGroup",
                             retention=RetentionDays.ONE_WEEK,
                             removal_policy=RemovalPolicy.DESTROY,
                             )

        container_def = ecs.ContainerDefinition(self, "ContainerDef",
                                                task_definition=task_def,
                                                image=ecs.ContainerImage.from_registry(
                                                    "pihole/pihole"),
                                                port_mappings=[ecs.PortMapping(
                                                    container_port=53,
                                                    host_port=53,
                                                    protocol=ecs.Protocol.TCP
                                                ), ecs.PortMapping(
                                                    container_port=53,
                                                    host_port=53,
                                                    protocol=ecs.Protocol.UDP
                                                ), ecs.PortMapping(
                                                    container_port=67,
                                                    host_port=67,
                                                    protocol=ecs.Protocol.UDP,
                                                    name='dhcp'
                                                ), ecs.PortMapping(
                                                    container_port=80,
                                                    host_port=80,
                                                    protocol=ecs.Protocol.TCP
                                                )],
                                                logging=ecs.AwsLogDriver(stream_prefix="EventDemo",
                                                                         mode=ecs.AwsLogDriverMode.NON_BLOCKING,
                                                                         log_group=log_group,
                                                                         ),
                                                environment={
                                                    "TZ": "Africa/Johannesburg"
                                                },
                                                )

        CfnOutput(self, 'ContainerName',
                  description='The name of this container.',
                  value=container_def.container_name,
                  )
        CfnOutput(self, 'ContainerPort',
                  description='The port the container will listen on.',
                  value=str(container_def.container_port),
                  )
        CfnOutput(self, 'ContainerCpu',
                  description='The number of cpu units reserved for the container.',
                  value=str(container_def.cpu),
                  )
        CfnOutput(self, 'ContainerIsEssential',
                  description='Specifies whether the container will be marked essential.',
                  value=str(container_def.essential),
                  )
        CfnOutput(self, 'ContainerImageName',
                  description='The name of the image referenced by this container.',
                  value=container_def.image_name,
                  )
