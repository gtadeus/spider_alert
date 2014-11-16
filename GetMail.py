#!/usr/bin/python
#
# Very basic example of using Python and IMAP to iterate over emails in a
# gmail folder/label.  This code is released into the public domain.
#
# RKI July 2013
# http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
#
import sys
import re
import imaplib
import getpass
import email
import email.header
import datetime
 
EMAIL_ACCOUNT = "spider_alert@gmx.de"
EMAIL_FOLDER = "INBOX"
 
 
def process_mailbox(M):
    """
    Do something with emails messages in the folder.  
    For the sake of this example, print some headers.
    """
 
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        #print "No messages found!"
        print("No messages found!")
        return
 
    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            #print "ERROR getting message", num
            print(num)
            return
        
        #python2 msg = email.message_from_string(data[0][1])
        msg = email.message_from_bytes(data[0][1])
        
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = str(decode[0]).lower()
        
        if "[spideralert]" in subject:
            #print 'Message %s: %s' % (num, subject)
            msg_body = msg.get_payload()
            print(subject)
            #print 'Raw Date:', msg['Date']
            #print(msg['Date'])
            # Now convert to local date-time
            
            if "set filter" in subject:
                msg_body = msg_body.replace('\r\n', ';')
                command_list=msg_body.split(';')
                command_list = [x for x in command_list if x]
                print(command_list)
            date_tuple = email.utils.parsedate_tz(msg['Date'])
            if date_tuple:
                local_date = datetime.datetime.fromtimestamp(
                    email.utils.mktime_tz(date_tuple))
                #print "Local Date:", \
                #    local_date.strftime("%a, %d %b %Y %H:%M:%S")
                #print("Local Date")
                print(local_date.strftime("%a, %d %b %Y %H:%M:%S"))
            #M.store(num, '+FLAGS', '\\Deleted')
 
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
if rv == 'OK':
    #print "Mailboxes:"
    #print mailboxes
    print(mailboxes)
 
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