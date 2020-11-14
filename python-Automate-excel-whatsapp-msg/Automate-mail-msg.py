# email link 

# https://www.youtube.com/redirect?v=JRCJ6RtE3xU&event=video_description&redir_token=QUFFLUhqbno2c2tTdExRbnFQNnhEbmlILS00VEJFRTJBZ3xBQ3Jtc0tuaEFralhWOU05YUpiWjlidk5IVzR0UlRicmFEMWxBT0E4alUyTjU0b3htT1ZUQllpeExUQXMwaUI0UXY3dFl3MDBIbFF5WU1VZWRMVXRFQVB1bmc5cHhvNi1YTkN1WTgtZ0JxRUdMLW5jUUZDV3J0SQ%3D%3D&q=https%3A%2F%2Fmyaccount.google.com%2Flesssecureapps
import urllib.parse
import re
import os,smtplib
import imghdr
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import urllib.parse
from selenium.webdriver.support.ui import WebDriverWait
import urllib
import time
# All the global terms
###############################################################################################################
EMAIL_ADDRESS = '\.com'
EMAIL_PASSWORD = ''
FILE_NAME = 'List-of-Bill-Pay.xlsx'
DUE_DATE_DIFF = 2

subject = 'dfdfd'

body = '''
Dear 

Thank you,
Kaushik
'''
###############################################################################################################

def config_read():
    global EMAIL_PASSWORD ,EMAIL_ADDRESS ,FILE_NAME , DUE_DATE_DIFF , subject , body
    filename = 'external.config.txt'
    contents = open(filename).read()
    
    config =eval(contents)
    
    EMAIL_ADDRESS = config['EMAIL_ADDRESS']
    EMAIL_PASSWORD = config['EMAIL_PASSWORD']
    FILE_NAME = config['FILE_NAME']
    DUE_DATE_DIFF = int(config['DUE_DATE_DIFF'])
    subject = config['subject']
    body = config['body']

config_read()
print(body)

# sending email
def sendEmail(subject , body , fromAddress , toAddress , filePath , fileName):

    filePath = filePath +"\\"+fileName
    filePath = re.sub(r"\\","//",filePath )
    print(filePath)
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = toAddress
    msg.set_content(body)

    with open(filePath,'rb') as f:
        file_data = f.read()

    msg.add_attachment(file_data ,maintype='application' , subtype='octet-stream', filename = fileName)

    with smtplib.SMTP_SSL('smtp.gmail.com' ,  465) as smtp:

        smtp.login(EMAIL_ADDRESS , EMAIL_PASSWORD)

        smtp.send_message(msg)
        print('mail sent')         
from selenium.webdriver.common.keys import Keys
# sending whatsapp message
def sendWhatsApp(phoneNum , body, filePath , fileName):    
    
    
    print("in sendWhatsApp method")
    url = 'https://web.whatsapp.com/send?phone='+str(phoneNum)+'&text='+urllib.parse.quote(bodyTemp)
    driver.get(url)
    filePath = filePath +"\\"+fileName
    filePath = re.sub(r"\\","//",filePath )
    time.sleep(5)
    send = driver.find_element_by_xpath('//span[@data-icon="send"]')
    send.click()
    
    print(filePath)
    
    attachment_box = driver.find_element_by_xpath('//div[@title = "Attach"]')
    attachment_box.click()
    
    print(" Attachement attached")    
    attachment = driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
    attachment.send_keys(file_name)
    
    sleep(5)
    boc = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div')
    boc.click()
    
    print("whatsapp  send successfully.")

from webdriver_manager.chrome import ChromeDriverManager
#loading web driver
try:
    driver= webdriver.Chrome()
except:
    print('installing webdriver')
    
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
wait = WebDriverWait(driver, 20)
driver.get('https://web.whatsapp.com/')
input('Enter anything after scanning QR code')

import pandas as pd
import shutil

df = pd.read_excel(FILE_NAME)

df['Due date'] = pd.to_datetime(df['Due date'])

from datetime import date, timedelta   


today = date.today()
day_prior =  today - timedelta(days = DUE_DATE_DIFF)
print('day_prior =', day_prior)

prior_year = str(day_prior.year)+'-'+str(day_prior.month)+'-'+str(day_prior.day)
df1 = df[df['Due date'] <=  prior_year ]

phoneNum =''
bodyTemp =''
filePath =''
fileName =''

from tqdm.auto import tqdm

for ind in tqdm(df1.index): 
    try:
        phoneNum = int(df1['Mobile Number'][ind])
        dueDate = df1['Due date'][ind]
        toAddress = df1['Email Id'][ind]
        filePath = df1['file location'][ind]
        fileName = df1['outstanding filename'][ind]
        if(df1['Already Done ?'][ind] =='yes'):
            continue

        partyName  = df1['Party name'][ind]
        print('partyName :',partyName)
        bodyTemp = re.sub(r"{CompanyName}", partyName,body )
    
        sendEmail(subject , bodyTemp , EMAIL_ADDRESS , toAddress , filePath , fileName)
        print("*"*8)
        #sendWhatsApp(phoneNum , bodyTemp, filePath , fileName)
        df1['Already Done ?'][ind] ='Yes'
        
    except Exception as e:
        print(' Failed :'+str(e))
        df1['Already Done ?'][ind] = 'Exception occured'+str(e)

# driver.quit()
df[df['Due date'] <=  prior_year] = df1

os.remove(FILE_NAME)
df.to_excel(FILE_NAME , index=False)        