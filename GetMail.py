#!/usr/bin/python

import sys
import re
import imaplib
import getpass
import email
import email.header
import datetime
import os
import time
import Filter as fi
import SendMail
import glob
 
EMAIL_ACCOUNT = "spider_alert@gmx.de"
EMAIL_FOLDER = "INBOX"
 
 
def process_mailbox(M):
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        #print "No messages found!"
        print("No messages found!")
        return
 
    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            #print "ERROR getting message", num
            print("ERROR getting message" + num)
            return
        
        #msg = email.message_from_string(data[0][1])  #python2?
        msg = email.message_from_bytes(data[0][1])
        
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = str(decode[0]).lower()
        
        from_mail = re.findall("\<(.*?)\>", msg['From'])[0]
        
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            pattern = '%d.%m.%Y %H:%M:%S'
            date_time = local_date.strftime(pattern)
            #filterID = str(int(time.mktime(time.strptime(date_time, pattern))))
            filterID = str(int(time.time()))
            pattern = '%Y-%m-%d'
            filterDate = local_date.strftime(pattern)
            pattern = '%H:%M'
            filterTime = local_date.strftime(pattern)
        
        if "[spideralert]" in subject:
            delete = True
            sm = SendMail.SendMail(from_mail)
            print("Message nr."+ str(int(num)))
            msg_body = msg.get_payload()
            print("From: " + from_mail)
            print(subject)
            #print 'Raw Date:', msg['Date']
            
            # Now convert to local date-time
            
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    print("text/plain:\n\n" + part.get_payload()) # prints the raw text
                    text_content = part.get_payload()
                #if part.get_content_type() == 'text/html':
                    #print("text/html:\n\n" + part.get_payload()) # prints the raw text
                    #text_content = part.get_payload()
            #print(text_content)
            #print(type(text_content))
            #return
            if "set filter" in subject:
                filterFileList = glob.glob("filter/"+from_mail)
                if len(filterFileList) != 1:
                    #print("user not registered")
                    sm.sendErrorMail("user not registered", from_mail)
                else:
                    #msg_body = msg_body.replace('\r\n', ';')
                    #command_list=msg_body.split(';')
                    #print(type(msg_body))
                    #print(msg_body.as_string())
                    command_list=text_content.split('\r\n')
                    command_list = [x for x in command_list if x]
                    print(command_list)
                    
                    filterFrequency="*"
                    filterBand="*"
                    filterCallsign="*"
                    filterType="*"
                    filterRemark="*"

                    for command in command_list:
                        try:
                            token = command.lower().split('=')[1]
                            token = token.replace(';', ',')
                            if token.startswith('"') and token.endswith('"'):
                                token = token[1:-1]
                            if token.endswith(";") or token.endswith(","):
                                token = token[0:-1]   
                            #print(re.sub('<[^>]*>', '', token))
                            if "frequency" in command.lower():
                                filterFrequency = token
                            if "band" in command.lower():
                                filterBand = token
                                print(filterBand)
                            if "callsign" in command.lower():
                                filterCallsign = token.upper()
                            if "type" in command.lower():
                                filterType = token.upper()
                            if "remark" in command.lower():
                                filterRemark = token
                        except IndexError:
                            end=0
                            
                    x=fi.Filter(filterID,filterDate,filterTime,filterFrequency,filterBand,filterCallsign,filterType,filterRemark)
                    x.writeFilter(from_mail)
                    info = "ID="+filterID+"\nDate="+filterDate+"\nTime="+filterTime+"\nFrequency="+filterFrequency+"\nBand="+filterBand+"\nCallsign="+filterCallsign+"\nType="+filterType+"\nRemark="+filterRemark
                    sm.sendConfirmationMail("filter set", info)
                
            elif "register user" in subject:
                filterFileList = glob.glob("filter/"+from_mail)
                if len(filterFileList) != 0:
                    #print("user not registered")
                    sm.sendErrorMail("user already registered", from_mail)
                #print(from_mail)
                user_filter_file = "filter/"+from_mail
                if not os.path.isfile(user_filter_file):
                    f0=open(user_filter_file, 'w')
                    f0.close()                    
                    sm.sendConfirmationMail("new user registered", from_mail)
                    delete = True
            elif "list filter" in subject:
                filterFileList = glob.glob("filter/"+from_mail)
                if len(filterFileList) != 1:
                    sm.sendErrorMail("user not registered", from_mail)
                else:
                    num_filters = sum(1 for line in open("filter/"+from_mail))
                    content_file=open("filter/"+from_mail, 'r') 
                    content = content_file.read()
                    content_file.close()
                    info = list()
                    info.append(str(num_filters))
                    info.append(content)
                    sm.sendConfirmationMail("list filter", info)
            elif "delete filter" in subject:
                filterFileList = glob.glob("filter/"+from_mail)
                if len(filterFileList) != 1:
                    sm.sendErrorMail("user not registered", from_mail)
                else:
                    command_list=msg_body.split('\r\n')
                    command_list = [x for x in command_list if x]
                    for command in command_list:
                        token = command.lower().split('=')[1]
                        token = token.replace(';', ',')
                        if token.startswith('"') and token.endswith('"'):
                            token = token[1:-1]
                        if token.endswith(";") or token.endswith(","):
                            token = token[0:-1]   
                        if "filterid" in command.lower():
                            filterID = token
                    f = open("filter/"+from_mail, "r")
                    lines = f.readlines()
                    filterfile_before=len(lines)
                    line_counter=0
                    f.close()
                    f = open("filter/"+from_mail, "w")
                    for line in lines:
                        if not filterID in line:
                            f.write(line)
                            line_counter+=1
                    f.close()
                    if line_counter < filterfile_before:
                        sm.sendConfirmationMail("filter deleted", filterID)
                    else:
                        sm.sendErrorMail("filter not found", filterID)
            else:
                info = list()
                info.append(subject)
                info.append(msg_body)
                sm.sendErrorMail("command not recognized", info)
                
                    
            if delete:
                M.store(num, '+FLAGS', '\\Deleted')
                delete=False
 
M = imaplib.IMAP4_SSL('imap.gmx.de')
 
try:
    #rv, data = M.login(EMAIL_ACCOUNT, getpass.getpass())
    rv, data = M.login(EMAIL_ACCOUNT, "dxspider")
except imaplib.IMAP4.error:
    #print "LOGIN FAILED!!! "
    print("LOGIN FAILED!!! ")
    sys.exit(1)
 
#print rv, data
 
rv, mailboxes = M.list()
#if rv == 'OK':
    #print "Mailboxes:"
    #print mailboxes
    #print(mailboxes)
 
rv, data = M.select(EMAIL_FOLDER)
if rv == 'OK':
    #print "Processing mailbox...\n"
    print("Processing mailbox...")
    process_mailbox(M)
    M.close()
else:
    #print "ERROR: Unable to open mailbox ", rv
    print("ERROR: Unable to open mailbox ")
M.logout()