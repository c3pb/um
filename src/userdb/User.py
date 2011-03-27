'''
Created on Mar 28, 2011

@author: meatz
'''

class User(object):
    '''
    classdocs
    '''
    #primary search key
    nick=""
    
    givenName=""
    email=""
    jid=""
    roles=[]
    passwordhash=""
    
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