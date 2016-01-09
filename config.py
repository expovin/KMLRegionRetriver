import logging
import os


class Info():
    author='Vincenzo Esposito'
    contact='ves@qlik.com'
    version='0.7'
    build='22/12/2015'

class FilePath():
    fpath='KMLFile'
    KMLext='.kml'

class KMLFile():
    regionNameTAG='name'

class JSONFile():
    mostWesternInitPoint=+180.0
    mostEasterInitPoint=180.0
    mostNorthernInitPoint=-90.0
    mostSouthernInitPoint=90.0

class RESTServer():
    listenPort=8880
    genericFileName='([0-9a-zA-Z.-]+)'
    genericCoords='([0-9,.-]+)'

class Cash():
    fpath='cash'
    file='point.json'
    fcash=os.path.join(fpath,file)
    maxkey=100000

class ParseCSVforCoords():
    fpath='CSV'
    file=''




class reqExample():
    Example = {'ES1':
                   {
                       'KMLFileName':'regioni.kml',
                       'Region':'Lombardia',
                       'Coords':'45.002875,11.504791'
                   }

               }


if(__name__=='__main__'):
    c = Config()
    print( c.Var2)

