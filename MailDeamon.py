#!/usr/bin/python

import sys
#import csv
from csv import reader
from operator import itemgetter
#import pandas as pd

def readInbox():
    return
def column(matrix, i):
    return [row[i] for row in matrix]
def processAlerts():
    alert_file="alert/alert.txt"

    file_alert = open(alert_file, "r")
    csv_reader = reader(file_alert,  delimiter=';')
    csv_reader.__next__()   # Skip header line

    csv_reader=sorted(csv_reader, key=itemgetter(7))
    
    for row in csv_reader:
        row=row[:-1]
        print(row)
    
    filterIDColumn=column(csv_reader, 7)
    uniqueFilterID = []
    [uniqueFilterID.append(i) for i in filterIDColumn if not uniqueFilterID.count(i)]
    print(uniqueFilterID)
    
    for filterID in uniqueFilterID:
        selection = [row for row in csv_reader if row[7] == filterID]
        print(len(selection))
   

    return
if __name__ == "__main__":
    readInbox();
    processAlerts();
