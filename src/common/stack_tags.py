import aws_cdk as cdk

def add_default_tags(stack):
    cdk.Tags.of(stack).add("Project", "IA-Elecciones-BO-2025")
    cdk.Tags.of(stack).add("Owner", "LlamitAI")