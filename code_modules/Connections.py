# Class for managing all AWS service connections
import boto
import boto.ec2
from boto.s3.connection import S3Connection
import boto.ec2.cloudwatch
from boto import config
import boto.ec2.autoscale
import boto.cloudtrail

'''Define the access key id and secret access 
key as set in the boto configuration file'''
aws_access_key_id = config.get('Credentials', 'aws_access_key_id')
# aws_access_key_id = ""
aws_secret_access_key = config.get('Credentials', 'aws_secret_access_key')
# aws_secret_access_key = ""

# noinspection PyMethodMayBeStatic


class Connections:

    def __init__(self):
        # Connections Constructor
        self.region = 'eu-west-1'

    def ec2_connection(self):
        # Creates and returns an EC2 Connection object
        conn = boto.ec2.connect_to_region(self.region)
        return conn

    def s3_connection(self):
        # Creates and returns an S3 connection object
        conn = S3Connection(aws_access_key_id, aws_secret_access_key)
        return conn

    def cw_connection(self):
        # Creates and returns a CloudWatch connection object
        conn = boto.ec2.cloudwatch.connect_to_region(self.region)
        return conn

    def as_connection(self):
        # Creates and returns an Auto Scaling connection object
        conn = boto.ec2.autoscale.connect_to_region(self.region)
        return conn

    def ct_connection(self):
        # Creates and returns a CloudTrail connection object
        conn = boto.cloudtrail.connect_to_region(self.region)
        return conn
