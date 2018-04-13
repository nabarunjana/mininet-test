import re

class Properties:
     filename=""
     def __init__(self):
          self=self

     def readFile(self,filename):
          try:
               rfile = open(filename, 'r')
               lines = rfile.readlines()
               rfile.close()
          except: print "Error loading file"
          return lines

     def list(self):
          properties = self.getAllProperties()
          for p in properties:
               print p


     def printFile(self,filename, val):
          try:
               wrfile = open(filename, 'w')
               wrfile.write(str(val))
               wrfile.close()
          except: "Error Writing to file"

     def load(self,filename):
          self.filename=filename

     def getAllProperties(self):
          properties = {}
          lines = self.readFile(self.filename)
          for line in lines:
               pr = re.split('=', line)
               properties[pr[0]] = pr[1].strip()
          return properties

     def getProperty(self,name):
          properties = self.getAllProperties()
          return properties[name]

if __name__ == '__main__':
     p = Properties()
     print "Usage -"
     print "p.load('file.properties')"
     print "p.getProperty('property')"


