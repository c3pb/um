'''
Created on Mar 28, 2011

@author: meatz
'''
import unittest
from userdb import UserDB
from userdb.User import User


class Test(unittest.TestCase):


    def setUp(self):
        print "test setUp"
        self.userDB = UserDB.UserDB("ldap_server", "people_basedn", "groups_basedn", "admin_dn", "admin_pw")
       


    def tearDown(self):
        print "test tearDown"
        pass


    def testCRD(self):
        u1 = User("meatz", "none", "matthias grawinkel", "matthias@grawinkel.com",  "matthias@grawinkel.com", ['member','admin'])
        self.userDB.addUser(u1)
        u11 = self.userDB.getUser("meatz")
        self.assertTrue(u1 == u11)
        
        userlist = self.userDB.getAllUsers()
        self.assertTrue(len(userlist) == 1) #only 1 user
    
    
        #add another user
        u2 = User("test", "none", "another user", "another@user.tld",  "another@user.tld", ['member'])
        self.userDB.addUser(u2)
        
        userlist = self.userDB.getAllUsers()
        self.assertTrue(len(userlist) == 2) #now 2 users
        
        self.userDB.removeUser(u2.nick)
        userlist = self.userDB.getAllUsers()
        self.assertTrue(len(userlist) == 1) #only 1 user
    
        
    def testPasswordHash(self):
        s = 'mein!secures>Pa$$w0rt1234'
        hash1 = self.userDB.getPasswordHash(s)
        hash2 = self.userDB.getPasswordHash(s)
        self.assertTrue(hash1 == hash2)
    
    def testPasswordUpdate(self):
        u1 = User("meatz", "none", "matthias grawinkel", "matthias@grawinkel.com",  "matthias@grawinkel.com", ['member','admin'])
        self.userDB.addUser(u1)
        
        newPassword = 'mein!secures>Pa$$w0rt1234'
        newPasswordHash = self.userDB.getPasswordHash(newPassword)
        self.userDB.updateUserPass("meatz", newPassword)
        
        u2 = self.userDB.getUser("meatz")
        self.assertTrue(newPasswordHash == u2.passwordhash) #password successfully changed
        


    def testLogin(self):
        u1 = User("meatz", "none", "matthias grawinkel", "matthias@grawinkel.com",  "matthias@grawinkel.com", ['member','admin'])
        self.userDB.addUser(u1)
        
        password = 'mein!secures>Pa$$w0rt1234'
        self.userDB.updateUserPass("meatz", password)
       
        user = self.userDB.login("meatz", "wrongPassword")
        self.assertTrue(user == None)
        
        user = self.userDB.login("meatz", password)
        self.assertTrue(user.nick == u1.nick)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()