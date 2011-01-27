#!/usr/bin/env python

#
# ----------------------------------------------------------------------------
# "THE CLUB-MATE LICENSE" (Revision 23):
# Some guys from the c3pb.de wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If you meet some of us some day, and you think
# this stuff is worth it, you can buy use a club-mate in return.
# ----------------------------------------------------------------------------
#




import os
import cherrypy
import ConfigParser

import cherrypy.lib.auth_basic

from jumpages.admin import Admin
from jumpages.member import Member

from jinja2 import Environment, PackageLoader

#This will create a template environment with the default settings
#and a loader that looks up the templates in the templates folder 
#inside the yourapplication python package.
env = Environment(loader=PackageLoader('um', 'templates'))

from ldaphelper import LdapConn

                
class Root(object):
    @cherrypy.expose
    def index(self):
        template = env.get_template('index.html')
        return template.render(title='UM')


def authAdmin(realm,user,password):
    print "auth admin"
    return True
    
def authMember(realm,user,password):
    print "auth member"
    return True
#    print realm,user,password
#    return ldapConn.hasAccess(user,password)

    
def main():
    config = ConfigParser.RawConfigParser()
    config.read('um.cfg')

    ldap_server = config.get("um", "ldap_server")
    people_basedn = config.get("um", "people_basedn")
    groups_basedn = config.get("um", "groups_basedn")
    admin_dn = config.get("um", "admin_dn")
    admin_pw = config.get("um", "admin_pw")    

    #create globally shared ldapConnection
    global ldapConn
    ldapConn = LdapConn(ldap_server,people_basedn,groups_basedn,admin_dn,admin_pw)    
    
    # Some global configuration; note that this could be moved into a
    # configuration file
    cherrypy.config.update({
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,
        'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
        
    })

    rootconf = {
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        }
    }
    
    adminconf = {
        '/': {'tools.auth_basic.on': True,
                  'tools.auth_basic.realm': 'Admins only',
                  'tools.auth_basic.checkpassword': authAdmin,
    },
    }
    
    memberconf = {
        '/': {'tools.auth_basic.on': True,
                  'tools.auth_basic.realm': 'Members',
                  'tools.auth_basic.checkpassword': authMember,
                  },
    }
    
    cherrypy.tree.mount(Root(),"/",rootconf)
    cherrypy.tree.mount(Admin(env,ldapConn),"/admin",adminconf)
    cherrypy.tree.mount(Member(env,ldapConn),"/member",memberconf)
    
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    main()
