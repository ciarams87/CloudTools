# Fifth CloudTools menu option class. Subclass of Main_Menu.

import time
import boto
from Main_Menu import Main_Menu


# noinspection PyUnresolvedReferences
class menu_5(Main_Menu):

    def __init__(self):
        """Constructor. Inherits from superclass"""
        Main_Menu.__init__(self)

    def main_menu(self):
        """Menu for management of AWS Cloud Trail services"""
        loop_lvl_2 = 1
        while loop_lvl_2 == 1:
            # displays first menu: service choice
            choice_lvl_2 = input("\n1) Start CloudTrail \n2) Go Back \nChoice: \n")

            # service option 1, display bucket choice menu
            if choice_lvl_2 == 1:
                choice_lvl_3 = input("\n1) Existing Bucket \n2) New Bucket \nChoice: \n")

                # bucket choice option 1, show list of existing buckets
                if choice_lvl_3 == 1:
                    b_list = self.s3_conn.get_all_buckets()
                    if any(b_list):
                        self.s3service.list_buckets(self.s3_conn)
                        bucket_name = raw_input("Please enter the name of the S3 bucket for the logs ("
                                                "cannot contain underscores): \n")
                        buck = self.s3_conn.lookup(bucket_name)
                        print "Retrieving bucket..."
                    else:
                        print "No buckets found"
                        time.sleep(2)
                        break
                # bucket choice option 2, create bucket
                elif choice_lvl_3 == 2:
                    b_name = raw_input("Please enter name for your new bucket (must be unique and not contain _): \n")
                    buck = self.s3service.new_bucket(self.s3_conn, b_name)
                    print "Creating bucket..."

                policy = self.cTrail.acl_policy(buck.name)   # retrieve policy for allowing Cloud Trail logs
                buck.set_policy(policy)                      # set policy to bucket
                time.sleep(3)
                trail = raw_input("Enter a name for the new trail (at least 3 characters): \n")
                try:
                    self.cTrail.create_trail(self.cTrail_conn, buck.name, trail)  # create trail
                except boto.cloudtrail.exceptions.InvalidTrailNameException:      # if trail name invalid
                    print "Trail names must have at least 3 characters"
                except boto.cloudtrail.exceptions.InvalidS3BucketNameException:   # if underscores etc. in bucket name
                    print "Invalid bucket name"
                except boto.cloudtrail.exceptions.InsufficientS3BucketPolicyException:  # if policy not set
                    print "Bucket is not authorised for Cloud Trail logs"
                time.sleep(3)

            # service option 2, exit loop
            elif choice_lvl_2 == 2:
                loop_lvl_2 = 0

            # choice out of range
            else:
                print "Please enter 1 or 2 only"
                time.sleep(2)
