# coding=utf-8
# Class for implementing AWS Auto Scaling configurations
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup
from boto.ec2.autoscale import ScalingPolicy
from boto.ec2.cloudwatch import MetricAlarm


# noinspection PyMethodMayBeStatic
class AutoScale:
    def __init__(self):
        """constructor for AutoScale class"""

    def launch_config(self, conn, launch_name, key_name):
        """ Creates a new launch config """
        lc = LaunchConfiguration(name=launch_name, image_id='ami-e1398992',
                                 instance_type='t2.micro', key_name=key_name)
        cf = conn.create_launch_configuration(lc)
        if cf:
            print "Launch Config Created"
        else:
            "Error creating launch config"

    def create_autoscale_group(self, conn, launch_c, group_name):
        """ Creates new auto scaling group """
        ag = AutoScalingGroup(group_name=group_name, availability_zones=['eu-west-1a', 'eu-west-1b', 'eu-west-1c'],
                              launch_config=launch_c, min_size=1, max_size=3, connection=conn)
        group = conn.create_auto_scaling_group(ag)
        if group:
            print "new group has been created,", group_name
        else:
            print "Error creating group"

    def list_group_instances(self, ec2conn, as_conn, group_name):
        """ Lists all instances associated with a group"""
        group = as_conn.get_all_groups(names=[group_name])[0]
        if group:
            instance_ids = [i.instance_id for i in group.instances]
            instances = ec2conn.get_only_instances(instance_ids)
            if instances:
                for i in instances:
                    print i
            else:
                print "No instances associated with this group"
        else:
            print "Cannot find group"

    def scale_up_alarm(self, as_conn, group_name, cw_conn):
        """ Creates an alarm which launches new instances when triggered """
        scale_up_policy = ScalingPolicy(name='scale_up', adjustment_type='ChangeInCapacity',
                                        as_name=group_name, scaling_adjustment=1, cooldown=180)
        as_conn.create_scaling_policy(scale_up_policy)
        scale_up_policy = as_conn.get_all_policies(as_group=group_name, policy_names=['scale_up'])[0]
        alarm_dimensions = {"AutoScalingGroupName": group_name}
        scale_up_alarm = MetricAlarm(name='scale_up_on_cpu', namespace='AWS/EC2', metric='CPUUtilization',
                                     statistic='Average', comparison='>', threshold=70.0, period=60,
                                     evaluation_periods=2, alarm_actions=[scale_up_policy.policy_arn],
                                     dimensions=alarm_dimensions)
        alarm = cw_conn.create_alarm(scale_up_alarm)
        if alarm:
            print "Alarm has been created,", alarm
        else:
            print "Error creating alarm"

    def list_all_launch_configs(self, as_conn):
        lcs = as_conn.get_all_launch_configurations()
        if lcs:
            for lc in lcs:
                print lc.name
        else:
            print "No launch configurations found"

    def list_all_groups(self, as_conn):
        groups = as_conn.get_all_groups()
        if groups:
            for group in groups:
                print group.name
        else:
            print "no groups found"


"""
Auto Scaling is an AWS service which allows the user to scale their Amazon 
EC2 capacity up or down automatically according to user-defined
launch configurations, groups and policies. 

lines 15,16: Creates a LaunchConfiguration object with attributes specified in parameters
            (name, ami id new instances should be launched from, instance type new instances
            should have, keypair to be associated with new instances)
line 17: Creates new launch configuration using LaunchConfiguration object.
line 18-21: If successful, print message, if not, print error message

lines 25,26: Creates new AutoScalingGroup object with attributes specified in parameters
            (name, the availability zones instances should be deployed into, name of launch
            config to use, minimum amount of instances to be maintained, maximum amount of
            instances to be maintained, autoscale connection object to use)
line 27: Creates Auto Scaling Group using AutoScalingGroup object as parameter.
line 28-31: If successful, print message and group name, if not, print error message

line 35: Gets group object with the name specified in parameters. Method "get_all_groups"
        returns a list; variable 'group' is assigned to the first item on the group list.
line 36: If the group specified was retrieved
line 37: Loops through instances attribute of group object, retrieves instance_id of each instance 
        and assigns them to list variable 'instance_ids'
line 38: Retrieve instances with get_only_instances method of ec2 connection object,
        using instance_ids variable as parameter
line 39-41: If instances are retrieved, loop through list and print details of each
lines 42-45: If no instances, print error message; if group cannot be retrieved, print error message

lines 49,50: Creates a new ScalingPolicy object with attributes specified in parameters
        (name of policy, the type of adjustment, autoscale group name, value of adjustment, and
        time (in seconds) before alarm related scaling activities can start after the previous
        scaling activity ends)
line 51: Creates scaling policy using ScalingPolicyObject as parameter
line 52: Requests the newly created policy from AWS. Returns a list, the first item on the list
        is assigned to 'scale_up_policy' variable.
line 53: creates a dictionary containing the auto scale group dimensions for the new alarm
line 54: creates new MetricAlarm object. Parameters: name of new alarm; namespace for the metric;
        the metric the alarm is to be associated with; the statistic to apply to the alarm’s
        associated metric; the comparison used to compare statistic with threshold; the value
        against which the specified statistic is compared; the period in seconds over which the
        specified statistic is applied; the number of periods over which data is compared to the
        specified threshold; the action to take when alarm is triggered; the dimensions associated
        with the alarm.
line 58: Creates the alarm by calling create_alarm method on cloudwatch connection object and
        passing MetricAlarm object as parameter
line 59-62: If alarm creation is successful; print message; if not, print error message

lines 64-70: Lists all current launch configurations associated with this account. If configs are
            found, loops through list and prints name of each launch config. Otherwise, prints error
            message.

lines 72-78: Lists all current auto-scaling groups associated with this account. If groups are
            found, loops through list and prints name of each launch config. Otherwise, prints error
            message.
"""
