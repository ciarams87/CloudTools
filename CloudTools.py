#!/usr/bin/env python
"""
This is a console-driven menu program for management of some AWS and OpenStack cloud services
"""

import time
from aws_compute import AWS_Compute
from Connections import Connections
from aws_storage import aws_S3
from monitoring import CloudWatch
from OpenStackConn import OSConnections
from open_stack import OpenStack
from autoscale import AutoScale
from CloudTrail import CloudTrail


def main():
    # OpenStack Connections
    OSConn = OSConnections()
    compute_driver = OSConn.os_compute_conn()
    storage_driver = OSConn.os_storage_conn()
    openS = OpenStack()

    # AWS Connections
    aws_conn = Connections()
    ec2_conn = aws_conn.ec2_connection()
    s3_conn = aws_conn.s3_connection()
    cW_conn = aws_conn.cw_connection()
    autoS_conn = aws_conn.as_connection()
    cTrail_conn = aws_conn.ct_connection()

    # AWS Services
    ec2 = AWS_Compute()
    s3 = aws_S3()
    cW = CloudWatch()
    autoS = AutoScale()
    cTrail = CloudTrail()

    loop_lvl_1 = 1
    while loop_lvl_1 == 1:
        # print what options you have
        print "Welcome to CloudTools. \nPlease make a selection by " \
              "entering the number of your chosen menu item below.\n" \
              "Your options are:\n" \
              "1) Compute \n2) Storage \n3) Monitoring \n" \
              "4) AutoScaling \n5) CloudTrail \n6) Quit CloudTools"

        choice_lvl_1 = input("Choose your option: \n")
        if choice_lvl_1 == 1:
            loop_lvl_2 = 1
            while loop_lvl_2 == 1:
                choice_lvl_2 = input("Please choose your provider:\n1) AWS \n2) OpenStack \n3) MainMenu \nChoice: \n")

                if choice_lvl_2 == 1:
                    loop_lvl_3 = 1

                    while loop_lvl_3 == 1:
                        choice_lvl_3 = input("Please select service required:\n1) List running instances \n"
                                             "2) Start an instance (AMI known)\n3) Stop instances \n4) Manage volumes \n"
                                             "5) Launch new instance (AMI unknown)\n6) Go back \nChoice: \n")

                        if choice_lvl_3 == 1:
                            loop_lvl_4 = 1

                            while loop_lvl_4 == 1:
                                choice_lvl_4 = input("1) Enter ID \n2) List all \n3) Go Back \n")

                                if choice_lvl_4 == 1:
                                    ec2.list_all_ins(ec2_conn)
                                    ins_id = raw_input("Enter instance ID: \n")
                                    ec2.list_run_instances(ec2_conn, ins_id)
                                    time.sleep(3)
                                    loop_lvl_4 = 0
                                elif choice_lvl_4 == 2:
                                    ec2.list_run_instances(ec2_conn)
                                    time.sleep(3)
                                    loop_lvl_4 = 0
                                elif choice_lvl_4 == 3:
                                    loop_lvl_4 = 0
                                else:
                                    print "Please enter number between 1 and 3 only"
                                    time.sleep(2)

                        elif choice_lvl_3 == 2:
                            ec2.get_keypair_list(ec2_conn)
                            keypair = raw_input("Please enter name of keypair from above list: \n")
                            ec2.start_instance(ec2_conn, keypair)
                            time.sleep(3)

                        elif choice_lvl_3 == 3:
                            loop_lvl_4 = 1

                            while loop_lvl_4 == 1:
                                choice_lvl_4 = input("1) Enter ID \n2) Stop all\n3) Go Back \nChoice: \n")

                                if choice_lvl_4 == 1:
                                    ec2.list_all_ins(ec2_conn)
                                    ins_id = raw_input("Enter instance ID from above list: \n")
                                    ec2.stop_instance(ec2_conn, ins_id)
                                    time.sleep(3)
                                    loop_lvl_4 = 0
                                elif choice_lvl_4 == 2:
                                    ec2.stop_all_instances(ec2_conn)
                                    time.sleep(3)
                                    loop_lvl_4 = 0
                                elif choice_lvl_4 == 3:
                                    loop_lvl_4 = 0
                                else:
                                    print "Please enter number between 1 and 3 only"
                                    time.sleep(2)

                        elif choice_lvl_3 == 4:
                            loop_lvl_4 = 1

                            while loop_lvl_4 == 1:
                                choice_lvl_4 = input(
                                    "1) Attach volume \n2) Detach volume \n3) Go Back \nChoice: \n")

                                if choice_lvl_4 == 1:
                                    ec2.list_all_ins(ec2_conn)
                                    ins_id = raw_input("Enter ID of instance the volume should be attached to:\n")
                                    loop_lvl_5 = 1
                                    while loop_lvl_5 == 1:
                                        choice_lvl_5 = input("1) Attach existing volume \n2) Attach new volume \nChoice: \n")
                                        if choice_lvl_5 == 1:
                                            ec2.list_all_vols(ec2_conn)
                                            vol_id = raw_input("Enter volume ID (Volume must be 'Available'"
                                                               "and in same Availability Zone as instance)): \n")
                                            loop_lvl_5 = 0
                                        elif choice_lvl_5 == 2:
                                            size = input("Please enter required size in GiB (Between 1 and 1000):\n")
                                            zone = raw_input("Choose required zone - must be same as instance.\n"
                                                             "Options are: eu-west-1a; eu-west-1b; eu-west-1c:\n")
                                            vol_id = ec2.create_volume(ec2_conn, size, zone)
                                            print "Creating volume..."
                                            time.sleep(10)
                                            loop_lvl_5 = 0
                                        else:
                                            print "Please enter 1 or 2 only"
                                            time.sleep(2)

                                    ec2.attach_volume(ec2_conn, vol_id, ins_id)
                                    time.sleep(3)
                                    loop_lvl_4 = 0
                                elif choice_lvl_4 == 2:
                                    ec2.list_all_vols(ec2_conn)
                                    vol_id = raw_input("Enter volume ID: \n")
                                    ec2.detach_volume(ec2_conn, vol_id)
                                    time.sleep(3)
                                    loop_lvl_4 = 0
                                elif choice_lvl_4 == 3:
                                    loop_lvl_4 = 0
                                else:
                                    print "Please enter number between 1 and 3 only"
                                    time.sleep(2)

                        elif choice_lvl_3 == 5:
                            loop_lvl_4 = 1
                            while loop_lvl_4 == 1:
                                choice_lvl_4 = input(
                                    "1) Launch Linux Instance \n2) Launch Windows Instance \n3) Go Back \nChoice: \n")

                                if choice_lvl_4 == 1:
                                    ec2.get_keypair_list(ec2_conn)
                                    keypair = raw_input("Please enter keypair from above list:\n")
                                    os = "linux"
                                    ec2.launch_instance(ec2_conn, os, keypair)
                                    time.sleep(3)
                                    loop_lvl_4 = 0
                                elif choice_lvl_4 == 2:
                                    ec2.get_keypair_list(ec2_conn)
                                    keypair = raw_input("Please enter keypair from above list:\n")
                                    os = "windows"
                                    ec2.launch_instance(ec2_conn, os, keypair)
                                    time.sleep(3)
                                    loop_lvl_4 = 0
                                elif choice_lvl_4 == 3:
                                    loop_lvl_4 = 0
                                else:
                                    print "Please enter number between 1 and 3 only"
                                    time.sleep(2)

                        elif choice_lvl_3 == 6:
                            loop_lvl_3 = 0

                elif choice_lvl_2 == 2:
                    loop_lvl_3 = 1
                    while loop_lvl_3 == 1:
                        choice_lvl_3 = input("1) List running instances \n2) Go Back \nChoice: \n")
                        if choice_lvl_3 == 1:
                            openS.list_run_nodes(compute_driver)
                            time.sleep(3)
                        if choice_lvl_3 == 2:
                            loop_lvl_3 = 0

                elif choice_lvl_2 == 3:
                    loop_lvl_2 = 0

                else:
                    print "Please enter number between 1 and 3 only"
                    time.sleep(2)

        elif choice_lvl_1 == 2:
            loop_lvl_2 = 1
            while loop_lvl_2 == 1:
                choice_lvl_2 = input("Please choose your provider:\n1) AWS \n2) OpenStack \n3) MainMenu \nChoice: \n")
                loop_lvl_3 = 1

                if choice_lvl_2 == 1:
                    provider = "AWS"
                elif choice_lvl_2 == 2:
                    provider = "OpenStack"
                elif choice_lvl_2 == 3:
                    loop_lvl_3 = 0
                    loop_lvl_2 = 0
                else:
                    print "Please enter number between 1 and 3 only"
                    time.sleep(3)

                while loop_lvl_3 == 1:
                    choice_lvl_3 = input("Please select service required:\n1) List all buckets \n"
                                         "2) List all objects in buckets \n3) Upload Object \n4) Download an Object \n"
                                         "5) Delete an Object \n6) Go back \nChoice: \n")

                    if choice_lvl_3 == 1:
                        if provider == "AWS":
                            s3.list_buckets(s3_conn)
                            time.sleep(3)
                        elif provider == "OpenStack":
                            openS.list_all_containers(storage_driver)
                            time.sleep(3)

                    elif choice_lvl_3 == 2:
                        loop_lvl_4 = 1

                        while loop_lvl_4 == 1:
                            choice_lvl_4 = input("1) From all buckets \n2) Enter bucket name \n3) Go Back \nChoice: \n")

                            if choice_lvl_4 == 1:
                                if provider == "AWS":
                                    s3.list_all_files(s3_conn)
                                elif provider == "OpenStack":
                                    openS.list_all_buckets_objects(storage_driver)
                                time.sleep(5)
                                loop_lvl_4 = 0
                            elif choice_lvl_4 == 2:
                                if provider == "AWS":
                                    s3.list_buckets(s3_conn)
                                    bucket_name = raw_input("Enter bucket name: \n")
                                    s3.list_files(s3_conn, bucket_name)
                                elif provider == "OpenStack":
                                    openS.list_all_containers(storage_driver)
                                    bucket_name = raw_input("Enter bucket name: \n")
                                    openS.list_buckets_objects(storage_driver, bucket_name)
                                time.sleep(5)
                                loop_lvl_4 = 0
                            elif choice_lvl_4 == 3:
                                loop_lvl_4 = 0
                            else:
                                print "Please enter number between 1 and 3 only"
                                time.sleep(2)

                    elif choice_lvl_3 == 3:
                        key_name = raw_input("Please enter a name for the object: \n")
                        fp = raw_input("Please enter full path of the object: \n")
                        if provider == "AWS":
                            s3.list_buckets(s3_conn)
                            bucket_name = raw_input("Please enter name of bucket: \n")
                            s3.upload_file(conn=s3_conn, bucket_name=bucket_name, key_name=key_name, file_path=fp)
                        elif provider == "OpenStack":
                            openS.list_all_containers(storage_driver)
                            bucket_name = raw_input("Please enter name of bucket: \n")
                            openS.upload_object(storage_driver, bucket_name, key_name, fp)
                        time.sleep(3)

                    elif choice_lvl_3 == 4:
                        fp = raw_input("Please enter full path of folder you want the object downloaded to: \n")
                        if provider == "AWS":
                            s3.list_buckets(s3_conn)
                            bucket_name = raw_input("Please enter name of bucket: \n")
                            s3.list_files(s3_conn, bucket_name)
                            key_name = raw_input("Please enter name of the object you want to download: \n")
                            s3.download_file(conn=s3_conn, bucket_name=bucket_name, file_name=key_name,
                                             path=fp)
                        elif provider == "OpenStack":
                            openS.list_all_containers(storage_driver)
                            bucket_name = raw_input("Please enter name of bucket: \n")
                            openS.list_buckets_objects(storage_driver, bucket_name)
                            key_name = raw_input("Please enter name of the object you want to download: \n")
                            openS.download_object(storage_driver, bucket_name, key_name, fp)
                        time.sleep(3)

                    elif choice_lvl_3 == 5:
                        if provider == "AWS":
                            s3.list_buckets(s3_conn)
                            bucket_name = raw_input("Please enter name of bucket: \n")
                            s3.list_files(s3_conn, bucket_name)
                            key_name = raw_input("Please enter name of the object you want to delete: \n")
                            s3.delete_file(s3_conn, bucket_name, key_name)
                        elif provider == "OpenStack":
                            openS.list_all_containers(storage_driver)
                            bucket_name = raw_input("Please enter name of bucket: \n")
                            openS.list_buckets_objects(storage_driver, bucket_name)
                            key_name = raw_input("Please enter name of the object you want to delete:")
                            openS.delete_object(storage_driver, bucket_name, key_name)
                        time.sleep(3)

                    elif choice_lvl_3 == 6:
                        loop_lvl_3 = 0

                    else:
                        print "Please enter number between 1 and 6"
                        time.sleep(2)

        elif choice_lvl_1 == 3:
            loop_lvl_2 = 1
            while loop_lvl_2 == 1:
                choice_lvl_2 = input("Please choose a service:\n1) Display all available metrics for an EC2 instance "
                                     "\n2) Enable CPU under-utilisation alarm \n3) MainMenu \nChoice: \n")

                if choice_lvl_2 == 1:
                    ec2.list_run_instances(ec2_conn)
                    instance_id = raw_input("Please choose an instance ID from the above list: \n")
                    cW.enable_specific_cw(ec2_conn, instance_id)
                    print "Preparing list..."
                    time.sleep(5)
                    cW.metric_list(cW_conn, instance_id)
                    time.sleep(5)

                elif choice_lvl_2 == 2:
                    ec2.list_run_instances(ec2_conn)
                    instance_id = raw_input("Please choose an instance ID from above list: \n")
                    email = raw_input("Please enter a valid e-mail address: \n")
                    cW.enable_specific_cw(ec2_conn, instance_id)
                    cW.cw_alarm(cW_conn, instance_id, email)
                    time.sleep(3)

                elif choice_lvl_2 == 3:
                    loop_lvl_2 = 0

                else:
                    print "Please enter number between 1 and 3"
                    time.sleep(2)

        elif choice_lvl_1 == 4:
            loop_lvl_2 = 1
            while loop_lvl_2 == 1:
                choice_lvl_2 = input("Please choose a service:\n1) Create new AutoScale group \n"
                                     "2) List group instances \n3) Create scale-up alarm \n4) MainMenu \nChoice: \n")

                if choice_lvl_2 == 1:
                    loop_lvl_3 = 1
                    while loop_lvl_3 == 1:
                        choice_lvl_3 = input("1) Use existing launch configuration "
                                             "\n2) Create new launch configuration "
                                             "\n3) Go back \nChoice: \n")
                        if choice_lvl_3 == 1:
                            autoS.list_all_launch_configs(autoS_conn)
                            lc_name = raw_input("Enter launch configuration name: \n")
                            loop_lvl_3 = 0
                        elif choice_lvl_3 == 2:
                            lc_name = raw_input("Enter a name for new launch configuration: \n")
                            print "\n"
                            ec2.get_keypair_list(ec2_conn)
                            keypair = raw_input("Enter name of the keypair you would like to use from above list: \n")
                            autoS.launch_config(autoS_conn, lc_name, keypair)
                            loop_lvl_3 = 0
                        elif choice_lvl_3 == 3:
                            loop_lvl_3 = 0
                        else:
                            print "Select number between 1 and 3 only"
                    group_name = raw_input("Enter a name for the group: \n")
                    autoS.create_autoscale_group(autoS_conn, lc_name, group_name)
                    time.sleep(5)

                elif choice_lvl_2 == 2:
                    autoS.list_all_groups(autoS_conn)
                    group_name = raw_input("Enter group name from above list: \n")
                    autoS.list_group_instances(ec2_conn, autoS_conn, group_name)
                    time.sleep(5)

                elif choice_lvl_2 == 3:
                    autoS.list_all_groups(autoS_conn)
                    group_name = raw_input("Enter group name from above list: \n")
                    autoS.scale_up_alarm(autoS_conn, group_name, cW_conn)
                    time.sleep(5)

                elif choice_lvl_2 == 4:
                    loop_lvl_2 = 0

                else:
                    print "Please enter number between 1 and 4"

        elif choice_lvl_1 == 5:
            loop_lvl_2 = 1
            while loop_lvl_2 == 1:
                choice_lvl_2 = input("1) Start CloudTrail \n2) Go Back \nChoice: \n")
                if choice_lvl_2 == 1:
                    s3.list_buckets(s3_conn)
                    bucket_name = raw_input("Please enter the name of the S3 bucket for the logs: \n")
                    trail = raw_input("Enter a name for the new trail: \n")
                    cTrail.create_trail(cTrail_conn, bucket_name, trail)
                    time.sleep(3)
                elif choice_lvl_2 == 2:
                    loop_lvl_2 = 0
                else:
                    print "Please enter 1 or 2 only"
                    time.sleep(2)

        elif choice_lvl_1 == 6:
            loop_lvl_1 = 0

        else:
            print "Please enter number between 1 and 6 only"
            time.sleep(2)

    print "Thank you for using CloudTools, Goodbye."


main()
