# Class for programatically manipulating OpenStack services
class OpenStack:

    def __init__(self):
        """constructor"""

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
                print b
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
            dlkey = conn.download_object(obj=key, destination_path=dest_path)
            if dlkey:
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
        key = conn.get_object(container_name = bucket_name, object_name = key_name)
        if key:
            del_ob = conn.delete_object(obj=key)
            if del_ob:
                print "Object %s has been deleted" % key.name
            else:
                print "Error deleting object"
        else:
            print "Object not found"

"""
list instances
line 9: Gets a list of all nodes (instances) associated with this OpenStack account 
        by calling the list_nodes method on the openstack compute driver object.
line 10: If nodes have been retrieved
line 11: Initialises count variable to 0
line 13: loops through node list
line 14: loops through the key value pairs in the extra attribute (type = dictionary) of the node.
        It calls the iteritems method; a built-in python method for iterating over dictionaries
line 15: if the value u"active" is present (i.e. if the instance is running)
line 16: prints node information to screen (including count variable)
line 17: increments count variable with each iteration of the node list for loops
lines 18/19: if no nodes are retrieved, prints error message

get container list
line 23: gets a list of all containers (buckets) by calling list_containers method on openstack
        storage driver object.
line 24: if containers are retrieved
line 26/27: loops through container list and print container information
line 28/29: if no containers are found, prints error message

get objects
line 33: retrieves container object by calling get_container method on OpenStack storage driver
        object using its name as a parameter
line 34: if container is found
line 35: gets list of objects by calling list_container_objects method on the storage driver object
        and passing in the container object as a parameter
line 36: if the objects list is populated
lines 38/39: loops through object list and prints name of each object
lines 40/41: if no objects in container, prints error message
lines 42/43: if container not found, prints error message

get all objects
lines 45-58: As above but returns list of all containers and loops through container list, printing
            all objects in each container

download
line 63: Retrieves object (key) by calling get_object method on the storage driver object and passing
        the container name and key name as parameters
line 64: if object has been retrieved
line 65: downloads the object to the specified destination by calling the download_object method on
        the storage driver object and passing the key object and destination path as parameters
lines 66/67: if the file has been downloaded, print success message

upload:
"""
