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
            self.payload = "Filter set successfully\n\n" + info
        #confirm filter change
        
        #confirm filter delete
        if "filter deleted" in subject:
            self.payload = "FilterID " + info +" deleted successfully"
        #confirm new user
        if "new user registered" in subject:
            self.payload = "New user " + info + " registered"
        # list filter
        if "list filter" in subject:
            self.payload = "Found " + info[0] + " filter(s)\n\n" + "FilterID;Date & Time created (local);Frequency;Band;Callsign;Type;Remark\n" + info[1]
        #DX Spider Alert
        if "DX Spot alert" in subject:
            self.payload = "DX Spot(s):\n\n"+info
        #confirm user deleted
        
        #send help
        if "help" in subject:
            self.payload = "SpiderAlert - Email Header Commands:\n\n1.)[SpiderAlert] register user\n\n2.)[SpiderAlert] set filter\n\n3.)[SpiderAlert] delete filter\n\n[SpiderAlert] list filter\n\n[SpiderAlert] help"
        self.subject = subject
        self.initMailText()
        return
    def sendErrorMail(self, subject, info):
        if "user alredy registered" in subject:
            self.payload = "ERROR: user " + info + " already registered\nTo get a list of the commands, please send an email with the subject: [SpiderAlert] help"
        if "user not registered" in subject:
            self.payload = "ERROR: user " + info + " not registered.\nPlease send a mail with the subject: [SpiderAlert] register user"
        if "filter not found" in subject:
            self.payload = "ERROR: Trying to delete FilterID " + info + " Filter not found\n\nTo get a list of all filters please send a mail with the subject: [SpiderAlert] list filter"
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