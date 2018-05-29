# -*- coding=utf-8 -*-
import re
import io
import html2textnew
import sqlite3
# output dictionary module for xiphos crosswire sword
bookhebfile=open('kjchebresult','w')
bookgrkfile=open('kjcgrkresult','w')
conn=sqlite3.connect('kjc.dct.mybible')
c=conn.cursor()

abres=["None","Gen","Exod","Lev","Num","Deut","Josh","Judg","Ruth","1Sam","2Sam","1Kgs","2Kgs","1Chr","2Chr","Ezra","Neh","Esth","Job","Ps","Prov","Eccl","Song","Isa","Jer","Lam","Ezek","Dan","Hos","Joel","Amos","Obad","Jonah","Mic","Nah","Hab","Zeph","Hag","Zech","Mal","Matt","Mark","Luke","John","Acts","Rom","1Cor","2Cor","Gal","Eph","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Heb","Jas","1Pet","2Pet","1John","2John","3John","Jude","Rev"]

sql="select word,data from dictionary"

c.execute(sql)
rs=c.fetchall()

def convertref(reob):
  xrefstrs=re.findall(r"<a class='bible' href='#b(.+?)'",reob.group(1))
  xrefs=u''
  for aitem in xrefstrs:
    nums=aitem.split('.')    
    xrefs=xrefs+abres[int(nums[0])]+'.'+nums[1]+'.'+nums[2]+' '
  return '<xr type="Bible"><ref osisRef="'+xrefs.strip()+'">'+xrefs+'</ref></xr>'+reob.group(2)

def seqnumprocess(seqnum):
  seqstr=re.search(r'[HG](\d+)',seqnum)
  sr=seqstr.group(1)
  count=5-len(sr)
  i=0
  while i<count:
    sr='0'+sr
    i+=1
  print sr
  return sr

n=0
contentheb=u''
contentgrk=u''
for item in rs:
  n=n+1
  print n
  refcontent=re.sub(r"(<a class='bible'.+?</a>)( </p>)",convertref,item[1])
  entryitem=u'<entryFree sortKey="'+seqnumprocess(item[0])+'">\n<def>'+item[0]+refcontent+'</def>\n</entryFree>\n'
  print item[0]
  typestr=re.match(r'([HG])\d+',item[0])
  if typestr.group(1)=='H':
    contentheb=contentheb+entryitem
  else:
    contentgrk=contentgrk+entryitem
  

bookhebfile.write(contentheb.encode('utf-8'))
bookgrkfile.write(contentgrk.encode('utf-8'))
bookhebfile.close()
bookgrkfile.close()

