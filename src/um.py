#!/usr/bin/env python

#
# ----------------------------------------------------------------------------
# "THE CLUB-MATE LICENSE" (Revision 23.5):
# Some guys from the c3pb.de wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If you meet one of us some day, and you think
# this stuff is worth it, you can buy them a club-mate in return.
# ----------------------------------------------------------------------------
#

import os
import cherrypy
import ConfigParser

import ldap

#from jumpages.admin import Admin
#from jumpages.member import Member

from jinja2 import Environment, PackageLoader
import ldaphelper

#This will create a template environment with the default settings
#and a loader that looks up the templates in the templates folder 
#inside the yourapplication python package.
env = Environment(loader=PackageLoader('um', 'templates'))

from ldaphelper import LdapConn
    
class RestrictedArea:
  
    @cherrypy.expose
    def index(self):
        template = env.get_template('restricted.html')
        return template.render(title='UM', session=cherrypy.session)
    
class Root(object):
    @cherrypy.expose
    def index(self):
        template = env.get_template('index.html')
        return template.render(title='UM')
    
    @cherrypy.expose
    def logout(self):
        print "logout"
        cherrypy.lib.sessions.expire()
        raise cherrypy.HTTPRedirect("/")
        
            
    restricted = RestrictedArea()    

    
    
def login_screen(self, from_page='/', username='', error_msg=''):
    template = env.get_template('login.html')
    return template.render(title='Login',from_page=from_page,username=username,error_msg=error_msg)    
    
    
def check_username_and_password(username,password):

    con = ldap.initialize(ldap_server)
    user_dn = people_basedn.format(USERNAME=username) #{"USERNAME" : username})

    try:
        # con = ldap.initialize(server)
        con.bind_s(user_dn, password)
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
                
def main():
    config = ConfigParser.RawConfigParser()
    config.read('um.cfg')
    
    
    global ldap_server
    global people_basedn 
    global groups_basedn 
    #     
    ldap_server = config.get("um", "ldap_server")
    people_basedn = config.get("um", "people_basedn")
    groups_basedn = config.get("um", "groups_basedn")

    admin_dn = config.get("um", "admin_dn")
    admin_pw = config.get("um", "admin_pw")    

    #create globally shared ldapConnection
    global ldapConn
    ldapConn = LdapConn(ldap_server, people_basedn, groups_basedn, admin_dn,admin_pw)    
    
    # Some global configuration; note that this could be moved into a
    # configuration file
    cherrypy.config.update({
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,
        'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
        'tools.sessions.on': True, 
        'tools.sessions.timeout': 15,
        'tools.session_auth.on' : True,
        'tools.session_auth.debug' : True,
        
        'tools.session_auth.check_username_and_password' : check_username_and_password,
        'tools.session_auth.login_screen' : login_screen,

        
    })

    rootconf = {
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        }
    }
    
#    adminconf = {
#        '/': {'tools.auth_basic.on': True,
#                  'tools.auth_basic.realm': 'Admins only',
#                  'tools.auth_basic.checkpassword': authAdmin,
#    },
#    }
#    
#    memberconf = {
#        '/': {
#              #'tools.auth_basic.on': True,
#              #'tools.auth_basic.realm': 'Members',
#              #'tools.auth_basic.checkpassword': authMember,
#             
#                  },
#    }
    
    cherrypy.tree.mount(Root(),"/",rootconf)
#    cherrypy.tree.mount(Admin(env,ldapConn),"/admin",adminconf)
#    cherrypy.tree.mount(Member(env,ldapConn),"/member",memberconf)
#    
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    main()
