#!/usr/bin/env python
"""
This is a console-driven menu program for management of some AWS and OpenStack cloud services
"""

import time
from Menu_Option_1 import menu_1
from Menu_Option_2 import menu_2
from Menu_Option_3 import menu_3
from Menu_Option_4 import menu_4
from Menu_Option_5 import menu_5


def main():

    menu1 = menu_1()
    menu2 = menu_2()
    menu3 = menu_3()
    menu4 = menu_4()
    menu5 = menu_5()

    # loop_lvl_1 displays the initial menu options
    loop_lvl_1 = 1
    while loop_lvl_1 == 1:
        # print initial menu options
        print "\nWelcome to CloudTools. \nPlease make a selection by " \
              "entering the number of your chosen menu item below.\n" \
              "Your options are:\n" \
              "1) Compute \n2) Storage \n3) CloudWatch Monitoring \n" \
              "4) AutoScaling \n5) CloudTrail \n6) Quit CloudTools"

        choice_lvl_1 = input("Choose your option: \n")
        if choice_lvl_1 == 1:
            menu1.main_menu()

        elif choice_lvl_1 == 2:
            menu2.main_menu()

        elif choice_lvl_1 == 3:
            menu3.main_menu()

        elif choice_lvl_1 == 4:
            menu4.main_menu()

        elif choice_lvl_1 == 5:
            menu5.main_menu()

        elif choice_lvl_1 == 6:
            loop_lvl_1 = 0

        else:
            print "Please enter number between 1 and 6 only"
            time.sleep(2)

    print "Thank you for using CloudTools, Goodbye."


main()

"""
lines 6 - 11: Import all required modules

line 14: Create the main method, i.e. the application

lines 16 - 20: instantiate the menu option objects

line 23: create loop variable
lines 24 - 31: while the loop is set to 1; print the menu to screen
lines 32 - 46: Reads in user input and calls relevant menu object
lines 48 - 49: If user hits 6, exit the loop and end the application
lines 51 - 53: If user enters a character not stated in the menu, print
                error message
line 55: prints goodbye message when application is ended

line 58: calls the main method
"""
