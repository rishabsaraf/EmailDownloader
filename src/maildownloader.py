import sys
import re
import imaplib
import comparedate
import getpass
import email
import datetime
import os
from email.parser import Parser

def login(email,password):
  match_server = re.search(r'\w+@(\w+)\.\w+',email)
  if not match_server:
    sys.stderr.write('\nArghhh! Could not locate the hostname in the email id. Did u specify it for sure?\n')
    sys.exit(1)
  server = match_server.group(1)
  if server=='gmail':
    server = 'imap.gmail.com'
  elif server =='rediffmail':
    server = 'imap.rediffmail.com'
  elif server == 'yahoomail' or server =='ymail' or server == 'rocketmail':
    server = 'imap.mail.yahoo.com'
  elif server =='aol':
    server = 'imap.aol.com'
  elif server == 'lycos':
    server = 'imap.mail.lycos.com'
  elif server == 'mail':
    server = 'imap.mail.com'
  else:
    sys.stderr.write('\nThe script cannot connect to the host specified!\n\t\t Sorry :(\n')
    sys.exit(1)
  print 'Connecting to',server
  try:
    mail = imaplib.IMAP4_SSL(server)
  except:
    try:
      mail = imaplib.IMAP4(server)
    except:
      sys.stderr.write('\nCould not connect to the server\n')
      sys.exit(1)
  print 'Signing in as',email
  try:
    mail.login(email,password)
  except:
    sys.stderr.write('\nLogin Failed. Please re-check the credentials\n')
    sys.exit(1)
  print 'Successfully logged in as',email
  return mail

def fetchmail(mail,first,last):
  mail.select('inbox')
  day,month,year = comparedate.breakdate(first)
  date = datetime.date(year,month,day).strftime("%d-%b-%Y")
  result, data = mail.uid('search', None, '(SENTSINCE {date})'.format(date=date))
  if result!='OK':
    sys.stderr.write('Error searching mailbox')
    sys.exit(1)
  idstring = data[0]
  uids = idstring.split()
  for i in uids:
    res, data = mail.uid('fetch',i,'(RFC822)')
    print 'Readin mail id:',i
    if res != 'OK':
      print 'Error fetching mail'
      continue
    text = data[0][1]
    msg = email.message_from_string(text)
    match_date = re.search(r'\d+\s\w+\s\d+',msg['Date'])
    date = match_date.group()
    checkdate = comparedate.compare(date,last)
    if checkdate == 1:
      break
    makefile(text,msg,i,date)
    print 'Processed mail id '+ i + '\n'

def makefile(text,msg, uid,date):
  root = msg['from'][:6] + date[:6]
  if not os.path.exists('maildownloads'):
    os.mkdir('maildownloads')
  root = os.path.join('maildownloads',root)
  if not os.path.exists(root):
    os.mkdir(root)
  folder = str(uid)
  working_dir = os.path.join(root,folder)
  if not os.path.exists(working_dir):
    os.mkdir(working_dir)
  maintype = msg.get_content_maintype()
  filename = 'message.txt'
  filename = os.path.join(working_dir,filename)
  f = open(filename,'w')
  f.write('From: '+str(msg['From'])+'\n')
  f.write('To: '+str(msg['To'])+'\n')
  f.write('Subject: '+str(msg['Subject'])+'\n')
  f.write('Date/Time: '+str(msg['Date'])+'\n\n')
  f.write('Message: ')
  for part in msg.walk():
    charset = part.get_content_charset()
    if part.get_content_type() == 'text/plain':
      abttowrite = part.get_payload(decode=1)
      f.write(abttowrite)
    if part.get_content_maintype() == 'multipart':
      continue
    if part.get('Content-Disposition') is None:
      continue
    fn = part.get_filename()
    if bool(fn):
      attach_dir = os.path.join(working_dir,'attachments')
      if not os.path.exists(attach_dir):
        os.mkdir(attach_dir)
      attachment = os.path.join(attach_dir,fn)
      fp = open(attachment, 'wb')
      fp.write(part.get_payload(decode=True))
      fp.close()
  f.close()

def main():
  args = sys.argv[1:]
  username = ''
  password = ''
  if len(args)==2:
    username = args[0]
    password = args[1]
  else:
    username =raw_input('Enter your email id: ')
    print 'Password will not echo on the screen, keep typing!!!'
    password = getpass.getpass('Enter password: ')
  mail = login(username,password)


  print 'Enter date in the format : \'1 Jan 1990\''
  print 'Leave empty to set it to yesterday'
  d = datetime.timedelta(days=1)
  
  first = raw_input('Enter start date: ')
  print 'Leave empty to set it to today'
  last  = raw_input('Enter end date: ')
  if not first:
    first = (datetime.date.today() - d).strftime("%d %b %Y")
  if not last:
    last = datetime.date.today().strftime("%d %b %Y")
  comparedates = comparedate.compare(first,last)
  
  if comparedates == 1:
    first,last = last,first
  
  fetchmail(mail,first,last)
  mail.close()
  mail.logout()
  

if __name__ == '__main__':
  main()
