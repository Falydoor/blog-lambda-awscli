import logging
import os
import subprocess

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def sync(event, context):
    # Lambda to sync two buckets using the aws cli
    s3_sync = subprocess.Popen(
        "/opt/awscli/aws s3 sync s3://{} s3://{}".format(os.environ['SOURCE'], os.environ['DESTINATION']).split(),
        stdout=subprocess.PIPE)

    # Stream logs from the cmd
    while True:
        output = s3_sync.stdout.readline()
        if s3_sync.poll() is not None:
            break
        if output:
            logger.info(output.strip())
    s3_sync.poll()
