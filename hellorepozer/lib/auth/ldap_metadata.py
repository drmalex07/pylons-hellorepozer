'''
This repoze.who plugin is based/influenced on repoze.who.plugins.ldap
and assumes that the user is identified as an LDAP entry.
'''

import ldap

from zope.interface import implements
from repoze.who.interfaces import IMetadataProvider

from  paste.deploy.converters import asbool

import logging
log1 = logging.getLogger(__name__)

#
# Metadata providers
#

class LdapUserMetadataPlugin(object):
    '''
    Loads the user metadata (attributes and optionally group membership)
    for an authenticated user.
    '''

    implements(IMetadataProvider)

    def __init__(self, ldap_url,
        bind_dn = '', bind_pass = '',
        start_tls = False,
        attributes = None):

        """
        Fetch metadata for an authenticated user.

        @param bind_dn: Connect to the LDAP endpoint and bind as this DN.
        @param bind_pass: The password for the bind operation.
        @param attributes: A list of user attributes to be fetched.

        """

        log1.info (' =-= Setting up metadata-provider: %s' %(self))

        self.ldap_url  = ldap_url
        self.bind_dn   = bind_dn
        self.bind_pass = bind_pass
        self.start_tls = start_tls

        if not ldap_url:
            raise ValueError('An LDAP url must be specified')

        # Note: We initialize the connection on server's startup and re-use it.
        # What about LDAP connection timeouts? Maybe we should refresh the connection
        # (re-connect and re-bind) after a certain interval

        self._setup_connection()

        self.attributes = None
        if isinstance(attributes, list):
            self.attributes = attributes
        elif isinstance(attributes, str):
            self.attributes = map(lambda v: v.strip(), attributes.split(','))

        return

    def _setup_connection(self):
        ''' Connect and bind to the LDAP server '''

        if hasattr(self,'ldap_conn'):
            self.ldap_conn.unbind_s()

        self.ldap_conn = ldap.initialize(self.ldap_url)

        if self.start_tls:
            try:
                self.ldap_conn.start_tls_s()
                log1.info (' =-= The connection is now speaking on TLS (StartTLS)')
            except ldap.LDAPError, ex:
                raise ValueError('Cannot upgrade the connection (StartTLS): %s' %(ex))

        if self.bind_dn:
            try:
                self.ldap_conn.bind_s(self.bind_dn, self.bind_pass)
                self.ldap_user = self.ldap_conn.whoami_s()
                log1.info (' =-= Bound to DN="%s" user="%s"' %(self.bind_dn, self.ldap_user))
            except ldap.LDAPError:
                raise ValueError("Cannot bind with supplied credentials for DN: %s" %(self.bind_dn))
        return

    #
    # IMetadataProvider interface
    #

    def add_metadata(self, environ, identity):
        """
        Add metadata about the authenticated user to the identity.
        It provides a set of desired attributes from the user's DN

        It modifies the C{identity} dictionary by adding/replacing a 'metadata' key.

        @param environ: The WSGI environment.
        @param identity: The repoze.who's identity dictionary.

        """

        user_dn = identity.get('repoze.who.userid')

        identity['metadata'] = {}

        # (a) Retrieve user attributes

        try:
            r = self.ldap_conn.search_s(user_dn, ldap.SCOPE_BASE, '(objectClass=*)', self.attributes)
        except ldap.LDAPError, ex:
            log1.warn(' =-= add_metadata(): userid=%s: %s' % (user_dn, ex))
            raise Exception(identity)
        else:
            log1.info (' =-= Loaded metadata for DN="%s"' %(user_dn))
            identity['metadata'].update(r[0][1])

        # (b) Retrieve groups the user belongs to

def make_plugin(ldap_connection,
        bind_dn = '',
        bind_pass = '',
        start_tls = False,
        attributes = None):
    return LdapUserMetadataPlugin(ldap_url = ldap_connection,
        bind_dn = bind_dn,
        bind_pass = bind_pass,
        start_tls = asbool(start_tls),
        attributes = attributes);


