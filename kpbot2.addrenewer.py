import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import win32com.client
import time
import os

shell = win32com.client.Dispatch("WScript.Shell")


#url="https://www.kupujemprodajem.com/Muzika-i-instrumenti/Gitarska-oprema-Efekti-i-pedale/Naga-viper-klon-77885974-oglas.htm?filter_id="

#url="https://www.kupujemprodajem.com/Muzika-i-instrumenti/Gitarska-oprema-Efekti-i-pedale/Super-hard-on-klon-77886533-oglas.htm?filter_id="

#url="https://www.kupujemprodajem.com/Muzika-i-instrumenti/Gitarska-oprema-Efekti-i-pedale/Keeley-katana-clean-klon-77887546-oglas.htm?utm_source=KP&utm_campaign=PrevAd&filter_id=0"
##url="https://www.kupujemprodajem.com/Lov-i-ribolov/Ribolov-Stapovi/Silstar-MXB-tele-rod-78706956-oglas.htm?filter_id=5368208"

#url="https://www.kupujemprodajem.com/Foto/Profesionalna-fotooprema/knjiga-o-fotografiji-1970-god--78665866-oglas.htm?filter_id=25"

#url="https://www.kupujemprodajem.com/Foto/Foto-adapteri/Preobratni-makro-prstenovi-58-58-36318410-oglas.htm?utm_source=KP&utm_campaign=NextAd"
#url="https://www.kupujemprodajem.com/Bela-tehnika-i-kucni-aparati/Ves-masine/Prodaja-i-popravak-ves-masina-22033127-oglas.htm?filter_id=155728982"
#url="https://www.kupujemprodajem.com/Automobili-Delovi-i-alati/Automobili-za-delove/Ford-polovni-delovi-78667710-oglas.htm?filter_id=16"
#url="https://www.kupujemprodajem.com/Kompjuteri-Laptop-i-tablet/Laptopovi-Maticne-ploce/Acer-Aspire-5230-maticna-ploca--63273921-oglas.htm?filter_id=3810398"

results = requests.get(url)
content = results.content
soup=BeautifulSoup(content,"lxml")


#some of the adds returned a lot of \t's and \n's so i wrote this little thing to remove those.
#this part is scraping the descritpion part of the add, or the central part of every add
tekst=soup.find("div",{"class":"oglas-description"})
tekst=tekst.text
if "\t" in tekst:
    tekst=tekst.replace("\t","")
if "\n" in tekst[0:5]:
    tekst=tekst[0:5].replace("\n","")+tekst[5:]

#this part scrapes the name of the add
naslov=soup.find("h1",{"class":"oglas-title"})
naslov=naslov.text

#this part gets the info used for cathegorizing the add
kategorija=soup.find("div",{"class":"breadcrumbs"})
kategorija=kategorija.find("a").text


#sub cathegory
breadcrumbs = soup.find("div", {"class": "breadcrumbs"})
pod_kategorija = breadcrumbs.find_all("a")
pod_kategorija
pk = []

for x in pod_kategorija:
    pk.append(x.text)

pod_kategorija = pk[-1]

#id_oglasa is the most important part for scrapping pictures.
#originally, i used the webpage it self to scrape pictures, 
#but those pictures were of lower quality,
#there is a special part of the website on which pictures are stored,
#but it is not in the most obvious part of the website
id_oglasa = breadcrumbs.find("span", {"class": "oglasId"}).text

if "> ID oglasa: #" in id_oglasa:
    id_oglasa = id_oglasa.replace("> ID oglasa: #", "")


#every id number had 8 characters, so ...
id_oglasa = id_oglasa[:8]

#id_oglasa
#this part gets the info about the status of the item being sold
stanje=soup.find("span",{"class":"item-state"})
stanje=stanje.text
stanje=stanje[1:-1]
if stanje == "Kao novo - nekorišćeno":
    stanje=stanje[:8]
if stanje =="Neispravno ili oštećeno":
    stanje="Neispravno / oštećeno"

#this is the part in whoich id_oglasa is used, to scrape good quality photos
url_slike = "https://www.kupujemprodajem.com/big-photo-" + id_oglasa + "-1.htm"

slicice_sajt = requests.get(url_slike)
slicice_content = slicice_sajt.content
soup2 = BeautifulSoup(slicice_content, "lxml")
slicice = soup2.find("div", {"class": "thumbs-holder-inner"})
slicice = slicice.find_all("a")

l1 = []

for x in slicice:
    x = x.get("photo-path")
    x = "https://images.kupujemprodajem.com" + x
    l1.append(x)

brojevi = []
for i in range(1, len(l1) + 1):
    brojevi.append(i)

#originally i wanted to use lists and functions, but i noticed that i needed 2 inputs
#because i wanted it to name pictures in a simple manner and use the list
#because i will later call the list to scrape the names
#of the pictures
dic = dict(zip(brojevi, l1))
dir_name = "slike"

#checks about the existence of slike folder, in which photos will be scraped
#if there is no such folder, it will create it.
try:

    # Create target Directory
    os.mkdir("C:\\" + dir_name)
    print("Directory ", dir_name, " Created ")
except FileExistsError:
    print("Directory ", dir_name, " already exists")

l2 = []

#this part simultaniously names pictures and makes a list of names to be used later
#when searching for pictures in folder
for k, i in dic.items():
    x = str(k) + '.jpg'
    f = open("c:\\slike\\" + x, "wb")
    f.write(requests.get(i).content)
    l2.append(str(k))
    f.close()
#i noticed that if i typed in "1" "2" "3" ....  exactly this way, with "" and no comas, i could at once upload several pictures
#this was very usefull, as selenium would lose it and stop working after uploading 5th pictures individually, one after the other
l3 = '""'.join(l2)
l3 = '"' + l3 + '"'

