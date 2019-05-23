from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.chrome.options import Options
import time
import os
import win32com.client



shell = win32com.client.Dispatch("WScript.Shell")


url="https://kupujemprodajem.com"
cena=
naslov=
tekst=
user=
pas=



browser = webdriver.Chrome("C:\chromedriver.exe")

browser.get(url)

browser.find_element_by_xpath("//a[contains(text(),'Ulogujte se')]").click()
browser.find_element_by_xpath("//input[@type='text']").send_keys(user)
browser.find_element_by_xpath("//input[@name='data[password]']").send_keys(pas)
browser.find_element_by_xpath("//input[@type='submit']").click()
browser.find_element_by_xpath("//a[@class='bigLink submitAd']").click()
browser.find_element_by_xpath("//input[@type='radio']").click()
browser.implicitly_wait(30)
browser.find_element_by_xpath("//div[@id='categorySelection']//div[@class='uiMenuButton']//div[@class='uiMenuButtonSelectionHolder']//div[@class='uiInlineBlock uiMenuHolder']//div//input").send_keys("muzika i instrumenti")
browser.implicitly_wait(30)
browser.find_element_by_xpath("//div[contains(text(),'Muzika i instrumenti')]").click()
browser.implicitly_wait(30)
browser.find_element_by_xpath("//div[@id='groupSelection']//div[@class='uiMenuButton']//div[@class='uiMenuButtonSelectionHolder']//div[@class='uiInlineBlock uiMenuHolder']//div//input").send_keys("efekt")
browser.implicitly_wait(30)
browser.find_element_by_xpath("//div[contains(text(),'Gitarska oprema | Efekti i pedale')]").click()
browser.implicitly_wait(30)
browser.find_element_by_xpath("//input[@id='data[name]']").send_keys(naslov)
browser.implicitly_wait(30)
browser.find_element_by_xpath("//label[contains(text(),'Kao novo')]").click()
browser.implicitly_wait(30)
browser.find_element_by_xpath("//input[@id='price_number']").send_keys(cena)
browser.implicitly_wait(30)
browser.find_element_by_xpath("//input[@value='rsd']").click()

time.sleep(3)


#For some reason, webdesigner used iframe for descritpion part
#so i had to find a way how to get around that one
#so i figured that switch_to.frame is the best solution for this


path=browser.find_element_by_xpath("//iframe[@id='data[description]_ifr']")

browser.switch_to.frame(path)

browser.implicitly_wait(30)

elem=browser.find_element_by_xpath("//body[@class='mceContentBody ']")
elem.send_keys(tekst)

browser.switch_to.default_content()

#i created this loop, because for other adds, i believe that i will have more than just 2 photos, and being lazy as i am
#loop was a much better choice than typing it over and over again

#fun fact, i really didn't know how to add a photo to a browser, from my HDD, it didn;t accept send_keys()
#with a variable which loaded the image from the HDD
#also drag and drop doesn't work here
#after trying many different things i accidentally stumbled upon win32com.client library.
#also, i had to use sleep, not implicitly wait, as win32 shell is much faster than selenium.
#it would type in only a couple of letters, so i figgured it needed time to load everything.

for x in ("prva.jpg","druga.jpg"):
    browser.find_element_by_xpath("//div[@class='thumbHolder']").click()
    time.sleep(3)
    shell.Sendkeys(x)
    shell.Sendkeys("~")
    time.sleep(5)

browser.implicitly_wait(30)
browser.find_element_by_xpath("//div[@class='table with-border']//div[@class='adFormPostButtonHolder']//input[@class='submit-button']").click()
browser.implicitly_wait(30)
time.sleep(3)
browser.find_element_by_xpath("//input[@id='data[promo_type]none']").click()
browser.implicitly_wait(30)
browser.find_element_by_xpath("//div[@id='adFormPromo']//div[@class='adFormPostButtonHolder']//input[@class='submit-button']").click()
time.sleep(3)
browser.find_element_by_xpath("//input[@id='swear_yes']").click()
browser.implicitly_wait(30)
browser.find_element_by_xpath("//input[@id='accept_yes']").click()
browser.implicitly_wait(30)
browser.find_element_by_xpath("//div[@class='prev-next-step-holder form-field']//div[@class='adFormPostButtonHolder']//input[@name='submit[post]']").click()
time.sleep(3)
browser.quit()
