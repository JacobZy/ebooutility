# -*- coding=utf-8 -*-
import re
import io
import sqlite3
import html2textnew

# for output vms commentary for xiphos crosswire sword module

conn=sqlite3.connect('barnes.cmt.mybible')
c=conn.cursor()

resultfile = io.open('barnes','w',encoding='utf8')

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
      ref=ref+abres[int(sl[0])]+'.'+sl[1]+'.'+sl[2]+'-'+ref+abres[int(sl[3])]+'.'+sl[4]+'.'+sl[5]
    else:
      ref=ref+abres[int(sl[0])]+'.'+sl[1]+'.'+sl[2]
    ref=ref+' '
  return '<reference osisRef="'+ref.strip()+'">'+ref+'</reference>'

def getChaptercontent(bookinfo):
  sql="select book,chapter,fromverse,data from commentary where book=="+str(bookinfo[0])+" and chapter=="+str(bookinfo[1])+" and fromverse==0"
  print sql
  c.execute(sql)
  rs=c.fetchone()
  if rs==None:
    return ''
  return rs[3]

def getBookcontent(bookinfo):
  sql="select book,chapter,fromverse,data from commentary where book=="+str(bookinfo[0])+" and chapter==0 and fromverse==0"
  c.execute(sql)
  rs=c.fetchone()
  if rs==None:
    return ''
  return rs[3]

allcon=u''
for item in rs:
  if item[1]==0 or item[2]==0:
    continue
  fullcontent=item[3]
  headercontent=u''
  if(item[2]==1):
    headercontent=getChaptercontent(item)
    if(item[1]==1):
       headercontent=getBookcontent(item)+headercontent
  fullcontent=headercontent+item[3]
  breakcontent1=re.sub(r'\r\n|<I>|</I>|<ol.*?>|</ol>|<TR.*?>|</TR>|<TD.*?>|</TD>|<TABLE.*?>|</TABLE>|<B>|</B>',' ',fullcontent)
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

