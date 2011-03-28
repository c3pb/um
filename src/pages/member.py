#
# ----------------------------------------------------------------------------
# "THE CLUB-MATE LICENSE" (Revision 23.5):
# Some guys from the c3pb.de wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If you meet one of us some day, and you think
# this stuff is worth it, you can buy them a club-mate in return.
# ----------------------------------------------------------------------------
#

import cherrypy

class Member():
    '''
     This class contains all pages for /member/**
    '''

    def __init__(self,env,ldapConn):
        '''
        Constructor
        '''
        self.env = env
        self.ldapConn = ldapConn
        
        
    @cherrypy.expose
    def index(self):
        print cherrypy.request.login
        allusers = self.ldapConn.get_users()
        template = self.env.get_template('user.index.html')
        return template.render(users=allusers, title='users list')

    @cherrypy.expose
    def view(self,username):
        print "view username=%s" % (username)
        return "wheee"
