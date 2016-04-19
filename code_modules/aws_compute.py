# Class for programmatically manipulating AWS Compute (EC2 and Volumes) functions
import time
import boto


# noinspection PyMethodMayBeStatic,PyUnboundLocalVariable
class AWS_Compute:

    def __init__(self):
        """ AWS Compute Class Constructor """

    def list_run_instances(self, conn, ins_id=''):
        """ List running EC2 Instances """
        instances = conn.get_only_instances()
        count = 0
        print 'Running EC2 instances:\n'
        for i in instances:
            if ins_id == i.id:
                if i.state == u'running':
                    print 'Instance Id: %s; Image: %s -> %s; Availability Zone: %s; Launch time: %s' \
                          % (i.id, i.image_id, i.instance_type, i.placement, i.launch_time)
                    break
                else:
                    print 'Instance not running'
                    break
            elif ins_id == '':
                if i.state == u'running':
                    print '%d Instance Id: %s; Image: %s -> %s; Region: %s; Launch time: %s' \
                          % (count, i.id, i.image_id, i.instance_type, i.placement, i.launch_time)
                    count += 1

    def start_instance(self, conn, keypair):
        """ Starts a new instance from known AMI """
        reservation = conn.run_instances("ami-3367d340", key_name=keypair, instance_type="t2.micro")
        if reservation:
            for i in reservation.instances:
                print 'New instance has been created with an id of ', i.id

    def stop_all_instances(self, conn):
        """ Stops all running instances """
        instances = conn.get_only_instances()
        for i in instances:
            if i.state == u'running':
                test = conn.stop_instances(instance_ids=[i.id])
                if test:
                    print 'instance %s has been stopped' % i.id
                else:
                    print 'cannot stop instance %s' % i.id

    def stop_instance(self, conn, instance_id):
        """ Stop a particular instance """
        instances = conn.get_only_instances()
        for i in instances:
            if i.id == instance_id:
                if i.state == u'running':
                    test = conn.stop_instances(instance_ids=[i.id])
                    if test:
                        print 'instance %s has been stopped' % i.id
                    else:
                        print 'cannot stop instance %s' % i.id
                else:
                    print 'instance %s is not running' % i.id

    def launch_instance(self, conn, os, keypair):
        """ Launch an instance without a known AMI by searching for an image """
        if os == 'linux':
            filters_lin = {'virtualization-type': 'hvm', 'root-device-type': 'ebs',
                           'description': 'Amazon Linux AMI 2016.03.0 x86_64 HVM GP2'}
            image_list = conn.get_all_images(owners=['amazon'], filters=filters_lin)
        elif os == 'windows':
            filters_win = {'virtualization-type': 'hvm', 'root-device-type': 'ebs',
                           'description': 'Microsoft Windows Server 2012 R2 RTM 64-bit Locale English AMI provided by '
                                          'Amazon'}
            image_list = conn.get_all_images(owners=['amazon'], filters=filters_win)
        else:
            print "Operating system not recognised, windows or linux only"
        if image_list:
            image = image_list[0]
            reservation = image.run(key_name=keypair, instance_type='t2.micro', placement='eu-west-1a')
            if reservation:
                for i in reservation.instances:
                    print 'New instance has been created with an id of %s' % i.id
            else:
                print 'could not launch instance'

    def attach_volume(self, conn, volume_id, instance_id):
        """ Attaches a volume to an EC2 instance """
        vols = conn.get_all_volumes()
        for v in vols:
            if v.id == volume_id and v.status == u'available':
                try:
                    v.attach(instance_id, '/dev/sda2')
                    print 'Volume %s successfully attached to %s' % (volume_id, instance_id)
                except boto.exception.EC2ResponseError:
                    print 'Unable to attach %s to instance %s' % (volume_id, instance_id)

    def detach_volume(self, conn, volume_id):
        """ Detaches a specific volume """
        vols = conn.get_all_volumes()
        for v in vols:
            if v.id == volume_id and v.status == u'in-use':
                try:
                    v.detach()
                    print 'Volume %s successfully detached' % volume_id
                except boto.exception.EC2ResponseError:
                    print "Unable to detach %s - root volume" % volume_id

    def list_all_vols(self, conn):
        """ Lists all volumes available for attachment """
        vols = conn.get_all_volumes()
        if vols:
            for v in vols:
                attachmentData = v.attach_data
                print "Volume ID: %s; Status: %s; Availability Zone: %s; Instance Id: %s; Device: %s" \
                      % (v.id, v.status, v.zone, attachmentData.instance_id, attachmentData.device)
        else:
            print "No volumes found"

    def list_all_ins(self, conn):
        """ Lists all instances of any status """
        instances = conn.get_only_instances()
        if instances:
            for i in instances:
                print 'Instance Id: %s; Availability Zone: %s; Status: %s' \
                          % (i.id, i.placement, i.state)
        else:
            print "No instances found"

    def get_keypair_list(self, conn):
        """ Returns a list of keypairs associated with this account"""
        keypairs = conn.get_all_key_pairs()
        if keypairs:
            for key in keypairs:
                print key.name
        else:
            print 'No keypairs associated with this account'

    def create_volume(self, conn, size, zone):
        """ Creates a new volume """
        vol = conn.create_volume(size, zone, volume_type="gp2")
        return vol.id

    def check_ins_id(self, conn, ins_id):
        """Checks if a given instance ID corresponds to an instance"""
        instances = conn.get_only_instances()
        id_list = []
        for i in instances:
            if i.id == ins_id:
                id_list.append(i.id)
        if any(id_list):
            return True
        else:
            print 'Instance ID entered incorrectly; please try again'
            time.sleep(2)
            return False

