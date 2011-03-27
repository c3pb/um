'''
Created on Mar 28, 2011

@author: meatz
'''

import hashlib
from userdb.User import User

class UserDB:
        
    def __init__(self,ldap_server, people_basedn, groups_basedn, admin_dn,admin_pw):
       
        self.userDB={} 

        #add some testUsers...
        u1 = User("meatz", "none", "matthias grawinkel", "matthias@grawinkel.com",  "matthias@grawinkel.com", ['member','admin'])
        self.addUser(u1)
        self.updateUserPass("meatz", "pass")
        
        u1 = User("test", "none", "test user", "test@user.tld",  "test@c3pb.de", ['member'])
        self.addUser(u1)
        self.updateUserPass("test", "pass")
        
        
    def login(self,nick,password):
        """Try to login as user. Return a user object,
         or None if not password is wrong or user does not exist"""
        
        user = self.userDB.get(nick)
        if user == None:
            return None
         
        if self.getPasswordHash(password) == user.passwordhash:
            return user
         
        return None

    def getAllUsers(self):    
        
        users=[]
        for (nick,user) in self.userDB.items():
            users.append(user)
        return users
        
    def addUser(self,user):
        self.userDB[user.nick] = user
        
    def removeUser(self,nick):
        return self.userDB.pop(nick)
    
    def getUser(self,nick):
        return self.userDB[nick]
    
    def getPasswordHash(self,password):
#        print hashlib.sha256(password).hexdigest()
        return hashlib.sha256(password).hexdigest()
    
    def updateUserPass(self,nick, newPasswordString):
        user = self.userDB[nick]
        user.passwordhash = self.getPasswordHash(newPasswordString)