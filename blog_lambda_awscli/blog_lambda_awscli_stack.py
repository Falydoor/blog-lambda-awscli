import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_s3 as s3_
import aws_cdk.aws_s3_deployment as s3_deployment_
from aws_cdk import core as cdk
from aws_cdk.lambda_layer_awscli import AwsCliLayer


class BlogLambdaAwscliStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 buckets
        bucket_source = s3_.Bucket(self, "Bucket Source")
        bucket_destination = s3_.Bucket(self, "Bucket Destination")

        # Create Lambda
        fn = lambda_.Function(self, "S3_Sync",
                              function_name="S3_Sync",
                              runtime=lambda_.Runtime.PYTHON_2_7,
                              handler="index.sync",
                              code=lambda_.Code.asset('lambda'),
                              environment={
                                  "SOURCE": bucket_source.bucket_name,
                                  "DESTINATION": bucket_destination.bucket_name
                              },
                              timeout=cdk.Duration.minutes(15))

        # Add Lambda layer containing the aws cli
        fn.add_layers(AwsCliLayer(self, "AwsCliLayer"))

        # Grant Lambda access to S3 buckets
        bucket_source.grant_read(fn)
        bucket_destination.grant_read_write(fn)

        # Deploy data folder to source bucket
        s3_deployment_.BucketDeployment(self, "Deploy files to source bucket",
                                        sources=[s3_deployment_.Source.asset("./data")],
                                        destination_bucket=bucket_source)
