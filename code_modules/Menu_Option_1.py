# First CloudTools menu option class. Subclass of Main_Menu.
import time
import boto
from Main_Menu import Main_Menu


# noinspection PyPep8Naming
class menu_1(Main_Menu):

    def __init__(self):
        """Constructor. Inherits from superclass."""
        Main_Menu.__init__(self)

    def main_menu(self):
        """Menu for management of AWS and OpenStack compute services (EC2 and block storage/ Nova nodes)"""
        loop_lvl_2 = 1
        while loop_lvl_2 == 1:
            # displays first menu: provider choice
            choice_lvl_2 = input("\nPlease choose your provider:\n1) AWS \n2) OpenStack \n3) MainMenu \nChoice: \n")

            # if provider is AWS, display AWS list of options
            if choice_lvl_2 == 1:
                loop_lvl_3 = 1

                while loop_lvl_3 == 1:
                    choice_lvl_3 = input("\nPlease select service required:\n1) List running instances \n"
                                         "2) Start an instance (AMI known)\n3) Stop instances \n4) Manage volumes \n"
                                         "5) Launch new instance (AMI unknown)\n6) Go back \nChoice: \n")

                    # if AWS option 1, display running instances menu
                    if choice_lvl_3 == 1:
                        loop_lvl_4 = 1

                        while loop_lvl_4 == 1:
                            choice_lvl_4 = input("\n1) Enter ID \n2) List all \n3) Go Back \n")

                            # if running instances option 1, invite user to enter ID from a list
                            if choice_lvl_4 == 1:
                                i_list = self.ec2_conn.get_only_instances()
                                # if list is populated i.e. if instances are associated with this account
                                if any(i_list):
                                    # check user input
                                    ins_id = self.check_instance_user_input()
                                    self.ec2.list_run_instances(self.ec2_conn, ins_id)
                                    time.sleep(3)
                                    loop_lvl_4 = 0
                                else:                           # if list isn't populated
                                    print "No instances found"
                                    loop_lvl_4 = 0              # exit loop

                            # if running instances option 2, display all running instances' details
                            elif choice_lvl_4 == 2:
                                self.ec2.list_run_instances(self.ec2_conn)
                                time.sleep(3)
                                loop_lvl_4 = 0

                            # if running instances option 3, exit loop
                            elif choice_lvl_4 == 3:
                                loop_lvl_4 = 0

                            # if none of above options, display error message
                            else:
                                print "Please enter number between 1 and 3 only"
                                time.sleep(2)

                    # if AWS option 2, start a new instance and return instance id
                    elif choice_lvl_3 == 2:
                        # display keypair list
                        self.ec2.get_keypair_list(self.ec2_conn)
                        # if keypair is entered correctly, start instance
                        try:
                            keypair = raw_input("Please enter name of keypair from above list: \n")
                            print "Creating instance..."
                            self.ec2.start_instance(self.ec2_conn, keypair)
                        # otherwise, catch exception and print error message
                        except boto.exception.EC2ResponseError:
                            print "Keypair not recognised"
                        time.sleep(3)

                    # if AWS option 3, display stop instances menu
                    elif choice_lvl_3 == 3:
                        loop_lvl_4 = 1

                        while loop_lvl_4 == 1:
                            choice_lvl_4 = input("\n1) Enter ID \n2) Stop all\n3) Go Back \nChoice: \n")
                            # if stop instance menu option 1, display all instances and get user input
                            if choice_lvl_4 == 1:
                                i_list = self.ec2_conn.get_only_instances()
                                if any(i_list):                             # if instances associated with this account
                                    ins_id = self.check_instance_user_input()        # check user enters ID correctly
                                    self.ec2.stop_instance(self.ec2_conn, ins_id)    # stop instance
                                    time.sleep(3)
                                    loop_lvl_4 = 0
                                else:
                                    print "No instances found"
                                    time.sleep(2)
                                    loop_lvl_4 = 0

                            # if stop instance menu option 2, stop all instances
                            elif choice_lvl_4 == 2:
                                self.ec2.stop_all_instances(self.ec2_conn)
                                time.sleep(3)
                                loop_lvl_4 = 0         # exit loop

                            # if stop instance menu option 3, exit loop
                            elif choice_lvl_4 == 3:
                                loop_lvl_4 = 0

                            # if user selects a number/ character outside of range of options
                            else:
                                print "Please enter number between 1 and 3 only"
                                time.sleep(2)

                    # if AWS option 4, display volume management menu
                    elif choice_lvl_3 == 4:
                        loop_lvl_4 = 1

                        while loop_lvl_4 == 1:
                            choice_lvl_4 = input("\n1) Attach volume \n2) Detach volume \n3) Go Back \nChoice: \n")

                            # if volume management menu choice is 1, display attach menu options
                            if choice_lvl_4 == 1:
                                i_list = self.ec2_conn.get_only_instances()
                                if any(i_list):                      # if instances associated with this account
                                    ins_id = self.check_instance_user_input()  # check user inputs instance ID correctly
                                    loop_lvl_5 = 1

                                    # while loop is set to 1, display attach volume menu
                                    while loop_lvl_5 == 1:
                                        choice_lvl_5 = input("\n1) Attach existing volume \n2) Attach new volume "
                                                             "\nChoice: \n")

                                        # if attach volume menu option 1, display list of volumes and get user input
                                        if choice_lvl_5 == 1:
                                            self.ec2.list_all_vols(self.ec2_conn)
                                            vol_id = raw_input("Enter volume ID (Volume must be 'Available"
                                                               "in same Availability Zone as the instance)): \n")
                                            loop_lvl_5 = 0

                                        # if attach vol menu option 2, get required user input for new volume creation
                                        elif choice_lvl_5 == 2:
                                            size = input("Please enter required size in GiB (Between 1 and 1000):\n")
                                            zone = raw_input("Choose required zone - must be same as instance. "
                                                             "Options are: eu-west-1a; eu-west-1b; eu-west-1c:\n")
                                            vol_id = self.ec2.create_volume(self.ec2_conn, size, zone)
                                            print "Creating volume..."
                                            time.sleep(10)
                                            loop_lvl_5 = 0

                                        # if character outside of range is chosen
                                        else:
                                            print "Please enter 1 or 2 only"
                                            time.sleep(2)

                                    # attach volume, using volume ID of either new or existing volume
                                    # noinspection PyUnboundLocalVariable
                                    self.ec2.attach_volume(self.ec2_conn, vol_id, ins_id)
                                    time.sleep(3)
                                    loop_lvl_4 = 0

                                # if no instances associated with this account
                                else:
                                    print "Cannot attach volumes - no instances found"
                                    loop_lvl_4 = 0

                            # if volume management menu choice is 2, detach specified volume
                            elif choice_lvl_4 == 2:
                                v_list = self.ec2_conn.get_all_volumes()
                                if any(v_list):
                                    self.ec2.list_all_vols(self.ec2_conn)
                                    vol_id = raw_input("Enter volume ID. Please note that it must"
                                                       " not be the root volume: \n")
                                    self.ec2.detach_volume(self.ec2_conn, vol_id)
                                else:
                                    print "No volumes found"
                                time.sleep(3)
                                loop_lvl_4 = 0

                            # if volume management menu choice is 3, exit loop
                            elif choice_lvl_4 == 3:
                                loop_lvl_4 = 0

                            # if character entered is out of range
                            else:
                                print "Please enter number between 1 and 3 only"
                                time.sleep(2)

                    # if AWS option 5, display launch instances menu
                    elif choice_lvl_3 == 5:
                        loop_lvl_4 = 1
                        while loop_lvl_4 == 1:
                            self.ec2.get_keypair_list(self.ec2_conn)
                            keypair = raw_input("Please enter keypair from above list:\n")

                            choice_lvl_4 = input("\n1) Launch Linux Instance \n2) Launch Windows Instance "
                                                 "\n3) Go Back \nChoice: \n")

                            # if launch instances menu option is 1: launch linux machine
                            if choice_lvl_4 == 1:
                                os = "linux"
                                print "Creating Linux instance..."
                                try:
                                    self.ec2.launch_instance(self.ec2_conn, os, keypair)
                                except boto.exception.EC2ResponseError:
                                    print "Keypair not recognised"
                                time.sleep(3)
                                loop_lvl_4 = 0

                            # if launch instances menu option is 2, launch windows instance
                            elif choice_lvl_4 == 2:
                                os = "windows"
                                print "Creating Windows instance..."
                                try:
                                    self.ec2.launch_instance(self.ec2_conn, os, keypair)
                                except boto.exception.EC2ResponseError:
                                    print "Keypair not recognised"
                                time.sleep(3)
                                loop_lvl_4 = 0

                            # if launch instances menu option is 3, exit loop
                            elif choice_lvl_4 == 3:
                                loop_lvl_4 = 0

                            else:
                                print "Please enter number between 1 and 3 only"
                                time.sleep(2)

                    # if AWS option 6, exit loop
                    elif choice_lvl_3 == 6:
                        loop_lvl_3 = 0

                    # if none of the above options, display error message
                    else:
                        print "Please enter number between 1 and 6 only"
                        time. sleep(3)

            # if provider is OpenStack, display OpenStack list of options
            elif choice_lvl_2 == 2:
                loop_lvl_3 = 1
                while loop_lvl_3 == 1:
                    choice_lvl_3 = input("\n1) List running instances \n2) Create node \n3) Go Back \nChoice: \n")

                    # if OpenStack Option 1, show list of running instances
                    if choice_lvl_3 == 1:
                        self.openS.list_run_nodes(self.compute_driver)
                        time.sleep(3)

                    # if OpenStack Option 2, create a node
                    elif choice_lvl_3 == 2:
                        print "Creating new cirrOS-backed node..."
                        self.openS.create_node(self.compute_driver)
                        time.sleep(3)

                    # if OpenStack Option 3, exit loop
                    elif choice_lvl_3 == 3:
                        loop_lvl_3 = 0

                    else:
                        print "Please enter number between 1 and 3 only"

            # if option 3 is chosen, break out of loop and exit the method
            elif choice_lvl_2 == 3:
                loop_lvl_2 = 0

            # if an unrecognised option is chosen, print error message
            else:
                print "Please enter number between 1 and 3 only"
                time.sleep(2)