user = ""
pas = ""
url2 = "https://kupujemprodajem.com"

browser = webdriver.Chrome("C:\chromedriver.exe")

browser.get(url2)

browser.find_element_by_xpath("//a[contains(text(),'Ulogujte se')]").click()
browser.find_element_by_xpath("//input[@type='text']").send_keys(user)
browser.find_element_by_xpath("//input[@name='data[password]']").send_keys(pas)
browser.find_element_by_xpath("//input[@type='submit']").click()
browser.find_element_by_xpath("//a[@class='bigLink submitAd']").click()
browser.find_element_by_xpath("//input[@type='radio']").click()
browser.implicitly_wait(30)
browser.find_element_by_xpath(
    "//div[@id='categorySelection']//div[@class='uiMenuButton']//div[@class='uiMenuButtonSelectionHolder']//div[@class='uiInlineBlock uiMenuHolder']//div//input").send_keys(
    kategorija)
browser.implicitly_wait(30)

#this is the first time in my life that i tried, and managed, to edit and manipulate xpath
#i noticed that there is a repeating pattern, except the part in which i placed my variable
#this, and other instances of such use, made this script so powerful and limitless
browser.find_element_by_xpath("//div[contains(text(),'" + kategorija + "')]").click()
browser.implicitly_wait(30)
browser.find_element_by_xpath(
    "//div[@id='groupSelection']//div[@class='uiMenuButton']//div[@class='uiMenuButtonSelectionHolder']//div[@class='uiInlineBlock uiMenuHolder']//div//input").send_keys(
    pod_kategorija)
browser.implicitly_wait(30)
browser.find_element_by_xpath("//div[contains(text(),'" + pod_kategorija + "')]").click()
browser.implicitly_wait(30)
browser.find_element_by_xpath("//input[@id='data[name]']").send_keys(naslov)
browser.implicitly_wait(30)
browser.find_element_by_xpath("//label[contains(text(),'" + stanje + "')]").click()
browser.implicitly_wait(30)
browser.find_element_by_xpath(
    "//div[@class='form-field']//div[@class='uiInlineBlock']//div[@class='uiMenuButtonInner']").click()
browser.implicitly_wait(30)
browser.find_element_by_xpath("//div[contains(text(),'Kontakt')]").click()
browser.implicitly_wait(30)
# browser.find_element_by_xpath("//input[@value='rsd']").click()

time.sleep(3)
#in this part, iframe and js made it a bit of a problem, so i had to go around it.
#i noticed that my xpath, the ELEM variable, shows up only when iframe was active.
#switch_to.frame was very very helpful
path = browser.find_element_by_xpath("//iframe[@id='data[description]_ifr']")
browser.switch_to.frame(path)
browser.implicitly_wait(30)

elem = browser.find_element_by_xpath("//body[@class='mceContentBody ']")
elem.send_keys(tekst)

browser.switch_to.default_content()

browser.implicitly_wait(30)


# so in this part it is necessary to click a button, which opens up a window
#by default it opens in c:\user\ directory
#i needed it to go to a specific directory.
#this was a bitch of a problem to fix.
#i tried using os, it didn't work.
#i tried many shell.COMMANDS but they didn't work.
#i am sure that there is a very precise command that gets this done
#however i couldn't find it
#so i used a brute force aproach, i calculated how many clicks are necessary, for example F4 command goes straight to
#the part in which addresses are being typed in
#and after that how, i also calculated many clicks of a tab button are necessary 
#to return to the part in which typing in name of the picture
#has to be done
#but it works
browser.find_element_by_class_name("addPhotoButtonSquare").click()
# browser.find_element_by_xpath("//div[@class='addPhotoButtonSquare']").click()
time.sleep(2)
# shell.SHBrowseForFolder(win32gui.GetDesktopWindow (),"C:\\slike",0,None,None)

shell.Sendkeys("{F4}")
time.sleep(2)
shell.Sendkeys("^a")
time.sleep(2)
# shell.Sendkeys("{BS}")
# for i in range(1,16):
#     shell.Sendkeys("{BS}")
#     time.sleep(1)

shell.Sendkeys("{BS}")
time.sleep(2)

shell.Sendkeys("c:\\slike")

time.sleep(3)
shell.Sendkeys("~")
time.sleep(3)
for i in range(1, 6):
    shell.Sendkeys("{TAB}")
    time.sleep(1)

shell.Sendkeys(l3)
time.sleep(3)
shell.Sendkeys("~")
time.sleep(15)

browser.implicitly_wait(30)
browser.find_element_by_xpath(
    "//div[@class='table with-border']//div[@class='adFormPostButtonHolder']//input[@class='submit-button']").click()
browser.implicitly_wait(30)
time.sleep(5)
browser.find_element_by_xpath("//input[@id='data[promo_type]none']").click()
browser.implicitly_wait(30)
browser.find_element_by_xpath(
    "//div[@id='adFormPromo']//div[@class='adFormPostButtonHolder']//input[@class='submit-button']").click()
time.sleep(5)
browser.find_element_by_xpath("//input[@id='swear_yes']").click()
time.sleep(5)
browser.implicitly_wait(30)
browser.find_element_by_xpath("//input[@id='accept_yes']").click()
browser.implicitly_wait(30)
browser.find_element_by_xpath(
    "//div[@class='prev-next-step-holder form-field']//div[@class='adFormPostButtonHolder']//input[@name='submit[post]']").click()
time.sleep(3)
browser.quit()

#this part goes to the folder, which pictures for the add are stored, and deltes them :)
for i in l2:
    i=str(i)+".jpg"
    #print(i)
    if i in os.listdir("c:\\slike\\"):

        #print(i)
        os.remove("c:\\slike\\"+i)
