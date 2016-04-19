# Class for programatically manipulating OpenStack services

# noinspection PyMethodMayBeStatic


class OpenStack:

    def __init__(self):
        """constructor"""

    def create_node(self, conn):
        """Creates a new cirrOS backed instance"""
        images = conn.list_images()
        sizes = conn.list_sizes()
        size = [s for s in sizes if s.ram == 512][0]
        image = [i for i in images if i.name == 'cirros'][0]
        node = conn.create_node(name='test node', image=image, size=size)
        print "Instance has been created: ", node.name, node.id

    def list_run_nodes(self, conn):
        """ Lists all running OpenStack Instances"""
        nodes = conn.list_nodes()
        if nodes:
            count = 0
            print '\nRunning OpenStack Instances: '
            for node in nodes:
                for k, v in node.extra.iteritems():
                    if v == u'active':
                        print count, node.name, node.id, k, ":", v
                        count += 1
        else:
            print "No instances found"

    def list_all_containers(self, conn):
        """ Lists all containers associated with this account """
        buckets = conn.list_containers()
        if buckets:
            print '\nAvailable OpenStack Containers: '
            for b in buckets:
                print b.name
        else:
            print "No Containers found"

    def list_buckets_objects(self, conn, bucket_name):
        """ Lists objects in a given container """
        container = conn.get_container(bucket_name)
        if container:
            objects = conn.list_container_objects(container)
            if objects:
                print '\nObjects in %s:' % container.name
                for o in objects:
                    print o.name
            else:
                print "no objects found in container"
        else:
            print "Container not found"

    def list_all_buckets_objects(self, conn):
        """ Lists objects in all containers """
        containers = conn.list_containers()
        if containers:
            for container in containers:
                print '\nObjects in %s:' % container.name
                objects = conn.list_container_objects(container)
                if objects:
                    for o in objects:
                        print o.name
                else:
                    print "no objects found in container"
        else:
            print "No containers found"

    def download_object(self, conn, bucket_name, key_name, dest_path):
        """ Downloads an object from an OpenStack container to a given location """
        key = conn.get_object(container_name=bucket_name, object_name=key_name)
        if key:
            dl_file = dest_path + "\\" + key.name
            dl_key = conn.download_object(obj=key, destination_path=dl_file)
            if dl_key:
                print 'Key %s has been downloaded' % key_name
        else:
            print "Object not found"

    def upload_object(self, conn, bucket_name, new_key_name, src_path):
        """ Uploads an object from a given source to an OpenStack container"""
        bucket = conn.get_container(bucket_name)
        if bucket:
            ob = conn.upload_object(file_path=src_path, container=bucket, object_name=new_key_name)
            if ob:
                print "Object %s has been uploaded" % ob.name
            else:
                print "Error uploading object"
        else:
            print "container not found"

    def delete_object(self, conn, bucket_name, key_name):
        """ Deletes an object from an OpenStack container """
        key = conn.get_object(container_name=bucket_name, object_name=key_name)
        if key:
            del_ob = conn.delete_object(obj=key)
            if del_ob:
                print "Object %s has been deleted" % key.name
            else:
                print "Error deleting object"
        else:
            print "Object not found"

    def create_new_container(self, conn, bucket_name):
        """Creates a new OpenStack Swift container"""
        bucket = conn.create_container(bucket_name)
        return bucket

"""
OpenStack is a private cloud software suite that controls large pools of compute, storage,
and networking resources throughout a datacenter

line 9: retrieves a list of images available with this account
line 10: retrieves a list of sizes available with this account
line 11: assigns the "size" variable to the first element of the returned sizes list where the ram attribute is 512MB
line 12: assigns the "image" variable to the first element of the returned images list where the name attribute is
         cirros
line 13: creates a new node using the size and image variables

line 18: Gets a list of all nodes (instances) associated with this OpenStack account
        by calling the list_nodes method on the openstack compute driver object.
line 19: If nodes have been retrieved
line 20: Initialises count variable to 0
line 22: loops through node list
line 23: loops through the key value pairs in the extra attribute (type = dictionary) of the node.
        It calls the iteritems method; a built-in python method for iterating over dictionaries
line 24: if the value u"active" is present (i.e. if the instance is running)
line 25: prints node information to screen (including count variable)
line 26: increments count variable with each iteration of the node list for loops
lines 27/28: if no nodes are retrieved, prints error message

get container list
line 23: gets a list of all containers (buckets) by calling list_containers method on openstack
        storage driver object.
line 24: if containers are retrieved
line 26/27: loops through container list and print container information
line 28/29: if no containers are found, prints error message

line 32: list all containers
line 33: if container retrieval successful
line 35/36: loop through container list and print each
line 37/38: if no containers found, print error message

line 42: retrieves container object by calling get_container method on OpenStack storage driver
        object using its name as a parameter
line 43: if container is found
line 44: gets list of objects by calling list_container_objects method on the storage driver object
        and passing in the container object as a parameter
line 45: if the objects list is populated
lines 47/48: loops through object list and prints name of each object
lines 49/50: if no objects in container, prints error message
lines 51/52: if container not found, prints error message

lines 54-67: As above but returns list of all containers and loops through container list, printing
            all objects in each container

line 72: Retrieves object (key) by calling get_object method on the storage driver object and passing
        the container name and key name as parameters
line 73: if object has been retrieved
line 74: downloads the object to the specified destination by calling the download_object method on
        the storage driver object and passing the key object and destination path as parameters
lines 75/76: if the file has been downloaded, print success message
lines 77/78: otherwise, print error message

line 82: retrieve specified bucket
line 83: if bucket retrieval successful
line 84: upload object to bucket from specified source path
line 85/86: if successful, success message
line 87-90: Error messages

line 94: retrieve object from container
line 95-100: if retrieved, delete object. If delete successful, success message; else print error message
line 101-102: if object cannot be retrieved

lines 110-111: creates a new container and returns the container object 
"""
