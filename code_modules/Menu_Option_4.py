# Fourth CloudTools menu option class. Subclass of Main_Menu.

import time
import boto
from Main_Menu import Main_Menu


# noinspection PyUnboundLocalVariable
class menu_4(Main_Menu):

    def __init__(self):
        """Constructor. Inherits from superclass."""
        Main_Menu.__init__(self)

    def main_menu(self):
        """Menu for management of AWS Auto Scaling services"""
        loop_lvl_2 = 1
        # displays first menu: service choice
        while loop_lvl_2 == 1:
            choice_lvl_2 = input("\nPlease choose a service:\n1) Create new AutoScale group \n"
                                 "2) List group instances \n3) Create scale-up alarm \n4) MainMenu \nChoice: \n")

            # service choice option is 1, display launch config options menu
            if choice_lvl_2 == 1:
                loop_lvl_3 = 1
                while loop_lvl_3 == 1:
                    choice_lvl_3 = input("\n1) Use existing launch configuration "
                                         "\n2) Create new launch configuration "
                                         "\n3) Go back \nChoice: \n")

                    # if launch config option 1, display list of available configs
                    if choice_lvl_3 == 1:
                        l_list = self.autoS_conn.get_all_launch_configurations()
                        if any(l_list):         # if launch configs are associated with this account
                            self.autoS.list_all_launch_configs(self.autoS_conn)
                            lc_name = raw_input("Enter launch configuration name: \n")
                            loop_lvl_3 = 0
                        else:           # if no launch configs found
                            print "No existing launch configurations"

                    # if launch config option 2, create new
                    elif choice_lvl_3 == 2:
                        lc_name = raw_input("Enter a name for new launch configuration: \n")
                        print "\n"
                        self.ec2.get_keypair_list(self.ec2_conn)
                        keypair = raw_input("Enter name of the keypair you would like to use from above list: \n")
                        try:
                            self.autoS.launch_config(self.autoS_conn, lc_name, keypair)
                        except boto.exception.EC2ResponseError:
                            print "Keypair not recognised"
                        loop_lvl_3 = 0

                    # if launch config option 3, exit loop
                    elif choice_lvl_3 == 3:
                        loop_lvl_3 = 0

                    # choice out of range
                    else:
                        print "Select number between 1 and 3 only"

                group_name = raw_input("Enter a name for the group: \n")
                self.autoS.create_autoscale_group(self.autoS_conn, lc_name, group_name)
                time.sleep(5)

            # service choice option is 2, list instances in a particular group
            elif choice_lvl_2 == 2:
                g_list = self.autoS_conn.get_all_groups()
                if any(g_list):  # if groups are associated with this account
                    self.autoS.list_all_groups(self.autoS_conn)
                    group_name = raw_input("Enter group name from above list: \n")
                    self.autoS.list_group_instances(self.ec2_conn, self.autoS_conn, group_name)
                else:  # if no groups associated
                    print "No groups available"
                time.sleep(5)

            # service choice option is 3, create scale-up alarm on particular group
            elif choice_lvl_2 == 3:
                g_list = self.autoS_conn.get_all_groups()
                if any(g_list):                         # if groups are associated with this account
                    self.autoS.list_all_groups(self.autoS_conn)
                    group_name = raw_input("Enter group name from above list: \n")
                    self.autoS.scale_up_alarm(self.autoS_conn, group_name, self.cW_conn)
                else:      # if no groups associated
                    print "No groups available"
                time.sleep(5)

            # service choice option is 4, exit loop
            elif choice_lvl_2 == 4:
                loop_lvl_2 = 0

            # choice out of range
            else:
                print "Please enter number between 1 and 4"
