# -*- coding=utf-8 -*-
import re
import io
import html2textnew
# for output commentary for xiphos crosswire sword module
def verserepel(reobj):
  rs=re.findall(r'_(\w.+?\d)_',reobj.group())
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
      ref=ref+sl[0]+'.'+sl[1]+'.'+sl[2]+'-'+sl[0]+'.'+sl[1]+'.'+sl[3]
    ref=ref+' '
  return '<reference osisRef="'+ref.strip()+'">'+ref+'</reference>'

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
  
  text=html2textnew.html2text(content)
  strongcontent=re.sub(r'\[(\w\d+)\]',lambda m:'<w lemma="'+'strong:'+m.group(1)+'">'+m.group(1)+'</w>',text)
  refcontent=re.sub(r'_\w.+\d_',verserepel,strongcontent)
  blcontent=re.sub(r'\n','<br />\n',refcontent)
  

  if bookt=='Rth':
        bookt='Ruth'
  allcon=allcon+'<div type="section" annotateType="commentary" annotateRef="'+bookt+'.'+chapternum+'.'+versenum+'"><p>'+blcontent+'</p></div>'+'\n'

  if '1'==chapternum and '1'==versenum:
    resultfile.write(allcon)
    resultfile.flush()
    allcon=u''

resultfile.write(allcon)
resultfile.close()

