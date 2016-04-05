Read Me:
__author__ = "Ciara Stacke"
__version__ = "1.0.1"
__status__ = "Alpha"

Welcome to the CloudTools package. In order to run the program,
there is some initial set-up configuration. The program also 
makes some assumptions the user should be aware of

BEFORE YOU START:
1. The application is run by running the CloudTools.py module.
2. AWS: Ensure environmental variables are configured to allow access to a boto configuration
    file containing AWS credentials. Otherwise, enter boto credentials directly into the
    "Connections.py" file.
3. OpenStack: Enter OpenStack Credentials in the OpenStackConn.py file. The SSL security
    check is set to "false"; the user can instead enter path to a SSL certificate
    if desired.
4. Ensure you have all necessary information to hand (see ASSUMPTIONS).
5. All modules in the package are necessary to run the program.
6. FULL PATH of all source and destination paths should be provided when
    eg. uploading a file to a bucket eg. C:\Users\Ciara\Desktop\File_Name.txt

ASSUMPTIONS:
1. The user has an AWS and OpenStack account.
2. The user has their AWS and OpenStack configuration credentials set (see above).
3. The user has entered their credentials in the OpenStackConn.py file (see above).
4. The user has at least one Keypair created on their AWS EC2 service.


		
