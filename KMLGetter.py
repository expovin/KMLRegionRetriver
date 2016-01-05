import config

import logging
import xml.etree.ElementTree as ET
from os import listdir
from os.path import isfile, join


'''
    KMLGetter. This module read KML file in the KML folder, create a JSON document containing for each file all the
    Multigeometry or Polygon (as Region) and compute for each region the vertex (themost Nothern, Southern, Eastern and
    Western point. The output is on the standard output, so you need to forward the stdout to file if needed.
    This module write a log file in logs directory. You can change the Log level using --DEBUG=<level>
    Levels are (DEBUG, INFO, WARNING)

'''

class KMLPolygonCoordinates():

    def getCoordinates(rootElement,data,file,nomeRegione):
        json=config.JSONFile
        logging.debug('Found MultiGeometry element, looping on Polygon')
        SerieDati={}
        Coords={'Polygon':'[]'}

        numPolygon=0
        eP=-json.mostEasterInitPoint
        wP=json.mostWesternInitPoint
        nP=json.mostNorthernInitPoint
        sP=json.mostSouthernInitPoint

        for Polygon in rootElement:
            logging.debug('Found element %s',Polygon.tag)

            if 'Polygon' in Polygon.tag:
                logging.debug('Found Polygon element, try to get Coordinates')
                numPolygon+=1
                try:
                    Coordinates=Polygon[0][0][0]
                    logging.debug('Coordinates : %s',Coordinates)
                    logging.debug('Try to split Coordinates')
                    myCoord=Coordinates.text.split()
                    logging.debug('myCoord : %s',myCoord)

                    #SerieDati.update({'Data'+str(numPolygon):myCoord})
                    #data[file][nomeRegione]=SerieDati
                    if(type(data[file][nomeRegione])==dict):
                        data[file][nomeRegione]['Polygon'].append(myCoord)
                    else:
                        data[file][nomeRegione]={'Polygon':[myCoord]}


                    #Find the most Nothern, Southern, Western and Eastern Point
                    for vertex in myCoord:
                        try:
                            long, lat = vertex.split(",")
                        except ValueError:
                            long,lat,height = vertex.split(",")

                        if(float(long) < wP):
                            westernPoint=vertex
                            wP=float(long)
                        if(float(long) > eP):
                            easternPoint=vertex
                            eP=float(long)
                        if(float(lat)> nP):
                            northernPoint=vertex
                            nP=float(lat)
                        if(float(lat)<sP):
                            southernPoint=vertex
                            sP=float(lat)

                    Vertex={'NothernPoint':northernPoint,'SouthernPoint':southernPoint,
                                    'EasternPoint':easternPoint,'WesternPoint':westernPoint}
                    data[file][nomeRegione]['Vertex']=Vertex

                    logging.debug('Data so far %s',data)

                except AttributeError:
                    logging.warning('Coordinates not found in file %s name %s',file,nomeRegione)



    def getPlacemark(Parent,file,data):

        kml=config.KMLFile
        logging.debug('Create new JSON Document file %s',file)
        if file not in data:
            data.update({file:'{}'})

        logging.debug('Start looping on all Element looking for Placemark')
        for Placemark in Parent:
            logging.debug('Found element %s', Placemark.tag)

            if 'Placemark' in Placemark.tag:
                logging.debug('Found Placemark Element')

                nomeRegione=''
                Poligoni={}
                logging.debug('Looping beneath looking for Name and MultiGeometry/Polygon')
                for child in Placemark:
                    logging.debug('Found element %s',child.tag)


                    if kml.regionNameTAG in child.tag:
                        logging.debug('Found name %s',child.text)
                        nomeRegione=child.text
                        Poligoni.update({nomeRegione :'{}'})


                        if(type(data[file])==dict):
                            data[file].update(Poligoni)
                        else:
                            data[file]=Poligoni

                    if 'MultiGeometry' in child.tag:
                        KMLPolygonCoordinates.getCoordinates(child,data,file,nomeRegione)
                    if 'Polygon' in child.tag:
                        KMLPolygonCoordinates.getCoordinates(Placemark,data,file,nomeRegione)

        logging.debug('For file %s made data %s',file, data)
        return data



def loopFile():
    p=config.FilePath           #Istanzio tutti i parametri di Path

    onlyfiles = [f for f in listdir(p.fpath) if isfile(join(p.fpath, f))]   #Set contenente tutti i file in fpath
    data={}

    #Loop su tutti i file KML
    for file in onlyfiles:

        if file.endswith(p.KMLext):
            logging.info('Open file %s',join(p.fpath,file))
            tree=ET.parse(join(p.fpath,file))
            root=tree.getroot()
            logging.debug('Root Element %s',root.tag)
            document=root[0]
            logging.debug('Document Element %s',document.tag)

            logging.debug('Looking for Folder or Placemark TAG')
            isFolder=0
            isPlacemark=0
            for child in document:  #Loop su tutti gli elementi di document per trovare Folder o Placemark
                logging.debug('Found element %s',child.tag)

                if 'Folder' in  child.tag:
                    logging.debug('Found element Folder')
                    isFolder=1

                if 'Placemark' in child.tag:
                    logging.debug('Found element Placemark')
                    isPlacemark=1

            if((isFolder==1) and (isPlacemark==1)):
                logging.warning('Found both Folder and Placemark element in file %s, file will be ingnored',file)
                continue

            if((isFolder==0) and (isPlacemark==0)):
                logging.warning('Found neither Folder nor Placemark element in file %s, file will be ingnored',file)
                continue

            if((isFolder==1) and (isPlacemark==0)):
                logging.info('Found Folder element, child will be pass')
                for child in document:
                    if 'Folder' in  child.tag:
                        data=KMLPolygonCoordinates.getPlacemark(child, file,data)
                continue


            if((isFolder==0) and (isPlacemark==1)):
                logging.info('Found Placemark element, this will be pass')
                data=KMLPolygonCoordinates.getPlacemark(document,file,data)
                continue

    return(data)


if(__name__=='__main__'):
    loopFile()
#else:
#    loopFile()




