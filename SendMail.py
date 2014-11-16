#!/usr/bin/python
import smtplib
import datetime
from email.mime.text import MIMEText

def send_ip():

        sender = "spider_alert@gmx.de" # Email des Absenders eintragen
        receiver = "maplemann411@gmail.com" # Email des Empfaenfers eintragen
        
        datestr =  datetime.date.today()
        subject = "sendmail with python"

        s = smtplib.SMTP("mail.gmx.net") # SMTP-Server deines Email-Anbieters eintragen
        s.login("spider_alert@gmx.de", "dxspider") # LogIn-Name und Passwort deines Email_Accounts eintragen
        
        body_text = "Lorem ipsum"
        
        msg = MIMEText(body_text)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver
        
        s.sendmail(sender, receiver, msg.as_string())
        s.quit()

if __name__ == "__main__":
        send_ip()