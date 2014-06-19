#!/usr/bin/python -tt
# Script by - Rishab Saraf
# Github profile: rishabsaraf93
import re
import sys

def breakdate(date):
  """
  breakdate takes a date as an argument in the format '1 Jan 2010' and returns a tuple of size 3 
  The tuple contains three integer values (day,month,year)
  """
  match = re.search(r'(\d+)\s(\w+)\s(\d+)',date)
  day = 0
  month = ''
  year = 0
  if not match:
    sys.stderr.write('\nError in reading date!!!\n')
    sys.exit(1)
  day = int(match.group(1))
  month = match.group(2)
  year = int(match.group(3))
  month = month.lower()
  
  if month[:3] == 'jan':
    month = 1
  elif month[:3] == 'feb':
    month = 2
  elif month[:3] == 'mar':
    month = 3
  elif month[:3] == 'apr':
    month = 4
  elif month[:3] == 'may':
    month = 5
  elif month[:3] == 'jun':
    month = 6
  elif month[:3] == 'jul':
    month = 7
  elif month[:3] == 'aug':
    month = 8
  elif month[:3] == 'sep':
    month = 9
  elif month[:3] == 'oct':
    month = 10
  elif month[:3] == 'nov':
    month = 11
  elif month[:3] == 'dec':
    month = 12
  return (day,month,year)


def compare(date1,date2):
  """
  compare takes two dates as agruments (date1,date2) in the format '1 Jan 2014' and returns an integer value.
  The value returned is -1 if date1 is older, 0 if both are same and 1 if date1 is newer.
  """
  d1,m1,y1 = breakdate(date1)
  d2,m2,y2 = breakdate(date2)
  if y2>y1:
    return -1
  elif y1>y2:
    return 1
  else:
    if m2>m1:
      return -1
    elif m1>m2:
      return 1
    else:
      if d2>d1:
        return -1
      elif d1>d2:
        return 1
      else:
        return 0

def main():
  first = input('enter date : ')
  second = input('enter date : ')
  res = compare(first,second)
  if res==-1:
    print second + ' is later'
  elif res==0:
    print 'both are same'
  else:
    print first + ' is later'


if __name__ == '__main__':
  main()

