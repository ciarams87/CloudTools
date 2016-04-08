# class for creating OpenStack Connections
import libcloud.security
from libcloud.compute.types import Provider as ComputeProvider
from libcloud.compute.providers import get_driver as get_compute_driver
import libcloud
from libcloud.storage.providers import get_driver as get_storage_driver
from libcloud.storage.types import Provider as StorageProvider

auth_username = '' #enter username
auth_password = '' #enter password
auth_url = 'http://' #enter url
project_name = '' #enter the name of the project
region_name = '' #enter the region name

#if security cert available, enter the path and delete/comment out next line
libcloud.security.VERIFY_SSL_CERT = False
#ssl_creds = libcloud.security.CA_CERTS_PATH = ['C:\Example\ca-bundle.crt']


class OSConnections:

    def __init__(self):
        """constructer"""

    def os_compute_conn(self):
        """ Create and return a OpenStack compute driver object """
        provider = get_compute_driver(ComputeProvider.OPENSTACK)
        conn = provider(auth_username, auth_password, ex_force_auth_url=auth_url,
                        ex_force_auth_version='2.0_password', ex_tenant_name=project_name,
                        ex_force_service_region=region_name)
        return conn

    def os_storage_conn(self):
        """ Create and return a OpenStack storage driver object """
        provider = get_storage_driver(StorageProvider.OPENSTACK_SWIFT)
        conn = provider(auth_username, auth_password, ex_force_auth_url=auth_url,
                        ex_force_auth_version='2.0_password', ex_tenant_name=project_name,
                        ex_force_service_region=region_name)
        return conn


