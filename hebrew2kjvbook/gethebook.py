# -*- coding=utf-8 -*-
import html2textnew
from docx import Document
from docx.shared import Inches
import urllib2
import urllib
import re
import hypermethods
import codecs
import sqlite3
import hypermethods


def convertverse(verse):
  sents=re.findall(r'<Q><H>(.+?)<WH\d+>((<WH\d+>)+?)(<WTM\d+>).*?<h><X>.+?<x><T>(.+?)<t><q>',verse)
  ss=u''
  for sent in sents:
    ss=ss+sent[0]+'-'+sent[4]+sent[1]+sent[3]
  return ss

bookfile=open('heb.csv','w')
conn=sqlite3.connect('ETCBC')
c=conn.cursor()

sql="select Book,Chapter,Verse,Scripture from Bible order by Book ASC,Chapter ASC,Verse ASC"

xreflist=[]

c.execute(sql)
rs=c.fetchall()

content=u''
n=0
for item in rs:
  n=n+1
  print n
  sen=convertverse(item[3])
  if sen=='':
    print 'err========'
    break
  content=content+sen+u'\n'  #str(item[0])+','+str(item[1])+','+str(item[2])+','+
  if n%1000==0:
    bookfile.write(content.encode('utf-8'))
    content=u''

bookfile.write(content.encode('utf-8'))
bookfile.close()
