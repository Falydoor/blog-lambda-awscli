from aws_cdk import (
    aws_events as events_,
    aws_lambda as lambda_,
    aws_s3 as s3_,
    aws_s3_deployment as s3_deployment_,
    aws_events_targets as targets_,
    lambda_layer_awscli as awscli_,
    core as cdk
)


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
        fn.add_layers(awscli_.AwsCliLayer(self, "AwsCliLayer"))

        # Grant Lambda access to S3 buckets
        bucket_source.grant_read(fn)
        bucket_destination.grant_read_write(fn)

        # Deploy data folder to source bucket
        s3_deployment_.BucketDeployment(self, "Deploy files to source bucket",
                                        sources=[s3_deployment_.Source.asset("./data")],
                                        destination_bucket=bucket_source)

        # Trigger lambda every day
        rule = events_.Rule(self, "Rule",
                            schedule=events_.Schedule.rate(cdk.Duration.days(1)),
                            )
        rule.add_target(targets_.LambdaFunction(fn))
