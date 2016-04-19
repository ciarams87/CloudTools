# Class for creating CloudTrail objects
from Connections import Connections
import json

# noinspection PyMethodMayBeStatic


class CloudTrail:

    def __init__(self):
        """CloudTrail Constructor"""
        self.aws_conn = Connections()
        self.ec2c = self.aws_conn.ec2_connection()

    def acl_policy(self, buck_name):
        """policy to allow Cloud Trail logs to be sent to a bucket"""
        # to retrieve the account ID
        groups = self.ec2c.get_all_security_groups()
        account_id = groups[0].owner_id
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AWSCloudTrailAclCheck20150319",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "cloudtrail.amazonaws.com"
                    },
                    "Action": "s3:GetBucketAcl",
                    "Resource": "arn:aws:s3:::%s" % buck_name
                },
                {
                    "Sid": "AWSCloudTrailWrite20150319",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "cloudtrail.amazonaws.com"
                    },
                    "Action": "s3:PutObject",
                    "Resource": "arn:aws:s3:::%s/AWSLogs/%s/*" % (buck_name, account_id),
                    "Condition": {
                        "StringEquals": {
                            "s3:x-amz-acl": "bucket-owner-full-control"
                        }
                    }
                }
            ]
        }
        return json.JSONEncoder().encode(policy)

    def create_trail(self, conn, bucket_name, trail_name):
        """ Creates and enables a trail that specifies the settings
        for delivery of log data to an Amazon S3 bucket """
        trail = conn.create_trail(name=trail_name, s3_bucket_name=bucket_name)
        if trail:
            conn.start_logging(trail_name)
            print 'CloudTrail Created'
        else:
            print 'unable to create trail'

"""
CloudTrail is an AWS web service that records AWS API calls for your AWS account and delivers
log files to an Amazon S3 bucket. The recorded information includes the identity of the user,
the start time of the AWS API call, the source IP address, the request parameters, and the
response elements returned by the service.

lines 10/11: creates ec2 connection instance inside __init__ method

lines 13 - 46: The S3 bucket designated for Cloud Trail logging must have a policy set to allow
            cloud trail access the bucket. This method creates this policy in the form of a JSON string.
line 16/17: As the account ID is not easily accessed through boto, this gets a list of security groups
            and retrieves the account id from a security group object's owner_id attribute
lines 18 - 45: Policy details. Includes the bucket name and account ID variables.
line 46: Encodes the policy into JSON format

line 51: creates a new CloudTrail object by calling the create_trail method on the cloudtrail
        connection object and passing in the name of the new trail (string object) and the name
        of the s3 bucket (string object) the log files should be sent to.
line 52: if the trail object has been created
line 53: Starts the recording of AWS API calls and log file delivery for a trail by calling the
        start_logging method on the cloudtrail connection object and passing the trail_name in
        as a parameter
line 54: prints success message
line 55/56: If trail was not successful, prints error message
"""
