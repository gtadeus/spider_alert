#!/usr/bin/python

import sys
import os
from csv import reader
from operator import itemgetter
#import pandas as pd
import glob
import ntpath
import SendMail

def column(matrix, i):
    return [row[i] for row in matrix]
def processAlerts():
    alertFileList = glob.glob("alert/*@*")
    filterID_col_nr=8
    for alertFile in alertFileList:
        username = ntpath.basename(alertFile)
        print("username: " + username)
        sm = SendMail.SendMail(username)
        file_alert = open(alertFile, "r")
        csv_reader = reader(file_alert,  delimiter=';')
        
        #csv_reader.__next__()   # Skip header line

        csv_reader=sorted(csv_reader, key=itemgetter(filterID_col_nr))
        file_alert.close()
        os.remove(alertFile)

        index=0
        csv_reader_new =[]
        for row in csv_reader:
            row=row[:-1]
            last_element = row[-1]
            last_element_list = last_element.split(",")
            
            if len(last_element_list) > 1:
                for e in last_element_list:
                    temp_row = row[:-1]
                    temp_row.append(e)

                    csv_reader_new.append(temp_row)
            else:
                csv_reader_new.append(row)
            index+=1

        #for c in csv_reader_new:
        #    print(c)

        filterIDColumn=column(csv_reader_new, filterID_col_nr)
        uniqueFilterID = []
        [uniqueFilterID.append(i) for i in filterIDColumn if not uniqueFilterID.count(i)]
        print(uniqueFilterID)
        
        for filterID in uniqueFilterID:
            selection = [row for row in csv_reader_new if row[filterID_col_nr] == filterID]
            print(len(selection))
            print(selection)
            file_filter = open("filter/"+username, "r")
            csv_reader_filter = reader(file_filter,  delimiter=';')

            for row in csv_reader_filter:
                #if not '#' in row:
                    if filterID in row:     
                        original_filter_row = ";".join(row)
            msg = ""
            msg_html="<html><head></head><body><p>DX Spot(s):<br><br>"
   
            for s in selection:
                    msg += "DX de " + s[0] + ":\nDate/Time (UTC): " + s[1] + " " + s[2] + "\nCallsign: " + s[4] + "\nFrequency: " + s[3]  + "\nBand: " + s[5] + "\nType: " + s[6] + "\nRemark: " + s[7] + "\n\nFilterID=" + s[8] + "\n\nFilter settings:\nFilterID;Created on Date & Time (local);Frequency;Band;Callsign;Type;Remark\n"+original_filter_row+"\n\n**********\n\n"
                    
                    msg_html += "DX de " + s[0] + ":<br>Date/Time (UTC): " + s[1] + " " + s[2] + "<br><b>Callsign: " + s[4] + "</b><br>Frequency: " + s[3]  + "<br>Band: " + s[5] + "<br>Type: " + s[6] + "<br>Remark: " + s[7] + "<br><br>FilterID=" + s[8] + "<br><br>Filter settings:<br>FilterID;Created on Date & Time (local);Frequency;Band;Callsign;Type;Remark<br>"+original_filter_row+"<br><br>**********<br><br>"
                    
            msg = msg+"\n\nTo delete this filter hit \"Reply\" and change subject to \"[SpiderAlert] delete filter\""        
            msg_html = msg_html+"\n\nTo delete this filter hit \"Reply\" and change subject to \"[SpiderAlert] delete filter\" </p></body></html>"   
            
            info = []
            info.append(msg)
            info.append(msg_html)
            
            sm.sendConfirmationMail("DX Spot alert", info)
            #for selected_filterID in selection:
            #put all alerts into one mail
            
            #send this mail
    return
if __name__ == "__main__":
    processAlerts();
