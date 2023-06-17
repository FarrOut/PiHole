import aws_cdk as core
import aws_cdk.assertions as assertions

from pi_hole.pi_hole_stack import PiHoleStack

# example tests. To run these tests, uncomment this file along with the example
# resource in pi_hole/pi_hole_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PiHoleStack(app, "pi-hole")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
