'''
Created on Mar 28, 2011

@author: meatz
'''

class LdapDB(object):
    '''
    classdocs
    '''


    def __init__(selfparams):
        '''
        Constructor
        '''
        
        
        
"""
 con = ldap.initialize(ldap_server)
    user_dn = people_basedn.format(USERNAME=username) #{"USERNAME" : username})
    
    try:
        # con = ldap.initialize(server)
        con.bind_s(user_dn, password)
        query = '(&(objectClass=groupOfUniqueNames)(uniqueMember=uid=%s,ou=people,dc=chaos-paderborn,dc=de))' % (username)
        groups = con.search_s(basedn,ldap.SCOPE_SUBTREE,query, ['cn'])
        filteredGroups=[]
        for group in groups:
            print group[1]['cn'][0]
            filteredGroups.append(group[1]['cn'][0])
        cherrypy.session['groups'] = filteredGroups
            
        #TODO read users groups from ldap and store them in the user's session.
        print "user authenticated"
        return None
    except ldap.LDAPError, e:
        if type(e.message) == dict and e.message.has_key('desc'):
            print e.message['desc']
        print u"Incorrect username or password."
        return u"Incorrect username or password."
    finally:
        if (con):
            con.unbind()
"""        