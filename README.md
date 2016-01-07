# KMLRegionRetriver
Package v.0.1

GENERAL DESCRIPTION
KMLRetriveRegion (KRR in short) is a PythonRESTServer module in charge of return a region  belonging to certain geographical coordinates (latitude, longitude). The regions are defined by the KML file. All KML file to use need to be copied into a KMLFile folder. KRR will load them while at PRS startup or invoking the reload method.
KRR use two different algorithms to determine whether a certain point is within a specific region, one fast and imprecise and one slower and more reliable. The first algorithm is based on the hypothesis that the necessary, but not sufficient condition which a certain point belong to a specific region, require that point need to be between the northern and the southern point and between the western and the eastern point of the region. When this algorithm return just one region for a specific point, that point cannot belong to other regions, so the result is reliable. When that algorithm return more that one region (point close to the border), then the second algorithm is invoked. The second algorithm is based on a standard method to find out whether or not a point belong to a polygon.

METHODS

The methods of this Module are:

getRegionSquarefromCoords : get region(s) belonging to certain coordinates based on the first algorithms
getRegionfromCoords : get the region belonging to certain coordinates based on the second algorithms
getReagionFromCoordsMulti : receive a llist of coordinates in the body request and return the region for each coords.
getKMLFileList : return the list of all KML file loaded
getRegionList : return the list of regions for a specific KMLFile
getRegionVertex : return the nothern, southern, western and eastern point for a specific region
getRegionPolygons : return all polygons for a specific region
cash : return the cashed point for faster response
saveCash : save the current cash to disk
readCash : force the reading cash from disk
doReload : force the reload for the KML Files

You can find a full description for each method in the online documentation.

UTILITY
parseCSVforCoords.py : Parse an imput file to retrive the Longitude and Latitude info


INSTALLATION

You have two different way to install this Module, both using the importModule utility
  1) Download the project zip file and move it to a temp path. From the RESTServer main folder locate the importModule utility and use it typing: python importModule.py -f <ModuleFile.zip>

  2) If the RESTServer can access directly to the internet you can avoid to download the Module project and live the importModule utility do it for you, typing: python importModule.py -w KMLRegionRetriver

To uninstall the module use the deleteModule.py utility from PRS.

KNOW LIMITATION AND ISSUES

Need to implement a limit for the number of points cashed.
Need to implement a multi region getter which return for a certain point regions coming from all KMLFiles
Need to implement a separate log file
