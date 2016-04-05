# Class for manipulating CloudWatch services

import boto.ec2.cloudwatch
import boto.sns

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

    def cw_alarm(self, cw_conn, instance_id, email_add):
        """ Create cloudwatch alarm on an instance based on CPU utilisation
         and send sns alert to an email address """
        sns = boto.sns.connect_to_region('eu-west-1')
        topic_name = 'cpu_alarm'+instance_id
        new_sns_topic = sns.create_topic(topic_name)
        # nested function for retrieving sns arn from created topic
        def get_sns_arn():
            for key, value in new_sns_topic.iteritems():
                for k, v in value.iteritems():
                    if k == u'CreateTopicResult':
                        for h, arn in v.iteritems():
                            return arn

        sns_arn = get_sns_arn()
        sns.subscribe(sns_arn, 'email', email_add)
        metric = cw_conn.list_metrics(dimensions={'InstanceId': instance_id}, metric_name="CPUUtilization")
        for m in metric:
            ec2_alarm = m.create_alarm(name=topic_name, comparison='<=', threshold=40.0, period=300,
                                       evaluation_periods=2, statistic='Average', alarm_actions=[sns_arn])
            if ec2_alarm:
                print 'cloudwatch alarm created'
