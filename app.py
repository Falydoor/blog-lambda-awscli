from aws_cdk import core
from aws_cdk.core import Tags

from blog_lambda_awscli.blog_lambda_awscli_stack import BlogLambdaAwscliStack

app = core.App()
stack = BlogLambdaAwscliStack(app, "BlogLambdaAwscliStack")
Tags.of(app).add('ippon:owner', 'tlebrun')
app.synth()
