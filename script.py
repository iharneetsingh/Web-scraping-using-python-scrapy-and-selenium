# import libraries
import csv
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# set up writer to store scrapped data into excel
writer = csv.writer(open('output.csv', 'w+', encoding='utf-8-sig', newline=''))
writer.writerow(['Name', 'Position', 'Company', 'Education', 'Location', 'URL'])

# login into your llinkedin account to scrap other profiles using selenium webdriver
driver = webdriver.Chrome('C://Users/Work/Downloads/chromedriver_win32/chromedriver')
driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
# replace 'you email id' with email id associated with your linkedin account
username = driver.find_element_by_name("session_key")
username.send_keys('you email id')
sleep(0.5)
# replace 'password' with your password associated to your linkedin account
password = driver.find_element_by_name('session_password')
password.send_keys('password')
sleep(0.5)

sign_in_button = driver.find_element_by_class_name('login__form_action_container ')
sign_in_button.click()
sleep(2)

# now extract urls of linkedin profiles
driver.get('https://www.google.com/')
search_query = driver.find_element_by_name('q')
# you can edit the "profile" and "place" as per you requirement
search_query.send_keys('site:linkedin.com/in AND "web developer" AND "Chandigarh"')
search_query.send_keys(Keys.RETURN)
sleep(0.5)

urls = driver.find_elements_by_xpath('//*[@class = "r"]/a[@href]')
urls = [url.get_attribute('href') for url in urls]
sleep(0.5)
# we scrape through the required details of each LinkedIn profile, such as name, position, experience, etc.
for url in urls:
    driver.get(url)
    sleep(2)

    sel = Selector(text = driver.page_source)

    name = sel.xpath('//*[@class = "inline t-24 t-black t-normal break-words"]/text()').extract_first().strip()
    position = sel.xpath('//*[@class = "mt1 t-18 t-black t-normal break-words"]/text()').extract_first().strip()
    ncompany = sel.xpath('//*[@class = "text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view"]/text()').extract_first()
    if(ncompany != None):
        company=ncompany.strip()
    else:
        company=ncompany
    education = sel.xpath('//*[@class = "pv-entity__school-name t-16 t-black t-bold"]/text()').extract_first()
    location = ' '.join(sel.xpath('//*[@class = "t-16 t-black t-normal inline-block"]/text()').extract_first().split())

    url = driver.current_url

    print('\n')
    print('Name: ', name)
    print('Position: ', position)
    print('Company: ', company)
    print('Education: ', education)
    print('Location: ', location)
    print('URL: ', url)
    print('\n')
# store the record into "writer"
    writer.writerow([name,
                 position,
                 company,
                 education,
                 location,
                 url])
# shutdown the webdriver
driver.quit()


