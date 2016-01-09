#!/usr/bin/python

import getRegionInfo
import config

import tornado.escape
import tornado.ioloop
import tornado.web
import logging
import json
import sys
import os

import KMLRegionRetriver

#log=config.Log
p = getRegionInfo.getRegionInfo()

# TODO : Implement a script utility in order to call all methods via command line

'''
    RESTServer
    This service enable a full REST Server API which allow to call the API via REST protocol. By default
    all file having extensions kml in "/KMLFiles" directory will be read
'''

'''
    GET:getRegionSquarefromCoords - /getRegionSquarefromCoords/<KMLFileName>/<Coords> - JSON
    This method get the KML file name and coordinates (Long, Lat) and return the list
    of regions where the Coords are between the Northern, Soutern, Estern and Werstern point of the region itself.
    This is a necessary condition but not sufficient to determin wheter or not the point belong to some region.
    This method is used by getRegionFromCoords in order to get the list of all candidate Regions.
'''
class getRegionSquarefromCoords(tornado.web.RequestHandler):

    def get(self, fileName,coords):
        logging.debug('Called getRegionFromCoords ')
        response = {
            'Method':'getRegionFromCoords',
            'FileName':fileName,
            'Coordinates':coords,
            'Regions':p.getRegionSquarefromCoords(fileName,coords)
        }
        self.write(response)

'''
    GET:getRegionromFromCoords - /getRegionromFromCoords/<KMLFileName>/<Coords> - JSON
    This method start from the result set returned by the getRegionSquarefromCoords and determine
    wheter or not a point belong to a specific region.
'''
class getRegionfromCoords(tornado.web.RequestHandler):
    def get(self, fileName,coords):
        logging.debug('Called getRegionFromCoords ')
        response = {
            'Method':'getRegionFromCoords',
            'FileName':fileName,
            'Coordinates':coords,
            'Regions':p.getRegionFromCoords(fileName,coords)
        }
        self.write(response)

# TODO : Implement methods getRegionsFromCoords to return for each point regions from all KMLFile

'''
     POST:getReagionFromCoordsMulti - /getReagionFromCoordsMulti - JSON
     This Method expect a JSON with the list of all the Coords to looking for and return the complete result set containing
     a Region for each Coordinates.
'''
class getReagionFromCoordsMulti(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        rs = {}
        cont=0
        for region in data:
            for coords in data[region]:
                r = p.getRegionFromCoords(region,coords)
                cont +=1
                rs.update(r)

        response = {
            'Method':'getReagionFromCoordsMulti',
            'Number Of Coords' : cont,
            'Regions':rs
        }

        self.write(response)

'''
    GET:getKMLFileList - /getKMLFileList - JSON
    This method has no params and return the list of KML file read and acquired.
'''

class GetKMLFileList(tornado.web.RequestHandler):
    def get(self):
        response = {
            'Method':'GetKMLFileList',
            'FileName':p.getFileName()
        }
        self.write(response)

'''
    GET:getRegionList - /getRegionList/<KMLFileName> - JSON
    This Method retorn the list of all Regions defined in a specific KML file passed as parameter

'''
class GetRegionList(tornado.web.RequestHandler):
    def get(self,fileName):
        response = {
            'Method':'GetRegionList',
            'FileName':fileName,
            'Regions':p.getRegion(fileName)
        }
        self.write(response)

'''
    GET:getRegionVertex - /getRegionVertex/<KMLFileName>/<Region> - JSON
    This Method return the most Northern, Southern, Eastern and Western point for a specific Region in a KMLFile
'''
class GetRegionVertex(tornado.web.RequestHandler):
    def get(self, fileName,region):
        response = {
            'Method':'GetRegionVertex',
            'FileName':fileName,
            'Region':region,
            'Vertex':p.getVertex(fileName,region)
        }
        self.write(response)

'''
    GET:getRegionPolygons - /getRegionPolygons/<KMLFileName>/<Region> - JSON
    This Method return all the Polygon vertex for a specific Region in a KML File.
'''

class GetRegionPolygons(tornado.web.RequestHandler):
    def get(self, fileName,region):
        response = {
            'Method':' GetRegionPolygons',
            'FileName':fileName,
            'Region':region,
            'Polygon':p.getPolygon(fileName,region)
        }
        self.write(response)

'''
    GET:info - /info - JSON
    Just return some info about the RESTServer such as version, author and last build date
'''

class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        i=config.Info
        response = { 'author':i.author,
                     'contact':i.contact,
                     'last build':i.build,
                     'version': i.version
                   }
        self.write(response)

'''
   GET:cash - /cash - JSON
   This Metho return the cashed points with the region found for each point
'''
class getCash(tornado.web.RequestHandler):
    def get(self):
        response = {
                     'Method':' GetCash',
                     'cash': p.getCash()

                   }
        self.write(response)

'''
    GET:saveCash - /saveCash - JSON
    This Methos save the cashed point to disk
'''

class saveCash(tornado.web.RequestHandler):
    def get(self):
        response = {
                     'Method':'SaveCash',
                     'Byte Wrote': p.saveCash()
                   }
        self.write(response)

'''
    GET:readCash - /readCash - JSON
    This Method replace the cashe with the one saved on disk
'''

class readCash(tornado.web.RequestHandler):
    def get(self):
        response = {
                     'Method':'ReadCash',
                     'Read': p.readCash()
                   }
        self.write(response)

'''
    GET:doReload - /doReload - JSON
    This Methd force the KMLFile reload from /KMLFile directory
'''
class doReload(tornado.web.RequestHandler):
    def get(self):
        response = {
                     'Method':'doReload',
                     'rc': p.doReload()
                   }
        self.write(response)

'''
   GET:getHelp - /getHelp - JSON
   This Method return the current page with the help for each function. The Help page is automatically build each time
   RESTServer start.
'''

class getRESTServerHelp(tornado.web.RequestHandler):
    def get(self):
        c = config.makeHtmlHelpFile()
        Nome = sys.argv[0].split("/")[-1]
        htmlFileName = os.path.join(c.outPath,Nome[:-3]+'.html')
        fh = open(htmlFileName,'r')
        self.write(fh.read())
        return

application = tornado.web.Application()

if (__name__=='__main__'):
    logging.basicConfig(filename='logFile.txt', format='%(asctime)s\t%(module)s:%(funcName)s\t%(levelname)s\t%(lineno)d\t%(message)s', level=logging.INFO)
    app = open('application.conf','r')
    appDict = {}
    appDict = eval(app.read())
    for app in appDict['Application']:
        application.add_handlers(r".*$",[app,])

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

    print(appDict)