"""

conn = ec2 connection object;
instance ID = the unique identifier of an AWS instance
keypair = amazon keypair needed for connecting to instances;

line 10: def list_instances(self, conn, ins_id = '')
line 12: retrieve all instances associated with this AWS account
        (calls get_only_instances method on EC2connection object)
line 13: initialize count variable for outputting numbered instance info to screen
line 15: loop through instances and extract their info
line 16: if an instance id has been provided, check it against all returned instances and see
            if it's there
line 17: check if instance is running
lines 18, 19: print to screen required details
line 20: break from for loop (line 14)
lines 21 - 23: if instance isn't running: error message and break from loop
lines 24 - 31: if no instance id has been provided in method parameters, return information (as above) for all
            running instances
line 28: increment counter

line 30: def start_instance(self, conn, keypair)
        could be modified to read in ami, instance_type etc from user
line 32: create reservation object by calling the run_instances method on ec2 connection object.
        I have given an ami image id (the only required parameter), the name of the keypair
        (passed in through outer method) and the instance type (defaults to m1.small if not
        specified)
line 33: if the method was successful
line 34: loops through instances-list attribute of the reservations object
line 35: prints information to screen

line 37: def stop_all_instances(self, conn)
lines 39 - 46: Retrieves list of instances. Loops through list. If any instance is running, stops
            instance (using stop_instances method called on ec2 conn object). If successful,
            prints success message. If not, prints error message.

line 48 - 60: As previous method, but for a particular instance passed in as parameter
            to outer method. Additionally, error message is given if instance isn't running.

line 64 - 73: Checks the 'os' passed in the parameters. if linux/ windows -> calls the get_all_images
            function, passing in specified parameters determining what kind of images to be
            returned. Else statement outputs an error message if os is not recognised.
line 75: Assigns the first element of the returned image_list to variable 'image'
line 76: Launches instance from the image, using parameters defining keypair to be used, instance
        type and availability zone the instance
        should be launched into. Returns Reservation object.
lines 77 - 81: If previous method is successful, loops through the instances list attribute of the
                reservations object and prints instance id to screen. If not, prints error message.

line 85: Retrieves all volumes. Returns list of volume objects.
lines 86-92: Loops through returned list , checks if volume corresponds to given volume ID and is
            available, if it is, attaches it to specified instance. Prints error message to
            screen if attachment fails.

lines 94 - 103: As previous method, but checks if volume is currently attached to an instance, and
                if so, detaches it. Prints error message if detachment fails.

lines 106 - 115: Gets a list of volumes, loops through list and prints information on each volume.
             If no volumes found; prints error message

lines 117 - 125: Gets a list of instances; loops through list; print out information on each instance.
                If there are no instances associated with the account - error message

lines 127 - 134: Gets list of keypairs; loops through list and prints name of each

lines 136 - 139: Creates a new volume of specified size in specified zone

lines 141 - 153: Retrieves list of instances, creates a new list variable, and adds the instance ID to
                list variable if it corresponds to the given ID. If the list is populated; i.e. if the ID
                 does correspond - returns True. Else, prints error message and returns false.
"""
