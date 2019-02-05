import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.common.action_chains  
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import unicodedata
import time


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)
#link = "http://localhost:5000"
#link = "http://www.google.com"
link = "http://www.cnn.com"
#link  = "https://www.geeksforgeeks.org/"
#link = "https://ttweb.indiainfoline.com/trade/Login.aspx"

driver.get(link)
driver.maximize_window()
time.sleep(5)
response = requests.get(link) #get page data from server, block redirects
sourceCode = response.content #get string of source code from response



#print(sourceCode)
htmlElem = html.document_fromstring(sourceCode) #make HTML element object
#print(htmlElem)
tdElems = htmlElem.cssselect("INPUT") #list of all td elems
#print(tdElems)

for elem in tdElems:
   if hasattr(elem, 'encode'):
       print(elem.encode("utf-8"))
   else:
       print(elem)


print("HREF:------------------------------------------------\n\n\n\n")   
tdElems = htmlElem.cssselect("a[href]") #list of all td elems
#print(len(tdElems))

for elem in tdElems:
   text = elem.text_content() #text inside each 
   #text = u.encode('ascii', elem.text_content())
   #text = elem.text_content().encode('ascii') 
   #str = unicode(str, errors='ignore') Copy pasted from stack overflow
   #text = unicode(elem.text_content(), errors='ignore')
   #text = unicode(elem.text_content.unicode(errors='ignore'))
   #print(dir(elem))

   if hasattr(text, 'encode'):
      print(text.encode("utf-8") , ":", elem.attrib)
   else:
      print(text, ":", elem.attrib)
  
tdElems = htmlElem.cssselect("[post]") #list of all td elems

for elem in tdElems:
   text = elem.text_content() #text inside each 
driver.quit()
