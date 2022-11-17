from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
# import re

driver = webdriver.Chrome()
driver.get("https://twitter.com/bbcbangla")
sleep(3)
count = 0


'''
css-1dbjc4n r-18u37iz r-1q142lx       <<----- Post URL, Post Time
css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0  <<------ Post Text
css-901oao r-1awozwy r-1bwzh9t r-6koalj r-37j5jr r-a023e6 r-16dba41 r-1h0z5md r-rjixqe r-bcqeeo r-o7ynqc r-clp7b1 r-3s2u2q r-qvutc0 <<----- option, No. of Comments, No. of Retweets, No. of Likes
'''

'''
Fields to Scrape: Posts, Post URL, Post Time, Post Text, No. of Comments, No. of Retweets, No. of Likes, Commenter Name, Commenter profile URL, Comment time, Comment, Who Retweets, Retweet Text, Retweeter URL
'''

while True:
    if count >= 20: # atlease 20
        break
    sleep(2)
    tweets = driver.find_elements(By.XPATH,"//div[@class='css-1dbjc4n r-1igl3o0 r-qklmqi r-1adg3ll r-1ny4l3l']") #.get_attribute("innerHTML").splitlines() 
    for tweet in tweets:
        texts = tweet.find_elements(By.XPATH, "//div[@class='css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0']")
        for text in texts:
            print("count : ", count)
            #print(re.sub('<[^<]+?>', '', text.get_attribute("innerHTML")))
            print(text.get_attribute("innerHTML"))
            count +=1
            print("")
            
            if count >= 20: # atlease 20
                break


        print("------------")
        break
    count += 1
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
driver.quit()