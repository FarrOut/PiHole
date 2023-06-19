from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

from pi_hole.networking.networking_stack import NetworkingStack
from pi_hole.service.service_stack import ServiceStack
from pi_hole.storage.storage_stack import StorageStack


# from pi_hole.storage import StorageStack

class PiHoleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        networking = NetworkingStack(self, "NetworkingStack", )

        storage = StorageStack(self, "StorageStack",
                               vpc=networking.vpc,
                               )

        ServiceStack(self, "ServiceStack",
                     vpc=networking.vpc,
                     file_system=storage.file_system,
                     )
