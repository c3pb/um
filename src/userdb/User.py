'''
Created on Mar 28, 2011

@author: meatz
'''

class User(object):
    '''
    classdocs
    '''
    
    def __init__(self, nick,fullname, passwordhash, email, jid, roles):
        '''
        Constructor
        '''
        self.nick = nick
        self.fullname = fullname
        self.passwordhash = passwordhash
        self.email = email
        self.jid = jid
        self.roles = roles
        
        #if not an admin, this variable is undefined. This is required for correct visualization.
        if 'admin' in roles:
            self.isAdmin = True
    