
#from safeeval import safeeval

import httplib


class ImportedMaterial:
    
    name = str
    type = str
    attrs = []
    
    textures = {}
    submats = []

    def __init__(self, name, type, attrs):
        self.name  = name
        self.type  = type
        self.attrs = attrs

class webfetch:
    
    host = 'qube.gotdns.org'
    path = '/lux/'
    
    materials = 'luxblend_materials.cfg'
    presets = 'luxblend_presets.cfg'
    
    error = False
    
    importedMaterials = []
    
    def get(self, file):
        conX = httplib.HTTPConnection(self.host)
        conX.request('GET', self.path + file)
        response = conX.getresponse()
        if not (response.status < 400 and response.status > 199):
            self.error = response.status, response.reason
            return
        else:
            data = response.read()
            return data
    
    def getMaterials(self):
        cfgFile = self.get(self.materials)
        if not self.error:
            matlib = eval(cfgFile.replace('\n','').replace('\r',''))
            importedMaterials = []
            for material in matlib:

                attrList = matlib[material]
                aOut = []
                for attr in attrList:
                    if attr not in ('type'):
                        aOut.append([attr, attrList[attr]])
                        
                importedMaterials.append( ImportedMaterial(material, matlib[material]['type'], aOut) )
                
            return importedMaterials

        else:
            print 'Error: %s %s' % self.error

    def getConfig(self):
        cfgFile = self.get(self.presets)
        if not self.error:
            cfgParams = eval(cfgFile.replace('\n','').replace('\r',''))
            for preset in cfgParams:
                print preset
        else:
            print 'Error: %s %s' % self.error