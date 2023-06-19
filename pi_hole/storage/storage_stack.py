from aws_cdk import (
    # Duration,
    Stack, aws_efs as efs, aws_ec2 as ec2,
    CfnOutput, )
from constructs import Construct


class StorageStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.file_system = efs.FileSystem(self, "MyEfsFileSystem",
                                          vpc=vpc,
                                          lifecycle_policy=efs.LifecyclePolicy.AFTER_14_DAYS,

                                          # files are not transitioned to infrequent access (IA) storage by default
                                          performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,  # default
                                          out_of_infrequent_access_policy=efs.OutOfInfrequentAccessPolicy.AFTER_1_ACCESS
                                          )

        CfnOutput(self, 'FileSystemArn',
                  description='The ARN of the file system.',
                  value=self.file_system.file_system_arn
                  )
        CfnOutput(self, 'FileSystemId',
                  description='The ID of the file system, assigned by Amazon EFS.',
                  value=self.file_system.file_system_id
                  )
        CfnOutput(self, 'MountTargetsAvailable',
                  description='The ID of the file system, assigned by Amazon EFS.',
                  value=str(self.file_system.mount_targets_available)
                  )
