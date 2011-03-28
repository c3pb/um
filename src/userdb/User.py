'''
Created on Mar 28, 2011

@author: meatz
'''

class User(object):
    '''
    classdocs
    '''
    
    def __init__(self, nick, passwordhash, givenName, email, jid, roles):
        '''
        Constructor
        '''
        self.nick = nick
        self.passwordhash = passwordhash
        self.givenName = givenName
        self.email = email
        self.jid = jid
        self.roles = roles
        
        #if not an admin, this variable is undefined. This is required for correct visualization.
        if 'admin' in roles:
            self.isAdmin = True
        
    