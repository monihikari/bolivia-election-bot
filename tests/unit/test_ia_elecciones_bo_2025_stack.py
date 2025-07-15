import aws_cdk as core
import aws_cdk.assertions as assertions

from ia_elecciones_bo_2025.ia_elecciones_bo_2025_stack import IaEleccionesBo2025Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in ia_elecciones_bo_2025/ia_elecciones_bo_2025_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = IaEleccionesBo2025Stack(app, "ia-elecciones-bo-2025")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
