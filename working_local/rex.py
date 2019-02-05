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
import time
global driver
def InitBrowser():
    global driver
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 5)
    #link = "http://www.google.com"
    #link = "http://localhost:5000"
    link = "http://www.cnn.com"
    driver.get(link)
    driver.maximize_window()
    time.sleep(5)
    #link = "http://www.cnn.com"
    #link = "https://ttweb.indiainfoline.com/trade/Login.aspx"
    response = requests.get(link) #get page data from server, block redirects
    sourceCode = response.content #get string of source code from response

def ExitBrowser():
    global driver
    driver.quit()

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

def FindAllInputs() :
    f = open('list.txt', 'r')
    listOfInputs = []
    while  True:
      ostr = f.readline()
      if ostr == '':
         break
      x = re.search("InputElement",ostr)
      if x != []:
         rlist = []
         rlist=ParseWordSepratedWithHyphen(ostr)
         if rlist !=[]:
            listOfInputs.append(rlist)
      else:
         print("No input Fields  found")
         listOfInputs =[]

    return listOfInputs
    
def OLDFindAllInputs() :
    f = open('list.txt', 'r')
    listOfInputs = []
    while  True:
      ostr = f.readline()
      if ostr == '':
         break
      x = re.search("InputElement",ostr)
      if x != []:
         result = re.findall(r'=\'\w+', ostr)
         print("Debug: ",result)
         length = len(result)
         rlist = []
         for i in range(length):
             r = re.findall('[a-zA-Z]+[0-9]*', result[i])
             rlist.append(r[0]) 
         if len(rlist) == 2: # There has to be two fields name and type
            listOfInputs.append(rlist)
      else:
         print("No input Fields  found")
         listOfInputs =[]
    print(listOfInputs)

    return listOfInputs
def FindSeleniumHandles(list):
    global driver
    print("---------------------------------------------------------------")	
    print("Finding Selenium Elements")
    print("---------------------------------------------------------------")	
    print(list)
    print("--------------------End of List----------------------")	
    for element in list:
        rlist = element
        name = rlist[0]
        #name = name[1:-1]
        print(name)
        selinium_element = driver.find_element_by_name(name) 
        time.sleep(2)
        print(selinium_element)
        rlist.append(selinium_element)       
    print("---------------------------------------------------------------")	
    print("Finding Selenium Elements DONE !!!")
    print("---------------------------------------------------------------")	
    return list

def RefreshSeliniumHandles(list):
    print("---------------------------------------------------------------")	
    print("RefreshSeliniumHandles")
    print("---------------------------------------------------------------")	
    print("Length of list = ", len(list)) 
    for element in list:
        rlist = element
        print(rlist)
        del rlist[2] #Remove the Old Selinium Handle
        print("Deleted old handle")
        name = rlist[0]
        #name = name[1:-1]
        print(name)
        print("Finding selinium element")
        selinium_element = driver.find_element_by_name(name)
        print("Selinium element found")
        time.sleep(1)
        print(selinium_element)
        rlist.append(selinium_element) #Update the with new Selinium Handle 
    return list

def ActivateElements(list):
    global driver
    print("---------------------------------------------------------------")	
    print("ActivateElements")
    print("---------------------------------------------------------------")	
    for eachelement in list:
        print(eachelement[0],eachelement[1],eachelement[2])
        current_url =  driver.current_url
        if eachelement[1] == "text":
           found = False
           while found == False:
              try:
                 #wd = webdriver.connection
                 #hov = ActionChains(wd).move_to_element(eachelement[2])
                 #hov.perform() 
                 # Check for same page or not
                 eachelement[2].send_keys("Donald Trump") 
                 eachelement[2].submit() 
                 alert_obj = driver.switch_to.alert
                 time.sleep(1)
                 alert_obj.accept()
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
           try:
             #wd = webdriver.connection
             #hov = ActionChains(wd).move_to_element(eachelement[2])
             #hov.perform() 
             eachelement[2].send_keys("Hello123") 
             eachelement[2].submit() 
             alert_obj = driver.switch_to.alert
             time.sleep(5)
             alert_obj.accept()  
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


if __name__ == '__main__':
  global driver
  inputList=FindAllInputs() 
  print(inputList)
  InitBrowser()
  try:
     inputList = FindSeleniumHandles(inputList) 
     print(inputList)
     ActivateElements(inputList)
     ExitBrowser() 
  except RuntimeError:
     ExitBrowser() 
