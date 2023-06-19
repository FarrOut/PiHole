from aws_cdk import (
    # Duration,
    Stack, aws_route53 as route53,
    aws_ec2 as ec2, CfnOutput, RemovalPolicy, )
from constructs import Construct


class Route53Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, zone_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.zone = route53.HostedZone(self, "HostedZone",
                                       zone_name=zone_name,
                                       vpcs=[vpc],
                                       )
        self.zone.apply_removal_policy(RemovalPolicy.DESTROY)

        CfnOutput(self, 'HostedZoneArn',
                  description='ARN of this hosted zone',
                  value=str(self.zone.hosted_zone_arn),
                  )

        CfnOutput(self, 'HostedZoneId',
                  description='ID of this hosted zone, such as “Z23ABC4XYZL05B”.',
                  value=str(self.zone.hosted_zone_id),
                  )

        # CfnOutput(self, 'HostedZoneNameServers',
        #           description='the set of name servers for the specific hosted zone.',
        #           value=str(self.zone.hosted_zone_name_servers),
        #           )
        CfnOutput(self, 'HostedZoneName',
                  description='FQDN of this hosted zone.',
                  value=str(self.zone.zone_name),
                  )