
class Filter(object):
    def __init__(self,filterID,filterDate,filterTime,filterFrequency,filterBand,filterCallsign,filterType,filterRemark):
        self.filterID=filterID
        self.filterDate=filterDate
        self.filterTime=filterTime
        self.filterFrequency=filterFrequency
        self.filterBand=filterBand
        self.filterCallsign=filterCallsign
        self.filterType=filterType
        self.filterRemark=filterRemark
        return
    def saveFilter():
    # appendtofile
        return
    def writeFilter(self, user):
        user_filter_file = "filter/"+user
        filterFile=open(user_filter_file, 'a')
        
        text = self.filterID + ";" + self.filterDate + ";" + self.filterTime + ";" + self.filterFrequency + ";" + self.filterBand + ";" + self.filterCallsign + ";" + self.filterType + ";" + self.filterRemark + "\n"
        #FilterID;Date;Time;Frequency;Band;Callsign;Type;Remark;
        filterFile.write(text)
        filterFile.close()
        return
    
    
        