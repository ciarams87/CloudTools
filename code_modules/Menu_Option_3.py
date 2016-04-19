# Third CloudTools menu option class. Subclass of Main_Menu.
import time
from Main_Menu import Main_Menu


class menu_3(Main_Menu):

    def __init__(self):
        """Constructor. Inherits from superclass."""
        Main_Menu.__init__(self)

    def main_menu(self):
        """Menu for management of AWS monitoring services (Cloud Watch)"""
        loop_lvl_2 = 1
        while loop_lvl_2 == 1:
            # displays first menu: service choice
            choice_lvl_2 = input("\nPlease choose a service:\n1) Display all available metrics for an EC2 instance "
                                 "\n2) Enable CPU under-utilisation alarm \n3) MainMenu \nChoice: \n")

            # if service choice option is 1, show list of instances for which cloudwatch metrics are available
            if choice_lvl_2 == 1:
                i_list = self.ec2_conn.get_only_instances()
                if any(i_list):                             # if instances are associated with the account
                    instance_id = self.check_instance_user_input()  # check ID is entered correctly
                    self.cW.enable_specific_cw(self.ec2_conn, instance_id)  # enable cw monitoring on the instance
                    print "Preparing list..."
                    time.sleep(5)                 # allow time for the cw monitoring to take effect
                    self.cW.metric_list(self.cW_conn, instance_id)  # print metric list
                    time.sleep(5)
                else:
                    print "No instances available"

            # if service choice option is 2, enable CPU alarm
            elif choice_lvl_2 == 2:
                i_list = self.ec2_conn.get_only_instances()
                if any(i_list):             # if any instances associated with this account
                    instance_id = self.check_instance_user_input()  # check user entered ID correctly
                    email = raw_input("Please enter a valid e-mail address: \n")  # enter email address
                    self.cW.enable_specific_cw(self.ec2_conn, instance_id)  # enable cw monitoring
                    self.cW.cw_alarm(self.cW_conn, instance_id, email)  # create alarm
                    time.sleep(3)
                else:
                    print "No instances found to monitor"  # if no instances found

            # if service choice option is 3, exit loop
            elif choice_lvl_2 == 3:
                loop_lvl_2 = 0

            # if character entered is outside of range
            else:
                print "Please enter number between 1 and 3"
                time.sleep(2)
