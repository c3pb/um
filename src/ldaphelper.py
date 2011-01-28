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
#    ldapcon = None
        
    def __init__(self,ldap_server,people_basedn,groups_basedn,admin_dn,admin_pw):
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
        
    def hasAccess(self,username,password):
        
        try:
            # con = ldap.initialize(server)
            user_dn = self.people_basedn.format(USERNAME=username) #{"USERNAME" : username})
            print user_dn
            self.ldapcon.bind_s(user_dn, password)
            print "user authenticated"
            return True
        except ldap.INVALID_CREDENTIALS:
            print "Username or password is incorrect."
            return False
        # finally:
        #     con.unbind()
