import csv
import re
import http.client

url = 'localhost:8880'



'''
    defCoordsByRegExp [invert]
        <order>
            0:    Order as found on file
            1:    Invert order
'''
def getCoordsByRegExp(order):
    p = re.compile('^-?([1-8]?[1-9]|[1-9]0)\.{1}\d{1,6}')   #RegExp to catch Lat and Long
    base_url='http://localhost:8880/getRegionromFromCoords/PostcodeSectors.kml/'
    with open('Example.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            i=0
            Coords=[0,0]
            for f in row:
                if(p.match(str(f))):
                    Coords[i]=f
                    i+=1
            if(not order):
                req = Coords

            else:
                req= ([Coords[1], Coords[0]])
            conn = http.client.HTTPConnection(url)
            qs="/getRegionromFromCoords/PostcodeSectors.kml/"+str(req[0])+","+str(req[1])
            conn.request("GET",qs)
            r1 = conn.getresponse()
            print(Coords," -->",r1.status,r1.reason)


if(__name__=='__main__'):
    print(getCoordsByRegExp(1))
