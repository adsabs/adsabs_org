'''
Basic website of adsabs.org
'''

import sys
from os.path import dirname, abspath
basedir = dirname(abspath(__file__)) + '/'
sys.path.append(basedir)
sys.path.append('/proj/ads/soft/python/lib/site-packages')

#import the webpy module
import web
import urllib
from ads import Looker

#General base URLS
#ADSLABS
base_url = 'http://labs.adsabs.harvard.edu'
abstract_base_url = base_url + '/adsabs/abs'



web.config.debug = False

#urls
urls = (
    '/(doi\:)?10\.[0-9]{4}\/.*', 'doi',
    '/[0-9]{4}.{15}', 'bibcode',
    '/[0-9]{4}.{1,14}', 'shortbibcode',
    '/.*', 'other'
)

#initialize the application
app = web.application(urls, globals())


class doi(object):
    """Class that redirect to labs in case of a DOI"""
    def __init__(self):
        """ Constructor"""
        pass
    def GET(self, arg):
        """manager of the get requests
            there is a second argument because in the regular expression 
            there are the parenthesis () that create a group:
            with webpy each group should have its own argument
        """
        #print 'doi'
        #capture all the get path
        path = web.ctx.path
        #I extract the DOI
        doi = path.lstrip('/')
        #I look for the actual bibcode
        lk = Looker.Looker('/proj/ads/abstracts/links/DOI.dat')
        try:
            #I search exactly for the short bibcode
            bibcode = lk.look(doi+'\t').rstrip('\n').split('\t')[1]
        except IndexError:
            bibcode = ''
            
        if bibcode != '':
            return web.redirect(abstract_base_url+'/'+urllib.quote(bibcode), '302 Found')
        else:
            return web.redirect(base_url, '302 Found')

        
class bibcode(object):
    """Class that redirect to labs in case of a bibcode"""
    def __init__(self):
        """ Constructor"""
        pass
    def GET(self):
        """manager of the get requests"""
        #print 'bibcode'
        #capture all the get path
        path = web.ctx.path
        
        return web.redirect(abstract_base_url+path, '302 Found') 

class shortbibcode(object):
    """Class that redirect to labs in case of a short bibcode"""
    def __init__(self):
        """ Constructor"""
        pass
    def GET(self):
        """manager of the get requests"""
        #print 'short'
        #capture all the get path
        path = web.ctx.path
        #I extract the short bibcode
        shortbib = path.lstrip('/')
        #I look for the actual bibcode
        lk = Looker.Looker('/proj/ads/abstracts/config/shortbib.dat')
        try:
            #I search exactly for the short bibcode
            bibcode = lk.look(shortbib+'\t').rstrip('\n').split('\t')[1]
        except IndexError:
            bibcode = ''
        
        if bibcode != '':
            return web.redirect(abstract_base_url+'/'+urllib.quote(bibcode), '302 Found')
        else:
            return web.redirect(base_url, '302 Found')

class other(object):
    def __init__(self):
        """ Constructor"""
        pass
    def GET(self):
        """manager of the get requests"""
        #print 'not previous'
        #if I don't recognize the URL I redirect to the base
        return web.redirect(base_url, '302 Found')
    
#if __name__ == "__main__": 
#    app.run()
    
# to enable wsgi
application = app.wsgifunc()
