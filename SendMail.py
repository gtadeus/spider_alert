#!/usr/bin/python
import smtplib
import datetime
from email.mime.text import MIMEText


# we have several types of mail 
# alerts and command confirmations
class SendMail(object):
    def __init__(self, receiver):
        self.sender = "spider_alert@gmx.de" 
        self.receiver = receiver 
        self.mailserver = "mail.gmx.net"
        self.passwd = "dxspider"
        self.payload = ""
        self.subject = ""
        self.msg =""
        return
    def initMailText(self):
        self.msg = MIMEText(self.payload)
        self.msg['Subject'] = "[SpiderAlert] "+self.subject
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver 
        self.send()
        return
    def sendAlert(self, AlertList):
        #for each alert in list
        #put in mail body
        #change subject
        return
    def sendConfirmationMail(self, subject, info):
        #confitm filter set
        if "filter set" in subject:
            self.payload = "Filter set successful\n\n" + info
        #confirm filter change
        
        #confirm filter delete
        if "filter deleted" in subject:
            self.payload = "FilterID " + info +" deleted successful"
        #confirm new user
        if "new user registered" in subject:
            self.payload = "New user " + info + " registered"
        # list filter
        if "list filter" in subject:
            self.payload = "Found " + info[0] + " filter(s)\n\n" + info[1]
        #DX Spider Alert
        if "DX Spot alert" in subject:
            self.payload = "DX Spot:\n\n"+info
        #confirm user deleted
        self.subject = subject
        self.initMailText()
        return
    def sendErrorMail(self, subject, info):
        if "user alredy registered" in subject:
            self.payload = "ERROR: user " + info + " already registered\nTo get a list of the commands, please send an email with the subject: [SpiderAlert] help"
        if "user not registered" in subject:
            self.payload = "ERROR: user " + info + " not registered.\nPlease send a mail with the subject: [SpiderAlert] register user"
        if "filter not found" in subject:
            self.payload = "ERROR: FilterID " + info + " not found\nTo get a list of all filters please send a mail with the subject: [SpiderAlert] list filter"
        if "command not recognized" in subject:
            self.payload = "ERROR: command not recognized\nSubject:\n" + info[0] + "\n\nMessage:\n" + info[1] + "\n\nTo get a list of the commands, please send an email with the subject: [SpiderAlert] help"
           
        self.subject = "ERROR: " + subject
        self.initMailText()
        return
    def send(self):
        s = smtplib.SMTP(self.mailserver) 
        s.login(self.sender, self.passwd) 
        
        s.sendmail(self.sender, self.receiver, self.msg.as_string())
        s.quit()
        return

#if __name__ == "__main__":
        #send_ip()
        #return 