import csv
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("user-agent=Applebot")

driver = webdriver.Chrome(chrome_options=opts)
driver.get('https://www.tiktok.com/tag/albumlookalike')
sleep(4)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(3)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(3)
videos = driver.find_element_by_xpath("//script[@type='application/json']")
page = driver.page_source
soup = BeautifulSoup(page, 'lxml')
links = []

for article in soup.find_all('a', class_='jsx-1229794949 video-feed-item-wrapper'):
    info = []
    link = article['href']
    user_link = link[:link.rfind('/v')]
    info.append(user_link)
    driver.get(user_link)
    sleep(4)
    user_page = driver.page_source
    user_soup = BeautifulSoup(user_page, 'lxml')
    description = user_soup.find('meta', attrs={'name':'description'})
    description = description['content']
    try:
        bio = description.split('Fans.')[1]
        followers = description.split('Likes.')[1].split('F')[0]
        info.append(followers)
    except IndexError:
         bio = 'please find bio manually'
         info.append(bio)
    links.append(info)
    sleep(4)

with open('tiktoknames.csv', 'w') as f:
    writer = csv.writer(f)
    for i in range(len(links)):
        writer.writerow(links[i])


