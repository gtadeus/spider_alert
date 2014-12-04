import re
import fnmatch
import Filter as fi

class DXSpot(object):   
    def __init__(self,string):
        self.errorState=0
        string = ' '.join(string.split())
        words = re.split(' ', string)
        if len(words) < 4:
            print("error, wrong DX String")
            self.errorState=1
            return
        frequency = float(words[3])
        callsign = words[4]
        last_word = words[len(words)-1]
        #print(last_word)
        if re.match('^[0-9]{4}Z', last_word):
            iterator=1
        else:
            iterator=2
        #print(iterator)
        remark = ' '.join(words[5:len(words)-iterator])
        time_list = re.findall(r'\d+', words[len(words)-iterator])
        time = time_list[0]
        
        self.frequency=frequency
        self.callsign=callsign
        self.remark=remark
        self.time=time
        return
    def getBand(self, frequency):
        f = open('band_definitions.txt', 'r')
        band = "undefined"
        for line in f:
            if line[0] != '#':
                line = line.strip()
                linelist = re.split(r'\t+',line)
                lower = int(linelist[1])
                upper = int(linelist[2])
                if frequency >= lower and frequency <= upper:
                    band = linelist[0]         
        return band

    def getTransmissionType(self, frequency):
        f = open('transmission_def.txt', 'r')
        type = "undefined"
        for line in f:
            if line[0] != '#':
                line = line.strip()
                linelist = re.split(r'\t+', line)
                lower = int(linelist[2])
                upper = int(linelist[3])
                if frequency >= lower and frequency < upper:
                    type = linelist[1]
        return type
    def checkPattern(self, filter_list, value):
        list = filter_list.split(",")
        value_list=value.split(",")
        #make to case iinsensitive
        list = map(str.lower, list)
        value_list = map(str.lower, value_list)
        result=0
        for val in value_list:
            filtered = fnmatch.filter(list, val)
            result+=len(filtered)
        #print(list)
        #print(value_list)
        #print(filtered)
        
        #result=len(filtered)
        #print(result)
        return result
    def compare(self, fi):
        compareResult = False
        matchFrequency = self.checkPattern(str(self.frequency), str(fi.filterFrequency))
        matchBand = self.checkPattern(self.getBand(self.frequency), fi.filterBand)
        matchCallsign = self.checkPattern(self.callsign, fi.filterCallsign)
        matchType = self.checkPattern(self.getTransmissionType(self.frequency), fi.filterType)
        matchRemark = self.checkPattern(self.remark, fi.filterRemark)
        
        if matchFrequency and matchBand and matchCallsign and matchType and matchRemark:
            compareResult = True
        print("finalResult:")
        print(compareResult)
        return compareResult
    def compareFilterList(self, FilterList):
        result = False
        self.filterHitList = []
        for Filter in FilterList:
            if self.compare(Filter) == True:
                self.filterHitList.append(Filter.filterID)
                result = True
        return result
    
    