# ------------------------------------------------------------------------------
# Lux exporter python script plugin for Maya
#
# This file is licensed under the GPL
# http://www.gnu.org/licenses/gpl-3.0.txt
#
# $Id$
#
# ------------------------------------------------------------------------------
#
# lrmdb: Lux Render [Materials] Database integration
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from Lux.LuxMiscModules.Importer import Importer

class lrmdb:
    WEB_Connect             = False
    WEB_host                = 'www.luxrender.net'
    WEB_url                 = '/lrmdb/en/material/download/'
    
    XMLRPC_Connect          = False
    XMLRPC_CookieTransport  = None
    XMLRPC_host             = 'http://www.luxrender.net/lrmdb/ixr'
    XMLRPC_username         = ""
    XMLRPC_password         = ""
    XMLRPC_logged_in        = False
    XMLRPC_SERVER           = None
    XMLRPC_last_error_str   = None
    
    def __init__(self):
        # try import of libraries
        try:
            import httplib
            self.WEB_Connect = True
            OpenMaya.MGlobal.displayInfo("INFO: Simple Web support available")
        except ImportError, err:
            OpenMaya.MGlobal.displayWarning("WARNING: Simple Web support not available: %s" % err)
            
        try:
            import cookielib, urllib2, xmlrpclib
            self.XMLRPC_Connect = True
            
            #---------------------------------------------------------------------------
            # pilfered from
            # https://fedorahosted.org/python-bugzilla/browser/bugzilla.py?rev=e6f699f06e92b1e49b1b8d2c8fbe89d9425a4a9a
            class CookieTransport(xmlrpclib.Transport):
                '''
                A subclass of xmlrpclib.Transport that supports cookies.
                '''
                
                cookiejar = None
                scheme = 'http'
                verbose = None
                
                # Cribbed from xmlrpclib.Transport.send_user_agent 
                def send_cookies(self, connection, cookie_request):
                    '''
                    Send all the cookie data that we have received
                    '''
                    
                    if self.cookiejar is None:
                        self.cookiejar = cookielib.CookieJar()
                    elif self.cookiejar:
                        # Let the cookiejar figure out what cookies are appropriate
                        self.cookiejar.add_cookie_header(cookie_request)
                        # Pull the cookie headers out of the request object...
                        cookielist = list()
                        for header, value in cookie_request.header_items():
                            if header.startswith('Cookie'):
                                cookielist.append([header, value])
                        # ...and put them over the connection
                        for header, value in cookielist:
                            connection.putheader(header, value)
            
                # This is the same request() method from xmlrpclib.Transport,
                # with a couple additions noted below
                def request(self, host, handler, request_body, verbose=0):
                    '''
                    Handle the request
                    '''
                    
                    host_connection = self.make_connection(host)
                    if verbose:
                        host_connection.set_debuglevel(1)
            
                    # ADDED: construct the URL and Request object for proper cookie handling
                    request_url = "%s://%s/" % (self.scheme, host)
                    cookie_request  = urllib2.Request(request_url) 
            
                    self.send_request(host_connection, handler, request_body)
                    self.send_host(host_connection, host) 
                    
                    # ADDED. creates cookiejar if None.
                    self.send_cookies(host_connection, cookie_request)
                    self.send_user_agent(host_connection)
                    self.send_content(host_connection, request_body)
            
                    errcode, errmsg, headers = host_connection.getreply()
            
                    # ADDED: parse headers and get cookies here
                    class CookieResponse:
                        '''
                        fake a response object that we can fill with the headers above
                        '''
                        
                        def __init__(self, headers):
                            self.headers = headers
                            
                        def info(self):
                            return self.headers
                        
                    cookie_response = CookieResponse(headers)
                    
                    # Okay, extract the cookies from the headers
                    self.cookiejar.extract_cookies(cookie_response, cookie_request)
                    
                    # And write back any changes
                    # DH THIS DOESN'T WORK
                    # self.cookiejar.save(self.cookiejar.filename)
            
                    if errcode != 200:
                        raise xmlrpclib.ProtocolError(
                            host + handler,
                            errcode, errmsg,
                            headers
                        )
            
                    self.verbose = verbose
            
                    try:
                        sock = host_connection._conn.sock
                    except AttributeError:
                        sock = None
            
                    return self._parse_response(host_connection.getfile(), sock)
            
            self.XMLRPC_CookieTransport = CookieTransport
            
            OpenMaya.MGlobal.displayInfo("INFO: Advanced Web support available")
        except ImportError, err:
            OpenMaya.MGlobal.displayWarning("WARNING: Advanced Web support not available: %s" % err)
    
    def download(self, mat, id):
        if not self.WEB_Connect: return None
        
        #if id.isalnum():
        #Blender_API.Window.DrawProgressBar(0.0,'Getting Material #'+id)
        import httplib
        conn = httplib.HTTPConnection(self.WEB_host)
        conn.request("GET", self.WEB_url + '%i'%id)
        r1 = conn.getresponse()
        if not r1.status == 200:
            OpenMaya.MGlobal.displayWarning('HTTP Error %i: %s' % (r1.status,r1.reason))
            return None
        else:
           str = r1.read().strip()
           if (str[0]=="{") and (str[-1]=="}"):
               return Importer.Import(str)
           else:
               OpenMaya.MGlobal.displayWarning("ERROR: downloaded data is not a material or texture")
       
        conn.close()
        #Blender_API.Window.DrawProgressBar(1.0,'')
        #else:
        #    OpenMaya.MGlobal.displayWarning("ERROR: material id is not valid")
        #    return None
    
    # XMLRPC Methods
    def last_error(self):
        return self.XMLRPC_last_error_str
    
    def login(self):
        try:
            result = self.XMLRPC_SERVER.user.login(
                self.XMLRPC_username,
                self.XMLRPC_password
            )
            if not result:
                raise
            else:
                self.XMLRPC_logged_in = True
                return True
        except:
            self.XMLRPC_last_error_str = 'Login Failed'
            self.XMLRPC_logged_in = False
            return False
    
    def submit_object(self, mat, basekey, tex):
        if not self.check_creds(): return False
        
        try:
            result = 'Unknown Error'
            
            if tex:
                name = 'TEST' #Blender_API.Draw.PupStrInput('Texture Name: ', '', 32)
            else:
                name = mat.name
            
            result = self.XMLRPC_SERVER.object.submit(
                name,
                Importer.MatTex2dict( Importer.getMatTex(mat, basekey, tex), tex )
            )
            if result is not True:
                raise
            else:
                return True
        except:
            self.XMLRPC_last_error_str = 'Submit failed: %s' % result
            return False
    
    def check_creds(self):
        if self.XMLRPC_SERVER is None:
            try:
                import xmlrpclib
                self.XMLRPC_SERVER = xmlrpclib.ServerProxy(self.XMLRPC_host, transport=self.XMLRPC_CookieTransport())
            except:
                self.XMLRPC_last_error_str = 'ServerProxy init failed'
                return False
        
        if not self.XMLRPC_logged_in:
            self.request_username()
            self.request_password()
                
            return self.login()
        else:
            return True
     
    def request_username(self):
        self.XMLRPC_username = 'TEST' #'Blender_API.Draw.PupStrInput("Username:", self.XMLRPC_username, 32)
    
    def request_password(self):
        self.XMLRPC_password = 'TEST' #Blender_API.Draw.PupStrInput("Password:", self.XMLRPC_password, 32)