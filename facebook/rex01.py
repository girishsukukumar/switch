import re
from  scanf import scanf
import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.common.action_chains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException  
from selenium.common.exceptions import NoSuchElementException  
from selenium.common.exceptions import StaleElementReferenceException  
import time
global driver
def InitBrowser():
    global driver
    driver = webdriver.Chrome()
    time.sleep(5)
    #link = "http://www.google.com"
    #link = "http://localhost:5000"
    #link = "http://www.yahoo.com"
    #link = "http://www.cnn.com"
    #link = "http://www.facebook.com"
    #link = "https://ttweb.indiainfoline.com/trade/Login.aspx"
    #response = requests.get(link) #get page data from server, block redirects
    #sourceCode = response.content #get string of source code from response
    #wait = WebDriverWait(driver, 5)
    #driver.get(link)
    #driver.maximize_window()

def ExitBrowser():
    global driver
    driver.quit()
def TestForInputElement(str):
   re1='.*?'       # Non-greedy match on filler
   re2='(InputElement)'    # Variable Name 1
   rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
   print(str)
   m = rg.search(str)
   returnVal = False 
   if m:
      var1=m.group(1)
      print(var1)
      returnVal = True
   return returnVal 
      
def ParseWordSepratedWithHyphen(txt):
#    txt='<InputElement 1b6885938b8 name=\'edition-pref-footer\' type=\'radio\'>'
#    txt='<InputElement 1b6885938b8 name=\'My Button\' type=\'radio\'>'

    re1='.*?'   # Non-greedy match on filler
    re2='(\\\'.*?\\\')' # Single Quote String 1
    re3='.*?'   # Non-greedy match on filler
    re4='(\\\'.*?\\\')' # Single Quote String 2

    rg = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)
    m = rg.search(txt)
    strn = []
    if m:
        strng1=m.group(1)
        strng2=m.group(2)
        strng1 = strng1[1:-1] 
        strng2 = strng2[1:-1] 
        strn.append(strng1)
        strn.append(strng2)
    return strn
def CheckAndExtractURL(str):
    txt='\'href\': \'http://www.google.com/\''

    re1='(.)'       # Any Single Character 1
    re2='(href)'    # Word 1
    re3='(.)'       # Any Single Character 2
    re4='(.)'       # Any Single Character 3
    re5='.*?'       # Non-greedy match on filler
    re6='((?:http|https)(?::\\/{2}[\\w]+)(?:[\\/|\\.]?)(?:[^\\s"]*))'       # HTTP URL 1

    rg = re.compile(re1+re2+re3+re4+re5+re6,re.IGNORECASE|re.DOTALL)
    m = rg.search(str)
    returnVal = "NO_MATCH"
    if m:
        c1=m.group(1)
        word1=m.group(2)
        c2=m.group(3)
        c3=m.group(4)
        httpurl1=m.group(5)
        returnVal = httpurl1
    return returnVal
def FindAllURL(rawList):
    print("-------------------------------------------")
    print("   ........ Extracting all URL ............")
    print("-------------------------------------------")

    listOfURL = []
    for ostr in rawList: 
      if ostr == '':
         break
      ans= CheckAndExtractURL(ostr) # Test this contain INPUTELEMENT or not
      if ans != "NO_MATCH": 
         print(ans)
         ans = ans[0:-2]
         print(ans)
         listOfURL.append(ans)
    return listOfURL

def FindAllInputs(rawList) :
    
    print("-------------------------------------------")
    print("   ........ Extracting all INPUT ELEMENTS .")
    print("-------------------------------------------")
    listOfInputs = []
    for ostr in rawList: 
      if ostr == '':
         break
      print(ostr)
      ans= TestForInputElement(str(ostr)) # Test this contain INPUTELEMENT or not
      if ans == True: 
         rlist = []
         rlist=ParseWordSepratedWithHyphen(str(ostr))
         if rlist !=[]:
            listOfInputs.append(rlist)
      else:
         print("skipping the line")

    return listOfInputs
    
