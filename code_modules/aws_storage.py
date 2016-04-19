# Class for programmatically manipulating AWS's S3 service
import os.path
import boto


# noinspection PyMethodMayBeStatic
class aws_S3:
    def __init__(self):
        """constructor"""

    def list_buckets(self, conn):
        """ List all current AWS S3 buckets """
        bucket = conn.get_all_buckets()
        print 'Current AWS S3 buckets:\n'
        for buck in bucket:
            print buck.name

    def upload_file(self, conn, bucket_name, key_name, file_path):
        """ Uploads a file from a source to an S3 bucket """
        if os.path.exists(file_path):
            bucket = conn.lookup(bucket_name)
            if bucket:
                key = bucket.new_key(key_name)
                file1 = key.set_contents_from_filename(file_path)
                if file1:
                    print 'file: %s has been uploaded' % key_name
                else:
                    print 'error in uploading %s to %s' % (key_name, bucket_name)
            else:
                print 'bucket not found'
        else:
            print "file path not found"

    def list_files(self, conn, bucket_name):
        """ lists all files (keys) in a specified bucket """
        bucket = conn.lookup(bucket_name)
        if bucket:
            print 'Files in %s:' % bucket.name
            key_list = bucket.list()
            for k in key_list:
                print k.name
        else:
            print "bucket not found"

    def list_all_files(self, conn):
        """ lists all files (keys) from all S3 buckets """
        bucket = conn.get_all_buckets()
        for buck in bucket:
            print 'Files in %s:' % buck.name
            key_list = buck.list()
            if key_list:
                for key in key_list:
                    print key.name
            print '\n'

    def download_file(self, conn, bucket_name, file_name, path):
        """ downloads a file from an S3 bucket to a specified location """
        if os.path.exists(path):
            bucket = conn.lookup(bucket_name)
            if bucket:
                key = bucket.get_key(file_name)
                if key:
                    dl_file = path+"\\"+key.name
                    key.get_contents_to_filename(dl_file)
                    print "File has been downloaded to %s" % dl_file
                else:
                    print 'key %s cannot be found' % file_name
            else:
                print 'bucket %s cannot be found' % bucket_name
        else:
            print "path not found"

    def delete_file(self, conn, bucket_name, file_name):
        """ deletes a file from an S3 bucket """
        bucket = conn.lookup(bucket_name)
        if bucket:
            del_file = bucket.delete_key(file_name)
            if del_file:
                print 'file %s has been deleted' % file_name
            else:
                print 'file %s cannot be deleted' % file_name
        else:
            print 'bucket cannot be found'

    def new_bucket(self, conn, new_name):
        try:
            bucket = conn.create_bucket(new_name)
            return bucket
        except boto.exception.S3CreateError:
            print new_name, 'cannot be created (name is not unique)'

"""
Amazon Simple Storage Service (Amazon S3) is easy to use, secure, durable, 
highly-scalable cloud object storage service.

line 12: gets list of buckets by calling get_all_buckets method on s3 connection
        object.
lines 14/15: Loops through bucket list and prints name of each bucket to screen

line 19:if the path exists
line 20:gets bucket by calling lookup method on s3 conn object using the name
        of the bucket as parameter (lookup instead of get_bucket so exception is not thrown)
line 21: if the bucket has been retrieved
line 22: creates new key (file) object by calling new_key method on bucket object
        and passing a name (string object) in as parameter
line 23: sets the the contents of the newly created key object by calling the
        set_contents_from_filename method on the key object and passing the
        source path of the contents as parameter
lines 24-27: If the key contents have been set, prints success message to screen.
            If not, prints error message
lines 28/29: If bucket cannot be retrieved, prints error message
lines 30/31: if path does not exist, print error message

line 35: gets bucket by calling lookup method on s3 conn object using the name
        of the bucket as parameter
line 36: if the bucket has been retrieved
lines 37 - 40: gets list of files (keys) in the bucket by calling list method on bucket object.
        Loops through file list and print the name of each file.
lines 41/42: if bucket cannot be retrieved, prints error message

lines 44-53: As above, but retrieves all buckets and loops through them

line 57: if path exists
line 58: gets bucket by calling lookup method on s3 conn object using the name
        of the bucket as parameter
line 59: if the bucket has been retrieved
line 60: retrieves key object using get_key method on bucket object and using the name of
        the key as parameter.
lines 61: if key has been retrieved
line 62: create filename to download key to by concatenating path, backslash and name of key
line 63: calls get_contents_to_filename on the key object, passing in filename as parameter (method returns nothing)
lines 65/66: if key cannot be retrieved, prints error message
lines 67/68: if bucket cannot be retrieved, prints error message
lines 69/70: if path not found, prints error message

line 74: gets bucket by calling lookup method on s3 conn object using the name
        of the bucket as parameter
line 75: if the bucket has been retrieved
line 76: deletes the key by calling delete_key method on bucket object and passing the key name
        as parameter
lines 77/78: If delete was successful, print success message, if not, print error message
lines 79/80: If not, print error message
lines 81/82: if bucket cannot be retrieved, prints error message
lines 85 - 89: Creates a new bucket of the specified name. Returns the bucket object if successful.
                If it cannot be created (names must be unique), prints an error message.
"""
