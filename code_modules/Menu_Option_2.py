# Second CloudTools menu option class. Subclass of Main_Menu.
import time
from Main_Menu import Main_Menu


class menu_2(Main_Menu):

    def __init__(self):
        """Constructor. Inherits from superclass."""
        Main_Menu.__init__(self)

    def main_menu(self):
        """ Menu for management of AWS and OpenStack object storage services (S3 and Swift)"""
        loop_lvl_2 = 1
        # displays first menu: provider choice
        while loop_lvl_2 == 1:
            choice_lvl_2 = input("\nPlease choose your provider:\n1) AWS \n2) OpenStack \n3) MainMenu \nChoice: \n")
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
                # displays second menu: service choice
                choice_lvl_3 = input("\nPlease select service required:\n1) List all buckets \n"
                                     "2) List all objects in buckets \n3) Upload Object \n4) Download an Object \n"
                                     "5) Delete an Object \n6) Create a new bucket \n7) Go back \nChoice: \n")

                # if service choice option is 1, list all the buckets/ containers
                if choice_lvl_3 == 1:
                    if provider == "AWS":
                        self.s3service.list_buckets(self.s3_conn)
                        time.sleep(3)
                    elif provider == "OpenStack":
                        self.openS.list_all_containers(self.storage_driver)
                        time.sleep(3)

                # if service choice option is 2, display file listing menu
                elif choice_lvl_3 == 2:
                    loop_lvl_4 = 1

                    while loop_lvl_4 == 1:
                        choice_lvl_4 = input("\n1) From all buckets \n2) Enter bucket name \n3) Go Back \nChoice: \n")

                        # if file listing menu option 1, list all files from all buckets
                        if choice_lvl_4 == 1:
                            # if provider choice is set to AWS
                            if provider == "AWS":
                                b_list = self.s3_conn.get_all_buckets()
                                if any(b_list):
                                    self.s3service.list_all_files(self.s3_conn)
                                else:
                                    print "No buckets found"
                            # if provider choice is set to OpenStack
                            elif provider == "OpenStack":
                                b_list = self.storage_driver.list_containers()
                                if any(b_list):
                                    self.openS.list_all_buckets_objects(self.storage_driver)
                                else:
                                    print "No containers found"
                            time.sleep(5)
                            loop_lvl_4 = 0

                        # if file listing menu option 2, list all files from particular bucket
                        elif choice_lvl_4 == 2:
                            # if provider is set to AWS
                            if provider == "AWS":
                                b_list = self.s3_conn.get_all_buckets()
                                if any(b_list):
                                    self.s3service.list_buckets(self.s3_conn)
                                    bucket_name = raw_input("Enter bucket name: \n")
                                    self.s3service.list_files(self.s3_conn, bucket_name)
                                else:
                                    print "No buckets found"
                            # if provider is set to OpenStack
                            elif provider == "OpenStack":
                                b_list = self.storage_driver.list_containers()
                                if any(b_list):
                                    self.openS.list_all_containers(self.storage_driver)
                                    bucket_name = raw_input("Enter bucket name: \n")
                                    self.openS.list_buckets_objects(self.storage_driver, bucket_name)
                                else:
                                    print "No containers found"
                            time.sleep(5)
                            loop_lvl_4 = 0

                        # if file listing menu option 2, exit the loop
                        elif choice_lvl_4 == 3:
                            loop_lvl_4 = 0

                        else:
                            print "Please enter number between 1 and 3 only"
                            time.sleep(2)

                # if service choice option is 3, get required user input for uploading a file
                elif choice_lvl_3 == 3:
                    key_name = raw_input("Please enter a name for the object: \n")
                    fp = raw_input("Please enter full path of the object: \n")
                    # if provider is set to AWS
                    if provider == "AWS":
                        b_list = self.s3_conn.get_all_buckets()
                        if any(b_list):                         # if buckets are associated with this account
                            self.s3service.list_buckets(self.s3_conn)
                            bucket_name = raw_input("Please enter name of bucket: \n")
                            self.s3service.upload_file(conn=self.s3_conn, bucket_name=bucket_name, key_name=key_name,
                                                       file_path=fp)
                        else:                   # if no buckets available, print error message
                            print "No available buckets"
                    # if provider is set to OpenStack
                    elif provider == "OpenStack":
                        b_list = self.storage_driver.list_containers()
                        if any(b_list):                     # if containers are associated with this account
                            self.openS.list_all_containers(self.storage_driver)
                            bucket_name = raw_input("Please enter name of bucket: \n")
                            self.openS.upload_object(self.storage_driver, bucket_name, key_name, fp)
                        else:
                            print "No available containers"
                    time.sleep(3)

                # if service choice option is 4, get required user input for downloading file
                elif choice_lvl_3 == 4:
                    fp = raw_input("Please enter full path of folder you want the object downloaded to: \n")
                    # if provider is set to AWS
                    if provider == "AWS":
                        b_list = self.s3_conn.get_all_buckets()
                        if any(b_list):                               # if buckets available
                            self.s3service.list_buckets(self.s3_conn)
                            bucket_name = raw_input("Please enter name of bucket from above list: \n")
                            buck = self.s3_conn.lookup(bucket_name)   # check bucket name is correct
                            if buck:
                                f_list = buck.get_all_keys()
                                if any(f_list):                       # if there are files/ objects in the chosen bucket
                                    self.s3service.list_files(self.s3_conn, bucket_name)
                                    key_name = raw_input("Please enter name of the object you want to download: \n")
                                    self.s3service.download_file(conn=self.s3_conn, bucket_name=bucket_name,
                                                                 file_name=key_name, path=fp)
                                else:
                                    print "No files in this bucket"
                            else:
                                print "Bucket name was entered incorrectly"
                        else:
                            "No buckets found"
                    # if provider is set to OpenStack
                    elif provider == "OpenStack":
                        b_list = self.storage_driver.list_containers()
                        if any(b_list):
                            self.openS.list_all_containers(self.storage_driver)
                            bucket_name = raw_input("Please enter name of bucket: \n")
                            self.openS.list_buckets_objects(self.storage_driver, bucket_name)
                            key_name = raw_input("Please enter name of the object you want to download: \n")
                            self.openS.download_object(self.storage_driver, bucket_name, key_name, fp)
                        else:
                            print "No containers found"
                    time.sleep(3)

                # if service choice option is 5, get required user input for uploading file
                elif choice_lvl_3 == 5:
                    # if provider is set to AWS. Similar process as Download Object option.
                    if provider == "AWS":
                        b_list = self.s3_conn.get_all_buckets()
                        if any(b_list):
                            self.s3service.list_buckets(self.s3_conn)
                            bucket_name = raw_input("Please enter name of bucket: \n")
                            buck = self.s3_conn.lookup(bucket_name)
                            if buck:
                                f_list = buck.get_all_keys()
                                if any(f_list):
                                    self.s3service.list_files(self.s3_conn, bucket_name)
                                    key_name = raw_input("Please enter name of the object you want to delete: \n")
                                    self.s3service.delete_file(self.s3_conn, bucket_name, key_name)
                                else:
                                    print "No files found"
                            else:
                                print "Bucket name entered incorrectly"
                        else:
                            print "No buckets found"

                    elif provider == "OpenStack":
                        b_list = self.storage_driver.list_containers()
                        if any(b_list):
                            self.openS.list_all_containers(self.storage_driver)
                            bucket_name = raw_input("Please enter name of bucket: \n")
                            self.openS.list_buckets_objects(self.storage_driver, bucket_name)
                            key_name = raw_input("Please enter name of the object you want to delete:\n")
                            self.openS.delete_object(self.storage_driver, bucket_name, key_name)
                        else:
                            print "No containers found"
                    time.sleep(3)

                # if service choice option is 6, get user to choose name for new bucket
                elif choice_lvl_3 == 6:
                    bucket_name = raw_input("Please enter name of bucket (must be globally unique):\n")
                    if provider == "AWS":
                        new_b = self.s3service.new_bucket(self.s3_conn, bucket_name)

                    elif provider == "OpenStack":
                        new_b = self.openS.create_new_container(self.storage_driver, bucket_name)

                    if new_b:
                        print "Bucket %s has been created" % bucket_name
                    time.sleep(2)

                # if service choice option is 7, exit loop
                elif choice_lvl_3 == 7:
                    loop_lvl_3 = 0

                else:
                    print "Please enter number between 1 and 7"
                    time.sleep(2)
