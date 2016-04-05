# Class for creating CloudTrail objects

class CloudTrail:

    def __init__(self):
        """CloudTrail Constructor"""

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

line 10: creates a new CloudTrail object by calling the create_trail method on the cloudtrail
        connection object and passing in the name of the new trail (string object) and the name
        of the s3 bucket (string object) the log files should be sent to.
line 11: if the trail object has been created
line 12: Starts the recording of AWS API calls and log file delivery for a trail by calling the
        start_logging method on the cloudtrail connection object and passing the trail_name in
        as a parameter
line 13: prints success message		
line 14/15: If trail was not successful, prints error message
"""
