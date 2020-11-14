from urllib.request import urlopen , Request
from bs4 import BeautifulSoup as bs
#from win10toast import ToastNotifier

header = {"User-Agent":"Mozilla"}

req = Request("https://www.worldometers.info/coronavirus/country/india/" , headers = header)

html = urlopen(req)

obj = bs(html, 'html.parser')

# we can use direclty strong to get the first child value
#new_cases = obj.find("li" , {"class":"news_li"}).strong.text.split()[0]
new_cases = obj.find("div" , {"class":"maincounter-number"}).text.split()[0]

print(new_cases)

#death = list(obj.find("li" , {"class":"news_li"}).next_sibilings)[1].text.split()[0]
death = obj.find("div" , {"id":"maincounter-wrap"}).text.split()[2]
print(death)