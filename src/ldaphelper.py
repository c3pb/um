#
# ----------------------------------------------------------------------------
# "THE CLUB-MATE LICENSE" (Revision 23.5):
# Some guys from the c3pb.de wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If you meet one of us some day, and you think
# this stuff is worth it, you can buy them a club-mate in return
# ----------------------------------------------------------------------------
#

import ldap

        
class LdapConn:
    global ldap_server
        
    def __init__(self,ldap_server, people_basedn, groups_basedn, admin_dn,admin_pw):
        self.ldap_server = ldap_server
        self.people_basedn = people_basedn
        self.groups_basedn = groups_basedn
        self.ldapcon = ldap.initialize(ldap_server)
        self.ldapcon.simple_bind_s( admin_dn, admin_pw )

    def get_users(self):    
        filter = '(objectclass=person)'
        attrs = ['uid', 'cn', 'sn', 'mail']
        users = self.ldapcon.search_s( self.people_basedn, ldap.SCOPE_SUBTREE, filter, attrs )
        return users
        
    