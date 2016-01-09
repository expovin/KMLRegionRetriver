from getRegionInfo import getRegionInfo
import argparse
import sys
import config


if(__name__ == '__main__'):

    RF = getRegionInfo()

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='Get Module info', action='store_true')
    parser.add_argument('-fl', help='Get KML File list', action='store_true')
    parser.add_argument('-rs', nargs='*', help='[KMLFileName] [Coords] Get Region Square from Coords (Long,Lat) in format nn.nnnnnn,mm.mmmmmm')
    parser.add_argument('-rx', nargs='*', help='[KMLFileName] [Coords] Get Region from Coords (Long,Lat) in format nn.nnnnnn,mm.mmmmmm')
    parser.add_argument('-rf', nargs='*', help='[KMLFileName] [FileCoords] Get Regions for all Coords in FileCoords')
    parser.add_argument('-rv', nargs='*', help='[KMLFileName] [Region] Get Region Vertex, the most Northern, Southern'
                                               'Eastern and Western point for a specific region')
    parser.add_argument('-rp', nargs='*', help='[KMLFileName] [Region] Get Region Polygons')
    parser.add_argument('-rl',  help='[KMLFileName] Get Region list for a specific KMLFile')
    parser.add_argument('-gc', help='Get Cash', action='store_true')

    args = parser.parse_args()

    if(len(sys.argv) < 2):
        parser.print_help()
    else:
        if(args.i):
            i = config.Info
            print("{'Author':'",i.author,"','contact' : '",i.contact,"','last build' :",i.build,", 'version' : ",i.version,"}")

        if(args.fl):
            print(RF.getFileName())

        if(args.rl):
            print(RF.getRegion(args.rl))

        if(args.rs):
            if(len(args.rs) != 2):
                print('-rs require exactly 2 parameters [KMLFileName] [Coords]')
                parser.print_help()
            else:
                print(RF.getRegionSquarefromCoords(args.rs[0],args.rs[1]))

        if(args.rx):
            if(len(args.rx) != 2):
                print('-rx require exactly 2 parameters [KMLFileName] [Coords]')
                parser.print_help()
            else:
                print(RF.getRegionFromCoords(args.rx[0],args.rx[1]))

        if(args.rv):
            if(len(args.rv) != 2):
                print('-rv require exactly 2 parameters [KMLFileName] [Region]')
                parser.print_help()
            else:
                print(RF.getVertex(args.rv[0],args.rv[1]))

        if(args.rp):
            if(len(args.rp) != 2):
                print('-rp require exactly 2 parameters [KMLFileName] [Region]')
                parser.print_help()
            else:
                print(RF.getPolygon(args.rp[0],args.rp[1]))

        if(args.rf):
            if(len(args.rf) != 2):
                print('-rf require exactly 2 parameters [KMLFileName] [FileCoords]')
                parser.print_help()
            else:
                fc = open(args.rf[1],'r')
                Coords = eval(fc.read())
                for coord in Coords:
                    region = RF.getRegionFromCoords(args.rf[0],str(coord[0])+','+str(coord[1]))
                    print(region)


        if(args.gc):
            print(RF.getRegion(args.gc))