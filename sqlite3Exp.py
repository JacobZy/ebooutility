# -*- coding: utf-8 -*-

from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.xhtml.reader import XHTMLReader
from pyth.plugins.xhtml.writer import XHTMLWriter
import rtf2text
import sqlite3



if __name__ == '__main__':
    # Parse the document and then reconstruct it using the xhtml
    # writer.
    #doc = XHTMLReader.read(content, css)
    #print XHTMLWriter.write(doc).getvalue()

    #doc = Rtf15Reader.read(content2)

    #print XHTMLWriter.write(doc, pretty=True).read()
    #print rtf2text.striprtf(content4)
    conn=sqlite3.connect('rmac.dct.mybible')
    connw=sqlite3.connect('Robinson.dct.twm')
    c=conn.cursor()
    cw=connw.cursor()
    sql="select word,data from dictionary" # where word like 'M%' order by word asc
    c.execute(sql)    
    
    i=0
    for item in c.fetchall():      
      if item[0].startswith('M')==False:
        continue
      print item[0]
      print item[1]
      i=i+1
      print item[0]
      print item[1]
      cw.execute("INSERT INTO topics (pid,subject,rel_order,content_type) VALUES (0,?,?,NULL)",(item[0],1100+i))         
      cw.execute("INSERT INTO topics_wordindex (id,word,priority) VALUES (?,?,1)",(1100+i,item[0]))
      cw.execute("INSERT INTO content (data,data2) VALUES ('"+item[1]+"',NULL)")
    connw.commit()

