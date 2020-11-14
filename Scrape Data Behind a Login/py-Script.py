import requests
from bs4 import BeautifulSoup as bs
"""https://twistedmatrix.com/Releases/Twisted/19.7/Twisted-19.7.0-cp27-cp27m-win_amd64.whl"""

'''
https://www.amazon.com/robots.txt  tells us the restricted scrapping data
'''
URL = 'https://shorttracker.co.uk/'
LOGIN_ROUTE = 'accounts/login/'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'origin' : URL ,
    'referer' : URL + LOGIN_ROUTE
}

login = 'agn28478@eoopy.com'
password = 'Test@123'

# getting the session which will work similar to browser sessions
s = requests.session()
csrf_token = s.get(URL).cookies['csrftoken']

login_payLoad = {
    'login': login,
    'password':password,
    'csrfmiddlewaretoken' : csrf_token
 }

# login is a post request we get from the session

login_req  = s.post(URL + LOGIN_ROUTE , headers = HEADERS , data = login_payLoad)

print(login_req.status_code)

cookies = login_req.cookies

soup = bs(s.get(URL + 'watchlist').text , 'html.parser')
tbody = soup.find('table', id= 'companies')

print(tbody)
