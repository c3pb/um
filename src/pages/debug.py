'''
Created on Mar 28, 2011

@author: meatz
'''
import cherrypy
class Debug:
  
    @cherrypy.expose
    def index(self):
        template = env.get_template('debug.html')
        return template.render(title='UM', session=cherrypy.session)