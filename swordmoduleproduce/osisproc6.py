# -*- coding=utf-8 -*-
import re
import io
import sqlite3
import html2textnew

# for output vms commentary for xiphos crosswire sword module

conn=sqlite3.connect('vws.cmt.mybible')
c=conn.cursor()

resultfile = io.open('vws','w',encoding='utf8')

abres=["None","Gen","Exod","Lev","Num","Deut","Josh","Judg","Ruth","1Sam","2Sam","1Kgs","2Kgs","1Chr","2Chr","Ezra","Neh","Esth","Job","Ps","Prov","Eccl","Song","Isa","Jer","Lam","Ezek","Dan","Hos","Joel","Amos","Obad","Jonah","Mic","Nah","Hab","Zeph","Hag","Zech","Mal","Matt","Mark","Luke","John","Acts","Rom","1Cor","2Cor","Gal","Eph","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Heb","Jas","1Pet","2Pet","1John","2John","3John","Jude","Rev"]

sql="select book,chapter,fromverse,data from commentary"

c.execute(sql)
rs=c.fetchall()

def verserepel(reobj):
  rs=re.findall(r"<a class='bible' href='#b(.+?)'",reobj.group())
  ref=''
  for item in rs:
    sl=re.split(r'\.|-',item)
    if len(sl)==6:
      ref=ref+abres[int(sl[0])]+'.'+sl[1]+'.'+sl[2]+'-'+ref+sl[0]+'.'+sl[1]+'.'+sl[3]
    else:
      ref=ref+abres[int(sl[0])]+'.'+sl[1]+'.'+sl[2]
    ref=ref+' '
  return '<reference osisRef="'+ref.strip()+'">'+ref+'</reference>'

allcon=u''
for item in rs:
  breakcontent1=re.sub(r'\r\n|<I>|</I>',' ',item[3])
  breakcontent2=re.sub(r'<P STYLE="text-indent: 1.25em; "></p>','</p>',breakcontent1)
  breakcontent=re.sub(r'<br>|</br>|<BR>|</BR>|<p>|</p>|<P>|</P>|<P.+?>|<p.+?>','<br />',breakcontent2)
  refcontent=re.sub(r"\(<a class='bible'.+?\)",verserepel,breakcontent)
  refcontent2=re.sub(r"<a class='bible'.+?</a>",verserepel,refcontent)

  allcon=allcon+'<div type="section" annotateType="commentary" annotateRef="'+abres[item[0]]+'.'+str(item[1])+'.'+str(item[2])+'"><p>'+refcontent2+'</p></div>'+'\n'

  breakcontent=re.sub(r'<BR>','',item[3])

  print item[0]
  print item[1]
  if 1==item[1] and 1==item[2]:
    resultfile.write(allcon)
    resultfile.flush()
    allcon=u''

resultfile.write(allcon)
resultfile.close()

