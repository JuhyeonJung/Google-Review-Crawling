# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 23:07:02 2021

@author: 정주현
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
url = 'https://play.google.com/store/apps/details?id=me.blog.korn123.easydiary&hl=ko&gl=US&showAllReviews=true'
driver = webdriver.Chrome('chromedriver.exe')
driver.get(url)
driver.implicitly_wait(1)

while(True):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    try:
        element=driver.find_element_by_xpath("//span[@class='RveJvd snByac']").click()
        if(element is not None):
            element.click()
            break
    except Exception:
        continue
        
errTime = 0
successTime = 0

while(errTime<20 and successTime < 10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    try:
        element=driver.find_element_by_xpath("//span[@class='RveJvd snByac']").click()   
        if(element is not None):
            element.click()
            successTime+=1
            print(successTime)
            errTime = 0
            print(errTime)
    except Exception:
        errTime+=1


## [전체 리뷰] 버튼 클릭하여 펼치기
from selenium.webdriver.common.keys import Keys
spread_review = driver.find_elements_by_xpath("//button[@jsaction='click:TiglPc']")
for i in range(len(spread_review)):
    isTrue = spread_review[i].is_displayed()
    print("Element is visible? " + str(isTrue)) 
    if isTrue:
        spread_review[i].click()
        print(str(i)+"th more button is clicked and wait 1.5 secs...")
        time.sleep(1.5)
reviews = driver.find_elements_by_xpath("//span[contains(@jsname, 'bN97Pc')]")
for i in range(len(reviews)):
    print(str(i) + "\t" + reviews[i].text)
    
long_reviews = driver.find_elements_by_xpath("//span[@jsname='fbQN7e']")
for i in range(len(reviews)):
    print(long_reviews[i].text)
## merge two list 
merged_review = [t.text if t.text!='' else long_reviews[i].text for i,t in enumerate(reviews)]
dates = driver.find_elements_by_xpath("//span[@class='p2TkOb']")
likes = driver.find_elements_by_xpath("//div[@aria-label='이 리뷰가 유용하다는 평가를 받은 횟수입니다.']")
stars = driver.find_elements_by_xpath("//span[@class='nt2C1d']/div[@class='pf5lIe']/div[@role='img']")
stars_text = stars[3].get_attribute('aria-label')




html = driver.page_source
driver.quit()

bs0bj = BeautifulSoup(html, 'lxml')



#div_reviews = bs0bj.find_all("div", {"class" : "d15Mdf bAhLNe"})
div_reviews = bs0bj.find_all("span", {"jsname" : "bN97Pc"})
div_dates_0 = bs0bj.find_all("div", {"class" : "bAhLNe kx8XBd"})

dates_all=[]
for j in range(len(div_dates_0)):
    dates_all.append(div_dates_0[j].find("span", {"class" : 'p2TkOb'}).text)



reviews_all=[]
for i in range(len(div_reviews)):
    reviews_all.append(div_reviews[i].text)




result_df = pd.DataFrame(
                {'date' : dates_all,
                 'review' : reviews_all})


result_df.to_csv('./crawling_data.csv', index=False, encoding='utf-8-sig')
