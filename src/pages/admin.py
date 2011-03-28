#
# ----------------------------------------------------------------------------
# "THE CLUB-MATE LICENSE" (Revision 23.5):
# Some guys from the c3pb.de wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If you meet one of us some day, and you think
# this stuff is worth it, you can buy them a club-mate in return.
# ----------------------------------------------------------------------------
#

import cherrypy

class Admin():
    '''
    This class contains all pages for /admin/**
    '''
    
    @cherrypy.expose
    def index(self):
        template = self.env.get_template('admin.html')
        users = self.userDB.getAllUsers()
        return template.render(title='Admin only area', users=users)

    def __init__(self,env,userDB):
        '''
        Constructor
        '''
        self.env = env
        self.userDB = userDB
#        self.ldapConn = ldapConn

