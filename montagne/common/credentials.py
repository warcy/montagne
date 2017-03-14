import os
from montagne import cfg
from montagne.common.log import getLogger

LOG = getLogger()

CONF = cfg.CONF
CONF.register_opts([
    cfg.StrOpt('auth_uri',
               default='http://localhost:5000/v2.0',
               help='Complete public Identity API endpoint'),
    cfg.StrOpt('identity_uri',
               default='http://localhost:35357',
               help='Complete admin Identity API endpoint. This should '
                    'specify the unversioned root endpoint '
                    'e.g. https://localhost:35357/'),
    cfg.StrOpt('admin_tenant_name',
               default='admin',
               help='Keystone service account tenant name to validate'),
    cfg.StrOpt('admin_user',
               default='admin',
               help='Keystone account username'),
    cfg.StrOpt('admin_password',
               secret=True,
               default='admin',
               help='Keystone account password')
], group='keystone_authtoken')


def set_openstack_auth():
    try:
        get_neutron_credentials()
        get_nova_v1_1_credentials()
        get_nova_v3_credentials()
    except:
        os.environ['OS_USERNAME'] = CONF.keystone_authtoken.admin_user
        os.environ['OS_PASSWORD'] = CONF.keystone_authtoken.admin_password
        os.environ['OS_AUTH_URL'] = CONF.keystone_authtoken.auth_uri
        os.environ['OS_TENANT_NAME'] = CONF.keystone_authtoken.admin_tenant_name
    LOG.info('set openstack auth with '
             'OS_AUTH_URL=%s, '
             'OS_USERNAME=%s, '
             'OS_PASSWORD=%s, '
             'OS_TENANT_NAME=%s',
             os.environ['OS_AUTH_URL'],
             os.environ['OS_USERNAME'],
             os.environ['OS_PASSWORD'],
             os.environ['OS_TENANT_NAME'])


def get_neutron_credentials():
    d = dict()
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['tenant_name'] = os.environ['OS_TENANT_NAME']
    return d


def get_nova_v1_1_credentials():
    d = dict()
    d['username'] = os.environ['OS_USERNAME']
    d['api_key'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_TENANT_NAME']
    return d


def get_nova_v3_credentials():
    d = dict()
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_TENANT_NAME']
    return d


def get_ceilometer_credentials():
    d = dict()
    d['os_username'] = os.environ['OS_USERNAME']
    d['os_password'] = os.environ['OS_PASSWORD']
    d['os_auth_url'] = os.environ['OS_AUTH_URL']
    d['os_tenant_name'] = os.environ['OS_TENANT_NAME']
    d['version'] = 2
    return d
