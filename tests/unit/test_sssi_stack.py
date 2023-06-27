import aws_cdk as core
import aws_cdk.assertions as assertions

from sssi.sssi_stack import SssiStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sssi/sssi_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SssiStack(app, "sssi")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
