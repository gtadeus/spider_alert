#!/usr/bin/python
import sys, getopt
import re
import Filter as fi
import DXSpot as dxs
import datetime
import glob
import ntpath
        
def getFilter(filterfile):
    f = open(filterfile, 'r')
    filterList = []
    for line in f:
        if line[0] != '#':
            line = line.strip()
            linelist = re.split(r';',line)
            filterList.append(fi.Filter(linelist[0], linelist[1], linelist[2], linelist[3], linelist[4], linelist[5], linelist[6], linelist[7]))
    return filterList        
        
        
def printDX():
    DXSpotString = "DX de EA3EJ:     21266.0  EH8FPR       Faro Punta Rasca              1441Z"
    dx = dxs.DXSpot(DXSpotString)
    print(dx.frequency)
    #print(getBand(dx.frequency))
    #print(getTransmissionType(dx.frequency))
    print(dx.callsign)
    print(dx.remark)
    print(dx.time)
    
    filterList = getFilter("filter/filter.txt")
    
    dx.compareFilterList(filterList)
    return


def main(argv):
    message = ''
    try:
        opts, args = getopt.getopt(argv,"hsm:",["message="])
    except getopt.GetoptError:
        #print 'SpiderAlert.py -m "DXSpot Message String"'
        print('SpiderAlert.py -m "DXSpot Message String"')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            #print 'SpiderAlert.py -m "DXSpot Message String"'
            print('SpiderAlert.py -m "DXSpot Message String"')
            sys.exit()
        if opt == '-s':
            message = "DX de EA3EJ:     21266.0  EH8FPR       Faro Punta Rasca              1441Z"
        elif opt in ("-m", "--message"):
            message = arg
        
            
            
    #message=re.sub('[^A-Za-z0-9 ]+', '', message)
    f0=open('debug.txt', 'a')
    f0.write(message)
    f0.close
    
    dx = dxs.DXSpot(message)
    if dx.errorState != 0:
        return
    filterFileList = glob.glob("filter/*@*")
    
    for filterFile in filterFileList:
        filterList = getFilter(filterFile)
        username = ntpath.basename(filterFile)
        result = dx.compareFilterList(filterList)
        #filterList = getFilter("filter/filter.txt")
        #result = dx.compareFilterList(filterList)
        if result == True:
            #print "filter hit!"
            print("filter hit " + username)
            
            fd = open('alert/'+username,'a')
            row=[]
            row.append(dx.DXfrom)
            row.append(str(datetime.datetime.utcnow().strftime('%Y-%m-%d')))
            row.append(str(dx.time))
            row.append(str(dx.frequency))
            row.append(dx.callsign)
            row.append(dx.getBand(dx.frequency))
            row.append(dx.getTransmissionType(dx.frequency))
            row.append(dx.remark)
            row.append(','.join(dx.filterHitList))
            row.append('\n')
            row_list = ';'.join(row)
            #row_list=row_list[:-1]
            fd.write(row_list)
            fd.close()
            print(dx.filterHitList)
        else:
            print("no hit!")

if __name__ == "__main__":
   main(sys.argv[1:])