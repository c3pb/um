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

from jinja2 import Environment, PackageLoader
from userdb.UserDB import UserDB
from userdb.User import User
#from pages.new import NewUser
#from pages.admin import Admin


userDB = None
#This will create a template environment with the default settings
#and a loader that looks up the templates in the templates folder 
#inside the yourapplication python package.
env = Environment(loader=PackageLoader('um', 'templates'))

class NewUser():
    @cherrypy.expose
    def index(self):
        user = cherrypy.session.get('user')
        if 'admin' in user.roles:
            template = env.get_template('new.html')
            return template.render(title='New user',user=user)
        return "not authorized"
    
    @cherrypy.expose
    def create(self, nick=None,fullname=None,email=None,jid=None,password=None,password_again=None):
        user = cherrypy.session.get('user')
        if 'admin' in user.roles:
            passwordhash = userDB.getPasswordHash(password)
            newUser = User(nick,fullname, passwordhash, email, jid, ['member'])
            
            userDB.addUser(newUser)
            
            template = env.get_template('user.html')
            return template.render(title='Details for '+newUser.nick , user=user, showuser=newUser)
        return "not authorized"
        
        
        
class Users():
    @cherrypy.expose
    def index(self):
        "/"
        user = cherrypy.session.get('user')
        template = env.get_template('all.html')
        users=userDB.getAllUsers()
        return template.render(title='All users',user=user,users=users)
        
    @cherrypy.expose
    def default(self,nick):
        "/users/$nick"
        user = cherrypy.session.get('user')
        if nick == user.nick:
            template = env.get_template('me.html')
            return template.render(title='ME',user=user)
        else:
            template = env.get_template('user.html')
            showuser = userDB.getUser(nick)
            if showuser:
                return template.render(title='Details for '+showuser.nick , user=user, showuser=showuser)
            else:
                return template.render(title='Details for '+showuser.nick , user=user, error="User "+showuser.nick+" does not exist")
    
class Root(object):
    @cherrypy.expose
    def index(self):
        "/"
        template = env.get_template('index.html')
        user = cherrypy.session.get('user')
        return template.render(title='UM',user=user)
        
     
    @cherrypy.expose
    def logout(self):
        """ /logout """
        print "logout"
        cherrypy.lib.sessions.expire()
        raise cherrypy.HTTPRedirect("/")
        

    user = Users()
    new = NewUser()


    
    
def showLoginScreen(from_page='/', username='', error_msg=''):
    template = env.get_template('login.html')
    print "from_page="+from_page
    print "username="+username
    print "error_msg="+error_msg
    return template.render(title='Login',from_page=from_page,username=username,error_msg=error_msg)    
    
    
def check_username_and_password(nick,password):
    user = userDB.login(nick, password)
    if (user == None):
        print u"Incorrect username or password."
        return u"Incorrect username or password."

    print "user authenticated"
    cherrypy.session['user'] = user
    return None
   
                
def main():
    config = ConfigParser.RawConfigParser()
    config.read('um.cfg')
    
    
    global ldap_server
    global people_basedn 
    global groups_basedn 
    global basedn
    #     
    ldap_server = config.get("um", "ldap_server")
    people_basedn = config.get("um", "people_basedn")
    groups_basedn = config.get("um", "groups_basedn")
    basedn = config.get("um", "basedn")
    
    
    admin_dn = config.get("um", "admin_dn")
    admin_pw = config.get("um", "admin_pw")    

    #create globally shared userDB
    global userDB
    userDB = UserDB(ldap_server, people_basedn, groups_basedn, admin_dn,admin_pw)    
    
    
      
    # Some global configuration; note that this could be moved into a
    # configuration file
    cherrypy.config.update({
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,
        'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
        'tools.sessions.on': True, 
        'tools.sessions.timeout': 15,
        'tools.session_auth.on' : True,
        'tools.session_auth.debug' : True,
        'tools.session_auth.check_username_and_password' : check_username_and_password,
        'tools.session_auth.login_screen' : showLoginScreen,
        'log.screen': True,

        
    })

    rootconf = {
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        }
    }
    
    cherrypy.tree.mount(Root(),"/",config=rootconf)
#    
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    main()
