from selenium import webdriver

URL = 'https://www.youtube.com/'

driver= webdriver.Chrome()
driver.get(URL)

searchbox = driver.find_element_by_xpath('//*[@id="search"]')
searchbox.send_keys('Iron man')


searchButton = driver.find_element_by_xpath('//*[@id="search-icon-legacy"]')
searchButton.click()

