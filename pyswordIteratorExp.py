from pysword.modules import SwordModules
import re
# Load module in zip
# NB: the zip content is only available as long as the SwordModules object exists
modules = SwordModules('KJV.zip')
# In this case the module found is:
# {'KJV': {'description': 'KingJamesVersion(1769)withStrongsNumbersandMorphology', 'encoding': 'UTF-8', ...}}
found_modules = modules.parse_modules()
bible = modules.get_bible_from_module('KJV')
# Get John chapter 3 verse 16
#output = bible.get(books=['john'], chapters=[3], verses=[16], clean=False)

#print bible.get_structure()
#print output

f=open('text.txt','w')

n=0
contents=u''
for item in bible.get_iter(clean=False):
  sentens=re.findall(r'<w lemma="(.+?)"( morph="(.+?)")?( src=".+?")?>(.+?)</w>(.)',item)
  for word in sentens:
    strongs=re.findall(r'strong:((G|H)\d+)',word[0])
    morphs=re.findall(r'(robinson|strongMorph):(\S+)',word[2])
    ww=word[4]
    comma=word[5]
   
    contents=contents+ww
    comp1=zip(strongs,morphs)
    for strong,morph in comp1:
      contents=contents+u'<W'+strong[0]+u'>'
      if morph[0]=='robinson':
        contents=contents+u'<WT'+morph[1]+u'>'
      elif morph[0]=='strongMorph':
        contents=contents+morph[1].replace(u'T',u'W')+u'>'
    for i in range(len(comp1),len(strongs)):
      contents=contents+u'<W'+strongs[i][0]+u'>'

    contents=contents+comma
  contents=contents+u'\n'
  n=n+1
  if n%1000==0:
    f.write(contents.encode('utf-8'))
    contents=u''
  print n
  


f.write(contents.encode('utf-8'))
f.flush()
f.close()