def FindSeleniumHandles(list):
    global driver
    print("---------------------------------------------------------------")	
    print("Finding Selenium Elements")
    print("---------------------------------------------------------------")
    rlist = [] 
    for element in list:
        rlist = element
        name = rlist[0]
        #name = name[1:-1]
        #print(name)
        selinium_element = driver.find_element_by_name(name) 
        #time.sleep(2)
        #print(selinium_element)
        rlist.append(selinium_element)       
        print(element[0], element[1], element[2])
    print("---------------------------------------------------------------")	
    print("Finding Selenium Elements DONE !!!", len(rlist),"Handles")
    print("---------------------------------------------------------------")	
    return list

def RefreshSeliniumHandles(list):
    print("---------------------------------------------------------------")	
    print("RefreshSeliniumHandles")
    print("---------------------------------------------------------------")	
    print("Length of list = ", len(list)) 
    for element in list:
        rlist = element
        #print(rlist)
        del rlist[2] #Remove the Old Selinium Handle
        #print("Deleted old handle")
        name = rlist[0]
        #name = name[1:-1]
        #print(name)
        #print("Finding selinium element")
        selinium_element = driver.find_element_by_name(name)
        #print("Selinium element found")
        #time.sleep(1)
        #print(selinium_element)
        rlist.append(selinium_element) #Update the with new Selinium Handle 
    print("---------------------------------------------------------------")	
    print("RefreshSeliniumHandles Done")
    print("---------------------------------------------------------------")	
    return list

def ActivateElements(list):
    global driver
    print("---------------------------------------------------------------")	
    print("ActivateElements")
    print("---------------------------------------------------------------")	
    for eachelement in list:
        print(eachelement[0],eachelement[1],eachelement[2])
        current_url =  driver.current_url
        if eachelement[1] == "email":
           #print("Entering :",eachelement[0],eachelement[1])
           eachelement[2].send_keys("Apollo 11") 
           if current_url != driver.current_url:
                driver.back()
                list = RefreshSeliniumHandles(list)
                time.sleep(1)
        elif eachelement[1] == "text":
           found = False
           while found == False:
              try:
                 #wd = webdriver.connection
                 #hov = ActionChains(wd).move_to_element(eachelement[2])
                 #hov.perform() 
                 # Check for same page or not
                 #print("Entering text")
                 eachelement[2].send_keys("Apollo 11") 
                 #eachelement[2].submit() 
                 #alert_obj = driver.switch_to.alert
                 #time.sleep(1)
                 #alert_obj.accept()
                 if current_url != driver.current_url:
                    driver.back()
                    list = RefreshSeliniumHandles(list)
                    time.sleep(1)
                 found = True  
              except NoAlertPresentException :
                 print("Pop up did not come up for type=",
                    eachelement[1], eachelement[0])
                 driver.switch_to.default_content() 
                 if current_url != driver.current_url:
                    time.sleep(1)
                    driver.back()
                    try:
                       list = RefreshSeliniumHandles(list)
                    except NoSuchElementException:
                       print("Element not found during refresh")
                    time.sleep(1)
                 found = True  
                  
                
        elif eachelement[1] == "button":
           print("Entering Button")
           try:
             #wd = webdriver.connection
             #hov = ActionChains(wd).move_to_element(eachelement[2])
             #hov.perform() 
             eachelement[2].click() 
             time.sleep(5)
             alert_obj = driver.switch_to.alert
             time.sleep(5)
             alert_obj.accept()  
           except NoAlertPresentException :
             print("Pop up did not come up for type=", 
                     eachelement[1],eachelement[0])
             driver.switch_to.default_content() 
             if current_url != driver.current_url:
                time.sleep(1)
                driver.back()
                list = RefreshSeliniumHandles(list)
                time.sleep(1)
        elif eachelement[1] == "password":
           print("Entering Password")
           try:
             #wd = webdriver.connection
             #hov = ActionChains(wd).move_to_element(eachelement[2])
             #hov.perform() 
             try:
               eachelement[2].send_keys("01WinMsofficeioT34") 
               #eachelement[2].submit() 
               if current_url != driver.current_url:
                  time.sleep(1)
                  driver.back()
                  list = RefreshSeliniumHandles(list)
                  time.sleep(1)
             except StaleElementReferenceException:
               if current_url != driver.current_url:
                  time.sleep(1)
                  driver.back()
                  list = RefreshSeliniumHandles(list)
                 
             time.sleep(5)
           except NoAlertPresentException :
             print("Pop up did not come up for type=",
                    eachelement[1], eachelement[0])
             driver.switch_to.default_content() 
        elif eachelement[1] == "submit":
           print("Not Ready submit")
        elif eachelement[1] == "radio":
           print("Not Ready radio")
        elif eachelement[1] == "checkbox":
           print("Not Ready radio")
        else:
           print("Unknown type:")
           print(eachelement[1])

        time.sleep(1)
    return
