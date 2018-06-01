# -*- coding=utf-8 -*-
import re
import sqlite3
import Rtf2Txt

abres=["None","Gen","Exod","Lev","Num","Deut","Josh","Judg","Ruth","1Sam","2Sam","1Kgs","2Kgs","1Chr","2Chr","Ezra","Neh","Esth","Job","Ps","Prov","Eccl","Song","Isa","Jer","Lam","Ezek","Dan","Hos","Joel","Amos","Obad","Jonah","Mic","Nah","Hab","Zeph","Hag","Zech","Mal","Matt","Mark","Luke","John","Acts","Rom","1Cor","2Cor","Gal","Eph","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Heb","Jas","1Pet","2Pet","1John","2John","3John","Jude","Rev"]


bookfile1=open('stronghebrewplus','w')
bookfile2=open('stronggreekplus','w')

conn=sqlite3.connect('strongplus.twm')
c=conn.cursor()

sqlstrong="select data from content where topic_id"
sqlstrongid="select id,subject from topics"

c.execute(sqlstrongid)

def seqnumprocess(seqnum):
  sr=seqnum
  count=5-len(sr)
  i=0
  while i<count:
    sr='0'+sr
    i+=1
  return sr

def seqnumprocess2(seqnum):
  sr=seqnum
  count=4-len(sr)
  i=0
  while i<count:
    sr='0'+sr
    i+=1
  return sr

def convertstrong(mstr):
  if mstr.group(1).startswith('G'):
    return '<xr type="xref"><ref target="'+'StrongsGreek'+':'+seqnumprocess2(mstr.group(2))+'">'+mstr.group(1)+'</ref></xr>'
  else:
    return '<xr type="xref"><ref target="'+'StrongsHebrew'+':'+seqnumprocess2(mstr.group(2))+'">'+mstr.group(1)+'</ref></xr>'

def convertref(reob):
  print reob.group()
  xrefstrs=re.findall(r'"tw://bible\.\*\?id=(\d+)\.(\d+)\.(\d+?)"',reob.group())
  xrefs=u''
  print xrefstrs
  for aitem in xrefstrs:  
    xrefs=xrefs+abres[int(aitem[0])]+'.'+aitem[1]+'.'+aitem[2]+' '
  return '<xr type="Bible"><ref osisRef="'+xrefs.strip()+'">'+xrefs+'</ref></xr>'

def convertstrongnum(num):
  return seqnumprocess(re.match(r'[HG](\d+)',num).group(1))

contentheb=u''
contentgrk=u''
n1=0
n2=0
for ids in c.fetchall():
  print ids[1]
  if ids[0]==4482:
    continue
  sqlstrong="select data from content where topic_id="+str(ids[0])
  print sqlstrong
  c.execute(sqlstrong)
  item=c.fetchone()
  s0=re.sub(r'\\pard','',item[0])
  s1=re.sub(r'\\par','</p>\n<p>',s0)
  s2=re.sub(r'\\\w+','',s1)
  s3=re.sub(r'\\[\* ]+','',s2)
  s4=re.sub(r'[\{\}]','',s3)
  s5=re.sub(r' - ','',s4)
  s6=re.sub(r'-360 ','',s5)
  print s6
  print 'convert'
  s7=re.sub(r'HYPERLINK "tw://\[self\]\?([HG](\d+))" [HG]\d+',convertstrong,s6)
  print s7
  s8=re.sub(r'<p>  HYPERLINK "tw://bible.+" \[vref\]',convertref,s7)
  print s8
  s9=re.sub(r'<p>  Total KJV Occurrences','Total KJV Occurrences',s8)
  s10=re.sub(r"<p>  \\'95 ",'',s9)
  s10='<p>'+s10+'</p>'
  print s10
  

  entryitem=u'<entryFree sortKey="'+convertstrongnum(ids[1])+'">\n<def>'+'<p>'+ids[1]+'</p>'+s10+'</def>\n</entryFree>\n'
  if ids[1].startswith('H'):
    contentheb=contentheb+entryitem
    n1=n1+1
    if n1%300==0:
      bookfile1.write(contentheb.encode('utf-8'))
      contentheb=u''
  else:
    contentgrk=contentgrk+entryitem
    n2=n2+1
    if n2%300==0:
      bookfile2.write(contentgrk.encode('utf-8'))
      contentgrk=u''
  
bookfile1.write(contentheb.encode('utf-8'))
bookfile2.write(contentgrk.encode('utf-8'))
bookfile1.close()
bookfile2.close()

