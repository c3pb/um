#
# ----------------------------------------------------------------------------
# "THE CLUB-MATE LICENSE" (Revision 23):
# Some guys from the c3pb.de wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If you meet some of us some day, and you think
# this stuff is worth it, you can buy use a club-mate in return.
# ----------------------------------------------------------------------------
#

import cherrypy

class Admin():
    '''
    This class contains all pages for /admin/**
    '''
    
    @cherrypy.expose
    def index(self):
        template = self.env.get_template('admin.index.html')
        return template.render(title='Admin only area')

    def __init__(self,env,ldapConn):
        '''
        Constructor
        '''
        self.env = env
        self.ldapConn = ldapConn
        