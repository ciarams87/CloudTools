# Superclass for menu option classes. Creates all necessary objects for menu functionality.
from Connections import Connections
from aws_storage import aws_S3
from CloudTrail import CloudTrail
from aws_compute import AWS_Compute
from monitoring import CloudWatch
from autoscale import AutoScale
from OpenStackConn import OSConnections
from open_stack import OpenStack


# noinspection PyUnboundLocalVariable
class Main_Menu:
    def __init__(self):
        aws_conn = Connections()
        self.cTrail_conn = aws_conn.ct_connection()
        self.ec2_conn = aws_conn.ec2_connection()
        self.cW_conn = aws_conn.cw_connection()
        self.autoS_conn = aws_conn.as_connection()
        self.s3_conn = aws_conn.s3_connection()

        # AWS Services
        self.ec2 = AWS_Compute()
        self.s3service = aws_S3()
        self.cW = CloudWatch()
        self.autoS = AutoScale()
        self.cTrail = CloudTrail()

        # OpenStack
        OSConn = OSConnections()
        self.openS = OpenStack()
        self.compute_driver = OSConn.os_compute_conn()
        self.storage_driver = OSConn.os_storage_conn()

    def check_instance_user_input(self):
        check = False  # initialise check variable
        while check is False:  # while it is false,
            self.ec2.list_all_ins(self.ec2_conn)  # display instance list and
            ins_id = raw_input("Enter instance ID:\n")  # ask for user input
            # calls check function. If ins id entered correctly, returns True
            check = self.ec2.check_ins_id(self.ec2_conn, ins_id)
        return ins_id
