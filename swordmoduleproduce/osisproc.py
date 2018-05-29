# -*- coding=utf-8 -*-
import re
import io


def verserepel(reobj):
  rs=re.findall(r'<u>(.+?)</u>',reobj.group())
  ref=''
  for item in rs:
    sl=re.split('_|:|-',item)
    if len(sl)==3:
      if sl[1]=='Rth':
        sl[1]='Ruth'
      ref=ref+sl[0]+'.'+sl[1]+'.'+sl[2]
    if len(sl)==4:
      if sl[1]=='Rth':
        sl[1]='Ruth'
      ref=ref+sl[0]+'.'+sl[1]+'.'+sl[2]+'-'+ref+sl[0]+'.'+sl[1]+'.'+sl[3]
    ref=ref+' '
  return '<p><reference osisRef="'+ref.strip()+'">'+ref+'</reference></p>'+reobj.group(1)

def verserepel1(reobj):
  rs=re.findall(r'<u>(.+?)</u>',reobj.group())
  ref=''
  for item in rs:
    sl=re.split('_|:|-',item)
    if len(sl)==3:
      if sl[1]=='Rth':
        sl[1]='Ruth'
      ref=ref+sl[0]+'.'+sl[1]+'.'+sl[2]
    if len(sl)==4:
      if sl[1]=='Rth':
        sl[1]='Ruth'
      ref=ref+sl[0]+'.'+sl[1]+'.'+sl[2]+'-'+ref+sl[0]+'.'+sl[1]+'.'+sl[3]
    ref=ref+' '
  return '<p><reference osisRef="'+ref.strip()+'">'+ref+'</reference></p>'

sourcefile = io.open('tske.txt','r',encoding='utf8')
with io.open('bookintro.csv','r',encoding='utf8') as bookfile:
    bookall = bookfile.read()
with io.open('chapterintro.csv','r',encoding='utf8') as chapterfile:
    chapterall = chapterfile.read()

resultfile = io.open('tskeResult','w',encoding='utf8')

allcon=u''
for line in sourcefile.readlines():
  verse=line.split('\t')
  content=verse[1]
  bookandnum=verse[0].split(' ')
  bookt=bookandnum[0]
  seqnum=bookandnum[1].split(':')
  chapternum=seqnum[0]
  versenum=seqnum[1]
  print bookt+' '+chapternum+' '+versenum
  
  if '1'==versenum:
      restr=r'^'+bookt+r' '+chapternum+':\t(.+?)$'
      print 'print chapter info'+bookt+' '+chapternum+' '+versenum
      chapterinfo=re.search(restr,chapterall,re.M)
      if chapterinfo!=None:
          content=content+'<br><br>'+chapterinfo.group(1)

      if '1'==chapternum and '1'==versenum:
          print 'print book info'+bookt+' '+chapternum+' '+versenum
          bookinfo=re.search(r'^'+bookt+r'\t(.+?)$',bookall,re.M)
          if bookinfo!=None:
              content=content+'<br><br>'+bookinfo.group(1)
      
  strongcontent=re.sub(r'\[(\w\d+)\]',lambda m:'<w lemma="'+'strong:'+m.group(1)+'">'+m.group(1)+'</w>',content)
  refcontent1=re.sub(r'<u>.+?</u>([^,])',verserepel,strongcontent)
  refcontent2=re.sub(r'<i>|</i>|<p>|</p><gu></gu>','',refcontent1)
  refcontent3=re.sub(r'<u>.+?</u>',verserepel1,refcontent2)
  refcontent4=re.sub(r'<table.+?</table>','',refcontent3)
  refcontent5=re.sub(r'\n','<br>',refcontent4)
  refcontent6=re.sub(r'<br>(.+?)<br>',lambda m:'<p>'+m.group(1)+'</p>',refcontent5)
  refcontent=re.sub(r'<br>|<b>|</b>',' ',refcontent6)

  if bookt=='Rth':
        bookt='Ruth'
  allcon=allcon+'<div type="section" annotateType="commentary" annotateRef="'+bookt+'.'+chapternum+'.'+versenum+'"><p>'+refcontent+'</p></div>'+'\n'

  if '1'==chapternum and '1'==versenum:
    resultfile.write(allcon)
    resultfile.flush()
    allcon=u''

  

  #print content    
  #break
  

resultfile.write(allcon)
resultfile.close()

