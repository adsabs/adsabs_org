'''
Basic website of adsabs.org
'''

import sys
from os.path import dirname, abspath
basedir = dirname(abspath(__file__)) + '/'
sys.path.append(basedir)

#import the webpy module
import web

#General base URLS
#ADSLABS
base_url = 'http://labs.adsabs.harvard.edu'
abstract_base_url = base_url + '/ui/abs'

web.config.debug = True

#urls
urls = (
    '/.{19}', 'index',
    '/.*', 'other'
)

#initialize the application
app = web.application(urls, globals())


class index(object):
    """Main class that renders the first page with the basic search"""
    def __init__(self):
        """ Constructor"""
        pass
    def GET(self):
        """manager of the get requests"""
        #capture all the get path
        path = web.ctx.path
        
        return web.redirect(abstract_base_url+path, '302') 

class other(object):
    def __init__(self):
        """ Constructor"""
        pass
    def GET(self):
        """manager of the get requests"""
        #if I don't recognize the URL I redirect to the base
        return web.redirect(base_url, '302 Found')
    
if __name__ == "__main__": 
    app.run()
    
#to enable wsgi
#application = app.wsgifunc()
