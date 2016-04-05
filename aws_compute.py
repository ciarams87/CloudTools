# Class for programmatically manipulating AWS Compute (EC2 and Volumes) functions

class AWS_Compute:

    def __init__(self):
        """ AWS Compute Class Constructor """

    def list_run_instances(self, conn, ins_id = ''):
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
                else:
                    print 'No running instances found'
                    break
            else:
                print 'Instance ID not found'
                break

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
        instances = conn.get_only_instances(instance_ids=[instance_id])
        if instances:
            for i in instances:
                if i.state == u'running':
                    test = conn.stop_instances(instance_ids=[i.id])
                    if test:
                        print 'instance %s has been stopped' % i.id
                    else:
                        print 'cannot stop instance %s' % i.id
                else:
                    print 'instance %s is not running' % i.id
        else:
            print 'instance not found'

    def launch_instance(self, conn, os, keypair):
        """ Launch an instance without a known AMI by searching for an image """
        if os == 'linux':
            filters_lin = {'virtualization-type': 'hvm', 'root-device-type': 'ebs', 'description':'Amazon Linux AMI 2016.03.0 x86_64 HVM GP2'}
            image_list = conn.get_all_images(owners=['amazon'], filters=filters_lin)
        elif os == 'windows':
            filters_win = {'virtualization-type': 'hvm', 'root-device-type': 'ebs', 'description':'Microsoft Windows Server 2012 R2 RTM 64-bit Locale English AMI provided by Amazon'}
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
        vols = conn.get_all_volumes(volume_id)
        if vols:
            for v in vols:
                if v.status == u'available':
                    new = v.attach(instance_id, '/dev/sda2')
                    if new:
                        print 'Volume %s successfully attached to %s' % (volume_id, instance_id)
                    else:
                        print 'Unable to attach %s to instance %s' % (volume_id, instance_id)
                else:
                    print 'Volume unavailable'
        else:
            print 'Volume not found'

    def detach_volume(self,conn,volume_id):
        """ Detaches a specific volume """
        vols = conn.get_all_volumes(volume_id)
        if vols:
            for v in vols:
                if v.status == u'in-use':
                    new = v.detach()
                    if new:
                        print 'Volume %s successfully detached' % volume_id
                    else:
                        print 'Unable to detach'
                else:
                    print "Volume already detached"
        else:
            print "Volume not found"

    def list_all_vols(self, conn):
        """ Lists all volumes available for attachment """
        vols = conn.get_all_volumes()
        if vols:
            for v in vols:
                attachmentData = v.attach_data
                print "Volume ID: %s; Status: %s; Availability Zone: %s; Instance Id: %s" \
                      % (v.id, v.status, v.zone, attachmentData.instance_id)
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
        keypairs= conn.get_all_key_pairs()
        for key in keypairs:
            print key.name

    def create_volume(self, conn, size, zone):
        """ Creates a new volume """
        vol = conn.create_volume(size, zone, volume_type="gp2")
        return vol.id

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
line 20,27: break from for loop (line 15)
lines 21 - 24: if no instance id has been provided in method parameters, return information for all running instances
line 25: if an instance id has been specified, but cannot be found in list of returned instances, give error message
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

line 48 - 62: As previous method, but for a particular instance passed in as parameter
            to outer method. Additionally, error messages are given if instance isn't running,
            or if not found.

line 66-73: Checks the 'os' passed in the parameters. if linux/ windows -> calls the get_all_images
            function, passing in specified parameters determining what kind of images to be
            returned. Else statement outputs an error message if os is not recognised.
line 74: Assigns the first element of the returned image_list to variable 'image'
line 75: Launches instance from the image, using parameters defining keypair to be used, instance
        type and availability zone the instance
        should be launched into. Returns Reservation object.
lines 76 - 80: If previous method is successful, loops through the instances list attribute of the
                reservations object and prints instance id to screen. If not, prints error message.

line 84: Retrieves the volume specified in the parameters. Returns list of volume objects.
lines 85-96: If volume retrieval successful, loops through returned list , checks if volume is
            available, if it is, attaches it to specified instance. Prints error messages to
            screen if any of the previous checks fail.

lines 98 - 112: As previous method, but checks if volume is currently attached to an instance, and
                if so, detaches it. Prints error messages if any steps fail.
"""