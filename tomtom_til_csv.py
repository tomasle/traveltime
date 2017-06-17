from pylr import init_binary_parsing, parse_binary
from xml.dom import minidom
import csv


filename = "data/traffictomtom_2016-03-03_1600.xml"

def createdate(filename):
    date, time = filename.split('_')[-2:]
    time = time.split('.')[0]
    time = time[0:2] + ":" + time[2:]
    #print date+"T"+time
    return date+"T"+time


csvfile = open('resultat.csv', 'wb')
writer = csv.writer(csvfile, delimiter=';',
                    quotechar='"', quoting=csv.QUOTE_MINIMAL)

writer.writerow(["timestamp","id", 
                 "flrp_lat","flrp_lon","flrp_frc","flrp_fow","flrp_dnp",
                 "llrp_lat","llrp_lon","llrp_frc","llrp_fow","llrp_dnp",
                 "quality","free_flow_speed","free_flow_traveltime","poffs","noffs"])



xmldoc = minidom.parse('data/traffictomtom_2016-03-03_1600.xml')
#observations = xmldoc.getElementsByTagName('basicDataValue')
timestamp = createdate(filename)

observations = xmldoc.getElementsByTagName('elaboratedData')
#print len(observations)

for observation in observations:
    id = observation.getAttribute('id')
    print id
    quality = observation.getElementsByTagName("supplierCalculatedDataQuality")[0].firstChild.data
    print "Quality of observation " + quality
    binary = observation.getElementsByTagName("binary")[0].firstChild.data
    #print binary
    
    free_flow_speed_object = observation.getElementsByTagName("freeFlowSpeed")
    if len(free_flow_speed_object)>0:
        free_flow_speed = free_flow_speed_object[0].firstChild.data
        print free_flow_speed
    
    free_flow_traveltime_object = observation.getElementsByTagName("freeFlowTravelTime")                                                     
    if len(free_flow_traveltime_object) > 0:
        free_flow_traveltime = free_flow_traveltime_object[0].firstChild.data
        print free_flow_traveltime
        
    data = parse_binary(binary, base64=True)
    #print data
    
    flrp_lat = data.flrp.coords.lat
    flrp_lon = data.flrp.coords.lon
    flrp_frc = data.flrp.frc
    flrp_fow = data.flrp.fow
    flrp_dnp = data.flrp.dnp
    
    llrp_lat = data.llrp.coords.lat
    llrp_lon = data.llrp.coords.lon
    llrp_frc = data.llrp.frc
    llrp_fow = data.llrp.fow
    llrp_dnp = data.llrp.dnp
    
    noffs = data.noffs
    poffs = data.poffs
    print noffs
    writer.writerow([timestamp,id, 
                 flrp_lat,flrp_lon,flrp_frc,flrp_fow,flrp_dnp,
                 llrp_lat,llrp_lon,llrp_frc,llrp_fow,llrp_dnp,
                 quality,free_flow_speed,free_flow_traveltime,poffs,noffs])
    
    
csvfile.close()