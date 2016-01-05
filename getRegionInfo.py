###
import KMLGetter
import config
###

import logging

class getRegionInfo:

    data={}
    cash={}

    def __init__(self):
        self.data=KMLGetter.loopFile()
        self.cash={}
        self.readCash()

    def getFileName(self):
        logging.debug('Called getFileName')
        fileName=[]
        for f in self.data:
            logging.debug('Found file :',f)
            fileName.append(f)
        logging.debug('Return list ',fileName)
        return fileName

    def getRegion(self,fileName):
        logging.debug('Called getRegion with params :',fileName)
        region=[]
        for r in self.data[fileName]:
            logging.debug('Found region :',r)
            region.append(r)
        logging.debug('Return list ',region)
        return region

    def getVertex(self,fileName,Region):
        logging.debug('Called getVertex with params :',fileName,' and ',Region)
        return self.data[fileName][Region]['Vertex']

    def getPolygon(self,fileName,Region):
        logging.debug('Called getPolygon with params :',fileName,' and ',Region)
        return self.data[fileName][Region]['Polygon']

    def getRegionSquarefromCoords(self,fileName,Coords):
        if Coords in self.cash:
            files = self.cash[Coords]
            if fileName in files:
                return [self.cash[Coords][fileName]]

        logging.debug('Called getRegionfromCoords with params :', fileName, ' and ',Coords)
        myLong, myLat =  Coords.split(",")
        mLat=float(myLat)
        mLong=float(myLong)
        Regions=[]

        for region in self.data[fileName]:
            logging.debug('Looking for Region : ',region)
            v=self.data[fileName][region]['Vertex']
            NothernLat, NothernLong=v['NothernPoint'].split(",")
            SouthernLat, SouthernLong=v['SouthernPoint'].split(",")
            WesternLat, WesternLong=v['WesternPoint'].split(",")
            EasternLat, EasternLong=v['EasternPoint'].split(",")
            nP=float(NothernLong)
            sP=float(SouthernLong)
            wP=float(WesternLat)
            eP=float(EasternLat)

            if(mLong <= nP) and (mLong >= sP) and (mLat >= wP) and (mLat <= eP):
                logging.debug('Found region :',region)
                Regions.append(region)

        return  Regions

    def calcoloDistanza(self,a,b,p):
        x1, y1 = a.split(",")
        x2, y2 = b.split(",")

        #Calcolo della retta passante per due punti
        x1 = float(x1)
        y1 = float(y1)
        x2 = float(x2)
        y2 = float(y2)

        m = (y2 - y1)/(x2 - x1)
        c = -x1*m - y1

        #Calcolo della distanza di un punto esterno alla retta
        x = (p - c)/m

        return x

    def getCash(self):
        return self.cash

    def doReload(self):
        try:
            self.data=loopFile()
            rc='OK'
        except:
            logging.warning('Error to reload file')
            rc='Error to reload'

        return rc

    def saveCash(self):
        c = config.Cash
        fw = open(c.fcash,'w')
        b = fw.write(str(self.cash))
        fw.close()
        return b

    def readCash(self):
        c = config.Cash
        try:
            fr = open(c.fcash,'r')
            self.cash = eval(fr.read())
            rc = 'OK'
            fr.close()
        except:
            logging.warning('Error to read from cash')
            self.cash={'Errore':'Errore caricamento Cash'}
            rc = 'Errore'

        return rc

    def getRegionFromCoords(self,fileName,Coords):
        logging.debug('Called getRegionfromCoords with params :', fileName, ' and ',Coords)
        myLat, myLong =  Coords.split(",")
        mLat = float(myLat)
        mLong = float(myLong)
        KML= getRegionInfo()
        Regions=KML.getRegionSquarefromCoords(fileName,Coords)

        if(not Regions[1:]):
            rc = {Coords:{fileName:Regions[0]}}
            self.cash.update(rc)
            return rc
        else:
            result={}
            for r in Regions:
                intersect=[0,0,0]
                for Polygon in self.data[fileName][r]['Polygon']:
                    for i in range(len(Polygon)):
                        Long,Lat = Polygon[i].split(",")
                        Lat=float(Lat)
                        k=i+1
                        if(k==len(Polygon)):
                            k=0
                        nLong,nLat = Polygon[k].split(",")
                        nLat=float(nLat)
                        if(Lat >= nLat):
                            H=Lat
                            L=nLat
                        else:
                            H=nLat
                            L=Lat
                        if (mLat >= L) and (mLat <= H):
                            x = KML.calcoloDistanza(Polygon[i],Polygon[k],mLat)
                            if x == 0:
                                intersect[2]+=1
                            if x > 0:
                                intersect[1]+=1
                            else:
                                intersect[0]+=1
                            result.update({r:intersect})


            rc={'Border':'[]','In':'[]'}
            for r in result:
                if(result[r][2]>0):
                    rc['Border'].append(r)
                if(result[r][0] %  2) and (result[r][0] % 2):
                    rc['In']=r
                    self.cash.update({Coords:{fileName:r}})


            return rc



if(__name__=='__main__'):
    KML = getRegionInfo()
    #print(KML.getFileName())
    #print(KML.getRegion('regioni.kml'))
    #print(KML.getVertex('regioni.kml','Sicilia'))
    print(KML.getRegionFromCoords('regioni.kml','43.507128,12.264953'))
    print(KML.getRegionFromCoords('regioni.kml','44.507128,11.264953'))
    print('Cash --> ',KML.cash)
    print(KML.readCash())