def TravelURL(list):
    l = len(list)
    i = 0
    for link in list:
      i = i  + 1
      print(i, "of" , l,link)
      driver.get(link)    
      time.sleep(7)
      driver.back()
    return
def sprintf(buf, fmt, *args):
    buf.write(fmt % args)

def ScrapePage(LINK):
    global driver 

    inputList = []
    URLList = []

    print("-------------------------------------------------------------------") 
    print("-----------------------------------Scrape Page --------------------") 
    print("-------------------------------------------------------------------") 

    link = LINK
    driver.get(link)
    #driver.maximize_window()
    time.sleep(5)
    response = requests.get(link) #get page data from server, block redirects
    sourceCode = response.content #get string of source code from response
    print("----- Scrap page : Finding inputs ----- ")
    htmlElem = html.document_fromstring(sourceCode) #make HTML element object
    tdElems = htmlElem.cssselect("INPUT") #list of all td elems
    for elem in tdElems:
       if hasattr(elem, 'encode'):
           #print(elem.encode("utf-8"))
           inputList.append(elem.encode("utf-8")) 
       else:
           #print(elem)
           inputList.append(elem) 

    print("----- Scrap page : Finding href ----- ")
    tdElems = htmlElem.cssselect("a[href]") #list of all td elems

    for elem in tdElems:
       text = elem.text_content() #text inside each 
       if hasattr(text, 'encode'):
          #print(text.encode("utf-8") , ":", elem.attrib)
      
          str1 = (text.encode("utf-8"))  
          #str2 =  ":" 
          str3 =  elem.attrib
          #str  = str2 + str3 
          buf = "%s:%s" % (str1, str3)
          URLList.append(buf)
       else:
          #print(text, ":", elem.attrib)
          str = text + ":" + elem.attrib
          URLList.append(str)
    print(" ------------------- ScrapePage done ------------")
    return inputList, URLList

if __name__ == '__main__':
  global driver
  #link = "https://www.geeksforgeeks.org/" worked very well
  #link = "https://www.youtube.com/" did not work
  #link = "https://www.manoramaonline.com/" 
  #link = "https://www.iiitb.ac.in/"  worked
  #link = "https://www.instagram.com/"  
  #link = "https://www.amazon.com/"  
  link = "https://www.facebook.com/"  

  InitBrowser()
  rawInputList, rawlistOfURL =  ScrapePage(link)
  print(rawInputList)
  inputList = FindAllInputs(rawInputList) 
  listOfURL = FindAllURL(rawlistOfURL)
  print("Length of input list",len(inputList))
  print("Length of URL list",len(listOfURL))
  try:
     inputList = FindSeleniumHandles(inputList) 
     #print(inputList)
     ActivateElements(inputList)
     print("Total", len(listOfURL), "Found")
     TravelURL(listOfURL)
     ExitBrowser() 
  except RuntimeError:
     ExitBrowser() 
