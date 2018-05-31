# -*- coding=utf-8 -*-
import re
import sqlite3

# output old testament kjv with morph module for xiphos crosswire sword  use morph pretent to be strong
abres=["None","Gen","Exod","Lev","Num","Deut","Josh","Judg","Ruth","1Sam","2Sam","1Kgs","2Kgs","1Chr","2Chr","Ezra","Neh","Esth","Job","Ps","Prov","Eccl","Song","Isa","Jer","Lam","Ezek","Dan","Hos","Joel","Amos","Obad","Jonah","Mic","Nah","Hab","Zeph","Hag","Zech","Mal","Matt","Mark","Luke","John","Acts","Rom","1Cor","2Cor","Gal","Eph","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Heb","Jas","1Pet","2Pet","1John","2John","3John","Jude","Rev"]
books=["None","Genesis","Exodus","Leviticus","Numbers","Deuteronomy","Joshua","Judges","Ruth","1 Samuel","2 Samuel","1 Kings","2 Kings","1 Chronicles","2 Chronicles","Ezra","Nehemiah","Esther[6]","Job","Psalms","Proverbs","Ecclesiastes","Song of Solomon","Isaiah","Jeremiah","Lamentations","Ezekiel","Daniel","Hosea","Joel","Amos","Obadiah","Jonah","Micah","Nahum","Habakkuk","Zephaniah","Haggai","Zechariah","Malachi","Matthew","Mark","Luke","John","Acts","Romans","1 Corinthians","2 Corinthians","Galatians","Ephesians","Philippians","Colossians","1 Thessalonians","2 Thessalonians","1 Timothy","2 Timothy","Titus","Philemon","Hebrews","James","1 Peter","2 Peter","1 John","2 John","3 John","Jude","Revelation"]

bookfile=open('kjvhebrewmorph','w')

conn=sqlite3.connect('kjvhebpar.bbl.mybible')
c=conn.cursor()

sql="select Book,Chapter,Verse,Scripture from Bible order by Book asc,Chapter asc,Verse asc"
c.execute(sql)

def seqnumprocess(seqnum):
  if len(seqnum)<5:
    seqnum='0'+seqnum
  return seqnum

def convertverse(verse):
  words=re.findall(r'[^<>]+(?:<WT?[HM]\d+>)+',verse)
  verss=u''
  for word in words:
    wo=re.match(r'(.+?)<',word)
    pars=re.findall(r'<WTM(\d+)>',word)
    strongs=u''
    morphs=u''
    for item in pars:
      strongs=strongs+'strong:H'+seqnumprocess(item)+' '
      #else:
       # morphs=morphs+'rmacplus:'+item+' '
    verss=verss+'<w lemma="'+strongs.strip()+'">'+wo.group(1)+'</w>'
  return verss

booknum=0
chapternum=0
versenum=0
n=0
content=u''
for item in c.fetchall():      
  n=n+1
  print n
  if item[0]==1 and item[1]==1 and item[2]==1:
    content=content+'<title>Old Testament</title>'
  if item[0]==40 and item[1]==1 and item[2]==1:
    content=content+'<title>New Testament</title>'

  if item[0]!=booknum:
    chapternum=0    
    if booknum!=0:
      content=content+'</div>\n'
    content=content+'<div type="book" osisID="'+abres[item[0]]+'" canonical="true">\n'
    content=content+'<title type="main" short="'+books[item[0]]+'">'+books[item[0]]+'</title>\n'

  if item[1]!=chapternum:
    bookfile.write(content.encode('utf-8'))
    bookfile.flush()
    content=u''
    if chapternum!=0:
      content=content+'</chapter>\n'
    content=content+'<chapter osisID="'+abres[item[0]]+'.'+str(item[1])+'" chapterTitle="CHAPTER '+str(item[1])+'.">'
    content=content+'<title type="chapter">CHAPTER '+str(item[1])+'.</title>\n'

  content=content+'<verse sID="'+abres[item[0]]+'.'+str(item[1])+'.'+str(item[2])+'" osisID="'+abres[item[0]]+'.'+str(item[1])+'.'+str(item[2])+'"/>'+convertverse(item[3])+'<verse eID="'+abres[item[0]]+'.'+str(item[1])+'.'+str(item[2])+'"/>\n'

  booknum=item[0]
  chapternum=item[1]
  versenum=item[2]
  
content=content+'</chapter>'
content=content+'</div>'
bookfile.write(content.encode('utf-8'))
bookfile.close()

