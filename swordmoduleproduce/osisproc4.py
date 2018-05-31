# -*- coding=utf-8 -*-
import re
import sqlite3

# output rmac hebrew morph module for xiphos crosswire sword

bookfile=open('rmacplus','w')

conn=sqlite3.connect('rmac.dct.mybible')
c=conn.cursor()

sql="select word,data from dictionary"

c.execute(sql)

def seqnumprocess(seqnum):
  sr=seqnum
  count=5-len(sr)
  i=0
  while i<count:
    sr='0'+sr
    i+=1
  print sr
  return sr

def convertstrong(mstr):
  pars=re.match(r'M(\d+)',mstr)
  return seqnumprocess(pars.group(1))

n=0
content=u''
for item in c.fetchall():      
  n=n+1
  print n
  if re.match(r'M(\d+)',item[0])!=None:
    entryitem=u'<entryFree sortKey="'+convertstrong(item[0])+'">\n<def>'+'<p>'+item[0]+'</p>'+item[1]+'</def>\n</entryFree>\n'
    content=content+entryitem

bookfile.write(content.encode('utf-8'))
bookfile.close()

