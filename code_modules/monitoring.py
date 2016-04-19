# Class for manipulating CloudWatch services

import boto.ec2.cloudwatch
import boto.sns


# noinspection PyMethodMayBeStatic
class CloudWatch:
    def __init__(self):
        """ Cloudwatch Constructor """

    def enable_specific_cw(self, ec2conn, ins_id):
        """ enable cloudwatch monitoring on an instance """
        ec2conn.monitor_instance(ins_id)

    def metric_list(self, cw_conn, instance_id):
        """ Query CloudWatch for list of available metrics """
        metric = cw_conn.list_metrics(dimensions={'InstanceId': instance_id})
        for m in metric:
            print m

    def get_sns_arn(self, sns_topic):
        """Retrieve Amazon Resource Name from a given Simple Notification Service topic"""
        for key, value in sns_topic.iteritems():    # "sns_topic" is of type dictionary
            for k, v in value.iteritems():          # "value" is of type dictionary
                if k == u'CreateTopicResult':
                    for h, arn in v.iteritems():    # "v" is of type dictionary
                        return arn

    def cw_alarm(self, cw_conn, instance_id, email_add):
        """ Create cloudwatch alarm on an instance when CPU utilisation is less
        than or equal to 40% for five minutes, and send sns alert to an email address """
        sns = boto.sns.connect_to_region('eu-west-1')
        topic_name = 'cpu_alarm'+instance_id
        new_sns_topic = sns.create_topic(topic_name)
        sns_arn = self.get_sns_arn(new_sns_topic)
        sns.subscribe(sns_arn, 'email', email_add)
        metrics = cw_conn.list_metrics(dimensions={'InstanceId': instance_id}, metric_name="CPUUtilization")
        ec2_alarm = metrics[0].create_alarm(name=topic_name, comparison='<=', threshold=40.0, period=300,
                                            evaluation_periods=2, statistic='Average', alarm_actions=[sns_arn])
        if ec2_alarm:
            print 'cloudwatch alarm created'

"""
Amazon CloudWatch is a monitoring service for AWS cloud resources and the applications you run on AWS. You can use
Amazon CloudWatch to collect and track metrics, collect and monitor log files, set alarms, and automatically react to
changes in your AWS resources.

line 12: calls the monitor_instance() method to enable CloudWatch

line 16: return a list of metrics where the instance_id matches given id
lines 17/18: loops through metric list and prints each available metric

line 22: loops through key value pairs (using iteritems() built-in method for looping through dictionaries) in the
        given "sns_topic" dictionary
line 23: loops through key value pairs in the "value" dictionary from above loop
line 24: if the key in previous loop is u'CreateTopicResult'
line 25: loop through "v" dictionary
line 26: return arn

line 31: create connection to the SNS service
line 32: create new SNS topic name by concatenating name of the alarm with instance id
line 33: create new SNS topic
line 34: retrieve ARN of the newly created topic
line 35: subscribe given email address to the sns topic
line 36: retrieve list of metrics for the given instance where the metric name is CPUUtilization
line 37/38: create alarm on first element of returned metric list when CPU utilization is below 40% for 5 minutes
line 39/40: if alarm has been created, print success message
"""
